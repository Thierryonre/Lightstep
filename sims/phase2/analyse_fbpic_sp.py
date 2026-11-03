"""Analysis of the FBPIC hollow-channel surface-plasmon run (S044)."""
import os, sys, glob, json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.constants import c

here = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(here, "..", "..")
out_name = sys.argv[1] if len(sys.argv) > 1 else "fbpic_sp_out"
tag = sys.argv[2] if len(sys.argv) > 2 else "FBPIC_surface_plasmon"
out_dir = os.path.join(here, out_name)
summ = json.load(open(os.path.join(out_dir, "summary.json")))
d = summ["design"]; E0w = d["E0_wall_GVm"] * 1e9; R = d["R_um"] * 1e-6; lam_sp = d["lam_sp_um"] * 1e-6
# only this run's snapshots (an earlier aborted attempt left snap_000050/100/200 in fbpic_sp_out)
files = [os.path.join(out_dir, f"snap_{r['step']:06d}.npz") for r in summ["snaps"]]
S = [np.load(f) for f in files]


def xcorr_velocity(s1, s2, half_width=12e-6):
    """Speed of the E_z pattern near the laser envelope: cross-correlate on-axis E_z of two
    snapshots in lab coordinates, searching displacements c*dt +- lam_sp/2."""
    z1, z2 = s1["z"], s2["z"]; dzg = z1[1] - z1[0]; dt = float(s2["t"] - s1["t"])
    env = s2["env_a"]; ze = np.sum(z2 * env ** 2) / np.sum(env ** 2)
    m = np.where(np.abs(z2 - ze) < half_width)[0]; a_ = s2["Ez_axis"][m]
    lags = np.arange(-int(0.5 * lam_sp / dzg), int(0.5 * lam_sp / dzg) + 1); cc = []
    for L in lags:
        b = np.interp(z2[m] - c * dt - L * dzg, z1, s1["Ez_axis"])
        cc.append(np.dot(a_, b) / np.sqrt(np.dot(a_, a_) * np.dot(b, b) + 1e-30))
    i = int(np.argmax(cc))
    return 1 + lags[i] * dzg / (c * dt), float(cc[i])


vel = []
for s1, s2 in zip(S[:-1], S[1:]):
    v_, q_ = xcorr_velocity(s1, s2)
    if q_ > 0.5:
        vel.append(v_)
s = S[-1]
z, Ea, Ew, env = s["z"], s["Ez_axis"], s["Ez_wall"], s["env_a"]
ze = np.sum(z * env ** 2) / np.sum(env ** 2)
we = np.sqrt(np.sum((z - ze) ** 2 * env ** 2) / np.sum(env ** 2))
behind = z < ze - 2.5 * we
per = []
if behind.any():
    edges = np.arange(z[behind].max(), z[behind].min(), -lam_sp)
    for k in range(len(edges) - 1):
        m = (z <= edges[k]) & (z > edges[k + 1])
        if m.sum() > 5:
            per.append(dict(period_behind=k + 1, Ez_axis_GVm=float(np.abs(Ea[m]).max() / 1e9),
                            Ez_wall_GVm=float(np.abs(Ew[m]).max() / 1e9)))
inside = np.abs(z - ze) < 2 * we
ratio_axis_wall = float(np.abs(Ea[inside]).max() / max(np.abs(Ew[inside]).max(), 1e-9))
T0 = S[0]["pT"]; T1 = s["pT"]; r0 = S[0]["pr"]; r1 = s["pr"]
res = dict(wave_phase_velocity_c=[float(v) for v in vel], wave_velocity_mean_c=float(np.mean(vel)) if vel else None,
           wave_velocity_std_c=float(np.std(vel)) if vel else None, target_velocity_c=0.9712,
           Ez_axis_max_in_train_GVm=float(np.abs(Ea[inside]).max() / 1e9),
           axis_over_wall_in_train=ratio_axis_wall, periods_behind=per,
           # particle order is not preserved between GPU snapshots -> compare distributions, not particles
           proton_T_mean_change_MeV=float(T1.mean() - T0.mean()),
           proton_T_std_MeV=[float(T0.std()), float(T1.std())],
           proton_T_range_MeV=[[float(T0.min()), float(T0.max())], [float(T1.min()), float(T1.max())]],
           proton_r_rms_um=[float(np.sqrt(np.mean(r0 ** 2)) * 1e6), float(np.sqrt(np.mean(r1 ** 2)) * 1e6)],
           proton_frac_inside_R=float(np.mean(r1 < R)), t_fs=float(s["t"] * 1e15),
           protons_behind_envelope_um=float((ze - np.mean(s["pz"])) * 1e6))
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(ROOT, "results", "data", f"{tag}_analysis.json"), "w"), indent=1)
fig, ax = plt.subplots(3, 1, figsize=(10, 8.5))
zz = z * 1e6
ax[0].plot(zz, env, color="#2a78d6", lw=1); ax[0].set_ylabel("laser a (axis)")
ax[1].plot(zz, Ea / 1e9, color="#2a78d6", lw=1.2, label="E_z on axis")
ax[1].plot(zz, Ew / 1e9, color="#eb6834", lw=1, label="E_z near wall (r = 0.9R)")
ax[1].scatter(s["pz"][::20] * 1e6, np.zeros(s["pz"][::20].size), s=2, color="#1baf7a", label="protons")
ax[1].set_ylabel("E_z [GV/m]"); ax[1].legend(fontsize=8, frameon=False)
r = s["r"][::2]
vm = np.abs(s["Ez_map"]).max()
ax[2].imshow(s["Ez_map"].T / 1e9, aspect="auto", origin="lower", cmap="RdBu_r",
             extent=[zz[0], zz[-1], 0, r[-1] * 1e6], vmin=-vm / 1e9, vmax=vm / 1e9)
ax[2].axhline(R * 1e6, color="k", lw=0.6, ls="--"); ax[2].set_ylabel("r [µm]"); ax[2].set_xlabel("z [µm]")
ax[2].set_title("E_z map (dashed: channel wall)")
for a_ in ax[:2]:
    a_.set_xlim(zz[0], zz[-1])
plt.tight_layout(); plt.savefig(os.path.join(ROOT, "results", "figures", f"{tag}.png"), dpi=110)
