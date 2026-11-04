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
