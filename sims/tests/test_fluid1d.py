"""Validation of fluid1d against analytic linear theory."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F

xi = np.linspace(-60, 10, 70001)
A = 1e-3
for sig in [0.5, 1.0, 2.0]:
    a2 = A * np.exp(-0.5 * (xi / sig) ** 2)
    phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), 1.0)
    Emax_num = np.abs(Ez[xi < -10]).max()
    Emax_th = 0.5 * A * sig * np.sqrt(2 * np.pi) * np.exp(-sig**2 / 2)
    print(f"luminal sigma={sig}: Emax num={Emax_num:.6e} theory={Emax_th:.6e} ratio={Emax_num/Emax_th:.5f}")

# subluminal linear: phi'' = (a2/2 - phi)/beta^2 -> wavelength 2*pi*beta, amplitude:
for bp in [0.3, 0.6, 0.9]:
    sig = 0.5 * bp
    a2 = A * np.exp(-0.5 * (xi / sig) ** 2)
    phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), bp)
    # theory: Ez amplitude = (1/(2 bp^2)) * |int a2 exp(i xi/bp) dxi| * (1/bp)*bp ... compute numerically
    k = 1 / bp
    I = np.trapezoid(a2 * np.exp(1j * k * xi), xi)
    # phi'' + phi/bp^2 = a2/(2 bp^2): phi amplitude = |I|/(2 bp), Ez amplitude = phi_amp/bp
    Emax_th = np.abs(I) / (2 * bp**2)
    Emax_num = np.abs(Ez[xi < -10]).max()
    # wavelength from zero crossings
    zc = np.where(np.diff(np.sign(Ez[xi < -5])))[0]
    lam = 2 * np.mean(np.diff(xi[xi < -5][zc]))
    print(f"subluminal beta={bp}: Emax num={Emax_num:.4e} th={Emax_th:.4e} ratio={Emax_num/Emax_th:.4f}; wavelength={lam:.4f} expected={2*np.pi*bp:.4f}")

# nonlinear luminal check: wave-breaking-ish amplitude for a0=2 linear pol, sigma ~ optimal
for a0 in [0.5, 1, 2, 3]:
    a2 = F.gaussian_envelope(xi, 0.0, 2.355 * 1.0, a0)
    phi, Ez, br = F.solve_wake(xi, a2, np.zeros_like(xi), 1.0)
    u = F.wake_energy_density(xi, phi, Ez, a2, 1.0, -20)
    UL = F.laser_energy_per_area(xi, a2, 20.0)
    print(f"a0={a0}: Emax={np.abs(Ez[xi<-5]).max():.3f} broken={br} wake u={u:.4f} L_pd(kp^-1)={UL/u:.1f}")
