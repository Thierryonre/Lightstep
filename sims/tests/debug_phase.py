import sys, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F
import pic1d_env as P
a0, fwhm = 2.0, 2.3548
drv = P.Driver([P.Pulse(a0, fwhm, 0.0, "gauss")], x_start=0.0, velocity=1.0)
sim = P.Sim1D(60.0, 0.02, lambda x: np.ones_like(x), drv, ppc=16, x_plasma_start=4*fwhm, dt=0.01)
sim.run(60.0)
xi_p = sim.grid - drv.xd
xi = np.linspace(-60, 10, 70001)
a2 = 0.5*a0**2*np.exp(-0.5*(xi/(fwhm/2.3548))**2)
phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), 1.0)
ne, uz, gam = F.fluid_quantities(phi, a2, 1.0)
fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
ax[0].plot(xi_p, sim.E, label="PIC"); ax[0].plot(xi, Ez, '--', label="fluid"); ax[0].legend(); ax[0].set_ylabel("Ez/E0")
ax[1].plot(sim.xe - drv.xd, sim.ue, ',', alpha=0.3); ax[1].plot(xi, uz, 'r-', lw=0.8); ax[1].set_ylabel("u_z"); ax[1].set_xlabel("xi")
ax[1].set_xlim(-45, 5); ax[1].set_ylim(-3, 10)
plt.savefig(os.path.join(os.path.dirname(__file__), "debug_phase.png"), dpi=90)
print("max u_e:", sim.ue.max(), " n electrons with u>5:", (sim.ue > 5).sum())
