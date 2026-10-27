import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F
import pic1d_env as P
a0, fwhm = 2.0, 2.3548
for Lx, tprop in [(40.0, 60.0), (120.0, 60.0)]:
    drv = P.Driver([P.Pulse(a0, fwhm, 0.0, "gauss")], x_start=0.0, velocity=1.0)
    sim = P.Sim1D(Lx, 0.02, lambda x: np.ones_like(x), drv, ppc=16, x_plasma_start=4*fwhm, dt=0.01)
    sim.run(tprop)
    xi_p = sim.grid - drv.xd
    lo, hi = -25.0, -2.0
    m = (xi_p > lo) & (xi_p < hi)
    fe = 0.5*np.sum(sim.E[m]**2)*sim.dx
    pe = ((sim.xe - drv.xd) > lo) & ((sim.xe - drv.xd) < hi)
    ke = np.sum(sim.we[pe]*(np.sqrt(1+sim.ue[pe]**2)-1))
    en = sim.energies()
    plasma_len = drv.xd - max(4*fwhm, sim.x0)
    print(f"Lx={Lx}: PIC energy density behind driver = {(fe+ke)/(hi-lo):.4f} (field {fe/(hi-lo):.4f}, kin {ke/(hi-lo):.4f})")
    print(f"   laser_work={en['laser_work']:.3f}, window field+kin={en['field']+en['kin_e']:.3f}, plasma length in window={plasma_len:.1f}, total plasma traversed={drv.xd-4*fwhm:.1f}")
xi = np.linspace(-60, 10, 70001)
a2 = 0.5*a0**2*np.exp(-0.5*(xi/(fwhm/2.3548))**2)
phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), 1.0)
ne, uz, gam = F.fluid_quantities(phi, a2, 1.0)
m = (xi > -25) & (xi < -2)
print("fluid: field", np.mean(0.5*Ez[m]**2), "kin", np.mean(ne[m]*(gam[m]-1)), "total", np.mean(0.5*Ez[m]**2 + ne[m]*(gam[m]-1)))
