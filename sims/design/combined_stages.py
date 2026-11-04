"""S049: combined staged accelerator - (1) can anything make the surface plasmon (SP) work for slow
protons? best on-axis/wall field of a proton-matched SP for any channel radius (S040 dispersion);
(2) how low in speed does the hollow channel's slow light keep the laser pulse with the protons?
(beat speed matched to the protons; LP01 group velocity of the pulse); (3) efficiency of staged
combinations [estimates on simulated ratios; SP efficiency is a scenario range, not simulated]."""
import os, sys, json
import numpy as np
from scipy.special import jv, kv as Kv
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, HERE)
import design_calc as d
src = open(os.path.join(ROOT, "sims", "phase1", "p1h_surface_plasmon_dispersion.py"), encoding="utf-8").read().split("rows = []")[0]
ns = {"__file__": os.path.join(ROOT, "sims", "phase1", "p1h_surface_plasmon_dispersion.py")}; exec(src, ns); matched = ns["matched"]
MP = 938.272
out = {"best_axis_over_wall": [], "slow_light_match": [], "staged": []}
for T in [10, 30, 100, 300, 1000, 3000]:
    g = 1 + T / MP; b = np.sqrt(1 - 1 / g ** 2); best = None
    for R in np.geomspace(0.05, 30, 120):
        m = matched(b, R)
        if m and (best is None or m["onaxis_over_wall"] > best[1]):
            best = (R, m["onaxis_over_wall"])
    out["best_axis_over_wall"].append(dict(T_MeV=T, beta=b, R_cwp=best[0], axis_over_wall=best[1]))
    print(f"T={T:5d} MeV: best SP axis/wall {best[1]:.3g} (R={best[0]:.2f} c/wp)")


def u01(V):
    f = lambda u: u * jv(1, u) / jv(0, u) - np.sqrt(V * V - u * u) * Kv(1, np.sqrt(V * V - u * u)) / Kv(0, np.sqrt(V * V - u * u))
    return brentq(f, 1e-6, min(V, 2.4048) - 1e-9)


for T in [300, 1000, 3000]:
    g = 1 + T / MP; b = np.sqrt(1 - 1 / g ** 2); sols = []
    for R in np.linspace(1.2, 4, 57):
        m = matched(b, R)
        if not m:
            continue
        wsp = m["w_over_wp"]; u = u01(R)
        beat = lambda wr: wsp / (np.sqrt(wr ** 2 - (u / R) ** 2) - np.sqrt((wr - wsp) ** 2 - (u / R) ** 2))
        wrs = np.linspace(wsp + u / R + 0.05, 8, 400); bs = np.array([beat(w) for w in wrs])
        for j in np.where(np.diff(np.sign(bs - b)))[0]:
            sols.append((R, wrs[j], wsp, np.sqrt(1 - (u / (R * wrs[j])) ** 2), m["onaxis_over_wall"]))
    if sols:
        s = sorted(sols, key=lambda x: abs(x[3] - b))[0]
        out["slow_light_match"].append(dict(T_MeV=T, beta=b, R_cwp=s[0], w_laser_over_wp=s[1], w_sp=s[2], pulse_speed=s[3],
                                            slip_per_length=(1 / b - 1 / s[3]), axis_over_wall=s[4]))
        print(f"T={T} MeV beta={b:.3f}: pulse speed {s[3]:.3f} (w/wp={s[1]:.2f})")
    else:
        out["slow_light_match"].append(dict(T_MeV=T, beta=b, match=None)); print(f"T={T} MeV: no two-colour fundamental-mode match")
eL = {"today": d.LASERS["fibre_today"]["eta"], "projected": d.LASERS["fibre_projected"]["eta"]}
pv, _ = d.pv_recovery_factor(eL["projected"], 0.62 * (1 - 0.64), 0.23, 1 - 0.62)
for las, e in eL.items():
    tr = e * 0.62 * 0.64 * 0.25 * 0.62                     # guided train, S038/S041 inputs
    for sp_name, sp in [("SP = train (0.25 wake->beam)", tr), ("SP without slippage loss (0.585, S024 rigid envelope)", e * 0.62 * 0.64 * 0.585 * 0.62)]:
        for front, Tf, ef in [("RF linac 15 % to 0.5 GeV", 0.5, 0.15), ("electric flying focus to 0.5 GeV, no recovery (0.23 %)", 0.5, 0.0023),
                              ("electric flying focus to 0.5 GeV, 80 % recovery (0.6 %)", 0.5, 0.006), ("RF linac 15 % to 1.5 GeV (no train)", 1.5, 0.15)]:
            low = Tf / ef; mid = max(1.5 - Tf, 0) / tr; hi = 4.5 / sp
            row = dict(laser=las, front_end=front, sp_scenario=sp_name, eff=6 / (low + mid + hi),
                       eff_with_PV=6 / (low + (mid + hi) / pv), GeV_wall_per_muon=((low + mid + hi) / 0.9, (low + mid + hi) / 0.5))
            out["staged"].append(row)
            print(f"{las:9s} {front:55s} {sp_name[:22]:22s} {100*row['eff']:.2f} % ({100*row['eff_with_PV']:.2f} % with PV)")
json.dump(out, open(os.path.join(ROOT, "results", "data", "combined_stages.json"), "w"), indent=1)

# ---- (4) per-section efficiencies, energy-bill shares, and PV recovery of the leftover light ----
chain = 0.62 * 0.64 * 0.62            # coupling into channel x laser->wake x f3D (S041 inputs); x wake->beam below
f_left = (1 - 0.62) + 0.62 * (1 - 0.64)   # laser light not used: never coupled + leaves the plasma
out["sections"] = {}
for las, e in eL.items():
    sec = {"RF linac [lit]": 0.15, "electric flying focus, no recovery [est on sim S046/S047]": 0.0023,
           "electric flying focus, 80 % recovery [est]": 0.006,
           "laser slow section (self-injection, TFF) [est on sim S041]": e * 0.0033786,
           "guided train [est on sim S038/S043]": e * chain * 0.25,
           "surface plasmon, low scenario": e * chain * 0.25, "surface plasmon, high scenario": e * chain * 0.585}
    rows = {}
    for name, eta in sec.items():
        laser = "RF" not in name and "electric" not in name
        L = 1 / (eta / e) if laser else 0.0             # laser energy per unit beam energy
        pv69 = 1 / (1 / eta - f_left * 0.69 * L) if laser else eta
        rows[name] = dict(eff=eta, eff_PV_realistic=eta * (pv if laser else 1), eff_PV_69pct_all_leftover=pv69)
    out["sections"][las] = rows
    print(f"\n{las}: leftover light {100*f_left:.0f} % of the laser energy")
    for k, v in rows.items():
        print(f"  {k:62s} {100*v['eff']:6.3f} %  PV(S039) {100*v['eff_PV_realistic']:6.3f} %  PV 69% all {100*v['eff_PV_69pct_all_leftover']:6.3f} %")
    # staged machine with 69 % PV on all leftover light, and energy-bill shares
    S = rows
    for front, Tf, key in [("electric FF (no recovery)", 0.5, "electric flying focus, no recovery [est on sim S046/S047]"),
                           ("electric FF (80 % recovery)", 0.5, "electric flying focus, 80 % recovery [est]"), ("RF", 0.5, "RF linac [lit]")]:
        for spk in ["surface plasmon, low scenario", "surface plasmon, high scenario"]:
            for pvk in ["eff", "eff_PV_realistic", "eff_PV_69pct_all_leftover"]:
                parts = [Tf / S[key][pvk], 1.0 / S["guided train [est on sim S038/S043]"][pvk], 4.5 / S[spk][pvk]]
                tot = sum(parts)
                out["staged"].append(dict(laser=las, front_end=front, sp_scenario=spk, pv=pvk, eff=6 / tot,
                                          shares=[p_ / tot for p_ in parts]))
                print(f"  {front:28s} {spk[17:]:15s} {pvk:26s} system {100*6/tot:5.2f} %  bill shares slow/train/SP = "
                      + "/".join(f"{100*p_/tot:.0f}" for p_ in parts))
json.dump(out, open(os.path.join(ROOT, "results", "data", "combined_stages.json"), "w"), indent=1)

# ---- (5) surface-plasmon efficiency MEASURED (S053, beam-loaded FBPIC, 1 pC, 0.65 mm) ----
sp_meas = json.load(open(os.path.join(ROOT, "sims", "phase2", "fbpic_sp_loaded_out", "summary.json")))
U0 = sp_meas["design"]["U_laser_expected_mJ"]; last = sp_meas["snaps"][-1]
dU_beam = (last["T_mean"] - 3000.0) * 1e6 * 1e-12 * 1e3               # mJ  (1 pC x mean gain)
dU_las = U0 - last["U_laser_mode1_mJ"]
eta_pass = dU_beam / U0; eta_consumed = dU_beam / dU_las
out["sp_measured"] = dict(U_laser0_mJ=U0, U_laser_end_mJ=last["U_laser_mode1_mJ"], beam_gain_mJ=dU_beam,
                          laser_to_beam_single_pass=eta_pass, laser_to_beam_of_consumed=eta_consumed)
print(f"\nSP measured: laser->beam {100*eta_pass:.2f} % of the injected laser per 0.65 mm pass, "
      f"{100*eta_consumed:.1f} % of the laser energy consumed ({U0 - last['U_laser_mode1_mJ']:.2f} of {U0:.2f} mJ)")
for las, e in eL.items():
    tr = e * chain * 0.25
    for tag, eta_sp in [("no reuse of leftover light", e * 0.62 * eta_pass), ("leftover light fully reused", e * 0.62 * eta_consumed)]:
        for front, Tf, ef in [("RF to 0.5 GeV", 0.5, 0.15), ("electric FF 80 % rec. to 0.5 GeV", 0.5, 0.006)]:
            w_sp = Tf / ef + 1.0 / tr + 4.5 / eta_sp
            w_tr = Tf / ef + 5.5 / tr
            out["staged"].append(dict(laser=las, front_end=front, sp="measured, " + tag, eta_sp_wallplug=eta_sp,
                                      eff_with_SP=6 / w_sp, eff_train_to_6GeV=6 / w_tr))
            print(f"  {las:9s} {front:32s} SP {tag:28s}: SP section {100*eta_sp:.2f} % -> system {100*6/w_sp:.2f} % "
                  f"(train all the way instead: {100*6/w_tr:.2f} %)")
json.dump(out, open(os.path.join(ROOT, "results", "data", "combined_stages.json"), "w"), indent=1)
