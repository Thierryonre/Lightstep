"""Clean cross-check (smooth 60 c/wp entrance ramp): full-EM 1D PIC vs envelope PIC vs fluid,
and laser depletion: EM laser energy loss vs envelope-PIC laser work."""
import sys, os, time
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F, pic1d_env as P, pic1d_em as EM
a0 = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
k0 = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
sigI = 1.0
bg = np.sqrt(1 - 1/k0**2)
Lx, Lr, Lflat = 60.0, 60.0, 60.0
xc0 = Lx - 8.0
xs = xc0 + 5
dens = lambda x: np.sin(0.5*np.pi*np.clip((x - xs)/Lr, 0, 1))**2
T = 5 + Lr + Lflat
dx = 2*np.pi/k0/32
ainit = lambda x: a0*np.exp(-(x-xc0)**2/(4*sigI**2))*np.cos(k0*(x-xc0))
t0 = time.time()
em = EM.SimEM1D(Lx, dx, k0, dens, ainit, ppc=8)
UL0 = em.laser_energy(); em.run(T); UL1 = em.laser_energy()
I = em.A**2; xL = np.sum(em.grid*I)/np.sum(I)
tem = time.time()-t0
drv = P.Driver([P.Pulse(a0, 2.3548*sigI, 0.0, "gauss")], x_start=xc0, velocity=bg)
env = P.Sim1D(Lx, 0.02, dens, drv, ppc=16, dt=0.01, x_window0=0.0)
env.run(T)
xi = np.linspace(-70, 10, 40001)
a2 = 0.5*a0**2*np.exp(-0.5*(xi/sigI)**2)
phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), bg)
u_fl = F.wake_energy_density(xi, phi, Ez, a2, bg, -20.0)
print(f"a0={a0} k0={k0}: EM run {tem:.0f}s")
for lo in [-10, -20, -30, -40]:
    def amp(g, E): m=(g>lo-10)&(g<lo); return np.abs(E[m]).max()
    print(f"  amp [{lo-10},{lo}]: EM={amp(em.grid-xL, em.E):.3f} env={amp(env.grid-drv.xd, env.E):.3f} fluid={amp(xi, Ez):.3f}")
# depletion: energy lost per unit length in the flat region vs fluid wake energy density
print(f"  EM laser energy {UL0:.2f} -> {UL1:.2f}: lost {UL0-UL1:.2f}; envelope laser work {env.pond_work:.2f}; "
      f"fluid estimate (u_wake x (Lr/2+Lflat)) = {u_fl*(Lr/2+Lflat):.2f}")
fig, ax = plt.subplots(figsize=(11,4))
ax.plot(em.grid - xL, em.E, label="EM PIC"); ax.plot(env.grid - drv.xd, env.E, label="envelope PIC")
ax.plot(xi, Ez, 'k--', lw=0.8, label="fluid"); ax.legend(); ax.set_xlim(-55, 8); ax.set_xlabel("xi [c/wp]"); ax.set_ylabel("Ez/E0")
ax.set_title(f"a0={a0}, k0/kp={k0}, smooth 60 c/wp ramp")
plt.tight_layout(); plt.savefig(os.path.join(os.path.dirname(__file__), f"em_vs_env_ramp_a{a0}_k{k0}.png"), dpi=90)
