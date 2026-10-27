"""Cross-check: full-EM 1D PIC vs envelope 1D PIC vs fluid for a0=2, k0/kp=10."""
import sys, os, time
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F, pic1d_env as P, pic1d_em as EM
a0, sigI, k0 = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0, 1.0, float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
bg = np.sqrt(1 - 1/k0**2)
Lx, T = 60.0, 60.0
dx = 2*np.pi/k0/32
xc0 = Lx - 8.0
ainit = lambda x: a0*np.exp(-(x-xc0)**2/(4*sigI**2))*np.cos(k0*(x-xc0))
t0 = time.time()
em = EM.SimEM1D(Lx, dx, k0, lambda x: np.ones_like(x), ainit, ppc=8, x_plasma_start=xc0+5)
UL0 = em.laser_energy()
em.run(T)
# laser centroid
I = em.A**2; xL = np.sum(em.grid*I)/np.sum(I)
print(f"EM done {time.time()-t0:.0f}s; laser energy {UL0:.2f} -> {em.laser_energy():.2f}; centroid xi=0 at x={xL:.2f}")
# envelope PIC with beta = v_g
drv = P.Driver([P.Pulse(a0, 2.3548*sigI, 0.0, "gauss")], x_start=xc0, velocity=bg)
env = P.Sim1D(Lx, 0.02, lambda x: np.ones_like(x), drv, ppc=16, x_plasma_start=xc0+5, dt=0.01, x_window0=0.0)
env.run(T)
xi = np.linspace(-70, 10, 40001)
a2 = 0.5*a0**2*np.exp(-0.5*(xi/sigI)**2)
phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), bg)
fig, ax = plt.subplots(2,1, figsize=(11,7), sharex=True)
ax[0].plot(em.grid - xL, em.E, label="EM PIC"); ax[0].plot(env.grid - drv.xd, env.E, label="envelope PIC")
ax[0].plot(xi, Ez, 'k--', lw=0.8, label="fluid"); ax[0].legend(); ax[0].set_xlim(-55, 8); ax[0].set_ylabel("Ez/E0")
ax[1].plot(em.xe - xL, em.ue, ',', alpha=0.3, label='EM'); ax[1].plot(env.xe - drv.xd, env.ue, ',', alpha=0.3, label='env')
ax[1].set_ylim(-3, 15); ax[1].set_ylabel("u_x"); ax[1].set_xlabel("xi")
fn = os.path.join(os.path.dirname(__file__), f"em_vs_env_a{a0}_k{k0}.png"); plt.savefig(fn, dpi=90)
for lo in [-10, -20, -30, -40]:
    def amp(g, E): m=(g>lo-10)&(g<lo); return np.abs(E[m]).max()
    print(f"amp in [{lo-10},{lo}]: EM={amp(em.grid-xL, em.E):.3f} env={amp(env.grid-drv.xd, env.E):.3f} fluid={amp(xi, Ez):.3f}")
print("max u: EM", em.ue.max(), "env", env.ue.max())
