"""1D two-velocity counterpart of the FBPIC guided-train run (same drive, same geometry, same
elapsed time) -> on-axis wake comparison and f_3D for the full train.
Drive: rigid-comb pattern at beta_a (spacings from the design frequencies), envelope at the
modes' group velocity, a_avg = sqrt(N) * a0_component, intensity FWHM = 2.5 plasma periods,
plasma from z = 0 with a 10 um linear ramp (lab frame as in FBPIC)."""
import os, sys, json, glob
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
import pic1d_env as P
import plasma as PL
from p1g_two_velocity_train import TwoVelocityDriver

here = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(here, "..", "..")
out_dir = os.path.join(here, sys.argv[1] if len(sys.argv) > 1 else "fbpic_train_out")
d = json.load(open(os.path.join(here, "fbpic_train_design.json")))
summ = json.load(open(os.path.join(out_dir, "summary.json")))
n0 = d["n_cm3"] * 1e6; kp = PL.k_p(n0); wp = PL.omega_p(n0); E0 = PL.E0(n0); c = PL.c
beta = d["beta"]
wq = 2 * np.pi * c / np.array(d["lambdas"])
spac = -np.diff(wq) / wp
dk = np.concatenate([[0.0], np.cumsum(spac)]) / beta
a_comp = summ["a0"]
a_avg = np.sqrt(len(wq)) * a_comp
# envelope group velocity of the guided modes (fundamental, design channel)
vg = 1 / np.sqrt(1 + (kp * c / wq[0]) ** 2 + 4 / (d["W"] ** 2) * (c / wq[0]) ** 2)
Tp = 2 * np.pi / wp
tau = summ["fwhm_periods"] * Tp / np.sqrt(2 * np.log(2))
sig_env = summ["fwhm_periods"] * 2 * np.pi * vg / 2.3548          # intensity sigma in c/wp
z0 = -2.6 * c * tau * kp                                              # FBPIC train centre at t = 0
ramp = 10e-6 * kp
snaps = sorted(glob.glob(os.path.join(out_dir, "snap_*.npz")))
last = np.load(snaps[-1])
t_end = float(last["t"]) * wp
drv = TwoVelocityDriver(a_avg, dk, sig_env, beta, vg, x0=z0)
dens = lambda x: np.clip(x / ramp, 0, 1)
Lx = (last["z"][-1] - last["z"][0]) * kp
x0w = last["z"][0] * kp - t_end           # window starts where FBPIC's started (moves at c)
sim = P.Sim1D(Lx, 0.02, dens, drv, ppc=16, dt=0.01, mobile_ions=True, x_window0=x0w, window_velocity=1.0)
# FBPIC's pattern is phase-referenced at the focus (z = 0); keep pattern origin there
drv.x_pat = z0 * beta / vg
while sim.t < t_end:
    sim.step()
    drv.x_pat += beta * sim.dt
z1 = sim.grid / kp
E1 = np.interp(last["z"], z1, sim.E)
zf = last["z"]; Ef = last["Ez0"] / E0
m = zf > 15e-6
f3D = np.abs(Ef[m]).max() / np.abs(E1[m]).max()
res = dict(t_fs=float(last["t"] * 1e15), Ez_FBPIC_max_E0=float(np.abs(Ef[m]).max()), Ez_1D_max_E0=float(np.abs(E1[m]).max()),
           f3D_field=float(f3D), f3D_energy=float(f3D ** 2), vg_env=float(vg), a_avg=float(a_avg), spacings=list(map(float, spac)))
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(ROOT, "results", "data", "FBPIC_vs_1D_two_velocity.json"), "w"), indent=1)
fig, ax = plt.subplots(figsize=(10, 3.6))
ax.plot(zf * 1e6, Ef, color="#2a78d6", lw=1.3, label="FBPIC (quasi-3D) on-axis E_z")
ax.plot(zf * 1e6, E1, color="#eb6834", lw=1, ls="--", label="1D two-velocity model, same drive")
ax.set_xlabel("z [µm]"); ax.set_ylabel("E_z / E0"); ax.legend(frameon=False, fontsize=8)
ax.set_title(f"Guided resonant train at t = {last['t']*1e15:.0f} fs: f_3D(field) = {f3D:.2f}", loc="left")
plt.tight_layout(); plt.savefig(os.path.join(ROOT, "results", "figures", "FBPIC_vs_1D_two_velocity.png"), dpi=110)
