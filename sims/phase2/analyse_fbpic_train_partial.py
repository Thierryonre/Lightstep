"""Partial-run analysis of the FBPIC guided-train simulation (run stopped by the host at step
~1500-2000 due to low system memory; snapshots up to step 1500 saved). At t = 313 fs the front
half of the train is inside the channel (plasma for lab z >= 0). Quasi-static causality: plasma
at z > 0 has only been driven by the train portion already inside, so the 1D comparison uses the
measured on-axis drive restricted to z >= 0.
Normalisation: FBPIC's azimuthal decomposition (ifft over theta) gives Er_{m=1} = E_x/2 on axis,
so the laser amplitude is a = 2 |Er_1| / E0_laser (checked: peak a = 0.89 vs design 3 x 0.3)."""
import os, sys, glob, json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F, plasma as PL
here = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(here, "..", "..")
d = json.load(open(os.path.join(here, "fbpic_train_design.json")))
n0 = d["n_cm3"] * 1e6; kp = PL.k_p(n0); E0 = PL.E0(n0); beta = d["beta"]
snaps = {int(os.path.basename(f)[5:11]): np.load(f) for f in sorted(glob.glob(os.path.join(here, "fbpic_train_out", "snap_*.npz")))}
s = snaps[max(snaps)]
z, Ez, a = s["z"], s["Ez0"], 2 * s["env_a"]
ramp = 10e-6
inp = z >= ramp + 2e-6
# peak-train velocity inside the plasma: track envelope peaks between the last two snapshots
k1, k2 = sorted(snaps)[-2:]
def peaks(sn):
    zz, aa = sn["z"], 2 * sn["env_a"]
    p, _ = find_peaks(aa, height=0.5 * aa.max(), distance=50)
    return zz[p], aa[p]
z1, a1 = peaks(snaps[k1]); z2, a2 = peaks(snaps[k2])
dt = float(snaps[k2]["t"] - snaps[k1]["t"])
in2 = z2 > ramp
vels = []
for zp in z2[in2]:
    # candidate previous positions: the peak that moved by v*dt with v in [0.7c, 1.0c]
    cand = z1[(zp - z1 > 0.7 * PL.c * dt) & (zp - z1 < 1.0 * PL.c * dt)]
    if cand.size:
        vels.append((zp - cand.max()) / (PL.c * dt))
spacing = np.diff(z2[in2]) if in2.sum() > 1 else np.array([])
# 1D fluid wake with the measured on-axis drive, plasma region only, beta = design
xi = z[inp] * kp
a2 = 0.5 * a[inp] ** 2
phi, E1d, br = F.solve_wake(xi - xi.max(), a2, np.zeros_like(xi), beta)
Ez_n = Ez[inp] / E0
cmp = (z[inp] > ramp + 5e-6)
f3D = np.abs(Ez_n[cmp]).max() / np.abs(E1d[cmp]).max()
# rms shape agreement over the compared region (after amplitude scaling)
res = dict(snapshot_step=max(snaps), t_fs=float(s["t"] * 1e15), peak_a_in_plasma=float(a[inp].max()),
           train_peak_velocity_c=[float(v) for v in vels], design_velocity_c=beta,
           peak_spacing_um=[float(x * 1e6) for x in spacing], design_spacing_um=float(beta * 2 * np.pi / kp * 1e6),
           Ez_max_FBPIC_GVm=float(np.abs(Ez[inp]).max() / 1e9), Ez_max_FBPIC_E0=float(np.abs(Ez_n[cmp]).max()),
           Ez_max_1D_E0=float(np.abs(E1d[cmp]).max()), f3D_on_axis_field=float(f3D),
           f3D_energy_like=float(f3D ** 2), note="partial run (front half of train inside plasma)")
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(ROOT, "results", "data", "FBPIC_train_analysis_partial.json"), "w"), indent=1)
fig, ax = plt.subplots(3, 1, figsize=(10, 8.5), sharex=False)
zz = z * 1e6
ax[0].plot(zz, a, color="#2a78d6", lw=1, label="FBPIC on-axis laser envelope a")
ax[0].axvspan(zz[0], 0, color="#e4e3df", alpha=0.6, label="vacuum (channel starts at z=0)")
ax[0].set_ylabel("a (on axis)"); ax[0].legend(fontsize=8, frameon=False)
ax[1].plot(zz[inp], Ez_n, color="#2a78d6", lw=1.3, label="FBPIC on-axis E_z (quasi-3D)")
ax[1].plot(zz[inp], E1d, color="#eb6834", lw=1, ls="--", label="1D fluid, same measured on-axis drive")
ax[1].set_ylabel("E_z / E0"); ax[1].legend(fontsize=8, frameon=False); ax[1].set_xlim(zz[0], zz[-1])
r = s["r"][::2]
vm = np.abs(s["Ez_map"]).max()
ax[2].imshow(s["Ez_map"].T / E0, aspect="auto", origin="lower", cmap="RdBu_r",
             extent=[zz[0], zz[-1], 0, r[-1] * 1e6], vmin=-vm / E0, vmax=vm / E0)
ax[2].set_ylabel("r [µm]"); ax[2].set_xlabel("z (lab) [µm]"); ax[2].set_title(f"E_z map (mode 0), t = {s['t']*1e15:.0f} fs")
plt.tight_layout(); plt.savefig(os.path.join(ROOT, "results", "figures", "FBPIC_guided_train_partial.png"), dpi=110)
