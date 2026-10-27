"""1D nonlinear cold-fluid quasi-static wake model for an arbitrary phase velocity.

Normalisation: xi in 1/k_p (k_p of the local density n0), phi = e*Phi/(m_e c^2),
E in E0 = m_e c w_p / e, densities in n0, energy densities in n0 m_e c^2.

Wake equation (Esarey, Schroeder & Leemans, RMP 81, 1229 (2009), eq. for arbitrary gamma_p):
    phi'' = gamma_p^2 { beta_p [1 - (1+a2)/(gamma_p^2 (1+phi)^2)]^(-1/2) - 1 } - Zb*nb
where a2 is the cycle-averaged <a^2> (a0^2/2 for linear polarisation), xi = z - v_p t,
the driver sits at large xi and we integrate from xi_max (phi = phi' = 0) towards xi_min.
nb is the density of a co-moving beam (Zb = +1 protons, -1 electrons).
E_z = -phi'.  Protons are accelerated where E_z > 0.

The model breaks down (wave breaking / trajectory crossing) when the square-root argument
becomes <= 0; this is flagged.
"""
import numpy as np
from numba import njit


@njit(cache=True)
def _rhs(phi, dphi, a2, nb, gp2, bp):
    s_arg = 1.0 - (1.0 + a2) / (gp2 * (1.0 + phi) ** 2)
    if s_arg <= 1e-12:
        return 0.0, 1  # broken
    if gp2 > 1e10:  # luminal limit
        f = 0.5 * ((1.0 + a2) / (1.0 + phi) ** 2 - 1.0)
    else:
        f = gp2 * (bp / np.sqrt(s_arg) - 1.0)
    return f - nb, 0


@njit(cache=True)
def solve_wake(xi, a2, nb, beta_p):
    """Integrate the wake from xi[-1] down to xi[0] on a uniform grid (RK4,
    linear interpolation of the sources at the half step).
    Returns phi, Ez, broken_index (-1 if never broken)."""
    n = xi.size
    h = xi[1] - xi[0]
    if beta_p >= 1.0:
        gp2 = 1e12
        bp = 1.0
    else:
        gp2 = 1.0 / (1.0 - beta_p * beta_p)
        bp = beta_p
    phi = np.zeros(n)
    dphi = np.zeros(n)
    broken = -1
    y0 = 0.0
    y1 = 0.0
    for i in range(n - 1, 0, -1):
        # step from xi[i] to xi[i-1]: step = -h
        hs = -h
        a_i = a2[i]
        a_m = 0.5 * (a2[i] + a2[i - 1])
        a_e = a2[i - 1]
        b_i = nb[i]
        b_m = 0.5 * (nb[i] + nb[i - 1])
        b_e = nb[i - 1]
        f1, br1 = _rhs(y0, y1, a_i, b_i, gp2, bp)
        k1y0 = y1
        k1y1 = f1
        f2, br2 = _rhs(y0 + 0.5 * hs * k1y0, y1 + 0.5 * hs * k1y1, a_m, b_m, gp2, bp)
        k2y0 = y1 + 0.5 * hs * k1y1
        k2y1 = f2
        f3, br3 = _rhs(y0 + 0.5 * hs * k2y0, y1 + 0.5 * hs * k2y1, a_m, b_m, gp2, bp)
        k3y0 = y1 + 0.5 * hs * k2y1
        k3y1 = f3
        f4, br4 = _rhs(y0 + hs * k3y0, y1 + hs * k3y1, a_e, b_e, gp2, bp)
        k4y0 = y1 + hs * k3y1
        k4y1 = f4
        if br1 + br2 + br3 + br4 > 0 and broken < 0:
            broken = i
        y0 = y0 + hs / 6.0 * (k1y0 + 2 * k2y0 + 2 * k3y0 + k4y0)
        y1 = y1 + hs / 6.0 * (k1y1 + 2 * k2y1 + 2 * k3y1 + k4y1)
        phi[i - 1] = y0
        dphi[i - 1] = y1
    Ez = -dphi
    return phi, Ez, broken


@njit(cache=True)
def fluid_quantities(phi, a2, beta_p):
    """Electron density n/n0, longitudinal momentum u_z, Lorentz factor gamma."""
    n = phi.size
    ne = np.empty(n)
    uz = np.empty(n)
    gam = np.empty(n)
    for i in range(n):
        if beta_p >= 1.0:
            # luminal limit: gamma - u_z = 1 + phi
            p = 1.0 + phi[i]
            g = (1.0 + a2[i] + p * p) / (2.0 * p)
            u = (1.0 + a2[i] - p * p) / (2.0 * p)
            gam[i] = g
            uz[i] = u
            ne[i] = 1.0 / (1.0 - u / g) if g != u else np.inf
        else:
            gp2 = 1.0 / (1.0 - beta_p * beta_p)
            p = 1.0 + phi[i]
            s_arg = 1.0 - (1.0 + a2[i]) / (gp2 * p * p)
            if s_arg <= 0:
                s_arg = 1e-12
            s = np.sqrt(s_arg)
            gam[i] = gp2 * p * (1.0 - beta_p * s)
            uz[i] = gp2 * p * (beta_p - s)
            ne[i] = gp2 * beta_p * (1.0 / s - beta_p)
    return ne, uz, gam


def wake_energy_density(xi, phi, Ez, a2, beta_p, xi_behind):
    """Mean wake energy density (field + electron kinetic) behind the driver,
    averaged over the region xi < xi_behind (should contain whole periods).
    Units: n0 m_e c^2. Equals energy deposited per unit area per unit length (k_p^-1)."""
    ne, uz, gam = fluid_quantities(phi, a2, beta_p)
    m = xi < xi_behind
    u = 0.5 * Ez[m] ** 2 + ne[m] * (gam[m] - 1.0)
    return u.mean()


def laser_energy_per_area(xi, a2, k0_over_kp):
    """Laser energy per unit area in units n0 m_e c^2 / k_p (xi in 1/k_p),
    using the cycle-averaged a2."""
    return k0_over_kp ** 2 * np.trapezoid(a2, xi)


# ---------------------------------------------------------------- driver shapes
def sin2_envelope(xi, xi_c, length, a0, pol="linear"):
    """<a^2> for a sin^2 *field* envelope of full length `length` (in 1/k_p),
    i.e. a(xi) = a0 sin^2(pi (xi-xi_c)/length + pi/2) on |xi-xi_c| < length/2."""
    fac = 0.5 if pol == "linear" else 1.0
    x = (xi - xi_c) / length
    env = np.where(np.abs(x) < 0.5, np.cos(np.pi * x) ** 2, 0.0)
    return fac * a0 ** 2 * env ** 2


def gaussian_envelope(xi, xi_c, tau_fwhm_I, a0, pol="linear"):
    """<a^2> for a Gaussian pulse; tau_fwhm_I = FWHM of intensity in 1/k_p (length)."""
    fac = 0.5 if pol == "linear" else 1.0
    sig = tau_fwhm_I / (2 * np.sqrt(2 * np.log(2)))
    return fac * a0 ** 2 * np.exp(-0.5 * ((xi - xi_c) / sig) ** 2)
