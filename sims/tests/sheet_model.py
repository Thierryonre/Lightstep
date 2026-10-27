"""Gridless 1D Dawson sheet model (exact 1D electrostatics) with ponderomotive driver.
Ions: immobile uniform background n=1 for x>x_p. Electron sheets of areal charge w."""
import sys, os, time
import numpy as np
from numba import njit
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F

@njit(cache=True)
def run(x, u, w, xp, xR, a0sq, sig, beta, x_d0, dt, nsteps):
    N = x.size
    for s in range(nsteps):
        t = s * dt
        xd = x_d0 + beta * t
        order = np.argsort(x)
        # field at each sheet: E(x) = -(charge to the right), own charge counted half
        nright = 0
        for jj in range(N - 1, -1, -1):
            k = order[jj]
            ion_right = (xR - max(x[k], xp)) if x[k] < xR else 0.0
            Ek = -(ion_right - w * (nright + 0.5))
            nright += 1
            xi = x[k] - xd
            a2 = a0sq * np.exp(-0.5 * (xi / sig) ** 2)
            da2 = -xi / sig**2 * a2
            g = np.sqrt(1 + u[k]**2 + a2)
            u[k] += dt * (-Ek - 0.5 * da2 / g)
            # NB: field evaluated before position update of this sheet (same time level)
        for k in range(N):
            xi = x[k] - (xd + beta*dt*0)
            a2 = a0sq * np.exp(-0.5 * (xi / sig) ** 2)
            x[k] += dt * u[k] / np.sqrt(1 + u[k]**2 + a2)
    return x, u

a0, sig = 2.0, 1.0
for beta, npu in [(1.0, 100), (1.0, 400), (0.995, 100)]:
    xp, xR = 5.0, 90.0
    x = xp + (np.arange(int((xR - xp) * npu)) + 0.5) / npu
    u = np.zeros_like(x)
    w = 1.0 / npu
    T, dt = 60.0, 0.0025
    t0 = time.time()
    x, u = run(x, u, w, xp, xR, 0.5 * a0**2, sig, beta, 0.0, dt, int(T / dt))
    xd = beta * T
    # field on a grid from sheets: E(x) = -(ion charge right - electron charge right)
    xs = np.sort(x)
    g = np.linspace(xd - 55, xd + 5, 6001)
    ion_right = xR - np.maximum(g, xp)
    e_right = w * (xs.size - np.searchsorted(xs, g))
    E = -(ion_right - e_right)
    xi = np.linspace(-70, 10, 40001)
    a2 = 0.5 * a0**2 * np.exp(-0.5 * (xi / sig) ** 2)
    phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), beta)
    out = []
    for lo in [-10, -20, -30, -40, -50]:
        m = (g - xd > lo - 10) & (g - xd < lo)
        out.append(f"[{lo-10},{lo}]: {np.abs(E[m]).max():.3f}")
    print(f"sheet model beta={beta} sheets/unit={npu} ({time.time()-t0:.0f}s): max u={u.max():.1f}; amplitude " + "  ".join(out))
