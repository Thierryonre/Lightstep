"""P2b: differentiable joint optimisation of laser driver shape + proton beam profile (beam
loading + injection phase) for a velocity-matched wake slice.  Mirrors the method of Crilly et al.
(PRR 8, 033353 (2026): JAX differentiable model + L-BFGS-B, ~500 parameters), applied to LWFA.

Per slice (proton kinetic energy T -> beta_p):
  parameters: driver <a^2> amplitudes on N_d Gaussian basis functions (pulse shape; trains
              allowed), beam density amplitudes on N_b basis functions (current profile + phase)
  objective : maximise eta = (int n_b E dxi) / W'   (wake->beam energy transfer efficiency)
  constraints (penalties): rms spread of E over the beam <= s_max; mean field at beam >= G_min;
              unbroken wake (sqrt-arg >= 0.05); |E| <= 0.8 E_wb; per-pulse a0 <= a0_max (bounds)
Baseline for comparison: hand-designed Gaussian driver (P1b design, tau = 2.355) + Gaussian
bunch at the lock point, evaluated with the same model.
"""
import sys, os, json, time, argparse
import numpy as np
import jax, jax.numpy as jnp
from scipy.optimize import minimize
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
import jax_wake as J
import fluid1d as F
from p1b_matched_acceleration import beta_of_T, a0_for_field, wake_for, first_bucket

MP = 938.27208816
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


def build(T, n_periods_drv=1.0, Nd=64, Nb=48, f_field=0.7, a0_max=None, s_max=0.05,
          grad_factor=1.0, load_base=0.5, a0frac=1.3):
    from scipy.optimize import nnls
    b = float(beta_of_T(T))
    lam = 2 * np.pi * b
    Ewb = np.sqrt(2 * T / MP)
    h = lam / 300
    tau = 2.355
    L = b * tau
    # baseline: P1b hand design (Gaussian driver + Gaussian bunch at the lock point)
    a0b = a0_for_field(b, tau, f_field * 0.8 * Ewb)
    xw, _, Ew, _, _ = wake_for(b, a0b, tau)
    xpk, Epk, xl = first_bucket(xw, Ew, b, tau, 0.8)
    # grid front->back; extend behind the last allowed driver position
    xi_front = 3 * L
    xi_back = min(xpk - 0.6 * lam, -(n_periods_drv - 1.0) * lam + xpk - 0.6 * lam) - 3 * L
    xi = np.arange(xi_front, xi_back, -h)
    # driver basis spans [-(n_periods_drv-1) lam - 1.5L, +1.5L]  (n_periods_drv>1 allows trains)
    cd = np.linspace(1.5 * L, -(n_periods_drv - 1.0) * lam - 1.5 * L, Nd)
    wd = max(abs(cd[1] - cd[0]) * 0.85, 1e-3)
    # beam basis spans the first proton-accelerating bucket behind the last driver pulse
    shift = -(n_periods_drv - 1.0) * lam
    cb = np.linspace(xpk + shift + 0.35 * lam, xpk + shift - 0.45 * lam, Nb)
    wb = abs(cb[1] - cb[0]) * 0.85
    Bd = np.exp(-0.5 * ((xi[None, :] - cd[:, None]) / wd) ** 2)
    Bb = np.exp(-0.5 * ((xi[None, :] - cb[:, None]) / wb) ** 2)
    a2_base = F.gaussian_envelope(xi, 0.0, L, a0b)
    sig = 0.03 * lam
    nb_shape = np.exp(-0.5 * ((xi - xl) / sig) ** 2)
    nb_base = load_base * Epk * nb_shape / (np.sum(nb_shape) * h)
    a2max = 0.5 * (a0_max if a0_max else a0frac * a0b) ** 2
    nbmax = 2.0 * nb_base.max()
    Bd_j, Bb_j = jnp.array(Bd * a2max), jnp.array(Bb * nbmax)

    def fields(p):
        a2 = p[:Nd] @ Bd_j
        nb = p[Nd:] @ Bb_j
        phiL, EL, sL = J.solve(h, a2, nb, b)
        phiU, EU, sU = J.solve(h, a2, jnp.zeros_like(a2), b)
        W = J.laser_work(h, phiU, a2, b)
        return a2, nb, EL, EU, sL, sU, W

    def metrics(a2, nb, EL, EU, sL, sU, W):
        Q = jnp.sum(nb) * h + 1e-12
        Eb = jnp.sum(nb * EL) * h / Q
        var = jnp.sum(nb * (EL - Eb) ** 2) * h / Q
        spread = jnp.sqrt(var + 1e-14) / jnp.abs(Eb + 1e-9)
        eta = Eb * Q / (W + 1e-12)
        Emax = jnp.maximum(jnp.max(jnp.abs(EU)), jnp.max(jnp.abs(EL)))
        return eta, Eb, spread, W, Q, Emax, jnp.minimum(sL, sU), jnp.max(a2)

    # baseline metrics with the same model
    fb = [np.asarray(v) for v in (lambda r: r)(())] if False else None
    phiL, ELb, sLb = J.solve(h, jnp.array(a2_base), jnp.array(nb_base), b)
    phiU, EUb, sUb = J.solve(h, jnp.array(a2_base), jnp.zeros(xi.size), b)
    Wb = J.laser_work(h, phiU, jnp.array(a2_base), b)
    eta0, Eb0, sp0, W0, Q0, Emax0, smin0, amax0 = [float(v) for v in metrics(jnp.array(a2_base), jnp.array(nb_base), ELb, EUb, sLb, sUb, Wb)]
    base = dict(eta=eta0, mean_field=Eb0, spread=sp0, W=W0, Q=Q0, a0=float(a0b), Emax=Emax0, smin=smin0)
    G_min = grad_factor * Eb0

    def loss(p):
        eta, Eb, spread, W, Q, Emax, smin, amax = metrics(*fields(p))
        pen = 0.0
        pen += 20.0 * jnp.maximum(spread - s_max, 0.0) ** 2 / s_max**2
        pen += 20.0 * jnp.maximum(G_min - Eb, 0.0) ** 2 / G_min**2
        pen += 200.0 * jnp.maximum(0.08 - smin, 0.0) ** 2 / 0.08**2
        pen += 50.0 * jnp.maximum(Emax - 0.8 * Ewb, 0.0) ** 2 / Ewb**2
        pen += 50.0 * jnp.maximum(amax - a2max, 0.0) ** 2 / a2max**2
        return -eta + pen, (eta, Eb, spread, W, Q, Emax, smin)

    vg = jax.jit(jax.value_and_grad(lambda p: loss(p)[0]))
    aux = jax.jit(lambda p: loss(p)[1])
    p0d = nnls(Bd.T * a2max, a2_base)[0]
    p0b = nnls(Bb.T * nbmax, nb_base)[0]
    p0 = np.clip(np.concatenate([p0d, p0b]), 0, 1)
    if n_periods_drv > 1.0:
        p0[:Nd] = 0.0
        # initial train guess: equal pulses spaced by lam, total similar wake
        npul = int(round(n_periods_drv))
        for k in range(npul):
            j = np.argmin(np.abs(cd - (-k * lam)))
            p0[j] = min(1.0, (a0b**2 * 0.5 / npul) / a2max * 1.5)
        # beam to the bucket behind the last pulse
    meta = dict(T=T, beta=b, lam=lam, Ewb=Ewb, h=h, Nd=Nd, Nb=Nb, a0_max=float(np.sqrt(2 * a2max)),
                s_max=s_max, G_min=float(G_min), xi=xi, a2_base=a2_base, nb_base=nb_base, a2max=a2max)
    print(f"   start point: {[round(float(v),4) for v in aux(jnp.array(p0))]}  (eta, field, spread, W, Q, Emax, smin)")
    return vg, aux, base, meta, p0, fields


def optimise(T, a0_max=None, n_periods_drv=1.0, s_max=0.05, grad_factor=1.0, maxiter=400,
             seed=0, restarts=3, verbose=True, a0frac=1.3):
    vg, aux, base, meta, p0, fields = build(T, n_periods_drv=n_periods_drv, a0_max=a0_max,
                                            s_max=s_max, grad_factor=grad_factor, a0frac=a0frac)
    Nd, Nb = meta["Nd"], meta["Nb"]
    bounds = [(0.0, 1.0)] * (Nd + Nb)
    rng = np.random.default_rng(seed)
    best = None
    t0 = time.time()
    for r in range(restarts):
        if r == 0:
            x0 = p0.copy()
        else:
            x0 = np.clip(p0 * (1 + 0.3 * rng.standard_normal(p0.size)) + 0.05 * rng.random(p0.size) * (r % 2), 0, 1)
        fun = lambda x: tuple(np.asarray(v, dtype=float) for v in vg(jnp.array(x)))
        res = minimize(fun, x0, jac=True, method="L-BFGS-B", bounds=bounds,
                       options=dict(maxiter=maxiter, maxfun=maxiter * 2))
        eta, Eb, spread, W, Q, Emax, smin = [float(v) for v in aux(jnp.array(res.x))]
        feasible = spread <= 1.05 * s_max and Eb >= 0.98 * meta["G_min"] and smin > 0.04 and Emax <= 0.81 * meta["Ewb"]
        rec = dict(eta=eta, mean_field=Eb, spread=spread, W=W, Q=Q, Emax=Emax, smin=smin,
                   feasible=bool(feasible), nit=int(res.nit), x=res.x)
        if verbose:
            print(f"   restart {r}: eta={eta:.4f} field={Eb:.4f} spread={spread:.4f} feasible={feasible} nit={res.nit} ({time.time()-t0:.0f}s)", flush=True)
        if best is None or (rec["feasible"], rec["eta"]) > (best["feasible"], best["eta"]):
            best = rec
    a2, nb, EL, EU, sL, sU, W = [np.asarray(v) for v in fields(jnp.array(best["x"]))]
    best.update(a2=a2, nb=nb, EL=EL, EU=EU)
    return base, best, meta


if __name__ == "__main__":
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=float, nargs="+", default=[100.0, 1000.0, 6000.0])
    ap.add_argument("--a0max", type=float, default=None)
    ap.add_argument("--nper", type=float, default=1.0)
    ap.add_argument("--a0frac", type=float, default=1.3)
    ap.add_argument("--tag", default="free")
    a = ap.parse_args()
    summary = []
    fig, axs = plt.subplots(len(a.T), 1, figsize=(10, 3.2 * len(a.T)))
    axs = np.atleast_1d(axs)
    for ax, T in zip(axs, a.T):
        print(f"T = {T} MeV, a0_max = {a.a0max}, a0frac = {a.a0frac}, driver window = {a.nper} periods")
        base, best, meta = optimise(T, a0_max=a.a0max, n_periods_drv=a.nper, a0frac=a.a0frac)
        print(f"  baseline: eta={base['eta']:.4f} field={base['mean_field']:.4f} spread={base['spread']:.4f} a0={base['a0']:.3f}")
        print(f"  optimised: eta={best['eta']:.4f} field={best['mean_field']:.4f} spread={best['spread']:.4f} "
              f"peak a0={np.sqrt(2*best['a2'].max()):.3f} feasible={best['feasible']}  -> x{best['eta']/base['eta']:.2f}")
        xi = meta["xi"]
        ax.plot(xi, meta["a2_base"], "C0:", label="baseline <a²>")
        ax.plot(xi, best["a2"], "C0-", label="optimised <a²>")
        ax.plot(xi, best["EL"], "C3-", label="optimised loaded E")
        ax.plot(xi, best["nb"] / max(best["nb"].max(), 1e-9) * best["EL"].max(), "k-", lw=0.8, label="optimised beam (norm.)")
        ax.set_title(f"T={T:.0f} MeV (β={meta['beta']:.3f}): η {base['eta']:.3f} → {best['eta']:.3f}")
        ax.legend(fontsize=7); ax.set_xlabel("ξ [c/ω_p]")
        summary.append(dict(T=T, beta=meta["beta"], a0_max=a.a0max, n_periods_drv=a.nper, baseline=base,
                            optimised={k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in best.items()},
                            xi=xi.tolist()))
    plt.tight_layout()
    plt.savefig(os.path.join(ROOT, "results", "figures", f"P2b_joint_opt_{a.tag}.png"), dpi=100)
    json.dump(summary, open(os.path.join(ROOT, "results", "data", f"P2b_joint_opt_{a.tag}.json"), "w"))
