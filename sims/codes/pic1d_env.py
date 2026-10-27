"""1D relativistic electrostatic PIC with a prescribed ponderomotive (envelope) laser driver.

Purpose: cheap, kinetic simulation of wakes driven by laser envelopes moving at ANY velocity
(conventional group-velocity drivers, luminal/sub-luminal/accelerating flying-focus drivers,
pulse trains), in arbitrary longitudinal density profiles, with mobile plasma ions and a
self-consistently loaded proton (or electron) beam.

Normalisation (reference density n_ref):
    time 1/w_p, length c/w_p, momentum m_s c (per species), E in E0 = m_e c w_p/e,
    density in n_ref, areal energy in n_ref m_e c^2 (c/w_p).
Physics:
    Gauss:  dE/dx = sum_s q_s n_s  (E = 0 ahead of the driver, at the right window edge)
    Push:   du/dt = (q/m) E - (q^2/m^2) (1/(2 gamma)) d<a^2>/dx,  gamma = sqrt(1+u^2+(q/m)^2 <a^2>)
            (cycle-averaged ponderomotive guiding-centre model, valid for w_laser >> w_p).
The driver <a^2>(x,t) is prescribed (no self-consistent laser evolution); the work done by the
ponderomotive force is accumulated so laser->plasma energy transfer is known exactly.
Limitations: 1D (no transverse physics, no focusing, no diffraction), no laser depletion or
evolution (optionally a crude energy-conserving amplitude depletion), cold plasma.
"""
import numpy as np
from numba import njit

ME_OVER_MP = 1.0 / 1836.15267343


# ------------------------------------------------------------------ numba kernels
@njit(cache=True)
def deposit(x, w, q, x0, dx, rho):
    n = rho.size
    for k in range(x.size):
        s = (x[k] - x0) / dx
        j = int(np.floor(s))
        f = s - j
        if j >= 0 and j < n - 1:
            rho[j] += q * w[k] * (1.0 - f) / dx
            rho[j + 1] += q * w[k] * f / dx


@njit(cache=True)
def gauss_field(rho, dx, E):
    n = rho.size
    E[n - 1] = 0.0
    for j in range(n - 2, -1, -1):
        E[j] = E[j + 1] - 0.5 * (rho[j] + rho[j + 1]) * dx


@njit(cache=True)
def gather(x, x0, dx, F):
    out = np.zeros(x.size)
    n = F.size
    for k in range(x.size):
        s = (x[k] - x0) / dx
        j = int(np.floor(s))
        f = s - j
        if j >= 0 and j < n - 1:
            out[k] = F[j] * (1.0 - f) + F[j + 1] * f
    return out


@njit(cache=True)
def push(x, u, w, qm, x0, dx, E, a2, da2, da2dt, dt, pond_on):
    """Leapfrog push. Returns the energy transferred from the laser envelope to this species
    during the step, sum_k w_k (q/m)^2 (d<a^2>/dt)|_x / (2 gamma) dt, converted to m_e c^2
    units (multiply by m_s/m_e = 1/|qm| for |q| = 1). For a rigidly moving envelope this is
    -v_d * F_pond summed over particles (the ponderomotive potential is static in the driver
    frame)."""
    n = E.size
    work = 0.0
    q2m2 = qm * qm
    for k in range(x.size):
        s = (x[k] - x0) / dx
        j = int(np.floor(s))
        f = s - j
        if j < 0 or j >= n - 1:
            continue
        Ek = E[j] * (1.0 - f) + E[j + 1] * f
        a2k = a2[j] * (1.0 - f) + a2[j + 1] * f
        d2k = da2[j] * (1.0 - f) + da2[j + 1] * f
        dtk = da2dt[j] * (1.0 - f) + da2dt[j + 1] * f
        uh = u[k] + 0.5 * dt * qm * Ek
        g = np.sqrt(1.0 + uh * uh + q2m2 * a2k)
        fp = 0.0
        if pond_on:
            fp = -q2m2 * 0.5 * d2k / g
            work += w[k] * q2m2 * 0.5 * dtk / g * dt / abs(qm)
        unew = u[k] + dt * (qm * Ek + fp)
        u[k] = unew
        gn = np.sqrt(1.0 + unew * unew + q2m2 * a2k)
        x[k] += dt * unew / gn
    return work


@njit(cache=True)
def kinetic(x, u, w, qm, x0, dx, a2):
    """Kinetic energy including the quiver energy inside the envelope (m_e c^2 units)."""
    n = a2.size
    tot = 0.0
    q2m2 = qm * qm
    for k in range(u.size):
        s = (x[k] - x0) / dx
        j = int(np.floor(s))
        f = s - j
        a2k = 0.0
        if j >= 0 and j < n - 1:
            a2k = a2[j] * (1.0 - f) + a2[j + 1] * f
        tot += w[k] * (np.sqrt(1.0 + u[k] * u[k] + q2m2 * a2k) - 1.0)
    return tot / abs(qm)


# ------------------------------------------------------------------ driver
class Pulse:
    """One envelope pulse, positioned relative to the driver reference point.
    shape: 'gauss' (length = FWHM of <a^2>) or 'sin2' (length = full length; field ~ cos^2).
    a0 is peak normalised vector potential; pol 'linear' -> <a^2> = a0^2/2."""

    def __init__(self, a0, length, offset=0.0, shape="gauss", pol="linear"):
        self.a0, self.length, self.offset, self.shape = a0, length, offset, shape
        self.fac = 0.5 if pol == "linear" else 1.0

    @classmethod
    def table(cls, xi_tab, a2_tab, offset=0.0):
        """Arbitrary <a^2> profile (e.g. from the differentiable optimiser), linear interpolation."""
        p = cls(1.0, 1.0, offset, "table")
        p.tab_xi = np.asarray(xi_tab, float)
        p.tab_a2 = np.asarray(a2_tab, float)
        if p.tab_xi[0] > p.tab_xi[-1]:
            p.tab_xi, p.tab_a2 = p.tab_xi[::-1], p.tab_a2[::-1]
        return p

    def a2(self, xi):
        if self.shape == "table":
            return np.interp(xi - self.offset, self.tab_xi, self.tab_a2, left=0.0, right=0.0)
        if self.shape == "gauss":
            sig = self.length / (2 * np.sqrt(2 * np.log(2)))
            return self.fac * self.a0**2 * np.exp(-0.5 * ((xi - self.offset) / sig) ** 2)
        x = (xi - self.offset) / self.length
        env = np.where(np.abs(x) < 0.5, np.cos(np.pi * x) ** 2, 0.0)
        return self.fac * self.a0**2 * env**2


class Driver:
    """A train of pulses whose reference point moves along x_d(t).
    velocity: float, or callable v(t, x_d, sim) -> beta (allows programmed or feedback
    flying-focus trajectories). amp(t, x_d): optional amplitude multiplier for <a^2>
    (e.g. focal ramps)."""

    def __init__(self, pulses, x_start, velocity, amp=None):
        self.pulses = pulses
        self.xd = x_start
        self.velocity = velocity
        self.amp = amp
        self.depletion_scale = 1.0

    def beta(self, t, sim):
        v = self.velocity
        return v(t, self.xd, sim) if callable(v) else v

    def a2(self, x, t):
        """<a^2> on a uniform grid x; each pulse is evaluated only over its own support
        (+-5 sigma for Gaussians, full length for sin^2), which keeps long trains cheap."""
        xi = x - self.xd
        out = np.zeros_like(x)
        dxg = x[1] - x[0] if x.size > 1 else 1.0
        for p in self.pulses:
            half = (5.0 * p.length / 2.3548) if p.shape == "gauss" else 0.5 * p.length
            if p.shape == "table":
                half = 0.5 * (p.tab_xi[-1] - p.tab_xi[0]) + abs(p.tab_xi[-1] + p.tab_xi[0]) / 2
            j0 = max(int(np.floor((p.offset - half - xi[0]) / dxg)), 0)
            j1 = min(int(np.ceil((p.offset + half - xi[0]) / dxg)) + 1, x.size)
            if j1 > j0:
                out[j0:j1] += p.a2(xi[j0:j1])
        m = self.depletion_scale
        if self.amp is not None:
            m = m * self.amp(t, self.xd)
        return out * m


# ------------------------------------------------------------------ simulation
class Sim1D:
    def __init__(self, Lx, dx, density, driver, x_window0=None, ppc=20, dt=None,
                 mobile_ions=False, ion_qm=ME_OVER_MP, window_velocity=None,
                 n_max=None, x_plasma_start=None):
        """Lx: window length; density: callable n(x) (in n_ref) for electrons (= ion charge
        density); driver: Driver; window_velocity: None -> follows driver; float; or callable.
        """
        self.dx = dx
        self.N = int(round(Lx / dx)) + 1
        self.x0 = (driver.xd - 0.8 * Lx) if x_window0 is None else x_window0
        self.density = density
        self.driver = driver
        self.ppc = ppc
        nmax = 1.0 if n_max is None else n_max
        self.dt = dt if dt is not None else min(0.9 * dx, 0.1 / np.sqrt(nmax))
        self.t = 0.0
        self.mobile_ions = mobile_ions
        self.ion_qm = ion_qm
        self.window_velocity = window_velocity
        self.win_accum = 0.0
        # particles
        xs = self._uniform_positions(self.x0, self.x0 + (self.N - 1) * dx)
        if x_plasma_start is not None:
            xs = xs[xs >= x_plasma_start]
        ws = density(xs) * dx / ppc
        keep = ws > 0
        self.xe, self.we = xs[keep].copy(), ws[keep].copy()
        self.ue = np.zeros_like(self.xe)
        self.xi, self.wi = xs[keep].copy(), ws[keep].copy()
        self.ui = np.zeros_like(self.xi)
        self.xb = np.zeros(0)
        self.ub = np.zeros(0)
        self.wb = np.zeros(0)
        self.beam_qm = ME_OVER_MP
        self.beam_q = 1.0
        self.beam_lost = 0.0
        self.pond_work = 0.0
        self.grid = self.x0 + dx * np.arange(self.N)
        self.rho = np.zeros(self.N)
        self.E = np.zeros(self.N)
        self.a2g = np.zeros(self.N)
        self.history = []
        self._a2_next = None
        self._a2_next_x0 = None

    def _uniform_positions(self, xa, xb):
        n = int(round((xb - xa) / self.dx))
        if n <= 0:
            return np.zeros(0)
        offs = (np.arange(self.ppc) + 0.5) / self.ppc
        return (xa + self.dx * (np.arange(n)[:, None] + offs[None, :])).ravel()

    def add_beam(self, x, u, w, q=1.0, qm=ME_OVER_MP):
        self.xb = np.asarray(x, float).copy()
        self.ub = np.asarray(u, float).copy()
        self.wb = np.asarray(w, float).copy()
        self.beam_q, self.beam_qm = q, qm

    # -------------------------------------------------------------- one step
    def step(self):
        dx, dt = self.dx, self.dt
        g = self.grid
        beta_d = self.driver.beta(self.t, self)
        # driver field at time t (particles at x^n) and at t+dt (for d<a^2>/dt at fixed x)
        if self._a2_next is not None and self._a2_next_x0 == self.x0:
            self.a2g = self._a2_next
        else:
            self.a2g = self.driver.a2(g, self.t)
        xd_save = self.driver.xd
        self.driver.xd = xd_save + beta_d * dt
        a2n = self.driver.a2(g, self.t + dt)
        self.driver.xd = xd_save
        da2dt = (a2n - self.a2g) / dt
        da2 = np.gradient(self.a2g, dx)
        # charge density
        rho = self.rho
        rho[:] = 0.0
        deposit(self.xe, self.we, -1.0, self.x0, dx, rho)
        deposit(self.xi, self.wi, 1.0, self.x0, dx, rho)
        if self.xb.size:
            deposit(self.xb, self.wb, self.beam_q, self.x0, dx, rho)
        gauss_field(rho, dx, self.E)
        # push
        self.pond_work += push(self.xe, self.ue, self.we, -1.0, self.x0, dx, self.E,
                               self.a2g, da2, da2dt, dt, True)
        if self.mobile_ions:
            self.pond_work += push(self.xi, self.ui, self.wi, self.ion_qm, self.x0, dx,
                                   self.E, self.a2g, da2, da2dt, dt, True)
        if self.xb.size:
            push(self.xb, self.ub, self.wb, self.beam_q * self.beam_qm, self.x0, dx, self.E,
                 self.a2g, da2, da2dt, dt, False)
        # driver motion
        self.driver.xd += beta_d * dt
        self.t += dt
        self._a2_next, self._a2_next_x0 = a2n, self.x0
        # window motion
        wv = self.window_velocity
        if wv is None:
            vw = beta_d
        elif callable(wv):
            vw = wv(self.t, self)
        else:
            vw = wv
        self.win_accum += vw * dt
        while self.win_accum >= dx:
            self.win_accum -= dx
            self._shift()

    def _shift(self):
        dx = self.dx
        x_old_end = self.x0 + (self.N - 1) * dx
        self.x0 += dx
        self.grid = self.x0 + dx * np.arange(self.N)
        # remove particles that left on the left
        for name in ("e", "i"):
            x = getattr(self, "x" + name)
            m = x >= self.x0
            if not m.all():
                setattr(self, "x" + name, x[m])
                setattr(self, "u" + name, getattr(self, "u" + name)[m])
                setattr(self, "w" + name, getattr(self, "w" + name)[m])
        if self.xb.size:
            m = self.xb >= self.x0
            if not m.all():
                self.beam_lost += self.wb[~m].sum()
                self.xb, self.ub, self.wb = self.xb[m], self.ub[m], self.wb[m]
        # inject fresh cold plasma in the new cell
        xs = self._uniform_positions(x_old_end, x_old_end + dx)
        ws = self.density(xs) * dx / self.ppc
        k = ws > 0
        if k.any():
            self.xe = np.concatenate([self.xe, xs[k]])
            self.ue = np.concatenate([self.ue, np.zeros(k.sum())])
            self.we = np.concatenate([self.we, ws[k]])
            self.xi = np.concatenate([self.xi, xs[k]])
            self.ui = np.concatenate([self.ui, np.zeros(k.sum())])
            self.wi = np.concatenate([self.wi, ws[k]])

    # -------------------------------------------------------------- diagnostics
    def energies(self):
        """Areal energies (n_ref m_e c^2 c/w_p). laser_work = energy given by the envelope."""
        a2 = self.driver.a2(self.grid, self.t)
        fe = 0.5 * np.sum(self.E**2) * self.dx
        ke = kinetic(self.xe, self.ue, self.we, -1.0, self.x0, self.dx, a2)
        ki = kinetic(self.xi, self.ui, self.wi, self.ion_qm, self.x0, self.dx, a2)
        kb = kinetic(self.xb, self.ub, self.wb, self.beam_qm, self.x0, self.dx,
                     np.zeros_like(a2)) if self.xb.size else 0.0
        return dict(field=fe, kin_e=ke, kin_i=ki, kin_b=kb, laser_work=self.pond_work)

    def beam_stats(self):
        if self.xb.size == 0:
            return None
        g = np.sqrt(1 + self.ub**2)
        T = (g - 1) / self.beam_qm  # kinetic energy in m_e c^2
        w = self.wb if self.wb.sum() > 0 else np.ones_like(self.wb)
        Tm = np.average(T, weights=w)
        Ts = np.sqrt(np.average((T - Tm) ** 2, weights=w))
        return dict(T_mean=Tm, T_std=Ts, T_max=T.max(), n=self.xb.size,
                    x_mean=np.average(self.xb, weights=w), weight=self.wb.sum())

    def run(self, t_end, diag_every=None, callback=None):
        nsteps = int(np.ceil((t_end - self.t) / self.dt))
        for s in range(nsteps):
            self.step()
            if diag_every and (s % diag_every == 0 or s == nsteps - 1):
                rec = dict(t=self.t, xd=self.driver.xd, Emax=np.abs(self.E).max())
                rec.update(self.energies())
                bs = self.beam_stats()
                if bs:
                    rec.update({"b_" + k: v for k, v in bs.items()})
                self.history.append(rec)
                if callback is not None:
                    callback(self, rec)
        return self.history
