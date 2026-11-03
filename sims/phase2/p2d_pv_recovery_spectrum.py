"""P2d: can the laser light left after the plasma be recovered with monochromatic photovoltaics?
Full-EM 1D PIC (laser resolved): track the transmitted laser spectrum as the driver depletes.
Photon deceleration in the wake (photon number ~ conserved) means energy given to the plasma is
taken as a red-shift, so the remaining light broadens to lower frequencies.
PV model: monochromatic laser power converter with bandgap matched to the drive line
(w_g = 0.95 w0); photons below w_g are not absorbed; photons above deliver eta_max * w_g / w
(thermalisation loss). eta_max = 0.55 (best demonstrated at ~1.07 um, Broadcom 2025 [lit]);
0.689 is the GaAs record at ~0.85 um [lit].
Outputs: recoverable fraction of the remaining laser energy vs fraction absorbed by the plasma.
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import pic1d_em as EM

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


def spectrum(em):
    """Energy spectrum of the transverse field vs normalised frequency w/w0 (w ~ c k in
    underdense plasma; |E_k|^2 + |B_k|^2 with E = -dA/dt, B = dA/dx)."""
    A = 0.5 * (em.A + em.Aold)
    Ey = -(em.A - em.Aold) / em.dt
    Bz = np.gradient(A, em.dx)
    k = 2 * np.pi * np.fft.rfftfreq(A.size, em.dx)
    Pk = np.abs(np.fft.rfft(Ey)) ** 2 + np.abs(np.fft.rfft(Bz)) ** 2
    # w = sqrt(k^2 + w_p^2) in units of w_p; normalise to w0 = sqrt(k0^2 + 1)
    w = np.sqrt(k ** 2 + 1.0) / np.sqrt(em.k0 ** 2 + 1.0)
    return w, Pk / Pk.sum()


def pv_recoverable(w, P, eta_max=0.55, wg=0.95):
    """wg: bandgap in units of w0, set 5 % below the LOWEST drive line (each line can have its own
    matched cell; a single cell at the lowest line is the conservative choice)."""
    eff = np.where(w >= wg, eta_max * wg / np.maximum(w, 1e-9), 0.0)
    return float(np.sum(P * eff)), float(np.sum(P[(w > 0.9) & (w < 1.1)]))


def run(case="beat", k0=10.0, a=0.7, sigI=6.0, L=6000.0, nsnap=12, ppc=8):
    """PV acceptance: photons with w >= 0.95 w_low (lowest drive line) are converted with
    efficiency eta_max * w_g / w; 'in-band' = fraction within +-10 % of w0."""
    dx = 2 * np.pi / k0 / 32
    Lx = 6 * sigI + 60
    xc = Lx - 3 * sigI - 5
    env = lambda x: np.exp(-(x - xc) ** 2 / (4 * sigI ** 2))
    if case == "beat":      # two lines spaced by w_p (resonant beat-wave train)
        k1 = k0
        k2 = np.sqrt((np.sqrt(k0 ** 2 + 1) - 1) ** 2 - 1)
        ainit = lambda x: a * env(x) * (np.cos(k1 * (x - xc)) + np.cos(k2 * (x - xc)))
    else:                   # single short resonant pulse
        ainit = lambda x: a * np.exp(-(x - xc) ** 2 / (4 * 1.0 ** 2)) * np.cos(k0 * (x - xc))
    Lr = 30.0
    dens = lambda x: np.sin(0.5 * np.pi * np.clip((x - (xc + 3 * sigI + 5)) / Lr, 0, 1)) ** 2
    em = EM.SimEM1D(Lx, dx, k0, dens, ainit, ppc=ppc)
    w_low = (np.sqrt(k0 ** 2 + 1) - 1) / np.sqrt(k0 ** 2 + 1) if case == "beat" else 1.0
    U0 = em.laser_energy()
    out = []
    t0 = time.time()
    every = L / nsnap
    nxt = 0.0
    while em.t < L:
        em.step()
        if em.t >= nxt:
            nxt += every
            U = em.laser_energy()
            w, P = spectrum(em)
            wg = 0.95 * w_low
            rec, inband = pv_recoverable(w, P, wg=wg)
            rec69, _ = pv_recoverable(w, P, eta_max=0.689, wg=wg)
            out.append(dict(t=em.t, absorbed_frac=float(1 - U / U0), remaining_frac=float(U / U0),
                            PV_eff_on_remaining=rec, PV_eff_on_remaining_GaAs_like=rec69,
                            inband_frac_10pct=inband, mean_w=float(np.sum(w * P))))
            r = out[-1]
            print(f"   t={em.t:6.0f} absorbed={r['absorbed_frac']:.3f} <w>/w0={r['mean_w']:.3f} "
                  f"in-band(+-10%)={r['inband_frac_10pct']:.3f} PV eff on remaining={r['PV_eff_on_remaining']:.3f} "
                  f"({time.time()-t0:.0f}s)", flush=True)
    return dict(case=case, k0_over_kp=k0, a=a, sigI=sigI, U0=U0, snaps=out, runtime_s=time.time() - t0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default="beat")
    ap.add_argument("--a", type=float, default=0.7)
    ap.add_argument("--L", type=float, default=6000.0)
    ap.add_argument("--k0", type=float, default=10.0)
    a = ap.parse_args()
    r = run(case=a.case, a=a.a, L=a.L, k0=a.k0)
    json.dump(r, open(os.path.join(ROOT, "results", "data", f"P2d_pv_spectrum_{a.case}.json"), "w"), indent=1)
