import sys, os, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F
import pic1d_env as P
a0, fwhm = 2.0, 2.3548
xi = np.linspace(-60, 10, 70001)
a2 = 0.5*a0**2*np.exp(-0.5*(xi/(fwhm/2.3548))**2)
phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), 1.0)
def amp_at(xg, E, lo, hi):
    m = (xg > lo) & (xg < hi); return np.abs(E[m]).max()
print("fluid amplitude in [-40,-30]:", amp_at(xi, Ez, -40, -30))
for dx, ppc, dtf, T in [(0.02,16,0.5,0.0),(0.01,32,0.5,0.0),(0.005,32,0.5,0.0),(0.02,16,0.1,0.0),(0.02,64,0.5,0.0),(0.02,16,0.5,1e-3)]:
    drv = P.Driver([P.Pulse(a0, fwhm, 0.0, "gauss")], x_start=0.0, velocity=1.0)
    sim = P.Sim1D(50.0, dx, lambda x: np.ones_like(x), drv, ppc=ppc, x_plasma_start=4*fwhm, dt=dtf*dx)
    if T > 0:
        rng = np.random.default_rng(0); sim.ue += rng.normal(0, np.sqrt(T), sim.ue.size)
    t0=time.time(); sim.run(50.0)
    xg = sim.grid - drv.xd
    print(f"dx={dx} ppc={ppc} dt={dtf}dx T={T}: amp[-40,-30]={amp_at(xg, sim.E, -40, -30):.3f}  amp[-20,-10]={amp_at(xg, sim.E, -20, -10):.3f} max u={sim.ue.max():.1f} ({time.time()-t0:.0f}s)")
