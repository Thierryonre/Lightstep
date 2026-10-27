import sys, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import pic1d_env as P
a0, fwhm = 2.0, 2.3548
for ps in [4*fwhm, -30.0]:
    drv = P.Driver([P.Pulse(a0, fwhm, 0.0, "gauss")], x_start=0.0, velocity=1.0)
    sim = P.Sim1D(60.0, 0.02, lambda x: np.ones_like(x), drv, ppc=16, x_plasma_start=ps, dt=0.01)
    sim.run(50.0)
    phi = np.zeros(sim.N)
    phi[:-1] = np.cumsum((sim.E[1:] + sim.E[:-1])[::-1] * 0.5 * sim.dx)[::-1]  # phi(x) = int_x^xmax E dx'
    a2 = drv.a2(sim.grid, sim.t)
    phik = np.interp(sim.xe, sim.grid, phi); a2k = np.interp(sim.xe, sim.grid, a2)
    H = np.sqrt(1 + sim.ue**2 + a2k) - sim.ue - phik
    xi = sim.xe - drv.xd
    for lo in [-5, -15, -25, -35, -45]:
        m = (xi > lo - 10) & (xi < lo)
        print(f"plasma_start={ps:6.1f} xi in [{lo-10},{lo}]: H mean={H[m].mean():.4f} std={H[m].std():.4f} min={H[m].min():.3f}")
