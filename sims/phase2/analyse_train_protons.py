"""Analysis of the guided-train run with a low-emittance 1 GeV proton bunch (S050): proton energy
change (distribution and vs position in the bunch), effective gradient at the best phase, emittance,
and export of the final bunch for the hand-off to the surface-plasmon stage."""
import os, sys, json
import numpy as np
from scipy.constants import c, m_p
here = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(here, "..", "..")
out_dir = os.path.join(here, sys.argv[1] if len(sys.argv) > 1 else "fbpic_train_p1_out")
summ = json.load(open(os.path.join(out_dir, "summary.json")))
S = [np.load(os.path.join(out_dir, f"snap_{r['step']:06d}.npz")) for r in summ["snaps"]]
MP = 938.272


def T(s):
    return (np.sqrt(1 + s["pux"] ** 2 + s["puy"] ** 2 + s["puz"] ** 2) - 1) * MP


def emit(s):
    x, ux = s["px"], s["pux"]
    return float(np.sqrt(np.mean(x ** 2) * np.mean(ux ** 2) - np.mean(x * ux) ** 2))


s0, s1 = S[0], S[-1]
T0, T1 = T(s0), T(s1)
hist = []
for s in S:
    t = T(s); r = np.sqrt(s["px"] ** 2 + s["py"] ** 2)
    env = s["env_a"]; z = s["z"]; ze = np.sum(z * env ** 2) / np.sum(env ** 2)
    hist.append(dict(t_fs=float(s["t"] * 1e15), T_mean=float(t.mean()), T_std=float(t.std()), T_min=float(t.min()),
                     T_max=float(t.max()), r_rms_um=float(np.sqrt(np.mean(r ** 2)) * 1e6), emit_n_x=emit(s),
                     bunch_minus_envelope_um=float((s["pz"].mean() - ze) * 1e6), Ez_axis_max_GVm=float(np.abs(s["Ez0"]).max() / 1e9)))
# phase-resolved energy change at the end
zc = s1["pz"] - s1["pz"].mean(); bins = np.linspace(zc.min(), zc.max(), 25); idx = np.digitize(zc, bins)
prof = [dict(z_um=float(0.5 * (bins[i - 1] + bins[i]) * 1e6), dT_mean=float(T1[idx == i].mean() - T0.mean()),
             n=int((idx == i).sum())) for i in range(1, len(bins)) if (idx == i).sum() > 30]
# distance travelled by the protons while inside the plasma (channel entrance at z = 0)
L_plasma = max(float(s1["pz"].mean()), 1e-9)
best = max(p["dT_mean"] for p in prof); worst = min(p["dT_mean"] for p in prof)
res = dict(history=hist, phase_profile=prof, L_in_plasma_um=L_plasma * 1e6,
           best_phase_gain_MeV=best, worst_phase_MeV=worst, eff_gradient_best_GVm=best / (L_plasma * 1e3) if L_plasma > 0 else None,
           T_std=[float(T0.std()), float(T1.std())], T_mean_change=float(T1.mean() - T0.mean()))
print(json.dumps({k: v for k, v in res.items() if k not in ("history", "phase_profile")}, indent=1))
for h in hist[::2]:
    print({k: round(v, 3) for k, v in h.items()})
json.dump(res, open(os.path.join(ROOT, "results", "data", "FBPIC_train_protons_analysis.json"), "w"), indent=1)
np.savez(os.path.join(here, "bunch_from_train.npz"), x=s1["px"], y=s1["py"], z=s1["pz"] - s1["pz"].mean(),
         ux=s1["pux"], uy=s1["puy"], uz=s1["puz"], w=s1["pw"])
