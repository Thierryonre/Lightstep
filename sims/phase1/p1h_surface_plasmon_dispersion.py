"""P1h: can a beat-driven surface plasmon in a hollow plasma channel (Lei et al., PRL 137,
105002 (2026)) be velocity-matched to slow protons?

Exact TM_0 surface mode of a vacuum cylinder (radius R) inside a cold plasma wall (eps = 1 -
w_p^2/w^2), slow wave (k > w/c):
   (1/kv) I1(kv R)/I0(kv R) = -(eps/kp) K1(kp R)/K0(kp R),
   kv = sqrt(k^2 - w^2/c^2), kp = sqrt(k^2 - eps w^2/c^2).
Units: w in w_p(wall), k in w_p/c, R in c/w_p.
For each proton velocity beta (phase velocity = beta c) and radius R: the matched frequency,
wavelength, and the on-axis/wall field ratio 1/I0(kv R) (how much of the surface field reaches a
beam on axis); also the planar limit beta^2 = (1+eps)/eps.
This is a linear dispersion analysis (no amplitudes / efficiency - those need PIC).
"""
import os, json
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e
from scipy.optimize import brentq

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
MP = 938.272


def f_disp(w, beta, R):
    k = w / beta
    eps = 1 - 1 / w ** 2
    if eps >= -1e-12:
        return np.nan
    kv = k * np.sqrt(1 - beta ** 2)
    kp = np.sqrt(k ** 2 - eps * w ** 2)
    lhs = (i1e(kv * R) / i0e(kv * R)) / kv
    rhs = -(eps / kp) * (k1e(kp * R) / k0e(kp * R))
    return lhs - rhs


def matched(beta, R):
    ws = np.linspace(1e-3, 1 / np.sqrt(2) - 1e-6, 4000)
    v = np.array([f_disp(w, beta, R) for w in ws])
    idx = np.where(np.isfinite(v[:-1]) & np.isfinite(v[1:]) & (np.sign(v[:-1]) != np.sign(v[1:])))[0]
    if not idx.size:
        return None
    w = brentq(f_disp, ws[idx[0]], ws[idx[0] + 1], args=(beta, R))
    k = w / beta
    kv = k * np.sqrt(1 - beta ** 2)
    axis_ratio = 1.0 / (i0e(kv * R) * np.exp(kv * R))
    return dict(w_over_wp=float(w), k=float(k), wavelength_cwp=float(2 * np.pi / k),
                kv_R=float(kv * R), onaxis_over_wall=float(axis_ratio))


rows = []
for T in [10, 100, 300, 1000, 3000]:
    g = 1 + T / MP
    b = np.sqrt(1 - 1 / g ** 2)
    w_pl = np.sqrt(1 / (2 - b ** 2)) * 0 + np.sqrt((1 - b ** 2) / (2 - b ** 2)) if False else None
    for R in [0.1, 0.3, 1.0, 3.0]:
        m = matched(b, R)
        rows.append(dict(T_MeV=T, beta=float(b), R_cwp=R, **(m or {"matched": False})))
        if m:
            print(f"T={T:5d} MeV beta={b:.3f} R={R:4.1f} c/wp: w={m['w_over_wp']:.3f} w_p, "
                  f"lambda={m['wavelength_cwp']:.2f} c/wp, on-axis/wall field = {m['onaxis_over_wall']:.3g}")
        else:
            print(f"T={T:5d} MeV beta={b:.3f} R={R:4.1f} c/wp: no slow surface mode")
json.dump(rows, open(os.path.join(ROOT, "results", "data", "P1h_surface_plasmon_dispersion.json"), "w"), indent=1)
