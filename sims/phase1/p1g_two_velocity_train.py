"""P1g: guided resonant train with the physically correct kinematics: the beat pattern (intensity
peaks) moves at v_a (rigid comb) but the energy envelope moves at the modes' group velocity
v_env ~ c. Protons (at v_a) therefore fall behind the envelope and ride the free plasma wave it
leaves, whose phase velocity is imprinted by the peak timing. 1D envelope PIC; the window moves
with the envelope (so the imprinted wave is kept); protons are loaded behind the envelope.
Compares with the rigid model (P1f, envelope moving with the pattern)."""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import pic1d_env as P

MP = 938.27208816
ME = 0.51099895
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


class TwoVelocityDriver(P.Driver):
    """<a^2>(x,t) = 0.5 a_avg^2 * env^2(x - x_env(t)) * |sum_q exp(i dk_q (x - x_pat(t)))|^2 / N"""

    def __init__(self, a_avg, dk, sig_env, beta_pat, beta_env, x0):
        super().__init__([], x0, beta_env)
        self.a_avg, self.dk, self.sig = a_avg, np.asarray(dk), sig_env
        self.bp, self.be = beta_pat, beta_env
        self.x_pat = x0
        self.N = len(dk)

    def a2(self, x, t):
        env = np.exp(-0.5 * ((x - self.xd) / self.sig) ** 2)
        m = env > 1e-8
        out = np.zeros_like(x)
        ph = self.dk[:, None] * (x[m][None, :] - self.x_pat)
        out[m] = 0.5 * self.a_avg ** 2 * env[m] * np.abs(np.exp(1j * ph).sum(axis=0)) ** 2 / self.N
        return out * self.depletion_scale


class TaperedTwoVelocityDriver(TwoVelocityDriver):
    """Static channel-width taper: the local pattern velocity at position z is v_pat(z), so the
    pattern is a function of (t - tau(z)), tau(z) = int dz / v_pat(z). Implemented on a fine
    tabulated grid. Omega_q (frequency offsets in units of w_p) set the comb."""

    def __init__(self, a_avg, Omega, sig_env, beta_env, x0, z_tab, tau_tab):
        super().__init__(a_avg, np.asarray(Omega), sig_env, 1.0, beta_env, x0)
        self.Om = np.asarray(Omega)
        self.z_tab, self.tau_tab = z_tab, tau_tab

    def a2(self, x, t):
        env = np.exp(-0.5 * ((x - self.xd) / self.sig) ** 2)
        m = env > 1e-8
        out = np.zeros_like(x)
        tau = np.interp(x[m], self.z_tab, self.tau_tab)
        ph = self.Om[:, None] * (t - tau)[None, :]
        out[m] = 0.5 * self.a_avg ** 2 * env[m] * np.abs(np.exp(-1j * ph).sum(axis=0)) ** 2 / self.N
        return out * self.depletion_scale


def run_taper(T_inj=3000.0, spac=(0.981, 1.019), a_avg=0.35, n_env=12.0, beta_env=0.9995,
              load_frac=0.4, sig_frac=0.04, L_acc=3000.0, G_MeV_per_cwp=0.07, dx=0.04, ppc=8,
              tag=None):
    """Open-loop static-taper design: v_pat(z) = beta of a proton gaining G per c/w_p after the
    injection point z_inj (the taper is fixed before the run; no feedback)."""
    g0 = 1 + T_inj / MP
    ba = np.sqrt(1 - 1 / g0 ** 2)
    lamw = 2 * np.pi * ba
    Om = np.concatenate([[0.0], np.cumsum(spac)])
    sig_env = n_env * 2 * np.pi * beta_env / 2.3548
    x0 = 0.0
    Lr = 60.0
    xs_pl = x0 + 3 * sig_env
    slip = (beta_env - ba) * (L_acc / ba + 200)
    Lx = 4 * sig_env + slip + 3 * lamw + 40
    # injection point estimate: where the protons will be loaded (behind the envelope tail when
    # the tail has passed the plateau start)
    z_inj_est = xs_pl + Lr + 10 + 3 * sig_env - 2.6 * sig_env - 0.5 * lamw - (beta_env - ba) * 0
    z_tab = np.linspace(-10, xs_pl + Lr + 4 * L_acc + 2000, 400001)
    T_z = T_inj + G_MeV_per_cwp * np.clip(z_tab - z_inj_est, 0, None)
    gz = 1 + T_z / MP
    vz = np.sqrt(1 - 1 / gz ** 2)
    tau_tab = np.concatenate([[0.0], np.cumsum(0.5 * (1 / vz[1:] + 1 / vz[:-1]) * np.diff(z_tab))])
    drv = TaperedTwoVelocityDriver(a_avg, Om, sig_env, beta_env, x0, z_tab, tau_tab)
    dens = lambda x, xs=xs_pl: np.sin(0.5 * np.pi * np.clip((x - xs) / Lr, 0, 1)) ** 2
    sim = P.Sim1D(Lx, dx, dens, drv, ppc=ppc, dt=0.5 * dx, mobile_ions=True,
                  x_window0=xs_pl - Lx + 10, window_velocity=beta_env)
    t0 = time.time()
    while drv.xd - 3 * sig_env < xs_pl + Lr + 10:
        sim.step()
    xi = sim.grid
    E = sim.E.copy()
    x_tail = drv.xd - 2.6 * sig_env
    m = (xi < x_tail) & (xi > x_tail - lamw)
    j = np.where(m)[0][np.argmax(E[m])]
    k = j
    while k < E.size - 1 and E[k] > 0.8 * E[j]:
        k += 1
    Epk = E[j]
    rng = np.random.default_rng(7)
    nm = 1500
    xb = xi[k] + sig_frac * lamw * rng.standard_normal(nm)
    gb = 1 + T_inj * (1 + 0.003 * rng.standard_normal(nm)) / MP
    sim.add_beam(xb, np.sqrt(gb ** 2 - 1), np.full(nm, load_frac * Epk / nm))
    W0 = sim.pond_work
    Kb0 = np.sum(sim.wb * (np.sqrt(1 + sim.ub ** 2) - 1)) * MP / ME
    xs = np.mean(sim.xb)
    snaps = []
    while np.mean(sim.xb) - xs < L_acc:
        sim.step()
        if not snaps or np.mean(sim.xb) - xs - snaps[-1]["dist"] > L_acc / 10:
            Tb = (np.sqrt(1 + sim.ub ** 2) - 1) * MP
            inside = sim.xb > sim.x0
            snaps.append(dict(dist=float(np.mean(sim.xb) - xs), T_mean=float(Tb[inside].mean()),
                              T_std=float(Tb[inside].std()), survival=float(inside.mean()),
                              behind_envelope=float(drv.xd - np.mean(sim.xb))))
            print(f"   dist={snaps[-1]['dist']:6.0f} <T>={snaps[-1]['T_mean']:8.1f}±{snaps[-1]['T_std']:5.1f} MeV "
                  f"(design {T_inj + G_MeV_per_cwp*snaps[-1]['dist']:.0f}) behind env {snaps[-1]['behind_envelope']:.0f} c/wp ({time.time()-t0:.0f}s)", flush=True)
            if snaps[-1]["survival"] < 0.5:
                break
    Kb1 = np.sum(sim.wb * (np.sqrt(1 + sim.ub ** 2) - 1)) * MP / ME
    # the envelope drove plasma beyond the protons' end point; count only the work done on the
    # plasma the protons actually traversed (work per unit length x proton path length)
    work_per_len = sim.pond_work / (drv.xd - xs_pl)
    res = dict(mode="static_taper", T_inj=T_inj, G_design=G_MeV_per_cwp, n_env=n_env, a_avg=a_avg,
               load_frac=load_frac, E_peak_behind_env=float(Epk), beam_gain=float(Kb1 - Kb0),
               T_final=float(snaps[-1]["T_mean"]), T_final_std=float(snaps[-1]["T_std"]),
               work_per_length=float(work_per_len),
               eff_wake_to_beam=float((Kb1 - Kb0) / (work_per_len * snaps[-1]["dist"])),
               snaps=snaps, runtime_s=time.time() - t0)
    if tag:
        json.dump(res, open(os.path.join(ROOT, "results", "data", f"P1g_{tag}.json"), "w"), indent=1)
    return res


def run(T_inj=3000.0, spac=(0.981, 1.019), a_avg=0.35, n_env=12.0, beta_env=0.9995,
        load_frac=0.4, sig_frac=0.04, L_acc=3000.0, dx=0.04, ppc=8, mobile_ions=True, tag=None):
    g0 = 1 + T_inj / MP
    ba = np.sqrt(1 - 1 / g0 ** 2)
    lamw = 2 * np.pi * ba
    dw = np.concatenate([[0.0], np.cumsum(spac)])
    dk = dw / ba
    sig_env = n_env * 2 * np.pi * beta_env / 2.3548        # envelope FWHM = n_env periods (duration at a point)
    drv = TwoVelocityDriver(a_avg, dk, sig_env, ba, beta_env, x0=0.0)
    slip = (beta_env - ba) * (L_acc / ba + 200)
    Lx = 4 * sig_env + slip + 3 * lamw + 40
    Lr = 60.0
    dens = lambda x: np.sin(0.5 * np.pi * np.clip((x - (drv.xd + 3 * sig_env)) / Lr, 0, 1)) ** 2
    dens0 = dens
    x_start_plasma = drv.xd + 3 * sig_env
    dens = lambda x, xs=x_start_plasma: np.sin(0.5 * np.pi * np.clip((x - xs) / Lr, 0, 1)) ** 2
    sim = P.Sim1D(Lx, dx, dens, drv, ppc=ppc, dt=0.5 * dx, mobile_ions=mobile_ions,
                  x_window0=drv.xd + 3 * sig_env - Lx + 10, window_velocity=beta_env)
    t0 = time.time()
    # advance pattern position alongside the envelope
    def step():
        sim.step()
        drv.x_pat += ba * sim.dt
    # propagate until the envelope tail is well inside the plateau
    while drv.xd - 3 * sig_env < x_start_plasma + Lr + 10:
        step()
    # find the proton-accelerating bucket just behind the envelope tail (E > 0 peak)
    xi = sim.grid
    E = sim.E.copy()
    x_tail = drv.xd - 2.6 * sig_env
    m = (xi < x_tail) & (xi > x_tail - lamw)
    j = np.where(m)[0][np.argmax(E[m])]
    k = j
    while k < E.size - 1 and E[k] > 0.8 * E[j]:
        k += 1
    Epk = E[j]
    rng = np.random.default_rng(7)
    nm = 1500
    xb = xi[k] + sig_frac * lamw * rng.standard_normal(nm)
    gb = 1 + T_inj * (1 + 0.003 * rng.standard_normal(nm)) / MP
    sim.add_beam(xb, np.sqrt(gb ** 2 - 1), np.full(nm, load_frac * Epk / nm))
    W0 = sim.pond_work
    Kb0 = np.sum(sim.wb * (np.sqrt(1 + sim.ub ** 2) - 1)) * MP / ME
    xs = np.mean(sim.xb)
    snaps = []
    while np.mean(sim.xb) - xs < L_acc:
        step()
        if not snaps or np.mean(sim.xb) - xs - snaps[-1]["dist"] > L_acc / 10:
            Tb = (np.sqrt(1 + sim.ub ** 2) - 1) * MP
            inside = sim.xb > sim.x0
            snaps.append(dict(dist=float(np.mean(sim.xb) - xs), T_mean=float(Tb[inside].mean()),
                              T_std=float(Tb[inside].std()), survival=float(inside.mean()),
                              behind_envelope=float(drv.xd - np.mean(sim.xb))))
            print(f"   dist={snaps[-1]['dist']:6.0f} <T>={snaps[-1]['T_mean']:8.1f}±{snaps[-1]['T_std']:5.1f} MeV "
                  f"protons {snaps[-1]['behind_envelope']:.0f} c/wp behind envelope centre, surv={snaps[-1]['survival']:.3f} "
                  f"({time.time()-t0:.0f}s)", flush=True)
            if snaps[-1]["survival"] < 0.5:
                break
    Kb1 = np.sum(sim.wb * (np.sqrt(1 + sim.ub ** 2) - 1)) * MP / ME
    res = dict(T_inj=T_inj, beta_pattern=ba, beta_env=beta_env, n_env=n_env, a_avg=a_avg, load_frac=load_frac,
               E_peak_behind_env=float(Epk), beam_gain=float(Kb1 - Kb0),
               laser_work_total=float(sim.pond_work), work_during=float(sim.pond_work - W0),
               note="wake->beam efficiency here = beam gain / laser work over the same plasma length "
                    "(the envelope drives plasma ahead of the protons; work is accounted over the full run)",
               eff_beam_over_total_work=float((Kb1 - Kb0) / sim.pond_work),
               T_final=float(snaps[-1]["T_mean"]), snaps=snaps, runtime_s=time.time() - t0)
    if tag:
        json.dump(res, open(os.path.join(ROOT, "results", "data", f"P1g_{tag}.json"), "w"), indent=1)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--nenv", type=float, default=12.0)
    ap.add_argument("--L", type=float, default=3000.0)
    ap.add_argument("--tag", default="nenv12")
    ap.add_argument("--taper", action="store_true")
    ap.add_argument("--G", type=float, default=0.07)
    a = ap.parse_args()
    if a.taper:
        r = run_taper(n_env=a.nenv, L_acc=a.L, G_MeV_per_cwp=a.G, tag=a.tag)
    else:
        r = run(n_env=a.nenv, L_acc=a.L, tag=a.tag)
    print(json.dumps({k: v for k, v in r.items() if k != "snaps"}, indent=1))
