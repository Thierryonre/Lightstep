# Energy-efficient laser wakefield acceleration of protons to ~6 GeV

Research project: find the most energy-efficient, affordable, **simulation-supported** laser
wakefield accelerator (LWFA) design that can deliver ~6 GeV protons for muon production
(muon-catalysed fusion), and compare it quantitatively against a conventional LWFA.

> Status: work in progress. Numbers marked *simulated* come from the codes in `sims/`;
> numbers marked *estimate* are analytic/literature-based and are not simulation results.

## Repository layout

| Path | Contents |
|---|---|
| `docs/SIMULATION_LOG.md` | Every simulation attempt: parameters, results, failures, conclusions |
| `docs/research/` | Literature notes (Phase 1, Phase 2, laser technology, proton wakes, muon production) |
| `original-sims/` | Original simulation inputs/code from the papers where publicly available (each with `SOURCE.md`) |
| `sims/codes/` | Simulation codes written for this project (1D fluid, 1D envelope PIC, 1D EM PIC, helpers) |
| `sims/tests/` | Validation / reproduction scripts |
| `sims/baseline/`, `sims/phase1/`, `sims/phase2/` | Study scripts for the conventional baseline and the technique combinations |
| `results/` | Figures and summary tables |

## Running

```bash
python -m venv .venv            # Python 3.11 recommended
.venv/Scripts/pip install numpy scipy numba matplotlib h5py wake-t
.venv/Scripts/python sims/tests/test_fluid1d.py
```

All local runs use a 4-core laptop CPU; the study therefore relies on 1D kinetic and
quasi-static reduced models, validated against each other and against theory (see the log).
