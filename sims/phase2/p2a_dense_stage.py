"""P2a: one 'density-matched, depletion-limited' LWFA stage for protons, full-EM 1D PIC.

A laser pulse (resolved, k0/kp, a0, Gaussian) enters a plasma (smooth ramp) whose density is
chosen so that the *actual* wake phase velocity (reduced below v_g by etching/red-shift, see
P2a-explore) is close to the proton velocity. The pulse depletes within the stage.
Step 1 (map): zero-weight test protons over a grid of injection phase x energy -> best gain.
Step 2 (loaded): a real proton bunch of areal weight sigma_b at the best (phase, energy) ->
laser->proton efficiency from the exact energy budget (laser EM energy vs beam kinetic energy).
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import pic1d_em as EM

MP = 938.27208816
ME = 0.51099895
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


def make(k0, a0, sig, Lr=30.0, Lx=None, ppc=8):
    dx = 2 * np.pi / k0 / 32
    Lx = Lx or 90.0
    xc = Lx - 8.0
    ainit = lambda x: a0 * np.exp(-(x - xc) ** 2 / (4 * sig ** 2)) * np.cos(k0 * (x - xc))
    xs = xc + 5
    dens = lambda x: np.sin(0.5 * np.pi * np.clip((x - xs) / Lr, 0, 1)) ** 2
    em = EM.SimEM1D(Lx, dx, k0, dens, ainit, ppc=ppc)
    return em, xc, xs + Lr


def run_stage(k0, a0, sig, T_grid, n_phase=60, t_stage=None, sigma_b=0.0, inject=None,
              verbose=False, depletion_stop=0.97):
    """inject: (xi_rel, T) to place a loaded bunch; else a map of test protons.
    The bunch/map is inserted when the laser centroid reaches the plateau start + 5."""
    em, xc, x_plat = make(k0, a0, sig)
    U0 = em.laser_energy()
    # advance to the plateau
    while True:
        I = em.A ** 2
        xL = np.sum(em.grid * I) / np.sum(I)
        if xL > x_plat + 5:
            break
        em.step()
    # wake period estimate
    lam = 2 * np.pi
    if inject is None:
        xis = np.linspace(-1.5 * lam, -0.2 * lam, n_phase)
        XI, TT = np.meshgrid(xis, T_grid, indexing="ij")
        xb = xL + XI.ravel()
        g = 1 + TT.ravel() / MP
        em.add_beam(xb, np.sqrt(g ** 2 - 1), np.zeros(xb.size))
    else:
        xi0, T0, sxi, nmac = inject
        rng = np.random.default_rng(3)
        xb = xL + xi0 + sxi * rng.standard_normal(nmac)
        g = 1 + T0 / MP
        em.add_beam(xb, np.full(nmac, np.sqrt(g ** 2 - 1)), np.full(nmac, sigma_b / nmac))
    Tb0 = (np.sqrt(1 + em.ub ** 2) - 1) * MP
    Kb0 = em.beam_kinetic_mec2()
    U_inj = em.laser_energy()
    x_start = xL
    Tmax = Tb0.copy()
    t0 = time.time()
    hist = []
    while True:
        em.step()
        if not (em.xb >= em.x0).any():
            break
        Tb = (np.sqrt(1 + em.ub ** 2) - 1) * MP
        if inject is None:
            Tmax = np.maximum(Tmax, Tb)
        if int(em.t / em.dt) % 200 == 0:
            U = em.laser_energy()
            I = em.A ** 2
            xL = np.sum(em.grid * I) / max(np.sum(I), 1e-30)
            hist.append((em.t, xL - x_start, U / U0, float(Tb.mean())))
            if U / U0 < 1 - depletion_stop or (t_stage and em.t > t_stage):
                break
            if verbose:
                print(f"   t={em.t:.0f} dist={xL-x_start:.0f} U/U0={U/U0:.3f} <T>={Tb.mean():.1f} ({time.time()-t0:.0f}s)", flush=True)
    res = dict(k0=k0, a0=a0, sig=sig, U0=U0, U_end=em.laser_energy(), stage_length=hist[-1][1] if hist else 0.0,
               runtime=time.time() - t0, hist=hist)
    if inject is None:
        gain = (Tmax - Tb0)
        n = len(T_grid)
        G = gain.reshape(n_phase, n)
        i, j = np.unravel_index(np.argmax(G), G.shape)
        res.update(best_gain_MeV=float(G[i, j]), best_xi=float(np.linspace(-1.5 * lam, -0.2 * lam, n_phase)[i]),
                   best_T=float(T_grid[j]), gain_map=G.tolist(), T_grid=list(map(float, T_grid)))
    else:
        Tb = (np.sqrt(1 + em.ub ** 2) - 1) * MP
        dK = em.beam_kinetic_mec2() - Kb0
        inside = em.xb >= em.x0
        res.update(T_in=float(Tb0.mean()), T_out=float(Tb[inside].mean()), T_out_std=float(Tb[inside].std()),
                   survival=float(inside.mean()), beam_gain_mec2=dK,
                   eff_laser_to_beam=float(dK / U0), laser_used_frac=float(1 - em.laser_energy() / U0))
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--k0", type=float, default=7.4)
    ap.add_argument("--a0", type=float, default=2.0)
    ap.add_argument("--sig", type=float, default=1.0)
    ap.add_argument("--Tc", type=float, default=1700.0)
    a = ap.parse_args()
    T_grid = a.Tc * np.linspace(0.6, 1.5, 19)
    r = run_stage(a.k0, a.a0, a.sig, T_grid, verbose=False)
    print(f"MAP k0={a.k0} a0={a.a0}: best gain {r['best_gain_MeV']:.1f} MeV at xi={r['best_xi']:.2f}, T={r['best_T']:.0f} MeV; "
          f"stage length {r['stage_length']:.0f} c/wp ({r['runtime']:.0f}s)", flush=True)
    out = dict(map=r)
    for sb in [0.05, 0.15, 0.3]:
        rl = run_stage(a.k0, a.a0, a.sig, None, sigma_b=sb, inject=(r["best_xi"], r["best_T"], 0.05, 1000))
        print(f"LOADED sigma_b={sb}: T {rl['T_in']:.0f} -> {rl['T_out']:.0f} ± {rl['T_out_std']:.0f} MeV, survival {rl['survival']:.3f}, "
              f"laser->proton eff = {rl['eff_laser_to_beam']:.4f}, laser used {rl['laser_used_frac']:.3f}, length {rl['stage_length']:.0f}", flush=True)
        out[f"loaded_{sb}"] = rl
    json.dump(out, open(os.path.join(ROOT, "results", "data", f"P2a_stage_k{a.k0}_a{a.a0}.json"), "w"))
