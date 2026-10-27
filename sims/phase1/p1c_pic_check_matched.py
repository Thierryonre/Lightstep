"""P1c: kinetic (1D envelope-PIC) check of a velocity-matched, beam-loaded proton segment,
compared with the quasi-static fluid tracker for the same parameters.

Checks: loaded accelerating field, energy gain, energy spread, wake->beam efficiency (exact
energy budget in the PIC), background-electron trapping (dark current) and ion motion.
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
sys.path.insert(0, os.path.dirname(__file__))
import fluid1d as F
import pic1d_env as P
import track1d as TR
from p1b_matched_acceleration import beta_of_T, wake_for, a0_for_field, first_bucket

ME = 0.51099895
MP = 938.27208816
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


def setup(T_inj, tau, f_field, load, sig_xi_frac, lock_frac):
    """Driver amplitude for the target field and the lock point in the FIRST proton-accelerating
    lobe (same definitions as p1b v2)."""
    b0 = float(beta_of_T(T_inj))
    Ewb0 = np.sqrt(2 * (T_inj / MP))
    a0 = a0_for_field(b0, tau, f_field * 0.8 * Ewb0)
    xi_w, phi_w, E_w, br_w, _ = wake_for(b0, a0, tau)
    xpk, Epk, xl = first_bucket(xi_w, E_w, b0, tau, lock_frac)
    return b0, a0, xl, Epk


def make_lock(T_inj, tau, a0, lock_frac):
    """Phase lock that re-locates the lock point as beta changes (fixed a0 over the segment)."""
    st = {}

    def xi_lock(b):
        if "b" not in st or abs(b - st["b"]) > 1e-2 * max(1 - b, 1e-3):
            xi, _, E, _, _ = wake_for(b, a0, tau)
            st["b"] = b
            st["xl"] = first_bucket(xi, E, b, tau, lock_frac)[2]
        return st["xl"]
    return xi_lock


def run(T_inj=1000.0, tau=2.355, f_field=0.7, load=0.4, sig_xi_frac=0.03, lock_frac=0.8,
        L_acc=2000.0, K=0.05, mobile_ions=True, ppc=16, dx=None, nmac=2000, Lramp=60.0):
    b0, a0, xi_lock, Epk = setup(T_inj, tau, f_field, load, sig_xi_frac, lock_frac)
    lockf = make_lock(T_inj, tau, a0, lock_frac)
    lam = 2 * np.pi * b0
    dx = dx or min(0.02, b0 * tau / 40)
    state = dict(beta=b0, beam_on=False)
    x_ramp0 = 10.0
    x_plateau = x_ramp0 + Lramp

    def vel(t, xd, sim):
        if not state["beam_on"] or sim.xb.size == 0:
            return b0
        bc = np.mean(sim.ub / np.sqrt(1 + sim.ub**2))
        xc = np.mean(sim.xb) - xd
        b = min(max(bc + K * (xc - lockf(bc)), 0.01), 0.99999)
        state["beta"] = b
        return b

    drv = P.Driver([P.Pulse(a0, b0 * tau, 0.0, "gauss")], x_start=0.0, velocity=vel)
    dens = lambda x: np.sin(0.5 * np.pi * np.clip((x - x_ramp0) / Lramp, 0, 1))**2
    Lx = 1.6 * lam + 8 * b0 * tau + 10
    sim = P.Sim1D(Lx, dx, dens, drv, ppc=ppc, dt=0.5 * dx, mobile_ions=mobile_ions,
                  x_window0=-(Lx - 6 * b0 * tau))
    # propagate until the driver is 2 wavelengths into the plateau, then add the beam
    t0 = time.time()
    while drv.xd < x_plateau + 2 * lam:
        sim.step()
    rng = np.random.default_rng(1)
    xb = drv.xd + xi_lock + sig_xi_frac * lam * rng.standard_normal(nmac)
    Tb = T_inj * (1 + 0.005 * rng.standard_normal(nmac))
    gb = 1 + Tb / MP
    sim.add_beam(xb, np.sqrt(gb**2 - 1), np.full(nmac, load * Epk / nmac))
    state["beam_on"] = True
    W0 = sim.pond_work
    x_start = drv.xd
    Tb0 = (np.sqrt(1 + sim.ub**2) - 1) * MP
    snaps = []
    while drv.xd < x_start + L_acc:
        sim.step()
        if len(snaps) == 0 or drv.xd - snaps[-1]["xd"] > L_acc / 20:
            Tb = (np.sqrt(1 + sim.ub**2) - 1) * MP
            ne_fast = int(np.sum(sim.ue > 2 * b0 / np.sqrt(1 - b0**2)))   # electrons faster than the wake
            snaps.append(dict(xd=float(drv.xd), T_mean=float(Tb.mean()), T_std=float(Tb.std()),
                              n_beam=int(sim.xb.size), e_trapped_macro=ne_fast, beta=float(state["beta"])))
            print(f"   xd-x0={drv.xd-x_start:7.0f} T={Tb.mean():8.1f}±{Tb.std():6.1f} MeV beam={sim.xb.size} "
                  f"fast e-={ne_fast} ({time.time()-t0:.0f}s)", flush=True)
    Tb = (np.sqrt(1 + sim.ub**2) - 1) * MP
    keep = np.isin(np.arange(nmac), np.arange(nmac))  # all macro-particles retained in array order
    gain = np.sum(sim.wb * (Tb - Tb0[:Tb.size])) / ME     # m_e c^2 areal units
    work = sim.pond_work - W0
    res = dict(T_inj=T_inj, a0=a0, tau=tau, xi_lock=xi_lock, E_peak0=Epk, load=load,
               L_acc=L_acc, T_final_mean=float(Tb.mean()), T_final_std=float(Tb.std()),
               gain_MeV=float(Tb.mean() - T_inj), mean_gradient_E0=float((Tb.mean() - T_inj) / ME / L_acc),
               eff_wake_to_beam=float(gain / work), laser_work_per_length=float(work / L_acc),
               beam_survival=float(sim.xb.size / nmac), mobile_ions=mobile_ions, snaps=snaps,
               runtime_s=time.time() - t0)
    return res


def tracker_same(T_inj=1000.0, tau=2.355, f_field=0.7, load=0.4, sig_xi_frac=0.03, lock_frac=0.8,
                 L_acc=2000.0, K=0.05, nmac=2000):
    b0, a0, xi_lock, Epk = setup(T_inj, tau, f_field, load, sig_xi_frac, lock_frac)
    lockf = make_lock(T_inj, tau, a0, lock_frac)
    lam = 2 * np.pi * b0
    st = dict(beta=b0)
    drv = lambda xi, t, xd: F.gaussian_envelope(xi, 0.0, b0 * tau, a0)

    def bp(t, xd, tr):
        al = tr.alive
        bc = np.mean(TR.proton_beta(tr.pu[al]))
        xc = np.mean(tr.pxi[al])
        b = min(max(bc + K * (xc - lockf(bc)), 0.01), 0.99999)
        st["beta"] = b
        return b

    tr = TR.Tracker(-1.6 * 2 * np.pi - 4 * b0 * tau, 4 * b0 * tau, min(lam / 300, b0 * tau / 30), drv, bp)
    rng = np.random.default_rng(1)
    xb = xi_lock + sig_xi_frac * lam * rng.standard_normal(nmac)
    Tb = T_inj * (1 + 0.005 * rng.standard_normal(nmac))
    tr.set_beam(xb, Tb, load * Epk / nmac)
    dt = 0.05 * lam
    i = 0
    while tr.xd < L_acc:
        tr.step(dt, energy_every=10, istep=i)
        i += 1
    T = tr.kinetic() * ME
    gain = np.sum(tr.pw * (T - tr.T0 * ME)) / ME
    return dict(T_final_mean=float(T.mean()), T_final_std=float(T.std()),
                gain_MeV=float(T.mean() - T_inj), eff_wake_to_beam=float(gain / tr.laser_work),
                laser_work_per_length=float(tr.laser_work / tr.xd), broken=bool(tr.broken))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--Tinj", type=float, default=1000.0)
    ap.add_argument("--L", type=float, default=2000.0)
    ap.add_argument("--load", type=float, default=0.4)
    ap.add_argument("--immobile", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    trk = tracker_same(T_inj=a.Tinj, L_acc=a.L, load=a.load)
    print("TRACKER:", json.dumps(trk), f"({time.time()-t0:.0f}s)", flush=True)
    pic = run(T_inj=a.Tinj, L_acc=a.L, load=a.load, mobile_ions=not a.immobile)
    print("PIC:", json.dumps({k: v for k, v in pic.items() if k != "snaps"}))
    with open(os.path.join(ROOT, "results", "data", f"P1c_pic_vs_tracker_T{int(a.Tinj)}_L{int(a.L)}_load{a.load}.json"), "w") as f:
        json.dump(dict(tracker=trk, pic=pic), f, indent=1)
