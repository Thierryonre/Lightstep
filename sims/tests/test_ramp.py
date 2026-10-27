import sys, os, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F, pic1d_env as P
a0, sig = 2.0, 1.0
xi = np.linspace(-70, 10, 40001)
a2 = 0.5*a0**2*np.exp(-0.5*(xi/sig)**2)
phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), 1.0)
for Lramp in [0.0, 10.0, 30.0, 60.0]:
    xs = 10.0
    def dens(x, xs=xs, L=Lramp):
        if L == 0: return np.where(x >= xs, 1.0, 0.0)
        r = np.clip((x - xs)/L, 0, 1)
        return np.sin(0.5*np.pi*r)**2
    drv = P.Driver([P.Pulse(a0, 2.3548*sig, 0.0, "gauss")], x_start=0.0, velocity=1.0)
    sim = P.Sim1D(60.0, 0.02, dens, drv, ppc=16, dt=0.01)
    T = xs + Lramp + 70.0
    t0=time.time(); sim.run(T)
    g = sim.grid - drv.xd
    amps = []
    for lo in [-10, -20, -30, -40]:
        m = (g > lo-10) & (g < lo); amps.append(np.abs(sim.E[m]).max())
    print(f"ramp L={Lramp}: amplitudes {np.round(amps,3)} (fluid 0.901) max u={sim.ue.max():.1f} n(u>3)={np.sum(sim.ue>3)} ({time.time()-t0:.0f}s)")
