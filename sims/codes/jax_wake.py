"""Differentiable (JAX) 1D nonlinear cold-fluid quasi-static wake, arbitrary phase velocity.

Same equations as fluid1d.py (validated in S001-S003), written with jax.lax.scan so that
gradients w.r.t. the driver envelope, beam profile and phase velocity can be taken by
reverse-mode autodiff (analogue of the differentiable-physics approach of Crilly et al.,
PRR 8, 033353 (2026), applied here to wakefield design).

Grid convention: arrays are ordered from the FRONT (largest xi) to the BACK, uniform step h>0.
Laser work per unit length (exact for a rigid steady driver, checked against the wake energy
density to <0.6 %): W' = -int (n_e / 2 gamma) d<a^2>/dxi dxi.
"""
import jax
import jax.numpy as jnp

jax.config.update("jax_enable_x64", True)


def _rhs(phi, a2, nb, gp2, bp):
    p = 1.0 + phi
    s_arg = 1.0 - (1.0 + a2) / (gp2 * p * p)
    s_c = jnp.maximum(s_arg, 1e-6)
    f = gp2 * (bp / jnp.sqrt(s_c) - 1.0)
    return f - nb, s_arg


def solve(h, a2, nb, beta):
    """a2, nb ordered front->back. Returns phi, E (=-dphi/dxi), min sqrt-argument (breaking
    indicator, must stay > 0)."""
    gp2 = 1.0 / (1.0 - beta * beta)
    hs = -h
    a_m = 0.5 * (a2[:-1] + a2[1:])
    b_m = 0.5 * (nb[:-1] + nb[1:])
    xs = (a2[:-1], a_m, a2[1:], nb[:-1], b_m, nb[1:])

    def step(carry, inp):
        y0, y1, smin = carry
        ai, am, ae, bi, bm, be = inp
        f1, s1 = _rhs(y0, ai, bi, gp2, beta)
        k1a, k1b = y1, f1
        f2, s2 = _rhs(y0 + 0.5 * hs * k1a, am, bm, gp2, beta)
        k2a, k2b = y1 + 0.5 * hs * k1b, f2
        f3, s3 = _rhs(y0 + 0.5 * hs * k2a, am, bm, gp2, beta)
        k3a, k3b = y1 + 0.5 * hs * k2b, f3
        f4, s4 = _rhs(y0 + hs * k3a, ae, be, gp2, beta)
        k4a, k4b = y1 + hs * k3b, f4
        y0n = y0 + hs / 6.0 * (k1a + 2 * k2a + 2 * k3a + k4a)
        y1n = y1 + hs / 6.0 * (k1b + 2 * k2b + 2 * k3b + k4b)
        smin = jnp.minimum(smin, jnp.minimum(jnp.minimum(s1, s2), jnp.minimum(s3, s4)))
        return (y0n, y1n, smin), (y0n, y1n)

    (y0, y1, smin), (phis, dphis) = jax.lax.scan(step, (0.0, 0.0, 1.0), xs)
    phi = jnp.concatenate([jnp.zeros(1), phis])
    E = -jnp.concatenate([jnp.zeros(1), dphis])
    return phi, E, smin


def fluid_ne_gamma(phi, a2, beta):
    gp2 = 1.0 / (1.0 - beta * beta)
    p = 1.0 + phi
    s = jnp.sqrt(jnp.maximum(1.0 - (1.0 + a2) / (gp2 * p * p), 1e-6))
    gam = gp2 * p * (1.0 - beta * s)
    ne = gp2 * beta * (1.0 / s - beta)
    return ne, gam


def laser_work(h, phi, a2, beta):
    ne, gam = fluid_ne_gamma(phi, a2, beta)
    da2 = jnp.gradient(a2) / (-h)        # d/dxi with front->back ordering
    return -jnp.sum(ne / (2 * gam) * da2) * h
