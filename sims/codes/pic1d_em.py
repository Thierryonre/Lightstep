"""1D relativistic electromagnetic PIC (laser resolved), moving window at c.

Normalisation (reference density n_ref): t in 1/w_p, x in c/w_p, A = e A_y/(m_e c),
E in m_e c w_p/e, densities in n_ref. Laser wavenumber k0 = w0/w_p (= sqrt(n_c/n_ref)).

Transverse dynamics via canonical momentum conservation (cold plasma, plane wave):
    u_y = -(q/m) A,     d^2A/dt^2 - d^2A/dx^2 = J_y = -sum_s (q_s^2/m_s) n_s A / gamma_s
Longitudinal:
    dE/dx = rho (Gauss, E = 0 at the right edge),
    du_x/dt = (q/m) E - (q/m)^2 d(A^2)/dx / (2 gamma),  gamma = sqrt(1 + u_x^2 + (q/m)^2 A^2)
The wave equation is advanced with leapfrog at dt = dx (dispersion-free in vacuum in 1D) with
the plasma current treated time-centred implicitly, J = -chi (A^{n+1} + A^{n-1})/2, which is
unconditionally stable at dt = dx and reproduces w^2 = k^2 + chi;
the window shifts exactly one cell per step. Includes laser depletion, red-shift, Raman etc.
"""
import numpy as np
from numba import njit

ME_OVER_MP = 1.0 / 1836.15267343


@njit(cache=True)
def deposit_rho_J(x, u, w, q, qm, x0, dx, A, rho, J):
    n = rho.size
    q2m2 = qm * qm
    for k in range(x.size):
        s = (x[k] - x0) / dx
        j = int(np.floor(s))
        f = s - j
        if j < 0 or j >= n - 1:
            continue
        Ak = A[j] * (1 - f) + A[j + 1] * f
        g = np.sqrt(1.0 + u[k] * u[k] + q2m2 * Ak * Ak)
        rho[j] += q * w[k] * (1 - f) / dx
        rho[j + 1] += q * w[k] * f / dx
        chi = q * qm * w[k] / g        # J_y = -chi*A  (q n u_y/gamma, u_y = -(q/m) A)
        J[j] += chi * (1 - f) / dx
        J[j + 1] += chi * f / dx


@njit(cache=True)
def gauss_field(rho, dx, E):
    n = rho.size
    E[n - 1] = 0.0
    for j in range(n - 2, -1, -1):
        E[j] = E[j + 1] - 0.5 * (rho[j] + rho[j + 1]) * dx


@njit(cache=True)
def push(x, u, qm, x0, dx, E, A, A2grad, dt):
    n = E.size
    q2m2 = qm * qm
    for k in range(x.size):
        s = (x[k] - x0) / dx
        j = int(np.floor(s))
        f = s - j
        if j < 0 or j >= n - 1:
            continue
        Ek = E[j] * (1 - f) + E[j + 1] * f
        Ak = A[j] * (1 - f) + A[j + 1] * f
        Gk = A2grad[j] * (1 - f) + A2grad[j + 1] * f
        uh = u[k] + 0.5 * dt * qm * Ek
        g = np.sqrt(1.0 + uh * uh + q2m2 * Ak * Ak)
        u[k] += dt * (qm * Ek - q2m2 * 0.5 * Gk / g)
        gn = np.sqrt(1.0 + u[k] * u[k] + q2m2 * Ak * Ak)
        x[k] += dt * u[k] / gn


class SimEM1D:
    def __init__(self, Lx, dx, k0, density, a_init, ppc=8, x_window0=0.0,
                 mobile_ions=False, x_plasma_start=None):
        """a_init(x): initial laser vector potential A(x, t=0) for a right-moving pulse
        (the t=-dt field is obtained by shifting by dx)."""
        self.dx = dx
        self.dt = dx
        self.N = int(round(Lx / dx)) + 1
        self.x0 = x_window0
        self.k0 = k0
        self.density = density
        self.ppc = ppc
        self.t = 0.0
        self.mobile_ions = mobile_ions
        self.grid = self.x0 + dx * np.arange(self.N)
        self.A = a_init(self.grid)
        self.Aold = a_init(self.grid + dx)   # pulse moving right: A(x,-dt) = A(x+dt,0)
        xs = self._uniform(self.grid[0], self.grid[-1])
        if x_plasma_start is not None:
            xs = xs[xs >= x_plasma_start]
        ws = density(xs) * dx / ppc
        k = ws > 0
        self.xe, self.we = xs[k].copy(), ws[k].copy()
        self.ue = np.zeros_like(self.xe)
        self.xi, self.wi = xs[k].copy(), ws[k].copy()
        self.ui = np.zeros_like(self.xi)
        self.rho = np.zeros(self.N)
        self.J = np.zeros(self.N)
        self.E = np.zeros(self.N)
        self.xb = np.zeros(0); self.ub = np.zeros(0); self.wb = np.zeros(0)
        self.beam_qm = ME_OVER_MP

    def _uniform(self, xa, xb):
        n = int(round((xb - xa) / self.dx))
        offs = (np.arange(self.ppc) + 0.5) / self.ppc
        return (xa + self.dx * (np.arange(n)[:, None] + offs[None, :])).ravel()

    def laser_energy(self):
        """Areal EM energy of the transverse field, units n_ref m_e c^2 c/w_p:
        (1/2)(E_y^2 + B_z^2) with E_y = -dA/dt, B_z = dA/dx."""
        Ey = -(self.A - self.Aold) / self.dt
        Bz = np.gradient(0.5 * (self.A + self.Aold), self.dx)
        return 0.5 * np.sum(Ey**2 + Bz**2) * self.dx

    def step(self):
        dx, dt = self.dx, self.dt
        self.rho[:] = 0.0
        self.J[:] = 0.0
        deposit_rho_J(self.xe, self.ue, self.we, -1.0, -1.0, self.x0, dx, self.A, self.rho, self.J)
        deposit_rho_J(self.xi, self.ui, self.wi, 1.0, ME_OVER_MP, self.x0, dx, self.A, self.rho, self.J)
        if self.xb.size:
            deposit_rho_J(self.xb, self.ub, self.wb, 1.0, self.beam_qm, self.x0, dx, self.A,
                          self.rho, self.J)
        gauss_field(self.rho, dx, self.E)
        A2g = np.gradient(self.A**2, dx)
        push(self.xe, self.ue, -1.0, self.x0, dx, self.E, self.A, A2g, dt)
        if self.mobile_ions:
            push(self.xi, self.ui, ME_OVER_MP, self.x0, dx, self.E, self.A, A2g, dt)
        if self.xb.size:
            push(self.xb, self.ub, self.beam_qm, self.x0, dx, self.E, self.A, A2g, dt)
        # wave equation, leapfrog with dt = dx
        A = self.A
        lap = np.zeros_like(A)
        lap[1:-1] = (A[2:] - 2 * A[1:-1] + A[:-2]) / dx**2
        a = 0.5 * dt**2 * self.J          # self.J holds chi = sum q^2/m n/gamma
        Anew = (2 * A - self.Aold * (1 + a) + dt**2 * lap) / (1 + a)
        # Mur boundaries (exact for dt = dx in 1D)
        Anew[0] = A[1]
        Anew[-1] = A[-2]
        self.Aold, self.A = A, Anew
        self.t += dt
        # move window by one cell (dt = dx, window speed c)
        self._shift()

    def _shift(self):
        dx = self.dx
        x_old_end = self.grid[-1]
        self.x0 += dx
        self.grid = self.x0 + dx * np.arange(self.N)
        self.A = np.concatenate([self.A[1:], [0.0]])
        self.Aold = np.concatenate([self.Aold[1:], [0.0]])
        for nm in ("e", "i"):
            x = getattr(self, "x" + nm)
            m = x >= self.x0
            if not m.all():
                setattr(self, "x" + nm, x[m]); setattr(self, "u" + nm, getattr(self, "u" + nm)[m])
                setattr(self, "w" + nm, getattr(self, "w" + nm)[m])
        if self.xb.size:
            m = self.xb >= self.x0
            self.xb, self.ub, self.wb = self.xb[m], self.ub[m], self.wb[m]
        xs = self._uniform(x_old_end, x_old_end + dx)
        ws = self.density(xs) * dx / self.ppc
        k = ws > 0
        if k.any():
            for nm, val in (("e", 0), ("i", 0)):
                setattr(self, "x" + nm, np.concatenate([getattr(self, "x" + nm), xs[k]]))
                setattr(self, "u" + nm, np.concatenate([getattr(self, "u" + nm), np.zeros(k.sum())]))
                setattr(self, "w" + nm, np.concatenate([getattr(self, "w" + nm), ws[k]]))

    def run(self, t_end, every=0, cb=None):
        n = int(np.ceil((t_end - self.t) / self.dt))
        for s in range(n):
            self.step()
            if every and cb is not None and s % every == 0:
                cb(self)
