"""B2: conventional LWFA (driver at the laser group velocity) acting on injected protons.

Driver: Gaussian, a0 (linear pol.), intensity FWHM 2.355 c/w_p (near-resonant), moving at
beta_g = sqrt(1 - 1/gamma_p^2), gamma_p = k0/kp. Test protons (no loading) are placed across
one full wake period at injection energy T_inj; we record the maximum energy gain reached by
any proton (best phase) before it slips out of the wake.
Also compares with the 1D Hamiltonian estimate of the trapped-orbit energy range.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F
import track1d as T

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
a0 = 2.0
fwhm = 2.3548
gammas = [5.0, 7.4, 10.0, 20.0, 40.0]
Tinj = [10.0, 100.0, 1000.0, 3000.0, 6000.0]
rows = []
for gp in gammas:
    bg = np.sqrt(1 - 1 / gp**2)
    drv = lambda xi, t, xd: F.gaussian_envelope(xi, 0.0, fwhm, a0)
    for Ti in Tinj:
        tr = T.Tracker(-40.0, 6.0, 0.01, drv, lambda t, xd, s, bg=bg: bg)
        xi0 = np.linspace(-2 * np.pi * bg - 4.0, -4.0, 400)   # one wake period behind the driver
        tr.set_beam(xi0, np.full_like(xi0, Ti), 0.0)
        tr.static_driver = True
        b_inj = T.proton_beta(tr.pu[0])
        slip = abs(b_inj - bg)
        dt = float(np.clip(0.02 / max(slip, 1e-6), 0.02, 20.0))
        Tmax = tr.kinetic().copy()
        t_end = 4e5
        nstep = 0
        while tr.t < t_end and tr.alive.any() and nstep < 400000:
            tr.step(dt, energy_every=10**9, istep=1)
            Tk = tr.kinetic()
            Tmax = np.where(tr.alive, np.maximum(Tmax, Tk), Tmax)
            nstep += 1
        gain_MeV = (Tmax - tr.T0).max() * 0.51099895
        # Hamiltonian estimate of trapped energy range: wake potential depth in proton units
        xi = np.linspace(-40, 6, 4601)
        phi, E, br = F.solve_wake(xi, drv(xi, 0, 0), np.zeros_like(xi), bg)
        m = xi < -2
        dphi_p = (phi[m].max() - phi[m].min()) * T.ME_MP     # e*DeltaPhi / (m_p c^2)
        bp = bg
        dgam_trapped = 2 * gp * bp * np.sqrt(2 * gp * dphi_p) if gp * dphi_p < 1 else np.nan
        rows.append(dict(gamma_p=gp, n_over_nc=1 / gp**2, T_inj_MeV=Ti, max_gain_MeV=gain_MeV,
                         E_max_E0=float(np.abs(E[m]).max()), dphi_proton=dphi_p,
                         bucket_height_MeV=dgam_trapped * 938.272 if np.isfinite(dgam_trapped) else None,
                         t_run=tr.t, steps=nstep))
        print(f"gamma_p={gp:5.1f} T_inj={Ti:6.0f} MeV: max gain = {gain_MeV:9.2f} MeV  (E_max={np.abs(E[m]).max():.2f} E0, "
              f"wake potential={dphi_p*938.272:.2f} MeV; trapped-bucket height ~ {rows[-1]['bucket_height_MeV']} MeV)")
os.makedirs(os.path.join(ROOT, "results", "data"), exist_ok=True)
with open(os.path.join(ROOT, "results", "data", "B2_conventional_protons.json"), "w") as f:
    json.dump(dict(a0=a0, fwhm_cwp=fwhm, rows=rows), f, indent=1)
