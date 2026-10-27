"""P1d scan: self-injection from rest vs alpha0/Lambda, and with a nanoparticle-like dense layer."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from p1d_self_injection_from_rest import run
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
cases = [dict(alpha_frac=0.5, n_np=0.0), dict(alpha_frac=0.8, n_np=0.0), dict(alpha_frac=1.2, n_np=0.0),
         dict(alpha_frac=0.5, n_np=9.0)]
res = []
for c in cases:
    out = run(a0=3.0, ell=1.0, T_final=300.0, dx=0.02, ppc=8, verbose=True, **c)
    res.append(out)
    print("RESULT", json.dumps({k: v for k, v in out.items() if k != "snaps"}), flush=True)
    json.dump(res, open(os.path.join(ROOT, "results", "data", "P1d_scan.json"), "w"), indent=1)
