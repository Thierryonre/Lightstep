"""Lowest proton energy for which a rigid, resonant waveguide train exists, vs constraints."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import plasma as PL
from p1e_waveguide_train_optics import design_rigid
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
lam = 1.0e-6; w0 = 2*np.pi*PL.c/lam
rows = []
for kpW_min in [2.2, 1.8, 1.4]:
    for T in [500, 750, 1000, 1500, 2000, 2500, 3000]:
        g = 1 + T/938.272; b = np.sqrt(1 - 1/g**2)
        found = None
        for P in [1, 2, 3, 4]:
            for n in np.geomspace(1e17, 3e20, 50):
                W = design_rigid(b, n*1e6, w0, P, 3)
                if W is None: continue
                kpW = PL.k_p(n*1e6)*W
                dn = 1/(np.pi*2.8179e-15*W**2)/1e6
                if kpW >= kpW_min and dn/n <= 2.0 and n <= 0.05*PL.n_crit(lam)/1e6:
                    found = dict(T=T, beta=b, P=P, n=n, W_um=W*1e6, kpW=kpW, dn_rel=dn/n, kpW_min=kpW_min); break
            if found: break
        rows.append(found or dict(T=T, beta=b, kpW_min=kpW_min, feasible=False))
        print(kpW_min, T, "feasible" if found else "none", {k: (round(v,3) if isinstance(v,float) else v) for k,v in (found or {}).items()})
json.dump(rows, open(os.path.join(ROOT, "results", "data", "P1e_feasibility_boundary.json"), "w"), indent=1)
