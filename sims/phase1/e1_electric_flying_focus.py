"""E1: "electric flying focus" - the electric analogue of Mach-Batlle et al., PRL 125, 177204 (2020)
(active surface sources emulating a mu = -1 shell create the field of a *virtual* source in a region
where no source can be placed) applied to protons: ring electrodes around the beam bore, fired with
programmable timing, emulate a field source that moves with the protons at any (accelerating) speed.

Physics used (exact for a pattern moving rigidly at v = beta c in vacuum): fields depend on
xi = z - v t and the wave equation reduces to  laplace_perp(phi) + (1/gamma^2) d^2 phi/d xi^2 = 0,
i.e. Laplace's equation in the proton rest frame. Each axial Fourier mode k of the wall field is
transmitted to the axis with the factor 1 / I0(|k| a / gamma).

Part A  - Mach-Batlle replicator, electric version, inward: wall potential that reproduces, for
          r < r_v, the field of a virtual ring charge at radius r_v inside the bore (r_v -> 0 = point
          charge on axis). Required wall field vs truncation k_max (the paper's n_T): fidelity and
          cost (peak wall field / peak axis field; stored field energy).
Part B  - best possible axis/wall field ratio for any moving pattern (maximum principle) and the
          flat-top patterns that approach it, vs pattern length / (gamma a).
Part C  - proton tracking (6D, paraxial fields) through a ring-electrode array with programmable
          firing times: 1 -> 100 MeV, discrete electrodes, switch timing jitter, external focusing.
Part D  - energy bookkeeping: field energy that must be created per metre per shot vs the energy a
          space-charge-limited bunch can take out.
"""
import os, json, time, argparse
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e
from scipy.constants import c, e, epsilon_0, m_p

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
MP = m_p * c ** 2 / e / 1e6          # 938.27 MeV
ap = argparse.ArgumentParser()
ap.add_argument("--parts", default="ABCD")
ap.add_argument("--quick", action="store_true")
ap.add_argument("--T1", type=float, default=100.0)
ap.add_argument("--Np", type=int, default=2000)
ap.add_argument("--tag", default="")
args = ap.parse_args()
RES = {}


def I0(x):
    return i0e(x) * np.exp(np.abs(x))


# ----------------------------------------------------------------------------------------------
# Part A: electric Mach-Batlle replicator (proton-frame coordinates, lengths in units of a)
# ----------------------------------------------------------------------------------------------
def part_A():
    a = 1.0
    zeta = np.linspace(-6, 6, 2401)
    out = []
    for rv in [0.75, 0.5, 0.25, 0.1]:
        # exact target on axis: ring charge Q (4 pi eps0 = 1 units): Ez = z / (z^2 + rv^2)^1.5
        Ez_t = zeta / (zeta ** 2 + rv ** 2) ** 1.5
        for kmax in [2, 4, 8, 12, 16, 24, 32]:
            k = np.linspace(1e-4, kmax, 3000); dk = k[1] - k[0]
            # phi(r, z) = (2/pi) int cos(kz) I0(kr) K0(k rv) dk   for r < rv  (continued to r = a)
            Kr = k0e(k * rv) * np.exp(-k * rv)
            wA = (2 / np.pi) * Kr * dk                                # mode weights of axis potential
            CS = np.sin(np.outer(zeta, k))
            Ez_axis = (CS * (wA * k)).sum(1)                          # -d/dz of cos -> k sin
            Ez_wall = (CS * (wA * k * I0(k * a))).sum(1)
            m = np.abs(zeta) < 3 * rv + 0.5
            fid = float(np.sqrt(np.mean((Ez_axis[m] - Ez_t[m]) ** 2)) / np.abs(Ez_t).max())
            out.append(dict(r_v_over_a=rv, kmax_a=kmax, axis_peak=float(np.abs(Ez_axis).max()),
                            target_axis_peak=float(np.abs(Ez_t).max()), wall_peak=float(np.abs(Ez_wall).max()),
                            wall_over_axis=float(np.abs(Ez_wall).max() / np.abs(Ez_axis).max()),
                            rms_error_vs_target=fid))
            print(f"A rv={rv:.2f}a kmax={kmax:3d}/a: axis {np.abs(Ez_axis).max():9.3g} (target {np.abs(Ez_t).max():.3g}) "
                  f"wall/axis {out[-1]['wall_over_axis']:10.3g} err {fid:6.3f}")
    RES["A_replicator"] = out


# ----------------------------------------------------------------------------------------------
# Part B: axis/wall gain of flat-top moving patterns vs length (max principle: always <= 1)
# ----------------------------------------------------------------------------------------------
def axis_from_wall(Ew, dz, a_eff):
    k = 2 * np.pi * np.fft.rfftfreq(Ew.size, dz)
    F = np.fft.rfft(Ew) / I0(k * a_eff)
    return np.fft.irfft(F, Ew.size), k, F


def flat_top(xi, L, w):
    return 0.25 * (1 + np.tanh((xi + L) / w)) * (1 - np.tanh(xi / w))


def part_B():
    out = []
    xi = np.linspace(-60, 20, 8192); dz = xi[1] - xi[0]
    for L in [0.5, 1, 2, 4, 8, 16]:
        for w in [0.25, 1.0]:
            Ew = flat_top(xi, L, w)
            Ea, _, _ = axis_from_wall(Ew, dz, 1.0)              # lengths in units of gamma*a
            # bore field energy per unit length of pattern ~ int (Ez^2+Er^2) dV / (pi a^2 * L * Ew^2)
            out.append(dict(L_over_gamma_a=L, edge_over_gamma_a=w, axis_over_wall_peak=float(Ea.max()),
                            axis_voltage_over_wall_voltage=float(Ea.sum() / Ew.sum())))
            print(f"B L={L:5.2f} w={w:4.2f} (units gamma*a): axis/wall peak {Ea.max():.3f}")
    RES["B_flat_top"] = out


# ----------------------------------------------------------------------------------------------
# Part C: tracking through a programmable ring-electrode array
# ----------------------------------------------------------------------------------------------
P = dict(a=2e-3, pitch=2e-3, Ew=50e6, L=20e-3, w=10e-3, g_sync=0.85, T0=1.0, T1=args.T1,
         sigz=0.5e-3, sigT_rel=2e-3, sigr=0.3e-3, emit_n=1e-7, focus_over_defocus=3.0, Np=args.Np,
         Ew_lo=None, T_ramp=None)


def Ew_T(T, P):
    """Peak wall field as a function of the synchronous energy: constant, or ramped linearly from
    Ew_lo at T0 to Ew at T_ramp (programmable - lower gradient where the protons are slowest)."""
    if P.get("Ew_lo") is None:
        return P["Ew"] + 0 * np.asarray(T, float)
    f = np.clip((np.asarray(T, float) - P["T0"]) / (P["T_ramp"] - P["T0"]), 0, 1)
    return P["Ew_lo"] + (P["Ew"] - P["Ew_lo"]) * f


def window_fields(s, gam_s, t, jitter, P, N=1024):
    """Wall field from discrete electrodes (line j fires the pattern evaluated at its own centre,
    delayed by its timing error), axis field and its derivatives on a window around the pattern."""
    a, L, w, p = P["a"], P["L"], P["w"], P["pitch"]
    zg = s + np.linspace(-L - 8 * w, 6 * w, N, endpoint=False); dz = zg[1] - zg[0]
    j = np.floor(zg / p).astype(int)
    zc = (j + 0.5) * p
    dt_j = jitter[np.clip(j, 0, jitter.size - 1)]
    sj = s_of_t(t + dt_j)
    Tj = np.interp(t + dt_j, SYNC["t"], SYNC["T"])
    Ew = Ew_T(Tj, P) * flat_top(zc - sj, L, w)
    k = 2 * np.pi * np.fft.rfftfreq(N, dz)
    F = np.fft.rfft(Ew) / I0(k * a / gam_s)
    E0 = np.fft.irfft(F, N); E1 = np.fft.irfft(1j * k * F, N); E2 = np.fft.irfft(-k ** 2 * F, N)
    return zg, E0, E1, E2


SYNC = {}


def build_sync(P):
    """Synchronous trajectory for the continuous pattern: proton held at the front-edge point where
    the axis field is g_sync of the flat-top value (longitudinally stable side)."""
    a, L, w = P["a"], P["L"], P["w"]
    xi = np.linspace(-L - 8 * w, 6 * w, 4096); dz = xi[1] - xi[0]
    Ew = flat_top(xi, L, w)                                   # unit amplitude: shape only
    # gamma ~ 1.0-1.1 over 1-100 MeV: compute xi_s and E_s at gamma = 1 (conservative) and check
    Ea, _, _ = axis_from_wall(Ew, dz, a)
    Emax = Ea.max(); i = np.argmax(Ea)
    front = np.where((xi > xi[i]) & (Ea <= P["g_sync"] * Emax))[0][0]
    xi_s, ratio = xi[front], Ea[front]
    slope = -np.gradient(Ea, dz)[front]                        # -dEz/dxi at the synchronous point (unit amplitude)
    E_s = ratio * float(Ew_T(P["T0"], P)); Emax = Emax * float(Ew_T(P["T0"], P))
    ts, zs, Ts = [0.0], [0.0], [P["T0"]]
    t, z, T = 0.0, 0.0, P["T0"]
    while T < P["T1"] + 2:
        g = 1 + T / MP; v = c * np.sqrt(1 - 1 / g ** 2)
        dt = 2e-4 / v
        T += ratio * float(Ew_T(T, P)) * v * dt / 1e6; z += v * dt; t += dt
        ts.append(t); zs.append(z); Ts.append(T)
    SYNC.update(t=np.array(ts), z=np.array(zs), T=np.array(Ts), xi_s=xi_s, E_s=E_s, Emax_axis=Emax, ratio=ratio, slope=slope)


def s_of_t(t):
    return np.interp(t, SYNC["t"], SYNC["z"]) - SYNC["xi_s"]


def track(P, jitter_ps, seed=1, Ext_scale=None):
    rng = np.random.default_rng(seed)
    n_lines = int(SYNC["z"][-1] / P["pitch"]) + 400
    jitter = rng.normal(0, jitter_ps * 1e-12, n_lines)
    N = P["Np"]
    T0 = P["T0"] * (1 + P["sigT_rel"] * rng.standard_normal(N))
    g = 1 + T0 / MP; bg = np.sqrt(g ** 2 - 1)
    x = P["sigr"] * rng.standard_normal(N); y = P["sigr"] * rng.standard_normal(N)
    sig_th = P["emit_n"] / (bg.mean() * P["sigr"])
    pz = bg * m_p * c
    px = pz * sig_th * rng.standard_normal(N); py = pz * sig_th * rng.standard_normal(N)
    z = s_of_t(0.0) + SYNC["xi_s"] + P["sigz"] * rng.standard_normal(N)   # on the synchronous point
    t = 0.0; alive = np.ones(N, bool); hist = []
    z_end = SYNC["z"][-1] - 0.05
    step = 0; Kdef_ref = []
    while True:
        Ts = np.interp(t, SYNC["t"], SYNC["T"]); gs = 1 + Ts / MP; vs = c * np.sqrt(1 - 1 / gs ** 2)
        s = s_of_t(t)
        if s + SYNC["xi_s"] > z_end:
            break
        dt = 1e-4 / vs
        zg, E0, E1, E2 = window_fields(s, gs, t, jitter, P)
        zi = np.clip(z, zg[0], zg[-1])
        e0 = np.interp(zi, zg, E0); e1 = np.interp(zi, zg, E1); e2 = np.interp(zi, zg, E2)
        r2 = x ** 2 + y ** 2
        gam = np.sqrt(1 + (px ** 2 + py ** 2 + pz ** 2) / (m_p * c) ** 2)
        Fz = e * (e0 - r2 / (4 * gam ** 2) * e2)
        kdef = e * e1 / (2 * gam ** 4)                          # radial force per unit r (co-moving)
        # external focusing (smooth approximation of a quadrupole/solenoid lattice), set to a multiple
        # of the defocusing at the synchronous point
        # defocusing of the smooth (continuous) pattern at the synchronous point: the external lattice
        # is programmed to this, not to electrode-to-electrode spikes
        Kdef_s = e * SYNC["slope"] * float(Ew_T(Ts, P)) / (2 * gs ** 4)
        Kext = P["focus_over_defocus"] * Kdef_s if Ext_scale is None else Ext_scale
        Kdef_ref.append((Ts, Kdef_s, Kext))
        Fx = (-kdef - Kext) * x; Fy = (-kdef - Kext) * y
        px += Fx * dt; py += Fy * dt; pz += Fz * dt
        gam = np.sqrt(1 + (px ** 2 + py ** 2 + pz ** 2) / (m_p * c) ** 2)
        x += px / (gam * m_p) * dt; y += py / (gam * m_p) * dt; z += pz / (gam * m_p) * dt
        t += dt
        alive &= (x ** 2 + y ** 2) < P["a"] ** 2
        if step % 2000 == 0:
            T = (gam - 1) * MP
            cap = alive & (np.abs(T - Ts) < 0.05 * Ts)
            hist.append(dict(z_m=float(s + SYNC["xi_s"]), T_sync=float(Ts), frac_captured=float(cap.mean()),
                             T_mean_cap=float(T[cap].mean()) if cap.any() else None,
                             T_std_cap=float(T[cap].std()) if cap.any() else None,
                             r_rms_mm=float(np.sqrt(np.mean(r2[alive])) * 1e3) if alive.any() else None))
        step += 1
    gam = np.sqrt(1 + (px ** 2 + py ** 2 + pz ** 2) / (m_p * c) ** 2)
    T = (gam - 1) * MP
    Tsf = float(np.interp(t, SYNC["t"], SYNC["T"]))
    cap = alive & (np.abs(T - Tsf) < 0.05 * Tsf)
    K = np.array(Kdef_ref)
    gK = 1 + K[:, 0] / MP; vK = c * np.sqrt(1 - 1 / gK ** 2)
    B_sol = np.sqrt(4 * gK * m_p * K[:, 2]) / e; G_q = K[:, 2] / (e * vK)
    return dict(jitter_ps=jitter_ps, length_m=float(s + SYNC["xi_s"]), T_sync_final=Tsf,
                frac_captured=float(cap.mean()), frac_lost_to_wall=float(1 - alive.mean()),
                T_mean_captured=float(T[cap].mean()) if cap.any() else None,
                T_rel_std_captured=float(T[cap].std() / T[cap].mean()) if cap.any() else None,
                r_rms_final_mm=float(np.sqrt(np.mean((x ** 2 + y ** 2)[alive])) * 1e3) if alive.any() else None,
                Kdef_at_1MeV=float(K[0, 1]), Kdef_at_end=float(K[-1, 1]), steps=step,
                B_sol_max_T=float(B_sol.max()), T_at_B_sol_max=float(K[np.argmax(B_sol), 0]),
                G_quad_max_Tpm=float(G_q.max()), T_at_G_quad_max=float(K[np.argmax(G_q), 0]), history=hist)


def part_C():
    build_sync(P)
    print(f"C sync: xi_s={SYNC['xi_s']*1e3:.2f} mm, E_s={SYNC['E_s']/1e6:.1f} MV/m (axis max {SYNC['Emax_axis']/1e6:.1f}, wall {P['Ew']/1e6:.0f}), "
          f"length to {P['T1']} MeV = {np.interp(P['T1'], SYNC['T'], SYNC['z']):.2f} m")
    runs = []
    for jit in ([0.0, 5.0] if args.quick else [0.0, 2.0, 10.0, 30.0]):
        t0 = time.time()
        r = track(P, jit)
        # equivalent external-focusing hardware at the start (1 MeV): solenoid B and quad gradient
        g = 1 + P["T0"] / MP; v = c * np.sqrt(1 - 1 / g ** 2)
        Kext0 = P["focus_over_defocus"] * r["Kdef_at_1MeV"]
        r["solenoid_T_equiv_at_1MeV"] = float(np.sqrt(4 * g * m_p * Kext0) / e)
        r["quad_gradient_Tpm_smooth_equiv_at_1MeV"] = float(Kext0 / (e * v))
        print(f"C jitter {jit:5.1f} ps: captured {r['frac_captured']:.3f} at {r['T_mean_captured']} MeV "
              f"(rel std {r['T_rel_std_captured']}), lost {r['frac_lost_to_wall']:.3f}, L={r['length_m']:.2f} m, "
              f"B_sol(1 MeV) = {r['solenoid_T_equiv_at_1MeV']:.1f} T ({time.time()-t0:.0f}s)")
        runs.append(r)
    r0 = track(P, 0.0, Ext_scale=0.0)
    print(f"C no external focusing: captured {r0['frac_captured']:.3f}, lost to wall {r0['frac_lost_to_wall']:.3f}")
    r0["note"] = "no external focusing (Earnshaw/Panofsky: the longitudinally stable edge defocuses)"
    runs.append(r0)
    RES["C_tracking"] = dict(params=P, sync=dict(xi_s_mm=float(SYNC["xi_s"] * 1e3), E_s_MVm=float(SYNC["E_s"] / 1e6),
                                                 E_axis_max_MVm=float(SYNC["Emax_axis"] / 1e6)), runs=runs)


# ----------------------------------------------------------------------------------------------
# Part D: energy per shot vs energy taken by a space-charge-limited bunch  [estimate on sim fields]
# ----------------------------------------------------------------------------------------------
def bore_energy_per_m(P, gam=1.0):
    """Electric field energy in the bore per metre of energised length (flat-top part), from the
    spectral solution (Ez, Er on an (r, z) grid)."""
    a, L, w = P["a"], P["L"], P["w"]
    N = 4096
    xi = np.linspace(-L - 8 * w, 6 * w, N, endpoint=False); dz = xi[1] - xi[0]
    Ew = P["Ew"] * flat_top(xi, L, w)
    k = 2 * np.pi * np.fft.rfftfreq(N, dz); ka = k * a / gam
    F = np.fft.rfft(Ew)
    U = 0.0
    rr = np.linspace(0, a, 41)[:-1] + a / 80
    for r in rr:
        Ez = np.fft.irfft(F * I0(k * r / gam) / I0(ka), N)
        with np.errstate(invalid="ignore", divide="ignore"):
            ratio = np.where(k > 0, (i1e(k * r / gam) / i0e(ka)) * np.exp(np.abs(k * r / gam) - np.abs(ka)), 0.0)
        Er = np.fft.irfft(-1j * F * ratio / gam, N)             # Er from phi_k = i Ez_k / k
        U += np.sum(0.5 * epsilon_0 * (Ez ** 2 + Er ** 2)) * dz * 2 * np.pi * r * (a / 40)
    L_eff = np.sum(flat_top(xi, L, w) ** 2) * dz
    return U / L_eff


def part_D():
    out = {}
    Ub = bore_energy_per_m(P)
    # insulator / driver region: DWA-like high-gradient insulator annulus (eps_r 5, 5 mm thick) at the
    # wall field, or vacuum-gap ring electrodes (fringe field ~ bore field over ~a beyond the wall)
    t_ins, eps_r = 5e-3, 5.0
    U_ins = 0.5 * eps_r * epsilon_0 * P["Ew"] ** 2 * np.pi * ((P["a"] + t_ins) ** 2 - P["a"] ** 2)
    U_vac = 0.5 * epsilon_0 * P["Ew"] ** 2 * np.pi * ((2 * P["a"]) ** 2 - P["a"] ** 2)
    out["U_bore_J_per_m"] = Ub; out["U_DWA_insulator_J_per_m"] = U_ins; out["U_vacuum_gap_fringe_J_per_m"] = U_vac
    E_s = SYNC["E_s"] if SYNC else 0.8 * P["Ew"]
    rows = []
    for T in [1, 10, 100, 1000, 6000]:
        g = 1 + T / MP; b = np.sqrt(1 - 1 / g ** 2); v = b * c
        # space-charge limit: transverse space-charge force constant of a uniform bunch (radius r_b,
        # length l_b) must stay below half the external focusing; external focusing = PMQ lattice with
        # smooth-equivalent gradient 100 T/m (assumption) or the 3x-defocusing value of Part C
        r_b, l_b = 0.5e-3, 3e-3
        K_ext = e * v * 100.0
        lam_max = 0.5 * K_ext * 2 * np.pi * epsilon_0 * r_b ** 2 * g ** 2 / e      # K_sc = e lam/(2 pi eps0 r_b^2 g^2)
        Q = lam_max * l_b
        for tag, U in [("DWA_insulator", Ub + U_ins), ("vacuum_gap_rings", Ub + U_vac)]:
            eta_raw = Q * E_s / U
            eta = min(eta_raw, 0.5)          # cannot take more than ~half the stored field without large droop
            # optional recovery of the unused field energy back into the pulsed-power store (assumed 80 %)
            eta_rec = eta / (1 - 0.8 * (1 - eta))
            rows.append(dict(T_MeV=T, design=tag, Q_max_nC=float(Q * 1e9), U_J_per_m=float(U),
                             loading_raw=float(eta_raw), beam_loading_eta=float(eta),
                             limited_by="beam loading" if eta_raw > 0.5 else "space charge",
                             wallplug_no_recovery=float(0.7 * eta), wallplug_80pct_recovery=float(0.7 * eta_rec)))
            print(f"D T={T:5d} MeV {tag:17s}: Q_max {Q*1e9:7.3f} nC, U {U:6.2f} J/m, field->beam {eta:.2e}, wall-plug {0.7*eta:.2e} / with recovery {0.7*eta_rec:.2e}")
    out["rows"] = rows
    RES["D_energy"] = out


def part_S():
    """How short can 1 -> 100 MeV be? Gradient scan with the same geometry, a longer flat-top, and a
    programmable gradient ramp. Efficiency estimate: field energy per energised metre scales as
    Ew^2 (0.56 J/m at 50 MV/m, vacuum-gap rings, Part D), beam takes Q * dV with the space-charge
    limited Q at 1 MeV (29 pC, Part D)."""
    global P
    base = dict(P)
    cases = [("50 MV/m (S046 baseline)", dict()),
             ("50 MV/m, 40 mm flat-top, sync at 0.92", dict(L=40e-3, g_sync=0.92)),
             ("100 MV/m", dict(Ew=100e6)),
             ("200 MV/m", dict(Ew=200e6)),
             ("200 MV/m, 40 mm flat-top, sync at 0.92", dict(Ew=200e6, L=40e-3, g_sync=0.92)),
             ("ramp 50 -> 200 MV/m by 20 MeV", dict(Ew=200e6, Ew_lo=50e6, T_ramp=20.0)),
             ("ramp 50 -> 200 MV/m by 20 MeV, 20 mm edges", dict(Ew=200e6, Ew_lo=50e6, T_ramp=20.0, w=20e-3, L=40e-3))]
    out = []
    Q = 29e-12
    for name, upd in cases:
        P = dict(base); P.update(upd)
        SYNC.clear(); build_sync(P)
        t0 = time.time(); r = track(P, 10.0)
        zz = SYNC["z"]; TT = SYNC["T"]; m = TT <= P["T1"]
        U = np.trapezoid(0.56 * (Ew_T(TT[m], P) / 50e6) ** 2, zz[m])
        eta = Q * (P["T1"] - P["T0"]) * 1e6 / U
        L_ = float(np.interp(P["T1"], TT, zz))
        out.append(dict(case=name, params={k: v for k, v in upd.items()}, length_m=L_,
                        mean_gradient_MVm=float((P["T1"] - P["T0"]) / L_),
                        frac_captured=r["frac_captured"], T_rel_std=r["T_rel_std_captured"],
                        lost_to_wall=r["frac_lost_to_wall"], B_sol_max_T=r["B_sol_max_T"], T_at_B_max=r["T_at_B_sol_max"],
                        G_quad_max_Tpm=r["G_quad_max_Tpm"], T_at_G_max=r["T_at_G_quad_max"],
                        field_energy_per_shot_J=float(U), field_to_beam=float(eta), wallplug_70pct=float(0.7 * eta)))
        o = out[-1]
        print(f"S {name:45s}: L={L_:.2f} m (<G>={o['mean_gradient_MVm']:.0f} MV/m) captured {o['frac_captured']:.2f} "
              f"dT/T {o['T_rel_std']} | focusing max {o['B_sol_max_T']:.1f} T sol / {o['G_quad_max_Tpm']:.0f} T/m quad "
              f"(at {o['T_at_G_max']:.0f} MeV) | field energy {U:.2f} J/shot, wall-plug {100*o['wallplug_70pct']:.3f} % ({time.time()-t0:.0f}s)")
    P = base
    RES["S_shorter"] = out


if "S" in args.parts:
    part_S()
    json.dump(RES, open(os.path.join(ROOT, "results", "data", "E1_shorter_scan.json"), "w"), indent=1)
    raise SystemExit
if "A" in args.parts:
    part_A()
if "B" in args.parts:
    part_B()
if "C" in args.parts:
    part_C()
if "D" in args.parts:
    if not SYNC:
        build_sync(P)
    part_D()
json.dump(RES, open(os.path.join(ROOT, "results", "data", f"E1_electric_flying_focus{args.tag}.json"), "w"), indent=1)
