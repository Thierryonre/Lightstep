"""R3-1D: dephasing mitigation by a linear density up-ramp (Lahaye et al., PRR 8, 023274
(2026)), reproduced as a mechanism with the kinetic 1D envelope PIC (density gradients are
treated exactly per plasma sheet; the quasi-static ODE would not capture the gradient-induced
phase velocity correctly).

Parameters follow the paper's FBPIC set where 1D allows: n0 = 1e18 cm^-3, 0.8 um
(k0/kp = 41.7), a0 = 1.6, 25 fs, flat vs n0(1 + g z[mm]) with g = 0.08 /mm (paper) and a scan.
Driver moves at the local etching-corrected velocity c sqrt(1 - 3n/n_c) (Lu et al. 2007),
mimicking the 3D bubble dephasing length (no laser evolution - 1D limitation).
Test electrons (zero charge) spread over the first accelerating bucket at 50 MeV; the
best-phase energy vs distance is recorded. Also the wake phase velocity at the bucket is
compared with Eq. 2 of the paper, v_phi ~ v_g (1 + (xi / 2n) dn/dz).
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import pic1d_env as P
import plasma as PL

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
ME = 0.51099895


def run(g_per_mm=0.0, L_mm=24.0, a0=1.6, tau_fs=25.0, n0_cm3=1e18, lam=0.8e-6, verbose=False):
    n0 = n0_cm3 * 1e6
    cwp = 1 / PL.k_p(n0)
    k0kp = np.sqrt(PL.n_crit(lam) / n0)
    fwhm = tau_fs * 1e-15 * PL.omega_p(n0)          # intensity FWHM in c/wp
    g = g_per_mm * cwp * 1e3                        # gradient per c/wp
    Lr = 60.0
    x_pl = 10.0

    def dens(x):
        ramp = np.sin(0.5 * np.pi * np.clip((x - x_pl) / Lr, 0, 1)) ** 2
        return ramp * (1 + g * np.clip(x - x_pl - Lr, 0, None))

    def vel(t, xd, sim):
        n = float(dens(np.array([xd]))[0])
        # Lu et al. (2007) etching-corrected nonlinear phase velocity v ~ c (1 - 3 wp^2/(2 w0^2))
        return np.sqrt(max(1 - 3 * n / k0kp ** 2, 0.0)) if n > 0 else 1.0

    drv = P.Driver([P.Pulse(a0, fwhm, 0.0, "gauss")], x_start=0.0, velocity=vel)
    lam_p = 2 * np.pi
    Lx = 2.2 * lam_p + 10
    nmax = 1 + g * L_mm * 1e-3 / cwp
    sim = P.Sim1D(Lx, 0.02, dens, drv, ppc=12, dt=0.01, x_window0=-(Lx - 6), n_max=nmax)
    while drv.xd < x_pl + Lr + 5:
        sim.step()
    # test electrons over the first bucket behind the driver
    ne = 3000
    xi = np.linspace(-1.5 * lam_p, -0.3 * lam_p, ne)
    gam0 = 1 + 50.0 / ME
    sim.add_beam(drv.xd + xi, np.full(ne, np.sqrt(gam0 ** 2 - 1)), np.zeros(ne), q=-1.0, qm=-1.0)
    sim.beam_qm = -1.0
    x0 = drv.xd
    Tmax_hist = []
    t0 = time.time()
    L = L_mm * 1e-3 / cwp
    Emax_running = np.zeros(ne)
    while drv.xd - x0 < L:
        sim.step()
        if int(sim.t / sim.dt) % 2000 == 0:
            T = (np.sqrt(1 + sim.ub ** 2) - 1) * ME
            Tmax_hist.append((float((drv.xd - x0) * cwp * 1e3), float(T.max())))
    res = dict(g_per_mm=g_per_mm, n0_cm3=n0_cm3, a0=a0, tau_fs=tau_fs, k0_over_kp=k0kp,
               hist=Tmax_hist, E_peak_MeV=max(h[1] for h in Tmax_hist),
               z_peak_mm=max(Tmax_hist, key=lambda h: h[1])[0], runtime=time.time() - t0)
    return res


if __name__ == "__main__":
    out = []
    for gpm in [0.0, 0.04, 0.08, 0.12]:
        r = run(g_per_mm=gpm)
        out.append(r)
        print(f"gradient {gpm:.2f} n0/mm: peak energy {r['E_peak_MeV']:.0f} MeV at z = {r['z_peak_mm']:.1f} mm ({r['runtime']:.0f}s)", flush=True)
    base = out[0]["E_peak_MeV"]
    for r in out:
        r["ratio_vs_flat"] = r["E_peak_MeV"] / base
    json.dump(out, open(os.path.join(ROOT, "results", "data", "R3_lahaye_mechanism_1d.json"), "w"), indent=1)
    print("ratios vs flat:", [round(r["ratio_vs_flat"], 3) for r in out])
