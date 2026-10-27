"""Design calculator: assembles complete ~6 GeV proton accelerator designs from
(a) SIMULATED quantities (1D PIC / fluid tracker / optics results in results/data, IDs S###),
(b) ESTIMATED / LITERATURE coupling and technology factors (explicitly sourced below).
Every output number carries a provenance tag: 'sim', 'est' or 'lit'.

Efficiency chain (wall-plug -> 6 GeV protons):
   eta_total = E_beam / (E_injector_wall + E_LWFA_wall)
   E_LWFA_wall per proton = dT_LWFA / (eta_laser * eta_couple * eta_lw * eta_wb * f_3D)
where eta_wb  = wake->beam (sim, 1D), eta_lw = laser->wake (sim energy accounting or lit),
      eta_couple = coupling of the laser into the plasma structure (lit/est),
      f_3D = multi-D correction on the 1D beam-loading efficiency (sim when available, else est).
"""
import os, json
import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
D = os.path.join(ROOT, "results", "data")


def load(name):
    p = os.path.join(D, name)
    return json.load(open(p)) if os.path.exists(p) else None


# ----------------------------------------------------------------- technology table (lit)
LASERS = {
    "TiSa": dict(eta=0.001, cost_per_W=(33e3, 250e3), src="lit: research notes Sec. 4.6 (<=0.1 % wall-plug; kBELLA ~$33k/W facility, BELLA ~$250k/W)"),
    "fibre_today": dict(eta=0.20, cost_per_W=(1e3, 10e3), src="lit/est: ultrafast Yb fibre ~25 % (Snowmass WP), system-level 20 % assumed; today's $/W est."),
    "fibre_projected": dict(eta=0.40, cost_per_W=(20, 115), src="lit: ICAN >30 %, Snowmass 50 %; ITF collider projection $20-115/W"),
    "TmYLF_projected": dict(eta=0.20, cost_per_W=(100, 1000), src="lit: LLNL BAT 20 % projected wall-plug; cost est."),
}
RF_INJECTOR = dict(eta=0.15, src="lit: PSI HIPA 18.3 % accelerator-only, SNS ~9 %; 15 % assumed for a ~1 GeV proton injector",
                   cost=(0.3e9, 1.0e9), length_m=(30, 300))


def pick(rows, **kw):
    for r in rows or []:
        if all(abs(r.get(k, -1) - v) < 1e-6 if isinstance(v, float) else r.get(k) == v for k, v in kw.items()):
            return r
    return None


def designs(f3D_train=None):
    out = {}
    MP = 938.272
    # --- simulated inputs ---------------------------------------------------------
    b3 = load("B3_conventional_protons_loaded.json")
    p1b = load("P1b_scan.json")
    p1d = load("P1d_scan.json")
    p2b = load("P2b_joint_opt_free.json")
    p1f = load("P1f_single_v2.json")
    # ---------------------------------------------------------------- D0 conventional
    # staged conventional LWFA, each stage ends at proton dephasing (B3), each driven by a
    # fresh guided pulse; laser->wake coupling per stage = L_stage / L_pd.
    L_pd_1e18 = 4950 * (41.7 / 20) ** 2      # sim S002 (k0/kp=20) scaled with (k0/kp)^2 -> 0.8 um, 1e18
    for Tinj, Lstage in [(100.0, 2 * np.pi / (2 * (1 - 0.428))), (1000.0, 2 * np.pi / (2 * (1 - 0.875)))]:
        r = pick(b3, gamma_p=41.7, T_inj=Tinj)
        eta_wb = r["eff"]
        gain = r["mean_gain_MeV"]
        eta_lw = Lstage / L_pd_1e18
        n_st = (6000 - Tinj) / max(gain, 1e-9)
        for las in ["TiSa", "fibre_projected"]:
            eta_l = LASERS[las]["eta"]
            e_lwfa = (6000 - Tinj) / (eta_l * eta_lw * eta_wb)
            e_inj = Tinj / RF_INJECTOR["eta"]
            out[f"D0_conventional_staged_inj{int(Tinj)}_{las}"] = dict(
                description=f"Conventional LWFA (group-velocity wake), staged at every proton dephasing, RF injector {Tinj:.0f} MeV, {las}",
                eta_wb=(eta_wb, "sim B3/S021"), eta_lw=(eta_lw, "sim S002+B3 (L_stage/L_pd)"),
                eta_laser=(eta_l, "lit"), stages=(n_st, "sim"), gain_per_stage_MeV=(gain, "sim"),
                eta_total=6000 / (e_lwfa + e_inj), eta_LWFA_part=(6000 - Tinj) / e_lwfa)
    # ---------------------------------------------------------------- D1 free-space FF
    r = pick(p1b, T_inj=1000.0, program="const", load=0.5)
    eta_wb = r["eff_wake_to_beam"]
    eta_wb_opt = None
    if p2b:
        eta_wb_opt = [s for s in p2b if abs(s["T"] - 1000) < 1][0]["optimised"]["eta"]
    for eta_lw in [0.01, 0.03]:
        for las in ["TiSa", "fibre_projected"]:
            eta_l = LASERS[las]["eta"]
            e_lwfa = 5000 / (eta_l * eta_lw * eta_wb * 0.6)
            out[f"D1_freespace_FF_lw{eta_lw}_{las}"] = dict(
                description="Velocity-matched free-space (on-axis) flying focus, 1->6 GeV, RF injector to 1 GeV",
                eta_wb=(eta_wb, "sim S015 (1D)"), eta_wb_jointopt=(eta_wb_opt, "sim S016 (1D)"),
                eta_lw=(eta_lw, "est (each focal zone used once; Palastro 2020/Shaw 2025 give <~1-5 %)"),
                f_3D=(0.6, "est"), eta_laser=(eta_l, "lit"),
                eta_total=6000 / (e_lwfa + 1000 / RF_INJECTOR["eta"]),
                note="free-space FF limited to beta >~ 0.9 by drive smearing (Gong 2024; P1e)")
    # ---------------------------------------------------------------- D2 guided resonant train
    if p1f:
        eta_wb_tr = p1f["eff_wake_to_beam"]
        Wp = p1f["work_during_acc"] / p1f["L_acc"]          # 1D laser work per unit length
        U0 = p1f["U0"]
        k0kp_run = p1f["k0_over_kp"]
        grad = (p1f["T_final"] - p1f["T_inj"]) / 0.511 / p1f["L_acc"]
        for k0kp in [20.0, 28.5, 40.0]:
            L_pd = U0 / Wp * (k0kp / k0kp_run) ** 2
            L_need = 5000 / 0.511 / grad
            eta_lw = 1 - np.exp(-L_need / L_pd)
            for las in ["fibre_today", "fibre_projected"]:
                eta_l = LASERS[las]["eta"]
                f3 = f3D_train if f3D_train else 0.6
                eta_couple = 0.64 * 0.97
                e_lwfa = 5000 / (eta_l * eta_couple * eta_lw * eta_wb_tr * f3)
                out[f"D2_guided_train_k0kp{int(k0kp)}_{las}"] = dict(
                    description="Guided resonant flying-focus train (N=3 fibre lines in LG_0,3,6 channel modes), channel-width taper, 1->6 GeV, RF injector to 1 GeV",
                    eta_wb=(eta_wb_tr, "sim P1f single-bunch v2 (1D PIC)"),
                    eta_wb_jointopt=(eta_wb_opt, "sim S016 (1D) upper bound"),
                    eta_lw=(float(eta_lw), f"sim energy accounting (P1f): L_pd={L_pd:.0f} c/wp, L_stage={L_need:.0f} c/wp"),
                    eta_couple=(eta_couple, "lit: Ross 2024 coupling 64 % x channel-forming overhead 3 %"),
                    f_3D=(f3, "sim FBPIC" if f3D_train else "est (pending FBPIC)"),
                    eta_laser=(eta_l, "lit"),
                    eta_LWFA_part=5000 / e_lwfa,
                    eta_total=6000 / (e_lwfa + 1000 / RF_INJECTOR["eta"]))
    # ---------------------------------------------------------------- D3 all-optical
    if p1d:
        r_np = [r for r in p1d if r["n_np"] > 0][0]
        r_0 = [r for r in p1d if r["n_np"] == 0 and abs(r["alpha_frac"] - 0.5) < 1e-6][0]
        for tag, eta_emb in [("TFF_lit", 1.3e-3 / 0.286), ("TPA_lit", 1.3e-5 / 0.286)]:
            # literature total laser->proton efficiencies (Gong 2024: 0.13 %, Nutting 2026: ~1e-5)
            # divided by our 1D wake->proton efficiency to get an embodiment coupling factor.
            for npl, r in [("noNP", r_0), ("NP", r_np)]:
                eta_low = r["eff_laser_to_trapped"] * eta_emb
                eta_l = LASERS["fibre_projected"]["eta"]
                e_low = 1000 / (eta_l * eta_low)
                d2 = out.get("D2_guided_train_k0kp28_fibre_projected")
                e_high = 5000 / (d2["eta_LWFA_part"] * eta_l) * eta_l if d2 else np.inf
                e_high = 5000 / d2["eta_LWFA_part"] if d2 else np.inf
                out[f"D3_alloptical_{tag}_{npl}"] = dict(
                    description="All-optical: self-injection from rest by slow accelerating side-pumped driver (0->1 GeV) + guided train (1->6 GeV)",
                    eta_low_1D=(r["eff_laser_to_trapped"], "sim S018 (1D, prescribed driver)"),
                    embodiment_factor=(eta_emb, "lit: Gong 2024 / Nutting 2026 normalised by 1D"),
                    eta_total=6000 / (e_low + e_high))
    # ---------------------------------------------------------------- D4 near-critical RPA
    out["D4_nearcritical_RPA_lit"] = dict(
        description="Ultra-intense near-critical schemes (RPA + wake / light-spring), single multi-PW Ti:Sa laser",
        eta_laser_to_proton=(0.06, "lit: Liu 2018 (6 %), Guo 2024 (11 %) 2D/3D PIC; not simulated here"),
        eta_total=0.06 * LASERS["TiSa"]["eta"],
        eta_total_if_efficient_PW_laser=0.06 * 0.2)
    out["RF_reference"] = dict(description="Conventional RF proton accelerator to 6 GeV (SC linac / RCS)",
                               eta_total=0.15, src="lit: PSI 18 %, SNS ~9 %")
    return out


if __name__ == "__main__":
    import sys
    f3 = float(sys.argv[1]) if len(sys.argv) > 1 else None
    res = designs(f3)
    json.dump(res, open(os.path.join(D, "design_calc.json"), "w"), indent=1, default=float)
    for k, v in sorted(res.items(), key=lambda kv: -kv[1]["eta_total"]):
        print(f"{v['eta_total']:10.3e}  {k}")


# --------------------------------------------------------------------- physical sheet
def d2_physical_sheet(f3D=0.6, eta_wb=0.585, eta_lw=0.5, eta_couple=0.62, grad_E0=0.3,
                      load_areal=0.2, kpW_beam_frac=0.4, P_beam_W=1e6):
    """Estimate-level physical design of D2 (RF injector to 1 GeV + 3 guided resonant-train
    stages). Uses simulated 1D ratios (gradient in E0 units, areal beam loading, efficiencies)
    and the rigid-comb optics designs (P1e: density, W per stage)."""
    import plasma as PL
    stages = [  # (T_in, T_out, n0 [cm^-3], W [m]) from P1e designs (lambda = 1 um)
        (1000, 2000, 3.09e18, 6.83e-6),
        (2000, 3500, 1.16e18, 11.1e-6),
        (3500, 6000, 6.0e17, 12.6e-6),
    ]
    rows, Ltot, Nps = [], 0.0, []
    for T_in, T_out, n, W in stages:
        nm = n * 1e6
        E0 = PL.E0(nm)
        G = grad_E0 * E0
        L = (T_out - T_in) * 1e6 / G
        cwp = 1 / PL.k_p(nm)
        A = np.pi * (kpW_beam_frac * W) ** 2
        Np = load_areal * nm * cwp * A
        rows.append(dict(T_in=T_in, T_out=T_out, n0_cm3=n, W_um=W * 1e6, gradient_GVm=G / 1e9,
                         length_cm=L * 100, protons_per_bunch=Np))
        Ltot += L
        Nps.append(Np)
    Np = min(Nps)                                  # charge limited by the narrowest stage
    E_beam_shot = Np * 5.0e9 * PL.e                # J gained in the LWFA (1 -> 6 GeV)
    eta_opt = eta_couple * eta_lw * eta_wb * f3D   # laser (at plasma entrance) -> beam
    E_laser_shot = E_beam_shot / eta_opt
    rep = P_beam_W / (Np * 6.0e9 * PL.e)
    sheet = dict(stages=rows, plasma_length_cm=Ltot * 100, protons_per_shot=Np,
                 charge_pC=Np * PL.e * 1e12, laser_energy_per_shot_J=E_laser_shot,
                 laser_to_beam_efficiency=eta_opt, rep_rate_Hz_for_1MW=rep,
                 laser_average_power_MW=E_laser_shot * rep / 1e6,
                 assumptions=dict(f3D=f3D, eta_wb=eta_wb, eta_lw=eta_lw, eta_couple=eta_couple,
                                  gradient_E0=grad_E0, load_areal=load_areal,
                                  beam_radius_over_W=kpW_beam_frac))
    for las in ["fibre_today", "fibre_projected"]:
        L_ = LASERS[las]
        P_wall = sheet["laser_average_power_MW"] / L_["eta"] + 1e6 * (1.0 / 6.0) / RF_INJECTOR["eta"] / 1e6
        sheet[f"wall_plug_MW_{las}"] = P_wall
        sheet[f"laser_cost_USD_{las}"] = [sheet["laser_average_power_MW"] * 1e6 * c for c in L_["cost_per_W"]]
    return sheet


if __name__ == "__main__" and False:
    pass
