"""P1a: wake that a velocity-matched (programmable-velocity) driver can sustain, vs beta_p.

For each phase velocity beta_p (matched to a proton of kinetic energy T), scan driver
amplitude a0 and local drive duration tau (Gaussian FWHM in time at a fixed point, units
1/w_p; spatial FWHM = beta_p * tau). Record the largest wake amplitude obtainable while the
cold-fluid wake stays unbroken with margin (E <= f_wb * E_wb, E_wb = sqrt(2(gamma_p-1))),
and the wake energy per unit length (= laser work per unit length, per unit area).
Also the 'proton-matched' density figure of merit is reported.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
MP = 938.27208816
T_list = [10, 30, 100, 300, 1000, 3000, 6000]
a0s = np.round(np.arange(0.1, 6.01, 0.1), 2)
taus = [1.5, 2.0, 2.355, 3.0, 4.0]
f_wb = 0.8
out = []
for T in T_list:
    g = 1 + T / MP
    b = np.sqrt(1 - 1 / g**2)
    Ewb = np.sqrt(2 * (g - 1))
    best = None
    for tau in taus:
        L = b * tau
        xi = np.arange(-12 * np.pi * b - 6 * L, 6 * L, min(0.01, L / 40))
        for a0 in a0s:
            a2 = F.gaussian_envelope(xi, 0.0, L, a0)
            phi, E, br = F.solve_wake(xi, a2, np.zeros_like(xi), b)
            if br >= 0:
                break
            m = xi < -3 * L
            Em = np.abs(E[m]).max()
            if Em > f_wb * Ewb:
                break
            u = F.wake_energy_density(xi, phi, E, a2, b, -3 * L)
            # proton-accelerating (E>0) peak behind driver
            Epos = E[m].max()
            rec = dict(T_MeV=T, beta=b, gamma=g, tau=tau, a0=float(a0), E_max=float(Em), E_pos=float(Epos),
                       E_wb=float(Ewb), u_wake=float(u), field_per_sqrt_u=float(Epos / np.sqrt(u)))
            if best is None or Epos > best["E_pos"]:
                best = rec
    out.append(best)
    print(f"T={T:5d} MeV beta={b:.3f}: E_wb={Ewb:.3f}; best E+={best['E_pos']:.3f} E0 (a0={best['a0']}, tau={best['tau']}) "
          f"u_wake={best['u_wake']:.4f}; E+/E_wb={best['E_pos']/Ewb:.2f}")
with open(os.path.join(ROOT, "results", "data", "P1a_matched_wake_scan.json"), "w") as f:
    json.dump(dict(f_wb=f_wb, rows=out), f, indent=1)
