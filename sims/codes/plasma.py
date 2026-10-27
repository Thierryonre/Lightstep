"""Physical constants and standard plasma/LWFA formulas (SI units).

Everything here is textbook physics (Esarey, Schroeder & Leemans, RMP 81, 1229 (2009);
Lu et al., PRST-AB 10, 061301 (2007)). Functions return SI unless stated.
"""
import numpy as np

c = 299792458.0
e = 1.602176634e-19
m_e = 9.1093837015e-31
m_p = 1.67262192369e-27
eps0 = 8.8541878128e-12
mu0 = 1.25663706212e-6
MeC2_MeV = 0.51099895
MpC2_MeV = 938.27208816
MP_OVER_ME = m_p / m_e


def n_crit(lam):
    """Critical density [m^-3] for laser wavelength lam [m]."""
    w = 2 * np.pi * c / lam
    return eps0 * m_e * w**2 / e**2


def omega_p(n):
    """Plasma frequency [rad/s] for electron density n [m^-3]."""
    return np.sqrt(n * e**2 / (eps0 * m_e))


def k_p(n):
    return omega_p(n) / c


def lambda_p(n):
    return 2 * np.pi / k_p(n)


def E0(n):
    """Cold non-relativistic wave-breaking field m_e c w_p / e [V/m]."""
    return m_e * c * omega_p(n) / e


def gamma_p_of_density(n, lam):
    """Wake Lorentz factor ~ w0/wp for a laser group velocity driven wake."""
    return np.sqrt(n_crit(lam) / n)


def a0_from_intensity(I, lam):
    """Peak normalized vector potential (linear polarization) from intensity [W/m^2]."""
    return 0.855 * lam * 1e6 * np.sqrt(I / 1e22)  # I in W/cm^2 -> 1e18 W/cm^2 = 1e22 W/m^2


def intensity_from_a0(a0, lam):
    return 1e22 * (a0 / (0.855 * lam * 1e6)) ** 2


def P_crit(n, lam):
    """Critical power for relativistic self-focusing [W] ~ 17 (w/wp)^2 GW."""
    return 17.4e9 * n_crit(lam) / n


def lu_scalings(n, lam, a0):
    """Lu et al. (2007) blowout-regime scalings: matched spot, dephasing, depletion,
    energy gain. Returns dict in SI (lengths m, energy J)."""
    kp = k_p(n)
    wr = n_crit(lam) / n                     # (w0/wp)^2
    R = 2 * np.sqrt(a0) / kp                 # matched blowout radius ~ w0
    L_d = (2.0 / 3.0) * wr * R               # dephasing length
    tau_fwhm = (2.0 / 3.0) * R / c           # recommended pulse FWHM duration (c*tau ~ 2R/3)
    L_pd = wr * c * tau_fwhm                 # pump depletion length
    dW = (2.0 / 3.0) * m_e * c**2 * wr * a0  # energy gain
    return dict(R=R, L_dephase=L_d, tau_fwhm=tau_fwhm, L_deplete=L_pd, dW=dW,
                dW_GeV=dW / e / 1e9)


def proton_gamma_from_T(T_MeV):
    return 1.0 + T_MeV / MpC2_MeV


def proton_beta_from_T(T_MeV):
    g = proton_gamma_from_T(T_MeV)
    return np.sqrt(1 - 1 / g**2)


def proton_T_from_gamma(g):
    return (g - 1.0) * MpC2_MeV
