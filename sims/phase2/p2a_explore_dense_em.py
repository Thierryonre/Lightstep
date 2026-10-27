"""P2a-explore: in dense plasma (k0/kp = gamma_g), measure with the full-EM 1D PIC
(i) the actual wake phase velocity behind a pulse (vs v_g and the etching-corrected estimate
v_g - v_etch), (ii) the pump-depletion length, and (iii) wake amplitude.
Wake phase velocity measured from the drift of the E-field zero crossings behind the pulse."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import pic1d_em as EM
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
out = []
for k0, a0, sig in [(4.0, 1.0, 1.0), (4.0, 2.0, 1.0), (7.4, 1.0, 1.0), (7.4, 2.0, 1.0)]:
    dx = 2 * np.pi / k0 / 32
    Lx = 70.0
    xc = Lx - 8.0
    ainit = lambda x: a0 * np.exp(-(x - xc)**2 / (4 * sig**2)) * np.cos(k0 * (x - xc))
    Lr = 30.0
    dens = lambda x: np.sin(0.5 * np.pi * np.clip((x - (xc + 5)) / Lr, 0, 1))**2
    em = EM.SimEM1D(Lx, dx, k0, dens, ainit, ppc=8)
    U0 = em.laser_energy()
    rec = []
    t0 = time.time()
    T_end = 400.0
    while em.t < T_end:
        em.step()
        if int(em.t / em.dt) % int(round(10.0 / em.dt)) == 0:
            I = em.A**2
            xL = np.sum(em.grid * I) / np.sum(I)
            # zero crossings of E in the 2nd/3rd period behind the laser centroid
            m = (em.grid < xL - 3) & (em.grid > xL - 25)
            g, E = em.grid[m], em.E[m]
            zc = g[:-1][(E[:-1] > 0) & (E[1:] <= 0)]
            rec.append((em.t, xL, em.laser_energy(), zc[-1] if zc.size else np.nan, np.abs(E).max()))
    rec = np.array(rec)
    t, xL, U, z, Em = rec.T
    sel = t > 5 + Lr + 40
    # phase velocity: slope of zero-crossing position (track the one nearest to the laser) -> unwrap jumps
    vz = np.polyfit(t[sel], z[sel], 1)[0] if np.isfinite(z[sel]).all() else np.nan
    vL = np.polyfit(t[sel], xL[sel], 1)[0]
    dU = np.polyfit(xL[sel], U[sel], 1)[0]
    vg = np.sqrt(1 - 1 / k0**2)
    r = dict(k0=k0, a0=a0, v_g=vg, gamma_g=k0, v_laser_centroid=vL, v_phase_wake=vz,
             gamma_phase=1 / np.sqrt(max(1 - vz**2, 1e-12)) if np.isfinite(vz) and vz < 1 else None,
             v_etch_estimate=vg - 1 / k0**2, E_max=float(np.median(Em[sel])),
             depletion_length=float(-U0 / dU) if dU < 0 else None, U_lost_frac=float(1 - U[-1] / U0), runtime=time.time() - t0)
    out.append(r)
    print(json.dumps(r), flush=True)
json.dump(out, open(os.path.join(ROOT, "results", "data", "P2a_explore_dense_em.json"), "w"), indent=1)
