"""Deuteron version of the P1b scan: velocity-matched acceleration to 3.6 GeV (1.8 GeV/u, the
energy used in the best published muon-cost studies), injected where the guided resonant train
becomes feasible (beta ~0.83-0.875 -> 1.5-2.0 GeV deuterons)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from p1b_matched_acceleration import run
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
res = []
for Tinj in [2000.0, 1500.0]:
    for load in [0.3, 0.5]:
        tag = f"D_T{int(Tinj)}_L{load}"
        out, tr, traj = run(T_inj=Tinj, T_final=3600.0, species="deuteron", load=load, tag=tag, verbose=False)
        res.append(out)
        print(f"{tag}: T={out['T_mean']:.0f} MeV L={out['length_cwp']:.0f} c/wp grad={out['mean_gradient_E0']:.3f} E0 "
              f"eff={out['eff_wake_to_beam']:.3f} spread={out['T_rms_frac']:.4f} capt={out['captured']:.3f} "
              f"stalled={out['stalled']} broken={out['broken']} ({out['runtime_s']:.0f}s)", flush=True)
        json.dump(res, open(os.path.join(ROOT, "results", "data", "P1b_deuteron_scan.json"), "w"), indent=1)
