"""Summary figures (static PNG) following the dataviz method: one axis per chart, fixed
categorical order (blue, orange, aqua), thin marks, direct labels + legend, provenance encoded
with a secondary channel (hatching), text in neutral ink."""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
D = os.path.join(ROOT, "results", "data")
FIG = os.path.join(ROOT, "results", "figures")
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False})


def fig_gain_per_stage():
    b2 = json.load(open(os.path.join(D, "B2_conventional_protons.json")))["rows"]
    p1b = json.load(open(os.path.join(D, "P1b_scan.json")))
    Tinj = [10, 100, 1000, 3000]
    conv = [max(r["max_gain_MeV"] for r in b2 if r["T_inj_MeV"] == t) for t in Tinj]
    mt = sorted({r["T_inj"] for r in p1b if r["program"] == "const" and r["T_mean"] > 5900})
    matched = [6000 - t for t in mt]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(Tinj, conv, "-o", color=ORANGE, lw=2, ms=8, label="Conventional LWFA (best density, best phase)")
    ax.plot(mt, matched, "-s", color=BLUE, lw=2, ms=8, label="Velocity-matched wake (reaches 6 GeV)")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Proton injection energy [MeV]")
    ax.set_ylabel("Energy gain in one stage [MeV]")
    ax.set_title("Simulated proton energy gain per stage (1D)", color=INK, loc="left")
    for t, g in zip(Tinj, conv):
        ax.annotate(f"{g:.2g}" if g < 10 else f"{g:.0f}", (t, g), textcoords="offset points", xytext=(6, -12), color=INK2, fontsize=8)
    for t, g in zip(mt, matched):
        ax.annotate(f"{g:.0f}", (t, g), textcoords="offset points", xytext=(6, 6), color=INK2, fontsize=8)
    ax.legend(frameon=False, loc="center right", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "summary_gain_per_stage.png"), dpi=150)
    plt.close(fig)


def fig_efficiency_ranking():
    dc = json.load(open(os.path.join(D, "design_calc.json")))
    pick = {
        "RF_reference": ("RF proton accelerator (reference, lit.)", True),
        "D2_guided_train_k0kp20_fibre_projected": ("D2 guided resonant FF train, projected fibre", False),
        "D2_guided_train_k0kp20_fibre_today": ("D2 guided resonant FF train, today's fibre", False),
        "D3_alloptical_TFF_lit_NP": ("D3 all-optical (self-injection + NP) + D2", False),
        "D1_freespace_FF_lw0.03_fibre_projected": ("D1 free-space flying focus, fibre", False),
        "D0_conventional_staged_inj1000_fibre_projected": ("D0 conventional LWFA staged, fibre", False),
        "D4_nearcritical_RPA_lit": ("D4 near-critical RPA, Ti:Sa (lit.)", True),
        "D1_freespace_FF_lw0.03_TiSa": ("D1 free-space flying focus, Ti:Sa", False),
        "D0_conventional_staged_inj1000_TiSa": ("D0 conventional LWFA staged, Ti:Sa (baseline)", False),
    }
    rows = [(v[0], dc[k]["eta_total"], v[1]) for k, v in pick.items() if k in dc]
    rows.sort(key=lambda r: r[1])
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    y = np.arange(len(rows))
    for i, (lab, val, lit) in enumerate(rows):
        ax.barh(i, val, height=0.62, color=BLUE if not lit else SURF, edgecolor=BLUE,
                hatch="////" if lit else None, linewidth=1.0)
        ax.text(val * 1.15, i, f"{val:.1e}" if val < 1e-3 else f"{100*val:.2g} %", va="center", color=INK2, fontsize=8)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=8, color=INK)
    ax.set_xscale("log"); ax.set_xlim(1e-7, 1)
    ax.set_xlabel("Wall-plug → 6 GeV proton efficiency")
    ax.set_title("Design ranking by overall energy efficiency", color=INK, loc="left")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=BLUE, edgecolor=BLUE, label="plasma/beam physics simulated here (1D/RZ) + sourced factors"),
                       Patch(facecolor=SURF, edgecolor=BLUE, hatch="////", label="literature only (not simulated here)")],
              frameon=False, fontsize=7, loc="lower right")
    ax.grid(axis="y", visible=False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "summary_efficiency_ranking.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    fig_gain_per_stage()
    fig_efficiency_ranking()
    print("figures written")
