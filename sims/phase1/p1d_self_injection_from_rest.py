"""P1d: proton self-injection from rest by a slow, accelerating ponderomotive driver
(1D longitudinal analogue of the transverse-flying-focus scheme, Gong et al. PRL 133, 265002),
with an optional nanoparticle-like dense hydrogen layer at the start point (Phase-1 'NP').

Driver: Gaussian <a^2> (FWHM ell), amplitude ramped up at rest over t_on, then constant proper
acceleration alpha0:  u_d(t) = alpha0 (t - t_on),  beta_d = u_d / sqrt(1 + u_d^2).
Plasma: hydrogen, electrons + mobile protons; optional layer n_np over thickness d_np centred
just ahead of the driver.  Diagnostics: protons with T > T_cut that ride with the driver,
their energy, number (areal), and the exact laser work -> efficiency.
Trapping criterion to compare with (Gong et al.): alpha0 < Lambda = e E_max / m_p,
here E_max = peak forward field on the driver front slope (1D adiabatic estimate
E = -d/dx sqrt(1+<a^2>)).
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import pic1d_env as P

MP = 938.27208816
ME = 0.51099895
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


def lambda_est(a0, ell):
    x = np.linspace(-4 * ell, 4 * ell, 4001)
    sig = ell / 2.3548
    g = np.sqrt(1 + 0.5 * a0**2 * np.exp(-0.5 * (x / sig) ** 2))
    E = -np.gradient(g, x)
    return E.max() * P.ME_OVER_MP, E.max()


def run(a0=3.0, ell=1.0, alpha_frac=0.5, t_on=20.0, T_final=1000.0, n_np=0.0, d_np=0.5,
        dx=0.01, ppc=16, max_t=None, verbose=True):
    Lam, Emax = lambda_est(a0, ell)
    alpha0 = alpha_frac * Lam
    x0 = 0.0
    state = {}

    def vel(t, xd, sim):
        if t < t_on:
            return 0.0
        u = alpha0 * (t - t_on)
        return u / np.sqrt(1 + u * u)

    def amp(t, xd):
        return min(1.0, t / t_on) ** 2

    drv = P.Driver([P.Pulse(a0, ell, 0.0, "gauss")], x_start=x0, velocity=vel, amp=amp)
    xs_np = x0 + 1.0 * ell

    def dens(x):
        base = np.ones_like(x)
        if n_np > 0:
            base = base + n_np * (np.abs(x - xs_np) < 0.5 * d_np)
        return base

    Lx = 20.0 * ell + 20
    sim = P.Sim1D(Lx, dx, dens, drv, ppc=ppc, dt=0.5 * dx if dx < 0.015 else 0.01, mobile_ions=True,
                  x_window0=x0 - 0.6 * Lx, n_max=1 + n_np)
    u_final = np.sqrt((1 + T_final / MP) ** 2 - 1)
    t_end = t_on + u_final / alpha0 * 1.05 if max_t is None else max_t
    t0 = time.time()
    snaps = []
    next_snap = 0.0
    while sim.t < t_end:
        sim.step()
        if sim.t >= next_snap:
            next_snap += (t_end - t_on) / 25
            Ti = (np.sqrt(1 + sim.ui**2) - 1) * MP
            fast = Ti > 1.0                       # > 1 MeV
            near = np.abs(sim.xi - drv.xd) < 5 * ell
            sel = fast & near
            rec = dict(t=sim.t, xd=drv.xd, beta_d=vel(sim.t, drv.xd, sim),
                       n_fast_near=float(sim.wi[sel].sum()),
                       T_mean_fast=float(np.average(Ti[sel], weights=sim.wi[sel])) if sel.any() else 0.0,
                       T_max=float(Ti.max()), laser_work=sim.pond_work)
            snaps.append(rec)
            if verbose:
                print(f"   t={sim.t:7.0f} xd={drv.xd:8.1f} beta_d={rec['beta_d']:.4f} riding protons: areal={rec['n_fast_near']:.4f} "
                      f"T_mean={rec['T_mean_fast']:.1f} MeV T_max={rec['T_max']:.1f} MeV ({time.time()-t0:.0f}s)", flush=True)
    Ti = (np.sqrt(1 + sim.ui**2) - 1) * MP
    sel = (Ti > 0.5 * T_final) & (np.abs(sim.xi - drv.xd) < 5 * ell)
    gain = float(np.sum(sim.wi[sel] * Ti[sel]) / ME)             # areal, m_e c^2 units
    Ekin_all_i = float(np.sum(sim.wi * Ti) / ME)
    out = dict(a0=a0, ell=ell, alpha_frac=alpha_frac, alpha0=alpha0, Lambda=Lam, E_front_max=Emax,
               n_np=n_np, d_np=d_np, t_end=sim.t, xd=drv.xd,
               trapped_areal=float(sim.wi[sel].sum()),
               T_trapped_mean=float(np.average(Ti[sel], weights=sim.wi[sel])) if sel.any() else 0.0,
               T_trapped_std=float(np.sqrt(np.average((Ti[sel] - np.average(Ti[sel], weights=sim.wi[sel]))**2, weights=sim.wi[sel]))) if sel.any() else 0.0,
               laser_work=float(sim.pond_work), eff_laser_to_trapped=gain / sim.pond_work if sim.pond_work > 0 else 0.0,
               eff_laser_to_all_ions_in_window=Ekin_all_i / sim.pond_work if sim.pond_work > 0 else 0.0,
               runtime_s=time.time() - t0, snaps=snaps)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a0", type=float, default=3.0)
    ap.add_argument("--ell", type=float, default=1.0)
    ap.add_argument("--alpha", type=float, default=0.5)
    ap.add_argument("--Tf", type=float, default=300.0)
    ap.add_argument("--np", type=float, default=0.0)
    ap.add_argument("--tag", default="test")
    a = ap.parse_args()
    out = run(a0=a.a0, ell=a.ell, alpha_frac=a.alpha, T_final=a.Tf, n_np=a.np)
    print(json.dumps({k: v for k, v in out.items() if k != "snaps"}, indent=1))
    json.dump(out, open(os.path.join(ROOT, "results", "data", f"P1d_{a.tag}.json"), "w"), indent=1)
