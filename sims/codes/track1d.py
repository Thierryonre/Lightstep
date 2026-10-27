"""Quasi-static 1D wake + proton beam tracker (fast model for long accelerations).

At every step the wake behind the driver is recomputed with the nonlinear cold-fluid model
(fluid1d.solve_wake) for the instantaneous driver velocity beta_d, including the beam-loading
term of the proton macro-particles. Protons are then pushed in that field:
    du/dt = (m_e/m_p) E_z(xi),   dxi/dt = beta - beta_d          (xi = x - x_d, units c/w_p)
Valid when beta_d varies slowly compared with w_p (adiabatic wake) and below wave breaking
(the fluid solver flags breaking = onset of background-electron trapping in a cold plasma).

Energy accounting per unit area (units n m_e c^2 c/w_p):
  - laser->plasma work per unit driver path = u_wake of the *unloaded* wake (causality: the
    beam behind the driver cannot change the work done by the driver ahead of it);
  - beam energy gain is integrated directly. wake->beam efficiency = gain / laser work.
"""
import numpy as np
from numba import njit
import fluid1d as F

ME_MP = 1.0 / 1836.15267343
MPC2_ME = 1836.15267343          # proton rest energy in m_e c^2


@njit(cache=True)
def deposit_cic(xk, wk, xi0, dxi, nb):
    n = nb.size
    for k in range(xk.size):
        s = (xk[k] - xi0) / dxi
        j = int(np.floor(s))
        f = s - j
        if j >= 0 and j < n - 1:
            nb[j] += wk[k] * (1 - f) / dxi
            nb[j + 1] += wk[k] * f / dxi


@njit(cache=True)
def gather_cic(xk, xi0, dxi, E):
    out = np.zeros(xk.size)
    n = E.size
    alive = np.ones(xk.size, dtype=np.bool_)
    for k in range(xk.size):
        s = (xk[k] - xi0) / dxi
        j = int(np.floor(s))
        f = s - j
        if j >= 0 and j < n - 1:
            out[k] = E[j] * (1 - f) + E[j + 1] * f
        else:
            alive[k] = False
    return out, alive


def proton_beta(u):
    return u / np.sqrt(1 + u * u)


class Tracker:
    """driver_a2(xi, t, xd): cycle-averaged <a^2> of the driver as a function of xi = x - x_d.
    beta_program(t, xd, tracker) -> beta_d. density(x) -> local n/n_ref (scales the wake;
    a uniform plasma uses lambda x: 1.0)."""

    def __init__(self, xi_min, xi_max, dxi, driver_a2, beta_program, density=None):
        self.xi = np.arange(xi_min, xi_max + dxi / 2, dxi)
        self.dxi = dxi
        self.driver_a2 = driver_a2
        self.beta_program = beta_program
        self.density = density if density is not None else (lambda x: 1.0)
        self.t = 0.0
        self.xd = 0.0
        self.beta_d = None
        self.laser_work = 0.0
        self.beam_gain = 0.0
        self.broken = False
        self.hist = []
        self._u = None
        self.static_driver = False   # if True and beam unloaded, reuse the wake between steps
        self._cache = None

    def set_beam(self, xi, T_MeV, weight):
        """Protons at positions xi (c/w_p behind/ahead of driver), kinetic energies T [MeV],
        areal weights (n_ref c/w_p units; 0 => test particles)."""
        self.pxi = np.asarray(xi, float).copy()
        g = 1 + np.asarray(T_MeV, float) / 938.27208816
        self.pu = np.sqrt(g * g - 1)
        self.pw = np.broadcast_to(np.asarray(weight, float), self.pxi.shape).copy()
        self.alive = np.ones(self.pxi.size, bool)
        self.T0 = self.kinetic().copy()

    def kinetic(self):
        """Kinetic energy of each proton in m_e c^2."""
        return (np.sqrt(1 + self.pu**2) - 1) * MPC2_ME

    def wake(self, beta_d, with_beam=True):
        """Return (E, broken, u_unloaded) in local-density normalisation."""
        a2 = self.driver_a2(self.xi, self.t, self.xd)
        nb = np.zeros_like(self.xi)
        if with_beam and self.pw.sum() > 0:
            deposit_cic(self.pxi[self.alive], self.pw[self.alive], self.xi[0], self.dxi, nb)
        phi, E, br = F.solve_wake(self.xi, a2, nb, beta_d)
        return E, br, a2, nb

    def step(self, dt, energy_every=1, istep=0):
        bd = self.beta_program(self.t, self.xd, self)
        self.beta_d = bd
        nloc = self.density(self.xd)
        loaded = self.pw.sum() > 0
        if self.static_driver and not loaded and self._cache is not None and self._cache[0] == bd:
            E, br, a2 = self._cache[1], self._cache[2], self._cache[3]
        else:
            E, br, a2, nb = self.wake(bd, with_beam=True)
            if self.static_driver and not loaded:
                self._cache = (bd, E, br, a2)
        if br >= 0:
            self.broken = True
        # laser work = unloaded wake energy per unit length x distance moved by the driver
        if self._u is None or istep % energy_every == 0:
            phi0, E0, br0 = F.solve_wake(self.xi, a2, np.zeros_like(self.xi), bd)
            behind = self.xi < (self.xi[0] + 0.5 * (self.xi[-1] - self.xi[0]))
            self._u = F.wake_energy_density(self.xi, phi0, E0, a2, bd, self.xi[0] + 0.5 * (self.xi[-1] - self.xi[0]))
        self.laser_work += self._u * bd * dt * nloc
        # push protons (field scaled to the reference-density normalisation: E_ref = E_loc*sqrt(n))
        Ek, alive_now = gather_cic(self.pxi, self.xi[0], self.dxi, E)
        self.alive &= alive_now
        du = ME_MP * Ek * np.sqrt(nloc) * dt
        du[~self.alive] = 0.0
        self.pu += du
        b = proton_beta(self.pu)
        self.pxi += (b - bd) * dt * np.sqrt(nloc)   # xi measured in local c/w_p
        self.xd += bd * dt
        self.t += dt
        return E

    def run(self, t_end, dt, record_every=100, stop=None):
        i = 0
        while self.t < t_end:
            E = self.step(dt, istep=i)
            if i % record_every == 0:
                T = self.kinetic()
                al = self.alive
                rec = dict(t=self.t, xd=self.xd, beta_d=self.beta_d,
                           laser_work=self.laser_work, broken=self.broken,
                           n_alive=int(al.sum()))
                if al.any():
                    w = self.pw[al] if self.pw[al].sum() > 0 else np.ones(al.sum())
                    rec.update(T_mean=np.average(T[al], weights=w), T_max=T[al].max(),
                               T_std=np.sqrt(np.average((T[al] - np.average(T[al], weights=w))**2, weights=w)),
                               xi_mean=np.average(self.pxi[al], weights=w),
                               beam_energy=np.sum(self.pw[al] * T[al]) - np.sum(self.pw[al] * self.T0[al]))
                self.hist.append(rec)
                if stop is not None and stop(self, rec):
                    break
            i += 1
        return self.hist
