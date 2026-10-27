"""Scan of P1b velocity-matched acceleration to 6 GeV: injection energy, field program, loading."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from p1b_matched_acceleration import run
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
cases = []
for Tinj in [1000.0, 300.0, 100.0, 30.0]:
    for program in ["const", "track"]:
        for load in [0.3, 0.5]:
            cases.append(dict(T_inj=Tinj, program=program, load=load))
results = []
fn = os.path.join(ROOT, "results", "data", "P1b_scan.json")
for c in cases:
    tag = f"T{int(c['T_inj'])}_{c['program']}_L{c['load']}"
    out, tr, traj = run(T_inj=c["T_inj"], program=c["program"], load=c["load"], tag=tag, verbose=False, max_time_s=1200)
    results.append(out)
    print(f"{tag}: T={out['T_mean']:.0f} MeV L={out['length_cwp']:.0f} c/wp grad={out['mean_gradient_E0']:.3f} E0 "
          f"eff={out['eff_wake_to_beam']:.3f} spread={out['T_rms_frac']:.3f} capt={out['captured']:.3f} "
          f"stalled={out['stalled']} broken={out['broken']} a0 {out['a0_inj']:.2f}->{out['a0_final']:.2f} ({out['runtime_s']:.0f}s)", flush=True)
    json.dump(results, open(fn, "w"), indent=1)
