"""P1f: velocity-matched resonant waveguide train (flying focus + resonant excitation) with
multi-bunch proton loading — 1D envelope PIC with an energy-consistent depletion model.

Driver: on-axis intensity of the rigid N-frequency comb designed in P1e,
    <a^2>(xi) = a2_avg * env(xi) * |sum_q exp(i dk_q xi)|^2 / N ,  dk_q = (dw_q/w_p)/beta_a [k_p]
(rigid pattern moving at beta_a), Gaussian envelope of FWHM n_env plasma periods.
Depletion: the train is guided, so its energy per area U = (k0/kp)^2 int <a^2> dxi is only lost
to the plasma; the driver amplitude is scaled so that U(t) = U0 - laser_work(t) (uniform
depletion along the train - an approximation).
Beam: proton bunches (Gaussian, sigma_xi) in every proton-accelerating bucket behind the first
n_skip periods (multi-bunch, like an RF linac bunch train), velocity-locked (feedback on mean).
Outputs: energy gain, laser-energy fraction used, laser->wake->beam efficiency (exact PIC
energy budget), wake amplitude.
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
sys.path.insert(0, os.path.dirname(__file__))
import pic1d_env as P
import plasma as PL

MP = 938.27208816
ME = 0.51099895
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


def run(T_inj=3000.0, k0_over_kp=56.4, spac=(0.981, 1.019), a_avg=0.35, n_env=12.0,
        n_skip=4, load_frac=0.4, sig_frac=0.04, L_acc=3000.0, dx=0.04, ppc=8, K=0.02,
        mobile_ions=True, depletion=True, verbose=True, tag=None, mode='multi'):
    """mode='multi': bunches in every bucket behind n_skip periods, TOTAL areal charge =
    load_frac*E_peak(last bucket) split equally (v1 loaded each bunch with load_frac*E_peak,
    which reversed the field - logged as a failure). mode='single': one bunch in the first
    bucket behind the train."""
    g0 = 1 + T_inj / MP
    b0 = np.sqrt(1 - 1 / g0 ** 2)
    lamw = 2 * np.pi * b0                 # wake wavelength in xi
    dw = np.concatenate([[0.0], np.cumsum(spac)])   # frequency offsets in units of w_p (below w0)
    dk = dw / b0                          # in k_p units
    Nf = len(dw)
    sig_env = n_env * lamw / 2.3548
    xi_c = -3 * sig_env                   # train centre behind the driver reference point

    def train_a2(xi):
        env = np.exp(-0.5 * ((xi - xi_c) / sig_env) ** 2)
        pat = np.abs(np.sum(np.exp(1j * dk[:, None] * (xi[None, :] - xi_c)), axis=0)) ** 2 / Nf
        return 0.5 * a_avg ** 2 * env * pat

    xi_tab = np.linspace(xi_c - 4 * sig_env, xi_c + 4 * sig_env, 20001)
    a2_tab = train_a2(xi_tab)
    U0 = k0_over_kp ** 2 * np.trapezoid(a2_tab, xi_tab)
    pulse = P.Pulse.table(xi_tab, a2_tab)
    st = dict(beta=b0, on=False)

    def vel(t, xd, sim):
        if not st["on"] or sim.xb.size == 0:
            return b0
        inside = sim.xb > sim.x0
        bc = np.mean(sim.ub[inside] / np.sqrt(1 + sim.ub[inside] ** 2))
        b = min(max(bc + K * (np.mean(sim.xb[inside]) - xd - st["xc_ref"]), 0.01), 0.99999)
        st["beta"] = b
        return b

    drv = P.Driver([pulse], x_start=0.0, velocity=vel)
    Lr = 60.0
    dens = lambda x: np.sin(0.5 * np.pi * np.clip((x - 10.0) / Lr, 0, 1)) ** 2
    Lx = 8 * sig_env + 4 * lamw + 10
    sim = P.Sim1D(Lx, dx, dens, drv, ppc=ppc, dt=0.5 * dx, mobile_ions=mobile_ions,
                  x_window0=-(Lx - 10))
    t0 = time.time()
    # propagate until the whole train is inside the plateau
    while drv.xd + xi_c - 4 * sig_env < 10 + Lr + 5:
        sim.step()
        if depletion:
            drv.depletion_scale = max(1 - sim.pond_work / U0, 0.0)
    # find proton-accelerating buckets along the train (E>0 peaks) behind the first n_skip periods
    xi_g = sim.grid - drv.xd
    E = sim.E.copy()
    front = xi_c + 2.0 * sig_env
    peaks = []
    x = front - n_skip * lamw if mode == 'multi' else xi_c - 2.6 * sig_env
    while x > (xi_c - 2.2 * sig_env if mode == 'multi' else xi_c - 2.6 * sig_env - 1.01 * lamw):
        m = (xi_g < x) & (xi_g > x - lamw)
        if m.any():
            j = np.where(m)[0][np.argmax(E[m])]
            # lock point on the front side (E = 0.8 peak)
            k = j
            while k < E.size - 1 and E[k] > 0.8 * E[j]:
                k += 1
            peaks.append((xi_g[k], E[j]))
        x -= lamw
    rng = np.random.default_rng(5)
    nper = 400
    xb, wb = [], []
    Eref = max(peaks[-1][1], 1e-6) if peaks else 0.0
    for (xl, Epk) in peaks:
        xb.append(drv.xd + xl + sig_frac * lamw * rng.standard_normal(nper))
        wb.append(np.full(nper, load_frac * Eref / (nper * len(peaks))))
    xb = np.concatenate(xb); wb = np.concatenate(wb)
    gb = 1 + T_inj * (1 + 0.003 * rng.standard_normal(xb.size)) / MP
    sim.add_beam(xb, np.sqrt(gb ** 2 - 1), wb)
    st["on"] = True
    st["xc_ref"] = np.mean(xb) - drv.xd
    W_start = sim.pond_work
    Kb0 = np.sum(sim.wb * (np.sqrt(1 + sim.ub ** 2) - 1)) * MP / ME
    x_start = drv.xd
    snaps = []
    while drv.xd - x_start < L_acc:
        sim.step()
        if depletion:
            drv.depletion_scale = max(1 - sim.pond_work / U0, 0.0)
        if not snaps or drv.xd - snaps[-1]["dist"] - x_start > L_acc / 15:
            Tb = (np.sqrt(1 + sim.ub ** 2) - 1) * MP
            inside = sim.xb > sim.x0
            snaps.append(dict(dist=float(drv.xd - x_start), T_mean=float(np.average(Tb[inside], weights=sim.wb[inside])),
                              T_std=float(np.sqrt(np.average((Tb[inside] - np.average(Tb[inside], weights=sim.wb[inside]))**2, weights=sim.wb[inside]))),
                              U_left=float(1 - sim.pond_work / U0), Emax=float(np.abs(sim.E).max()),
                              survival=float(inside.mean())))
            if verbose:
                s = snaps[-1]
                print(f"   dist={s['dist']:7.0f} <T>={s['T_mean']:8.1f}±{s['T_std']:5.1f} MeV laser left={s['U_left']:.3f} "
                      f"Emax={s['Emax']:.3f} surv={s['survival']:.3f} ({time.time()-t0:.0f}s)", flush=True)
    Kb1 = np.sum(sim.wb * (np.sqrt(1 + sim.ub ** 2) - 1)) * MP / ME
    work = sim.pond_work - W_start
    Tb = (np.sqrt(1 + sim.ub ** 2) - 1) * MP
    res = dict(mode=mode, T_inj=T_inj, k0_over_kp=k0_over_kp, a_avg=a_avg, n_env=n_env, Nf=Nf, n_bunches=len(peaks),
               load_frac=load_frac, L_acc=L_acc, U0=U0, laser_work_total=float(sim.pond_work),
               laser_used_frac=float(sim.pond_work / U0), work_during_acc=float(work),
               beam_gain=float(Kb1 - Kb0), eff_wake_to_beam=float((Kb1 - Kb0) / work),
               eff_laser_to_beam_1D=float((Kb1 - Kb0) / U0),
               T_final=float(np.average(Tb, weights=sim.wb)), runtime_s=time.time() - t0,
               depletion=depletion, snaps=snaps)
    if tag:
        json.dump(res, open(os.path.join(ROOT, "results", "data", f"P1f_{tag}.json"), "w"), indent=1)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=float, default=0.35)
    ap.add_argument("--L", type=float, default=3000.0)
    ap.add_argument("--load", type=float, default=0.4)
    ap.add_argument("--nenv", type=float, default=12.0)
    ap.add_argument("--mode", default="multi")
    ap.add_argument("--tag", default="test")
    a = ap.parse_args()
    r = run(a_avg=a.a, L_acc=a.L, load_frac=a.load, n_env=a.nenv, tag=a.tag, mode=a.mode)
    print(json.dumps({k: v for k, v in r.items() if k != "snaps"}, indent=1))
