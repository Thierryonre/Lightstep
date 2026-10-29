"""P1b: full proton acceleration T_inj -> T_final in a velocity-matched ("flying-focus" /
programmable-velocity) wake. 1D quasi-static fluid wake + beam-loaded proton tracking.

Driver: Gaussian <a^2>; drive duration tau at a fixed point (spatial FWHM = beta_d * tau);
amplitude a0(beta) found by bisection so that the unloaded proton-accelerating peak equals the
field program E_target(beta):
  'const' : E_target = f * 0.8 * E_wb(T_inj)   (constant gradient)
  'track' : E_target = f * 0.8 * E_wb(beta)    (gradient grows with energy)
Phase lock: the beam centroid is kept at a fixed *phase* of the first proton-accelerating lobe
behind the driver (front side, where E = lock_frac * E_peak), re-located from the current
unloaded wake whenever beta changes. beta_d = beta_centroid + K (xi_c - xi_lock).
The recorded x_d(t) is the focal trajectory the optics must produce.

History of this script: v1 locked at a fixed distance xi behind the driver; because the wake
wavelength grows with beta, the beam drifted to a field zero and stalled (logged in S013).
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F
import track1d as TR

MP = 938.27208816
MD = 1875.61294257
ME = 0.51099895
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


def beta_of_T(T, M=MP):
    g = 1 + np.asarray(T) / M
    return np.sqrt(1 - 1 / g**2)


def wake_for(beta, a0, tau, nper=400):
    L = beta * tau
    lam = 2 * np.pi * beta
    dxi = min(lam / nper, L / 30)
    xi = np.arange(-1.6 * lam - 4 * L, 4 * L, dxi)
    a2 = F.gaussian_envelope(xi, 0.0, L, a0)
    phi, E, br = F.solve_wake(xi, a2, np.zeros_like(xi), beta)
    return xi, phi, E, br, a2


def first_bucket(xi, E, beta, tau, lock_frac):
    """First proton-accelerating (E>0) lobe behind the driver: peak position/value and the
    lock point on its front (stable) side where E = lock_frac*E_peak."""
    L = beta * tau
    lam = 2 * np.pi * beta
    m = (xi < -0.5 * L) & (xi > -0.5 * L - 1.1 * lam)
    idx = np.where(m)[0]
    ipk = idx[np.argmax(E[idx])]
    j = ipk
    while j < xi.size - 1 and E[j] > lock_frac * E[ipk]:
        j += 1
    return xi[ipk], E[ipk], xi[j]


def a0_for_field(beta, tau, E_target):
    lo, hi = 0.0, 10.0
    for _ in range(36):
        mid = 0.5 * (lo + hi)
        xi, phi, E, br, a2 = wake_for(beta, mid, tau)
        if br >= 0:
            hi = mid
            continue
        xpk, Epk, xl = first_bucket(xi, E, beta, tau, 0.5)
        if Epk > E_target:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def run(T_inj=100.0, T_final=6000.0, tau=2.355, program="const", f_field=0.7, load=0.4,
        sig_xi_frac=0.03, dT_frac=0.005, nmac=1000, K=0.05, lock_frac=0.8, verbose=True,
        tag=None, max_time_s=1500, species="proton"):
    M = MD if species == "deuteron" else MP
    b0 = float(beta_of_T(T_inj, M))
    Ewb0 = np.sqrt(2 * T_inj / M)
    Tgrid = np.geomspace(T_inj, T_final * 1.1, 30)
    bgrid = beta_of_T(Tgrid, M)
    if program == "const":
        Et = np.full_like(Tgrid, f_field * 0.8 * Ewb0)
    else:
        Et = f_field * 0.8 * np.sqrt(2 * Tgrid / M)
    a0grid = np.array([a0_for_field(b, tau, e) for b, e in zip(bgrid, Et)])
    a0_of_beta = lambda b: float(np.interp(b, bgrid, a0grid))

    xi_w, _, E_w, _, _ = wake_for(b0, a0_of_beta(b0), tau)
    xpk0, Epk0, xl0 = first_bucket(xi_w, E_w, b0, tau, lock_frac)
    st = dict(beta=b0, xi_lock=xl0, b_lock=b0, E_pk=Epk0)

    def relock(b):
        xi, _, E, br, _ = wake_for(b, a0_of_beta(b), tau)
        xpk, Epk, xl = first_bucket(xi, E, b, tau, lock_frac)
        st.update(xi_lock=xl, b_lock=b, E_pk=Epk)

    def drv(xi, t, xd):
        b = st["beta"]
        return F.gaussian_envelope(xi, 0.0, b * tau, a0_of_beta(b))

    def bprog(t, xd, tr):
        al = tr.alive
        if not al.any():
            return st["beta"]
        w = tr.pw[al]
        bc = np.average(TR.proton_beta(tr.pu[al]), weights=w)
        if abs(bc - st["b_lock"]) > 2e-4 * max(1 - bc, 1e-3) * 50:
            relock(bc)
        xc = np.average(tr.pxi[al], weights=w)
        b = min(max(bc + K * (xc - st["xi_lock"]), 0.01), 0.999999)
        st["beta"] = b
        return b

    lam_f = 2 * np.pi
    tr = TR.Tracker(-1.6 * lam_f - 4 * tau, 4 * tau, min(2 * np.pi * b0 / 300, b0 * tau / 30), drv, bprog,
                    species=species)
    rng = np.random.default_rng(1)
    lam0 = 2 * np.pi * b0
    xi0 = xl0 + sig_xi_frac * lam0 * rng.standard_normal(nmac)
    T0 = T_inj * (1 + dT_frac * rng.standard_normal(nmac))
    tr.set_beam(xi0, T0, load * Epk0 / nmac)
    t_start = time.time()
    traj = []
    i = 0
    stalled = False
    last_check = (0.0, T_inj)
    while True:
        b = st["beta"]
        dt = 0.03 * 2 * np.pi * b
        E = tr.step(dt, energy_every=25, istep=i)
        i += 1
        if i % 50 == 0:
            al = tr.alive
            T = tr.kinetic() * ME
            Tm = float(np.average(T[al], weights=tr.pw[al])) if al.any() else 0.0
            Ek, _ = TR.gather_cic(tr.pxi[al], tr.xi[0], tr.dxi, E)
            traj.append([tr.t, tr.xd, tr.beta_d, Tm, float(Ek.mean()) if Ek.size else 0.0,
                         a0_of_beta(tr.beta_d), tr.laser_work, float(al.sum() / nmac)])
            if Tm >= T_final or al.sum() < 0.05 * nmac:
                break
            if tr.xd - last_check[0] > 2000:
                if Tm - last_check[1] < 1e-3 * Tm:
                    stalled = True
                    break
                last_check = (tr.xd, Tm)
            if time.time() - t_start > max_time_s:
                break
            if verbose and i % 20000 == 0:
                print(f"   xd={tr.xd:9.0f} beta={tr.beta_d:.5f} T={Tm:8.1f} MeV E_beam={traj[-1][4]:.3f} "
                      f"alive={al.sum()} ({time.time()-t_start:.0f}s)", flush=True)
    al = tr.alive
    T = tr.kinetic() * ME
    w = tr.pw
    Tm = float(np.average(T[al], weights=w[al]))
    gain = np.sum(w[al] * (T[al] - tr.T0[al] * ME)) / ME
    out = dict(species=species, T_inj=T_inj, T_final_target=T_final, program=program, tau=tau, f_field=f_field,
               load=load, K=K, lock_frac=lock_frac, length_cwp=float(tr.xd), time_wp=float(tr.t),
               T_mean=Tm, T_rms_frac=float(np.sqrt(np.average((T[al] - Tm)**2, weights=w[al])) / Tm),
               captured=float(w[al].sum() / w.sum()), eff_wake_to_beam=float(gain / tr.laser_work),
               laser_work_per_area=float(tr.laser_work), beam_areal_weight=float(w.sum()),
               E_peak_inj=float(Epk0), mean_gradient_E0=float((Tm - T_inj) / ME / tr.xd),
               broken=bool(tr.broken), stalled=stalled, a0_inj=a0_of_beta(b0),
               a0_final=a0_of_beta(tr.beta_d), runtime_s=time.time() - t_start)
    if tag:
        np.save(os.path.join(ROOT, "results", "data", f"P1b_traj_{tag}.npy"), np.array(traj))
        out["trajectory_file"] = f"results/data/P1b_traj_{tag}.npy"
    if verbose:
        print(json.dumps(out, indent=1))
    return out, tr, np.array(traj)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--Tinj", type=float, default=100.0)
    ap.add_argument("--Tfinal", type=float, default=6000.0)
    ap.add_argument("--program", default="const")
    ap.add_argument("--f", type=float, default=0.7)
    ap.add_argument("--load", type=float, default=0.4)
    ap.add_argument("--lock", type=float, default=0.8)
    ap.add_argument("--tag", default=None)
    a = ap.parse_args()
    run(T_inj=a.Tinj, T_final=a.Tfinal, program=a.program, f_field=a.f, load=a.load,
        lock_frac=a.lock, tag=a.tag)
