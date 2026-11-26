# Energy-efficient laser wakefield acceleration of protons to ~6 GeV

Research project: find the most energy-efficient, affordable, **simulation-supported** laser
wakefield accelerator (LWFA) design that can deliver ~6 GeV protons for muon production
(muon-catalysed fusion), and compare it quantitatively against a conventional LWFA.

**Start here:** [`docs/RESULTS.md`](docs/RESULTS.md) (findings, rankings, recommended design) ·
[`docs/SIMULATION_LOG.md`](docs/SIMULATION_LOG.md) (every simulation attempt, incl. failures) ·
[`docs/research/SUMMARY.md`](docs/research/SUMMARY.md) (literature synthesis).

> Numbers are tagged **[sim]** (simulated here), **[lit]** (published) or **[est]** (estimate).

## Key findings (short)

- A conventional LWFA cannot accelerate protons from a practical injector: < 1 MeV per stage
  for 100 MeV protons, 8 MeV for 1 GeV protons [sim].
- A wake whose phase velocity is programmed to follow the protons (flying-focus principle)
  accelerates them 0.03–1 GeV → 6 GeV in one continuous stage with 35–53 % wake→beam efficiency,
  60–71 % after joint differentiable optimisation of pulse shape and bunch profile [sim, 1D,
  PIC-validated].
- Best optical embodiment found: a **guided resonant flying-focus train** — 3–5 fibre-laser lines
  spaced by the plasma frequency, each in a different mode of a plasma channel; the beat pattern
  is a resonant pulse train moving at a programmable sub-luminal velocity, set along the
  accelerator by tapering the channel width [sim optics + 1D PIC; quasi-3D check in progress].
- Recommended design (RF injector to 1 GeV + three guided stages, ≈18 cm of plasma): ≈3–6 %
  wall-plug efficiency [est], ≈300× a conventional LWFA with the same lasers — but below RF proton
  accelerators (~10–18 %), and not enough to make muon-catalysed fusion break even with
  demonstrated μCF physics [lit].
- Published results reproduced: Palastro 2020 flying-focus DLWFA (75 MeV vs 1.22 GeV),
  Hooker 2014 multi-pulse (5.0 GV/m vs 4.7), Ross 2024 resonance (4.3×10¹⁷ cm⁻³), Lahaye 2026
  gradient mechanism (in 1D).

## Repository layout

| Path | Contents |
|---|---|
| `docs/RESULTS.md` | Results, multipliers, rankings, recommended design |
| `docs/SIMULATION_LOG.md` | Every simulation attempt: parameters, results, failures, conclusions |
| `docs/research/` | Literature notes and synthesis |
| `original-sims/` | Original simulation inputs/code from the papers where public (each with `SOURCE.md`) |
| `sims/codes/` | Codes written here: 1D fluid (numpy + JAX), 1D envelope PIC, 1D full-EM PIC, proton/electron tracker |
| `sims/tests/` | Code validation scripts |
| `sims/baseline/`, `sims/phase1/`, `sims/phase2/` | Studies (baseline, Phase-1 techniques, Phase-2 optimisation; FBPIC scripts) |
| `sims/design/` | Design calculator and summary figures |
| `results/data`, `results/figures` | Simulation outputs (JSON/NPY, small) and figures |

## Running

```bash
python -m venv .venv               # Python 3.11
.venv/Scripts/pip install numpy scipy numba matplotlib h5py jax wake-t
.venv/Scripts/python sims/tests/test_fluid1d.py           # validation
.venv/Scripts/python sims/phase1/p1b_scan.py              # velocity-matched 6 GeV scan (~20 min)
.venv/Scripts/python sims/design/design_calc.py           # design synthesis
# quasi-3D check (Linux/WSL): pip install fbpic pyfftw; python3 sims/phase2/fbpic_waveguide_train.py
```

All runs used a 4-core laptop CPU (no GPU): the study relies on validated 1D kinetic and
quasi-static models plus one quasi-3D FBPIC check; see the log for each model's limits.
