"""R4: reproduce the linear-regime dephasingless LWFA (flying focus) example of Palastro et al.,
PRL 124, 134802 (2020): lambda = 1 um, 30 fs, a0 = 0.5, n = 3.5e18 cm^-3, 8 cm.
Paper: conventional LWFA 75 MeV (dephasing-limited) vs DLWFA 1.3 GeV.
1D fluid wake + test electrons (track1d, species='electron'):
 - conventional: driver at the linear group velocity v_g = c sqrt(1 - n/n_c), electrons at the
   best phase (dephasing-limited max energy);
 - DLWFA: driver at v = c (ideal flying focus), electrons phase-locked.
1D gives the plasma physics only (no diffraction; the paper's flying focus provides the
constant intensity over 8 cm)."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F, track1d as TR, plasma as PL
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
lam = 1e-6; n = 3.5e18*1e6; a0 = 0.5
cwp = 1/PL.k_p(n); k0kp = np.sqrt(PL.n_crit(lam)/n)
fw = 30e-15*PL.omega_p(n)
L = 0.08/cwp
out = {}
for name, beta in [("conventional", np.sqrt(1 - 1/k0kp**2)), ("DLWFA_flying_focus", 1.0)]:
    drv = lambda xi, t, xd: F.gaussian_envelope(xi, 0.0, fw, a0)
    tr = TR.Tracker(-2.2*2*np.pi, 4.0, 0.01, drv, lambda t, xd, s, b=beta: b, species="electron")
    tr.static_driver = True
    xi0 = np.linspace(-2.0*2*np.pi, -0.2, 800)
    tr.set_beam(xi0, np.full_like(xi0, 10.0), 0.0)
    dt = 2.0; Emax = np.zeros(xi0.size); hist = []
    while tr.xd < L:
        tr.step(dt, energy_every=10**9, istep=1)
        T = tr.kinetic()*0.511
        Emax = np.maximum(Emax, np.where(tr.alive, T, 0))
        if int(tr.t/dt) % 500 == 0: hist.append((tr.xd*cwp*100, float(T[tr.alive].max()) if tr.alive.any() else 0.0))
    out[name] = dict(beta=beta, E_max_MeV=float(Emax.max()), final_best_MeV=float(T.max()), hist=hist)
    print(f"{name}: max energy reached = {Emax.max():.0f} MeV; best at 8 cm = {T.max():.0f} MeV")
out["paper"] = dict(conventional_MeV=75, DLWFA_MeV=1300)
out["k0_over_kp"] = k0kp; out["L_cwp"] = L
json.dump(out, open(os.path.join(ROOT, "results", "data", "R4_palastro2020.json"), "w"), indent=1)
