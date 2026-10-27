"""B3: conventional LWFA (driver at laser group velocity, gamma_p = k0/kp) with a LOADED proton
bunch from the same injector energies as the velocity-matched designs. Efficiency =
proton energy gain / laser work, evaluated at the point of maximum beam energy (best case:
stage terminated exactly at dephasing). Fluid tracker (validated vs PIC in S012/S014)."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F, track1d as TR
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
ME = 0.51099895
rows = []
for gp in [7.4, 20.0, 41.7]:
    bg = np.sqrt(1 - 1/gp**2)
    a0, fw = 2.0, 2.3548
    drv = lambda xi, t, xd: F.gaussian_envelope(xi, 0.0, fw, a0)
    xi = np.linspace(-20, 6, 2601)
    phi, E, br = F.solve_wake(xi, drv(xi, 0, 0), np.zeros_like(xi), bg)
    m = (xi < -1.2) & (xi > -1.2 - 2*np.pi)
    ipk = np.where(m)[0][np.argmax(E[m])]; Epk = E[ipk]
    for Tinj in [100.0, 1000.0, 3000.0]:
        best = None
        for xi0 in np.linspace(xi[ipk] - 2.5, xi[ipk] + 1.5, 9):
            tr = TR.Tracker(-25.0, 6.0, 0.01, drv, lambda t, xd, s, bg=bg: bg)
            rng = np.random.default_rng(0)
            tr.set_beam(xi0 + 0.1*rng.standard_normal(500), Tinj*(1 + 0.005*rng.standard_normal(500)), 0.4*Epk/500)
            b0 = TR.proton_beta(tr.pu[0]); dt = float(np.clip(0.02/max(abs(b0-bg),1e-6), 0.02, 5.0))
            best_case = (0.0, 0.0, 0.0)
            for i in range(200000):
                tr.step(dt, energy_every=50, istep=i)
                if i % 10 == 0:
                    T = tr.kinetic()*ME; al = tr.alive
                    gain = np.sum(tr.pw[al]*(T[al] - tr.T0[al]*ME))/ME
                    if gain > best_case[0]:
                        best_case = (gain, tr.laser_work, float(np.average(T[al] - tr.T0[al]*ME, weights=tr.pw[al])))
                    if not al.any() or tr.t*abs(b0-bg) > 40:
                        break
            eff = best_case[0]/best_case[1] if best_case[1] > 0 else 0.0
            if best is None or eff > best["eff"]:
                best = dict(gamma_p=gp, T_inj=Tinj, xi0=float(xi0), eff=float(eff), mean_gain_MeV=best_case[2])
        rows.append(best)
        print(f"gamma_p={gp:5.1f} T_inj={Tinj:6.0f} MeV: best wake->proton efficiency = {best['eff']:.2e}, mean gain {best['mean_gain_MeV']:.2f} MeV", flush=True)
json.dump(rows, open(os.path.join(ROOT, "results", "data", "B3_conventional_protons_loaded.json"), "w"), indent=1)
