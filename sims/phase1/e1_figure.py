"""Figure for E1 (electric flying focus)."""
import os, json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
R = json.load(open(os.path.join(ROOT, "results", "data", "E1_electric_flying_focus.json")))
COL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
INK, MUTED = "#2b2b2b", "#8a8a86"
plt.rcParams.update({"axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False, "font.size": 9})
fig, ax = plt.subplots(2, 2, figsize=(10, 7.5))
A = R["A_replicator"]
for i, rv in enumerate([0.75, 0.5, 0.25, 0.1]):
    rows = [r for r in A if r["r_v_over_a"] == rv]
    ax[0, 0].semilogy([r["kmax_a"] for r in rows], [r["wall_over_axis"] for r in rows], "-o", color=COL[i], lw=2, ms=4,
                      label=f"virtual charge at r = {rv} a")
ax[0, 0].axhline(1, color=MUTED, lw=0.8, ls="--")
ax[0, 0].set_xlabel("modes kept, k_max·a  (Mach-Batlle truncation n_T)"); ax[0, 0].set_ylabel("peak wall field / peak axis field")
ax[0, 0].set_title("A. Replicating a virtual charge inside the bore", loc="left", color=INK)
ax[0, 0].legend(frameon=False, fontsize=8)
B = R["B_flat_top"]
for i, w in enumerate([0.25, 1.0]):
    rows = [r for r in B if r["edge_over_gamma_a"] == w]
    ax[0, 1].plot([r["L_over_gamma_a"] for r in rows], [r["axis_over_wall_peak"] for r in rows], "-o", color=COL[i], lw=2, ms=4,
                  label=f"edge width {w} γa")
ax[0, 1].axhline(1, color=MUTED, lw=0.8, ls="--"); ax[0, 1].set_xscale("log")
ax[0, 1].set_xlabel("flat-top length / (γ a)"); ax[0, 1].set_ylabel("peak axis field / peak wall field")
ax[0, 1].set_title("B. Best case: long moving flat-top (bound = 1)", loc="left", color=INK)
ax[0, 1].legend(frameon=False, fontsize=8)
C = R["C_tracking"]["runs"]
for i, r in enumerate([r for r in C if "note" not in r]):
    h = r["history"]
    ax[1, 0].plot([q["z_m"] for q in h], [q["T_mean_cap"] for q in h], color=COL[i], lw=2,
                  label=f"timing jitter {r['jitter_ps']:.0f} ps: {100*r['frac_captured']:.0f} % captured")
ax[1, 0].set_xlabel("distance [m]"); ax[1, 0].set_ylabel("mean proton energy [MeV]")
ax[1, 0].set_title("C. Tracking 1 → 100 MeV, ring electrodes, 50 MV/m wall", loc="left", color=INK)
ax[1, 0].legend(frameon=False, fontsize=8)
D = R["D_energy"]["rows"]
for i, tag in enumerate(["vacuum_gap_rings", "DWA_insulator"]):
    rows = [r for r in D if r["design"] == tag]
    ax[1, 1].loglog([r["T_MeV"] for r in rows], [100 * r["wallplug_no_recovery"] for r in rows], "-o", color=COL[i], lw=2, ms=4,
                    label=f"{tag.replace('_', ' ')}, no recovery")
    ax[1, 1].loglog([r["T_MeV"] for r in rows], [100 * r["wallplug_80pct_recovery"] for r in rows], "--o", color=COL[i], lw=1.2, ms=3,
                    label=f"{tag.replace('_', ' ')}, 80 % recovery")
ax[1, 1].axhline(15, color=MUTED, lw=0.8, ls=":"); ax[1, 1].text(1.1, 17, "RF proton linac ~15 %", color=MUTED, fontsize=8)
ax[1, 1].set_xlabel("energy where the section starts [MeV] (bunch charge set there)"); ax[1, 1].set_ylabel("wall-plug → beam [%]  (estimate)")
ax[1, 1].set_title("D. Space-charge-limited efficiency (estimate)", loc="left", color=INK)
ax[1, 1].legend(frameon=False, fontsize=7)
plt.tight_layout()
plt.savefig(os.path.join(ROOT, "results", "figures", "E1_electric_flying_focus.png"), dpi=110)
