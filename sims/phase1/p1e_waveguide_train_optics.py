"""P1e (optics): arbitrary-velocity *resonant* pulse train formed by N laser frequencies
spaced by w_p, each launched into a different radial mode of a matched parabolic plasma
channel (combination of Phase-1 flying focus [arbitrary velocity in a waveguide, Palastro et
al. 2025/26] and Phase-1 resonant excitation in a channel [peaks spaced by one plasma period]).

Exact linear modal dispersion of a matched parabolic channel (Laguerre-Gauss LG_{p,0}, spot W):
    k_p(w) = sqrt(w^2/c^2 - k_p0^2 - 4(2p+1)/W^2)
Components q = 0..N-1: w_q = w0 - q*w_p, mode p_q = q*P, equal power, Gaussian temporal envelope
of FWHM T_env. On-axis (r=0, L_p(0)=1) and transverse intensity are evaluated directly from
the superposition; peak velocity, duration, transverse size, contrast are measured.
First-order design rule: 1/beta_a = 1/beta_g0 + 4P/(k_p0 k0 W^2).
"""
import sys, os, json
import numpy as np
from scipy.special import eval_laguerre
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import plasma as PL

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
c = PL.c


def design_W(beta_a, n_cm3, lam, P):
    n = n_cm3 * 1e6
    k0 = 2 * np.pi / lam
    kp = PL.k_p(n)
    bg0 = 1 / np.sqrt(1 + (kp / k0) ** 2)          # approx group velocity (no mode term)
    D = 1 / beta_a - 1 / bg0
    if D <= 0:
        return None
    return np.sqrt(4 * P / (kp * k0 * D))


def kmode(w, kp0, W, p):
    arg = (w / c) ** 2 - kp0 ** 2 - 4 * (2 * p + 1) / W ** 2
    return np.sqrt(arg)


def rigid_comb(beta_a, n, w0, P, N, W):
    """Exact rigid design: component q (mode p = qP) sits on the line w = v_a (k - k_ref) + w0,
    k_ref = k_0(w0). Returns frequencies w_q (solved by bisection) or None if no solution."""
    from scipy.optimize import brentq
    kp0 = PL.k_p(n)
    va = beta_a * c
    kref = kmode(w0, kp0, W, 0)
    if not np.isfinite(kref):
        return None
    wq = [w0]
    for q in range(1, N):
        p = q * P
        wcut = c * np.sqrt(kp0 ** 2 + 4 * (2 * p + 1) / W ** 2) * (1 + 1e-9)
        f = lambda w: kmode(w, kp0, W, p) - (kref + (w - w0) / va)
        lo, hi = max(wcut, 0.2 * w0), w0 * (1 - 1e-12)
        if lo >= hi:
            return None
        try:
            wq.append(brentq(f, lo, hi))
        except ValueError:
            return None
    return np.array(wq)


def design_rigid(beta_a, n, w0, P, N):
    """Choose W so that the mean spacing of the rigid comb equals w_p (resonant train)."""
    from scipy.optimize import brentq
    wp = PL.omega_p(n)

    def g(W):
        wq = rigid_comb(beta_a, n, w0, P, N, W)
        if wq is None:
            return np.nan
        return np.mean(-np.diff(wq)) / wp - 1.0
    Ws = np.geomspace(0.3e-6, 300e-6, 240)
    vals = np.array([g(W) for W in Ws])
    ok = np.isfinite(vals)
    idx = [i for i in range(len(Ws) - 1) if ok[i] and ok[i + 1] and vals[i] * vals[i + 1] <= 0]
    if not idx:
        return None
    i = idx[-1]
    return brentq(g, Ws[i], Ws[i + 1])


def analyse(beta_a, n_cm3, lam, N, P, T_env_periods=20.0, W=None, z_obs=None, verbose=True):
    n = n_cm3 * 1e6
    w0 = 2 * np.pi * c / lam
    kp0 = PL.k_p(n)
    wp = PL.omega_p(n)
    W = W or design_rigid(beta_a, n, w0, P, N)
    if W is None:
        if verbose:
            print(f"beta={beta_a} n={n_cm3:.2g} N={N} P={P}: no rigid resonant design")
        return None, None
    q = np.arange(N)
    wq = rigid_comb(beta_a, n, w0, P, N, W)
    pq = q * P
    kq = np.array([kmode(wq[i], kp0, W, pq[i]) for i in range(N)])
    vg = np.array([c**2 * kq[i] / wq[i] for i in range(N)])   # group velocity of each component
    # train velocity from a linear fit of k_q vs w_q (peaks move at d w/d k across components)
    va = np.polyfit(kq, wq, 1)[0]
    # on-axis envelope intensity |sum A_q exp(i(dk_q z - dw_q t))|^2 in the frame of the train
    Tp = 2 * np.pi / wp
    t = np.linspace(-3 * Tp, 3 * Tp, 3001)
    z_obs = z_obs or 0.0
    # carrier-removed field at fixed z_obs (phase reference: component 0)
    phase = (kq - kq[0])[:, None] * z_obs - (wq - wq[0])[:, None] * t[None, :]
    E = np.sum(np.exp(1j * phase), axis=0)
    I = np.abs(E) ** 2                      # units of single-mode on-axis intensity
    pk = I.max()
    # FWHM of the central peak
    i0 = np.argmax(I)
    half = I >= pk / 2
    j = i0
    while j > 0 and half[j]:
        j -= 1
    k = i0
    while k < I.size - 1 and half[k]:
        k += 1
    fwhm_t = t[k] - t[j]
    # transverse intensity profile at the peak (r), relative
    r = np.linspace(0, 3 * W, 600)
    u = np.array([eval_laguerre(pq[i], 2 * r ** 2 / W ** 2) * np.exp(-r ** 2 / W ** 2) for i in range(N)])
    Ipk_r = np.abs(u.sum(axis=0)) ** 2
    rr = r[Ipk_r >= Ipk_r[0] * np.exp(-2)]
    w_peak = rr.max() if rr.size else np.nan
    # dephasing of the comb from strict linearity -> residual phase error per component
    lin = np.polyval(np.polyfit(wq, kq, 1), wq)
    dk_err = kq - lin
    L_coh = np.pi / np.max(np.abs(dk_err)) if np.max(np.abs(dk_err)) > 0 else np.inf
    dn_ch = 1 / (np.pi * PL.e**2 / (4 * np.pi * PL.eps0 * PL.m_e * c**2) * W ** 2) / 1e6
    spac = -np.diff(wq) / wp
    res = dict(beta_target=beta_a, beta_train=va / c, n_cm3=n_cm3, lam=lam, N=N, P=P, W_um=W * 1e6,
               spacing_over_wp=list(spac), bandwidth_rel=float((wq[0] - wq[-1]) / w0),
               kpW=kp0 * W, channel_depth_cm3=dn_ch, channel_depth_rel=dn_ch / n_cm3,
               peak_over_avg=pk / N, peak_fwhm_over_Tp=fwhm_t / Tp, w_peak_over_W=w_peak / W,
               max_mode_p=int(pq.max()), comb_coherence_length_mm=L_coh * 1e3,
               component_vg=list(vg / c))
    if verbose:
        print(f"beta_target={beta_a:.4f} n={n_cm3:.2g} lam={lam*1e6:.2f}um N={N} P={P}: W={W*1e6:.1f}um "
              f"(k_pW={kp0*W:.2f}, channel dn/n0={dn_ch/n_cm3:.2f}); train beta={va/c:.5f}; "
              f"peak/avg={pk/N:.2f}, peak FWHM={fwhm_t/Tp:.3f} Tp, peak radius={w_peak/W:.2f} W, "
              f"modes up to p={pq.max()}, spacings/w_p={np.round(spac,3)}, bandwidth={100*(wq[0]-wq[-1])/w0:.1f}%")
    return res, (t / Tp, I, r / W, Ipk_r / Ipk_r[0])


if __name__ == "__main__":
    cases = []
    fig, axs = plt.subplots(2, 3, figsize=(13, 6))
    designs = [(0.875, 1000), (0.971, 3000), (0.9908, 6000)]
    lam = 1.0e-6
    w0 = 2 * np.pi * c / lam
    for col, (beta, T) in enumerate(designs):
        print(f"--- proton T = {T} MeV (beta = {beta})")
        for P in [1, 2]:
            for N in [3, 4, 5]:
                chosen = None
                for n in np.geomspace(1e17, 1e20, 40):
                    W = design_rigid(beta, n * 1e6, w0, P, N)
                    if W is None:
                        continue
                    if PL.k_p(n * 1e6) * W >= 2.2:
                        chosen = n
                        break
                if chosen is None:
                    print(f"   P={P} N={N}: no design with k_pW>=2.2")
                    continue
                res, data = analyse(beta, chosen, lam, N, P)
                if res is None:
                    continue
                res["T_proton_MeV"] = T
                cases.append(res)
                if P == 1:
                    tt, I, rr, Ir = data
                    axs[0, col].plot(tt, I / N, label=f"N={N}, n={chosen:.1e}")
                    axs[1, col].plot(rr, Ir, label=f"N={N}")
        axs[0, col].set_title(f"T_p={T} MeV (beta={beta}), P=1")
        axs[0, col].set_xlabel("t / T_p (on axis)"); axs[0, col].set_ylabel("I / <I>")
        axs[1, col].set_xlabel("r / W"); axs[1, col].set_ylabel("I(r) at peak (norm.)")
        axs[0, col].legend(fontsize=7); axs[1, col].legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(os.path.join(ROOT, "results", "figures", "P1e_waveguide_train_optics.png"), dpi=100)
    json.dump(cases, open(os.path.join(ROOT, "results", "data", "P1e_waveguide_train_optics.json"), "w"), indent=1)
