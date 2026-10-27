"""Quasi-3D (FBPIC, RZ + azimuthal modes) check of one density-matched, depletion-limited
proton stage — the multi-D counterpart of the 1D EM-PIC study P2a.

Physics parameters mirror the 1D case k0/kp = 7.4, a0 = 2, intensity FWHM = 2.355 c/w_p:
lambda0 = 1 um, n0 = n_c/54.8 = 2.03e19 cm^-3 (c/w_p = 1.18 um), tau_FWHM(I) = 9.3 fs
(2.8 cycles), w0 = 3.5 um (k_p w0 = 3), parabolic guiding channel matched to w0.
A proton test bunch (and optionally a loaded bunch) is injected behind the pulse.
Run from WSL:  python3 fbpic_dense_stage.py --steps N [--loaded Q_pC]
"""
import sys, time, argparse, json
import numpy as np
from scipy.constants import c, e, m_e, m_p, epsilon_0
from fbpic.main import Simulation
from fbpic.lpa_utils.laser import add_laser_pulse, GaussianLaser
from fbpic.openpmd_diag import FieldDiagnostic, ParticleDiagnostic

ap = argparse.ArgumentParser()
ap.add_argument("--steps", type=int, default=200)
ap.add_argument("--dz_per_lambda", type=float, default=24)
ap.add_argument("--Nm", type=int, default=2)
ap.add_argument("--T_inj", type=float, default=1700.0, help="proton kinetic energy [MeV]")
ap.add_argument("--xi_inj", type=float, default=-6.0, help="bunch position behind pulse [c/w_p]")
ap.add_argument("--charge_pC", type=float, default=0.0)
ap.add_argument("--out", default="fbpic_out")
ap.add_argument("--diag_period", type=int, default=0)
a = ap.parse_args()

lam0 = 1.0e-6
k0 = 2 * np.pi / lam0
n_c = epsilon_0 * m_e * (c * k0) ** 2 / e ** 2
n0 = n_c / 7.4 ** 2
wp = np.sqrt(n0 * e ** 2 / (epsilon_0 * m_e))
kp = wp / c
a0 = 2.0
w0 = 3.0 / kp
tau_fwhm_I = 2.355 / kp / c
tau = tau_fwhm_I / np.sqrt(2 * np.log(2))       # FBPIC: E ~ exp(-t^2/tau^2)
r_e = e ** 2 / (4 * np.pi * epsilon_0 * m_e * c ** 2)
dn_ch = 1.0 / (np.pi * r_e * w0 ** 2)            # matched parabolic channel depth

Lz = 6 * 2 * np.pi / kp
Lr = 4.5 * w0
dz = lam0 / a.dz_per_lambda
dr = dz * 3
Nz = int(Lz / dz)
Nr = int(Lr / dr)
zmax = 0.0
zmin = -Lz
z0 = -1.5 * c * tau_fwhm_I * 2                    # laser centre
ramp = 20 / kp
z_plasma = z0 + 4 * c * tau


def dens(z, r):
    prof = np.where(z < z_plasma, 0.0, np.where(z < z_plasma + ramp,
                    np.sin(0.5 * np.pi * (z - z_plasma) / ramp) ** 2, 1.0))
    return prof * (1.0 + dn_ch / n0 * (r / w0) ** 2)


sim = Simulation(Nz, zmax, Nr, Lr, a.Nm, dz / c, zmin=zmin,
                 n_order=-1, use_cuda=False, boundaries={"z": "open", "r": "reflective"})

plasma_e = sim.add_new_species(q=-e, m=m_e, n=n0, dens_func=dens, p_nz=2, p_nr=2, p_nt=4,
                               p_zmin=z_plasma, p_rmax=0.9 * Lr)
plasma_i = sim.add_new_species(q=e, m=m_p, n=n0, dens_func=dens, p_nz=2, p_nr=2, p_nt=4,
                               p_zmin=z_plasma, p_rmax=0.9 * Lr)
laser = GaussianLaser(a0=a0, waist=w0, tau=tau, z0=z0, zf=z_plasma + ramp, lambda0=lam0)
add_laser_pulse(sim, laser)
sim.set_moving_window(v=c)
print(f"n0={n0/1e6:.3e} cm^-3, w0={w0*1e6:.2f} um, tau_FWHM(I)={tau_fwhm_I*1e15:.1f} fs, "
      f"channel dn/n0={dn_ch/n0:.2f}, grid {Nz}x{Nr}x{a.Nm}", flush=True)
t0 = time.time()
sim.step(a.steps)
dtps = (time.time() - t0) / a.steps
print(f"{a.steps} steps in {time.time()-t0:.1f}s -> {dtps:.3f} s/step; "
      f"steps per mm = {1e-3/dz:.0f} -> {1e-3/dz*dtps/3600:.2f} h per mm", flush=True)
