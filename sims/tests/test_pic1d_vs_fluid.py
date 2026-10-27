"""Validate the 1D envelope PIC against the 1D nonlinear fluid model (before wave breaking)."""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F
import pic1d_env as P

def run_case(a0, beta, fwhm, Lx=40.0, dx=0.02, ppc=16, t_prop=60.0):
    drv = P.Driver([P.Pulse(a0, fwhm, 0.0, "gauss")], x_start=0.0, velocity=beta)
    sim = P.Sim1D(Lx, dx, lambda x: np.ones_like(x), drv, ppc=ppc,
                  x_plasma_start=4 * fwhm, dt=0.5 * dx * max(beta, 0.2))
    t0 = time.time()
    sim.run(t_prop / beta if beta < 1 else t_prop)
    xi_p = sim.grid - drv.xd
    # fluid solution on same xi grid
    xi = np.linspace(xi_p[0], xi_p[-1], 20001)
    a2 = 0.5 * a0**2 * np.exp(-0.5 * (xi / (fwhm / 2.3548)) ** 2)
    phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), beta)
    Ef = np.interp(xi_p, xi, Ez)
    # compare in a window behind the driver but inside the region already traversed
    m = (xi_p < -2) & (xi_p > -min(25, 0.9 * t_prop))
    err = np.sqrt(np.mean((sim.E[m] - Ef[m])**2)) / np.abs(Ef[m]).max()
    print(f"a0={a0} beta={beta}: Emax PIC={np.abs(sim.E[m]).max():.4f} fluid={np.abs(Ef[m]).max():.4f} "
          f"rel.rms diff={err:.3%}  fluid_broken={br}  ({time.time()-t0:.1f}s, {sim.xe.size} e-)")
    return sim, xi_p, Ef

for a0 in [0.5, 1.0, 2.0]:
    run_case(a0, 1.0, 2.3548)
run_case(0.3, 0.5, 2.3548 * 0.5)
run_case(0.5, 0.9, 2.3548 * 0.9)
