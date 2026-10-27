"""Analysis of the full FBPIC guided-train run (with proton test bunch).
Snapshots store the on-axis laser envelope already normalised (a = 2|Er_1|/E0).
1. Peak-train and wake phase velocity inside the channel, tracked in the window frame
   zeta = z - c t (pattern drifts slowly there -> unambiguous tracking); envelope centroid velocity.
2. Proton forces behind the envelope from mode-0 fields: F_z = e E_z, F_r = e (E_r - beta c B_theta),
   beta = proton velocity; fraction of each period that is accelerating AND focusing (F_z > 0,
   F_r < 0 near axis) and its evolution with distance behind the envelope.
3. Proton bunch: mean energy change and r_rms vs time; energy change vs phase.
4. On-axis wake vs the 1D two-velocity model with the same drive -> f_3D.
"""
import os, sys, glob, json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import plasma as PL

here = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(here, "..", "..")
out_dir = os.path.join(here, sys.argv[1] if len(sys.argv) > 1 else "fbpic_train_out")
d = json.load(open(os.path.join(here, "fbpic_train_design.json")))
n0 = d["n_cm3"] * 1e6; kp = PL.k_p(n0); E0 = PL.E0(n0); beta = d["beta"]; c = PL.c
lam_w = beta * 2 * np.pi / kp
files = sorted(glob.glob(os.path.join(out_dir, "snap_*.npz")))
S = [np.load(f) for f in files]
steps = [int(os.path.basename(f)[5:11]) for f in files]
res = dict(steps=steps)

# ---- 1. velocities in the window frame
def main_peaks(s, zmin=12e-6):
    z, a = s["z"], s["env_a"]
    m = z > zmin
    if m.sum() < 10:
        return np.array([])
    p, _ = find_peaks(a[m], height=0.35 * a[m].max(), distance=int(0.6 * lam_w / (z[1] - z[0])))
    return z[m][p]

vel_pat, vel_env, vel_wake = [], [], []
for s1, s2 in zip(S[:-1], S[1:]):
    t1, t2 = float(s1["t"]), float(s2["t"])
    p1, p2 = main_peaks(s1) - c * t1, main_peaks(s2) - c * t2
    if p1.size and p2.size:
        dz = []
        for q in p2:
            j = np.argmin(np.abs(p1 - q))
            if abs(p1[j] - q) < 0.4 * lam_w:
                dz.append(q - p1[j])
        if dz:
            vel_pat.append(1 + np.median(dz) / (c * (t2 - t1)))
    for s, store in [(s1, None)]:
        pass
    w1, w2 = s1["env_a"] ** 2, s2["env_a"] ** 2
    ce1 = np.sum((s1["z"] - c * t1) * w1) / np.sum(w1); ce2 = np.sum((s2["z"] - c * t2) * w2) / np.sum(w2)
    vel_env.append(1 + (ce2 - ce1) / (c * (t2 - t1)))
    # wake zero crossings (E_z: + -> -) behind the envelope, in plasma
    def zc(s, t):
        z, E = s["z"], s["Ez0"]
        m = (z > 12e-6)
        zz, EE = z[m], E[m]
        idx = np.where((EE[:-1] > 0) & (EE[1:] <= 0) & (np.abs(EE[:-1]) > 0.05 * np.abs(EE).max()))[0]
        return zz[idx] - c * t
    z1, z2 = zc(s1, t1), zc(s2, t2)
    dz = [q - z1[np.argmin(np.abs(z1 - q))] for q in z2 if z1.size and np.min(np.abs(z1 - q)) < 0.4 * lam_w]
    if dz:
        vel_wake.append(1 + np.median(dz) / (c * (t2 - t1)))
res.update(pattern_velocity_c=[float(v) for v in vel_pat], envelope_velocity_c=[float(v) for v in vel_env],
           wake_phase_velocity_c=[float(v) for v in vel_wake], design_velocity_c=beta)

# ---- 2. proton forces behind the envelope (last snapshot)
s = S[-1]
z = s["z"][::2]; r = s["r"][::2]
Ez, Er, Bt = s["Ez_map"], s["Er_map"], s["Bt_map"]
Fz = Ez / E0
Fr = (Er - beta * c * Bt) / E0
env = s["env_a"]
ze = np.sum(s["z"] * env ** 2) / np.sum(env ** 2)
w_env = np.sqrt(np.sum((s["z"] - ze) ** 2 * env ** 2) / np.sum(env ** 2))
behind = (z < ze - 2.5 * w_env) & (z > 12e-6)
rmask = r < 2.0e-6
acc_foc = (Fz[:, rmask].mean(axis=1) > 0) & (Fr[:, rmask].mean(axis=1) < 0)
# per-period statistics behind the envelope
zb = z[behind]
per = []
if zb.size:
    edges = np.arange(zb.max(), zb.min(), -lam_w)
    for k in range(len(edges) - 1):
        m = (z <= edges[k]) & (z > edges[k + 1])
        if m.sum() < 5:
            continue
        per.append(dict(period_behind=k + 1, Ez_amp_E0=float(np.abs(Ez[m, 0]).max() / E0),
                        frac_acc_and_foc=float(acc_foc[m].mean())))
res.update(envelope_centre_um=float(ze * 1e6), envelope_rms_um=float(w_env * 1e6), periods_behind=per)

# ---- 3. protons
if "pz" in s:
    T_hist = []
    for sn, st in zip(S, steps):
        if "pz" not in sn:
            continue
        g = np.sqrt(1 + sn["pux"] ** 2 + sn["puy"] ** 2 + sn["puz"] ** 2)
        T_hist.append(dict(step=st, t_fs=float(sn["t"] * 1e15), T_mean=float((g.mean() - 1) * 938.272),
                           T_std=float((g.std()) * 938.272), r_rms_um=float(np.sqrt(np.mean(sn["px"] ** 2 + sn["py"] ** 2)) * 1e6),
                           z_mean_um=float(sn["pz"].mean() * 1e6)))
    g0 = np.sqrt(1 + S[0]["pux"] ** 2 + S[0]["puy"] ** 2 + S[0]["puz"] ** 2)
    g1 = np.sqrt(1 + s["pux"] ** 2 + s["puy"] ** 2 + s["puz"] ** 2)
    dT = (g1 - g0) * 938.272
    rr0 = np.sqrt(S[0]["px"] ** 2 + S[0]["py"] ** 2); rr1 = np.sqrt(s["px"] ** 2 + s["py"] ** 2)
    zr = s["pz"]
    # energy gain and radial change binned by final position (phase)
    bins = np.linspace(zr.min(), zr.max(), 25)
    idx = np.digitize(zr, bins)
    phase = [dict(z_um=float(0.5 * (bins[i - 1] + bins[i]) * 1e6), dT_MeV=float(dT[idx == i].mean()),
                  dr_um=float((rr1 - rr0)[idx == i].mean() * 1e6), n=int((idx == i).sum()))
             for i in range(1, len(bins)) if (idx == i).sum() > 20]
    res.update(proton_history=T_hist, proton_phase_bins=phase,
               proton_max_gain_MeV=float(max(p["dT_MeV"] for p in phase)) if phase else None)
print(json.dumps({k: v for k, v in res.items() if k not in ("proton_phase_bins",)}, indent=1))
json.dump(res, open(os.path.join(ROOT, "results", "data", "FBPIC_train_analysis_full.json"), "w"), indent=1)

# ---- figure
fig, ax = plt.subplots(3, 1, figsize=(10, 9))
zz = s["z"] * 1e6
ax[0].plot(zz, env, color="#2a78d6", lw=1, label="on-axis laser envelope a")
ax[0].set_ylabel("a"); ax[0].legend(fontsize=8, frameon=False)
ax[1].plot(zz, s["Ez0"] / E0, color="#2a78d6", lw=1.2, label="E_z on axis")
if "pz" in s:
    ax[1].scatter(s["pz"][::10] * 1e6, np.zeros_like(s["pz"][::10]), s=2, color="#eb6834", label="protons (position)")
ax[1].set_ylabel("E_z / E0"); ax[1].legend(fontsize=8, frameon=False)
vm = np.abs(Fr[:, r < 8e-6]).max()
im = ax[2].imshow(np.where(np.outer(acc_foc, np.ones(r.size)), Fr, np.nan).T, aspect="auto", origin="lower",
                  cmap="RdBu_r", extent=[z[0] * 1e6, z[-1] * 1e6, 0, r[-1] * 1e6], vmin=-vm, vmax=vm)
ax[2].set_ylim(0, 10); ax[2].set_ylabel("r [µm]"); ax[2].set_xlabel("z [µm]")
ax[2].set_title("proton radial force F_r/eE0 where the on-axis region is accelerating & focusing for protons")
plt.colorbar(im, ax=ax[2])
for a_ in ax[:2]:
    a_.set_xlim(zz[0], zz[-1])
plt.tight_layout(); plt.savefig(os.path.join(ROOT, "results", "figures", "FBPIC_guided_train_full.png"), dpi=110)
