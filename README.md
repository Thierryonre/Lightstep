# Lightstep

**Simulating compact laser-plasma accelerators that keep their wave in step with slow protons and carry them to 6 GeV, as energy-efficiently as possible, to make muons for muon-catalysed fusion.**

---

## The problem in one paragraph

Muon-catalysed fusion needs a steady supply of muons. Muons are made by hitting a target with
protons of a few GeV, and today that takes a big, expensive accelerator. Laser wakefield
accelerators (LWFAs) are hundreds of times shorter because a laser drives a wave in a plasma with
enormous electric fields. But they were built for electrons, which already move at nearly the
speed of light. **Protons start slow, and a normal plasma wave runs away from them before they gain
anything.** This project looks for laser (and laser-plus-electric) designs that keep the wave
in step with the protons, and measures how much of the electricity ends up in the proton beam.

## The answer so far

| Design | What it is | Wall-plug → beam efficiency* |
|---|---|---|
| Conventional LWFA (baseline) | Ordinary laser-driven wave, restaged repeatedly | ~0.02%: it barely accelerates protons at all |
| **Best overall** | RF linac to 1 GeV, then the **guided resonant laser train** to 6 GeV | **2.9%** for protons, **4.6%** for deuterons |
| Best without RF | **Electric flying focus** to 0.5 GeV, then the guided train | 1.4-2.0% |
| **Best optical-only** | Protons picked up from rest by a slow laser driver, then the guided train | **1.0%** (1.2% with PV cells) |
| For comparison | A conventional RF proton accelerator | ~15% |

\* With projected 40%-efficient fibre lasers; today's lasers give about half. These are
estimates built on simulated numbers. See [`docs/RESULTS.md`](docs/RESULTS.md) for how each
was obtained.

**In plain terms:** the best laser design is about 140× more efficient than a conventional laser
accelerator for protons, and much shorter than an RF machine, but still about 5× less efficient
than RF. It does not on its own make muon-catalysed fusion produce net energy.

## The key ideas, explained

- **Make the wave move at the protons' speed.** A *flying focus* shapes a laser pulse so that
  its bright spot travels at any speed you choose, even slower than light. A wave driven by it
  can stay with the protons for the whole acceleration instead of a few micrometres.
- **Guided resonant train (the main accelerator).** Three laser colours, spaced by the plasma's
  natural frequency, travel together inside a plasma channel (a plasma "optical fibre"). Their
  beating makes a train of pulses that builds the wave up resonantly. Making the channel
  gradually wider or narrower sets how fast the pattern moves, so it can follow the protons as
  they speed up. Measured in 3D simulation: **16 GV/m on protons** (several hundred times a
  conventional RF accelerator).
- **Picking protons up from rest (optical-only front end).** A laser driven from the side makes
  a field peak that starts slow and speeds up, scooping protons out of a dense hydrogen layer.
- **Electric flying focus (non-RF front end).** Rings of electrodes fired in sequence make a
  field that travels with the protons at any speed. It locks protons from 1 MeV to 100 MeV in
  about 2 m, but needs strong magnetic focusing and is only efficient with energy recovery.
- **Deuterium.** Using deuterium for the plasma, or accelerating deuterons instead of protons,
  improves efficiency and the energy cost per muon.
- **PV cells at the end.** About 60% of the laser light is left over. Turning it back into
  electricity gains only ×1.1-1.2, because the light that drove the wave comes out spread across
  many colours. Reusing the unused light optically in the next stage is the better lever.

## Ideas tested and set aside

| Idea | Why it was set aside |
|---|---|
| Conventional LWFA | Protons fall out of the wave within micrometres (<1 MeV per stage at 100 MeV) |
| Free-space flying focus | Wastes most of the light; can't make slow, short drivers |
| Surface plasmon in a hollow channel | Accelerates 3 GeV protons at ~30 GV/m, but measured laser→proton efficiency is only 0.75% per pass, the 1-2 µm channel only accepts extremely fine beams, and it doesn't work below ~3 GeV |
| Extra laser colours in the hollow channel | Help for the first 0.1 mm, then fall out of step |
| "Virtual charge" field concentration (electric version of *Tailoring magnetic fields in inaccessible regions*) | The field on the beam axis can never exceed the field at the electrodes, so it gives no extra gradient |

## What is proven and what isn't

- **Simulated:** baseline LWFA, velocity-matched acceleration (1D, checked with particle-in-cell
  codes), the guided train's optics and proton acceleration (quasi-3D, FBPIC on GPUs),
  self-injection (1D), the electric flying focus (tracking), surface plasmons (quasi-3D), and
  PV light spectra. Four published results were reproduced first (Palastro 2020, Hooker 2014,
  Ross 2024, Lahaye 2026).
- **Still estimates:** the end-to-end efficiency of the guided train (pieced together from 1D
  and 3D results, not yet one loaded 3D run), the laser coupling of the optical-only front end
  (from the literature), and all laser and wall-plug figures.
- **Biggest open problems:** the train's light runs ahead of the protons, so stages need
  picosecond-long pulses; and the beams must be very fine (micrometre-scale) to fit.

Every number in the docs is tagged **[sim]** (simulated here), **[lit]** (published) or
**[est]** (estimate).

## Where to read more

| File | What's in it |
|---|---|
| [`docs/RESULTS.md`](docs/RESULTS.md) | Full results, rankings and designs. §12 is a plain-language optical-only summary; §14 covers combining the stages |
| [`docs/SIMULATION_LOG.md`](docs/SIMULATION_LOG.md) | All 53 simulation runs (S001-S053), including failures and corrections |
| [`docs/research/`](docs/research/) | Literature notes; start with `SUMMARY.md` |
| [`OLD-README.md`](OLD-README.md) | The previous README (its efficiency figures are out of date) |

## Repository layout

| Path | Contents |
|---|---|
| `sims/codes/` | Codes written for this project: 1D fluid (numpy and JAX), 1D envelope and full-EM particle-in-cell, particle tracker |
| `sims/baseline/` | Conventional LWFA baseline |
| `sims/phase1/` | Individual techniques: flying focus, self-injection, resonant trains, electric flying focus |
| `sims/phase2/` | Optimisation, density gradients, PV spectra, and the FBPIC quasi-3D runs (with Modal GPU launchers) |
| `sims/design/` | Design and efficiency calculators |
| `sims/tests/` | Code validation |
| `original-sims/` | Original simulation inputs from the papers, where public |
| `results/data/`, `results/figures/` | Simulation outputs and figures |

## Running it

```bash
python -m venv .venv                                    # Python 3.11
.venv/Scripts/pip install numpy scipy numba matplotlib h5py jax
.venv/Scripts/python sims/tests/test_fluid1d.py         # check the codes
.venv/Scripts/python sims/phase1/p1b_scan.py            # velocity-matched acceleration to 6 GeV (~20 min)
.venv/Scripts/python sims/phase1/e1_electric_flying_focus.py   # electric flying focus (~2 min)
.venv/Scripts/python sims/design/combined_stages.py     # efficiency of the staged designs
```

The quasi-3D runs use FBPIC on a cloud GPU via [Modal](https://modal.com), for example:

```bash
modal run --detach sims/phase2/modal_fbpic_generic.py --script fbpic_waveguide_train.py \
    --args "--steps 6000 --protons" --out my_run
```

Most 1D studies ran on a 4-core laptop. The 3D runs took 10 minutes to 5 hours each on a
single GPU (about $0.5-9 per run).
