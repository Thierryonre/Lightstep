# SOURCE: TWEAC (Traveling-Wave Electron Acceleration): PIConGPU setup and TWTS laser model

- **Related paper:** A. Debus et al., "Circumventing the dephasing and depletion limits of laser-wakefield acceleration," Phys. Rev. X 9, 031044 (2019), DOI 10.1103/PhysRevX.9.031044 (CC-BY 4.0).
- **Upstream repository:** https://github.com/ComputationalRadiationPhysics/picongpu
  - Branch `dev`, commit `93cba5b61b628659a6ec8181f5e2dd28b8006f29`.
  - Files fetched individually from `https://raw.githubusercontent.com/ComputationalRadiationPhysics/picongpu/<commit>/<path>`.
- **Retrieved:** 2026-10-27
- **License:** PIConGPU main simulation, `share/picongpu`, `include/picongpu` and `lib/python/picongpu` are **GPLv3+**; libraries are LGPLv3+. See `picongpu/LICENSE.md`, `picongpu/COPYING` and `picongpu/COPYING.LESSER` (copied alongside).
- **Status:** downloaded only. **Not executed, not built.** Total size about 0.4 MB, 52 files.

## Contents

The directory structure mirrors the upstream repository paths.

| Path | What it is |
|---|---|
| `picongpu/share/picongpu/benchmarks/TWEAC-FOM/` | Official PIConGPU **TWEAC 3.5° figure-of-merit benchmark** (README: "TWEAC 3.5deg FOM setup used for the FOM simulations on Frontier/Summit"). `.param` files (laser, density, species, solver) and `.cfg` run files for 4 to 27600 GPUs. `cmakeFlags` chooses between incident-field and field-background laser generation. |
| `picongpu/include/picongpu/fields/incidentField/profiles/TWTSPulse.def` | TWTS pulse-front-tilted laser incident-field profile. |
| `picongpu/include/picongpu/fields/background/templates/TWTS/`, `.../twtstight/` | Analytic field models of the tilted-pulse-front (traveling-wave Thomson-scattering) lasers used to drive TWEAC. `TWTSTight` is the newer, more accurate model (Plasma-PEPSC D1.12, Zenodo 10.5281/zenodo.17980114). |
| `picongpu/lib/python/picongpu/picmi/lasers/twts_laser.py` | PICMI Python wrapper for the TWTS laser. |

## Notes for reuse

- **These are benchmark inputs, not a faithful copy of the PRX 2019 physics runs.**
  - `TwtsBackgroundLaser.param` sets `_A0 = PARAM_A0 * 0.01` with PARAM_A0 = 3.25 ("reduced for FOM benchmark").
  - Plasma density: BASE_DENSITY_SI = 0.8e23 m^-3 × REL_DENSITY_HIGH 2.0 = 1.6e17 cm^-3 (uniform).
  - Grid: cells of 0.16 × 0.02 × 0.16 µm with dt = 65.4 as. Periodic, no moving window, 1000 steps.
  - To reproduce PRX 2019 physics, restore a0 ≈ 3.0–3.5 per arm and n_e ≈ 2.5–3.2e18 cm^-3, and add the density shock and downramp. See the PRX paper, Table I and Appendix C.
- **Other laser parameters in the param file:**
  - λ = 0.8 µm
  - 10 fs FWHM
  - w0 = 1.2 µm (line-focus height)
  - φ = ±3.5°
  - polarizations ±45°
- **Key knob for the MCF proton study:** `BETA_0`, the "propagation speed of overlap normalized to the speed of light [default = 1.0]".
  - The TWTS model implements the general matching condition α = arctan[(1 − β0 cos φ)/(β0 sin φ)].
  - In principle this lets you simulate a **subluminal TWEAC overlap (β0 < 1)** without code changes.
  - It cannot represent a time-varying β0(y), which would need a modified field model.
- Upstream PRX runs used PIConGPU releases beta-rc6, 0.3.1 and 0.4.0. Those old release inputs were not located. The PRX paper has no data/code repository link.
- **Related but not downloaded:** E. Marquardt, "Generating and testing flying focus laser pulses with Lasy for PIConGPU simulations" (thesis, 2025, CC-BY 4.0), Zenodo 10.5281/zenodo.18695682 (5.3 MB PDF). It describes importing LASY-generated axiparabola/echelon flying-focus pulses into PIConGPU, and reports discrepancies between predicted and measured focal velocities.
