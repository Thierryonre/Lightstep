"""Analyse the FBPIC guided-train run: on-axis laser envelope and wake, peak-train velocity,
comparison with the 1D fluid wake driven by (a) the designed on-axis intensity and (b) the
measured on-axis envelope. Outputs f_3D = |Ez| (FBPIC) / |Ez| (1D) behind the train and a figure."""
import os, sys, glob, json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F
import plasma as PL

here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(here, "..", "..")
out_dir = os.path.join(here, sys.argv[1] if len(sys.argv) > 1 else "fbpic_train_out")
d = json.load(open(os.path.join(here, "fbpic_train_design.json")))
summ = json.load(open(os.path.join(out_dir, "summary.json")))
a0c = summ["a0"]
files = sorted(glob.glob(os.path.join(out_dir, "snap_*.npz")))
n0 = d["n_cm3"] * 1e6
kp = PL.k_p(n0)
E0 = PL.E0(n0)
beta = d["beta"]
snaps = [np.load(f) for f in files]
# --- peak-train velocity: track the strongest envelope peak between consecutive snapshots
vel = []
for s1, s2 in zip(snaps[:-1], snaps[1:]):
    z1 = s1["z"][np.argmax(s1["env_a"])]
    z2 = s2["z"][np.argmax(s2["env_a"])]
    dt = float(s2["t"] - s1["t"])
    # window moves at c: lab position = z (window coords are lab coords in FBPIC)
    vel.append((z2 - z1) / (PL.c * dt))
last = snaps[-1]
z = last["z"]; Ez = last["Ez0"]; env = last["env_a"]
# xi relative to the laser train centre-of-mass
w = env ** 2
zc = np.sum(z * w) / np.sum(w)
xi = (z - zc) * kp
# (b) 1D wake from the measured on-axis envelope: <a^2> = env^2/2 (linear polarisation)
order = np.argsort(xi)
xi_s, a2_meas = xi[order], 0.5 * env[order] ** 2
phi, E1d_meas, br = F.solve_wake(xi_s, a2_meas, np.zeros_like(xi_s), beta)
# (a) 1D wake from the designed on-axis intensity (rigid comb, equal a0 per component)
wq = 2 * np.pi * PL.c / np.array(d["lambdas"])
dk = (wq[0] - wq) / PL.omega_p(n0) / beta            # in k_p units (rigid: dk = dw / v_a)
Tp = 2 * np.pi / PL.omega_p(n0)
tau = summ["fwhm_periods"] * Tp / np.sqrt(2 * np.log(2))
sig_xi = PL.c * tau * kp * beta / np.sqrt(2) / np.sqrt(2)   # intensity sigma in xi (approx.)
env_design = np.exp(-(xi_s / (PL.c * tau * kp)) ** 2)        # field envelope exp(-(z/c tau)^2)
pat = np.abs(np.sum(np.exp(1j * dk[:, None] * xi_s[None, :]), axis=0)) ** 2
a2_design = 0.5 * a0c ** 2 * env_design ** 2 * pat
phi2, E1d_des, br2 = F.solve_wake(xi_s, a2_design, np.zeros_like(xi_s), beta)
behind = xi_s < xi_s[np.argmax(a2_meas)] - 1.5 * PL.c * tau * kp
Ez_s = (Ez / E0)[order]
f3D_meas = np.abs(Ez_s[behind]).max() / max(np.abs(E1d_meas[behind]).max(), 1e-12)
f3D_des = np.abs(Ez_s[behind]).max() / max(np.abs(E1d_des[behind]).max(), 1e-12)
res = dict(train_velocity_snapshots=[float(v) for v in vel], beta_design=beta,
           Ez_max_FBPIC_E0=float(np.abs(Ez_s[behind]).max()), Ez_max_FBPIC_GVm=float(np.abs(Ez_s[behind]).max() * E0 / 1e9),
           Ez_max_1D_measured_drive_E0=float(np.abs(E1d_meas[behind]).max()),
           Ez_max_1D_design_drive_E0=float(np.abs(E1d_des[behind]).max()),
           f3D_vs_measured_drive=float(f3D_meas), f3D_vs_design_drive=float(f3D_des),
           max_envelope_a=float(env.max()), t_fs=float(last["t"] * 1e15), n_snapshots=len(files))
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(ROOT, "results", "data", "FBPIC_train_analysis.json"), "w"), indent=1)
fig, ax = plt.subplots(3, 1, figsize=(10, 9))
ax[0].plot(xi_s, np.sqrt(2 * a2_meas), color="#2a78d6", lw=1, label="FBPIC on-axis envelope a")
ax[0].plot(xi_s, np.sqrt(2 * a2_design), color="#eb6834", lw=1, ls="--", label="design (rigid comb)")
ax[0].set_ylabel("a (on axis)"); ax[0].legend(fontsize=8, frameon=False)
ax[1].plot(xi_s, Ez_s, color="#2a78d6", lw=1.2, label="FBPIC E_z on axis")
ax[1].plot(xi_s, E1d_meas, color="#1baf7a", lw=1, label="1D fluid, measured drive")
ax[1].plot(xi_s, E1d_des, color="#eb6834", lw=1, ls="--", label="1D fluid, design drive")
ax[1].set_ylabel("E_z / E0"); ax[1].legend(fontsize=8, frameon=False); ax[1].set_xlabel("ξ k_p")
r = last["r"][::2]
ax[2].imshow(last["Ez_map"].T / E0, aspect="auto", origin="lower", cmap="RdBu_r",
             extent=[(z[0] - zc) * kp, (z[-1] - zc) * kp, 0, r[-1] * 1e6], vmin=-np.abs(Ez_s).max(), vmax=np.abs(Ez_s).max())
ax[2].set_ylabel("r [µm]"); ax[2].set_xlabel("ξ k_p"); ax[2].set_title("E_z (mode 0)")
plt.tight_layout()
plt.savefig(os.path.join(ROOT, "results", "figures", "FBPIC_guided_train.png"), dpi=110)
