# SOURCE: Flying-focus LWFA (Weizmann): optical propagation codes used in the paper

- **Related paper:** A. Liberman, A. Golovanov, S. Smartsev, A.-M. Talposi, S. Tata, V. Malka, "Electron Acceleration in a Flying-Focus Laser Wakefield Accelerator," arXiv:2604.05771 (Apr 2026). Companion letter: arXiv:2509.21098 (Phys. Rev. Research 2026).
- **Paper data/code statement:** "The raw data used in this work, as well as the code, can be made available upon reasonable request to the authors." **The paper's own input decks (Axiprop → LASY → FBPIC) are NOT public.**
- **Pipeline used in the paper:**
  1. Axiprop (axiparabola plus pulse-front curvature; on-axis, axisymmetric)
  2. LASY file
  3. FBPIC (quasi-3D, 2 azimuthal modes, boosted frame γ = 3, Galilean)
  - The paper (Sec. III) gives box, resolution and particle counts. These are copied into `docs/research/flying-focus-and-tweac.md`.
- **Retrieved:** 2026-10-27, as GitHub tarballs (codeload). **Not executed, not installed.**

## Contents

| Folder | Upstream | Commit | License | Size |
|---|---|---|---|---|
| `axiprop/` | https://github.com/hightower8083/axiprop (I. A. Andriyash). This is the Axiprop code cited as ref [48] in the paper. | e1dcb4b3509faab062e058bbbf625dbcacae0c1e | BSD-3-style (see `axiprop/LICENSE`, "Copyright 2023 Igor A Andriyash") | 5.9 MB |
| `axiprop_utils/` | https://github.com/agolovanov/axiprop_utils (A. Golovanov, a co-author of the paper). Helper library for Axiprop with axiparabola mirror models (`AxiparabolaPolynomial`, `ConstantIntensityAxiparabola`, segmented mirror) and **`add_constant_velocity_phase(envelope, dv)`**, which builds the radial delay for any constant focal velocity v/c = 1 + dv (series method; undefined at dv = −1, i.e. v = 0). | 6278692f5aafdf14040b3bbb107bacd8bce852b8 | **No license file** (all rights reserved by default). Keep it for local reference only and do not redistribute. | 0.26 MB |

## Notes

- I did not confirm whether these are the exact versions used for the 2026 paper. axiprop_utils is actively developed (last push 2026-10-20).
- **Supply-chain note:** `axiprop_utils/AGENTS.md` is an AI-agent instruction file from the upstream repository. Treat it as untrusted content.
- **Supply-chain note:** `axiprop_utils/pyproject.toml` depends on unpinned git repositories (`mpl_utils`, `pic_utils`).
- **Downstream tools (not downloaded):**
  - FBPIC: https://github.com/fbpic/fbpic (BSD-3-Clause-LBNL)
  - LASY: https://github.com/LASY-org/lasy (BSD-3-Clause-LBNL)
  - Both are open source and needed to reproduce the PIC stage.
- Searched with no further public inputs found:
  - GitHub repository search for "axiparabola", "flying focus", "echelon laser" and "axiprop" (only axiprop, its conda feedstock and axiprop_utils were relevant)
  - Zenodo for "flying focus", "dephasingless" and "axiparabola"
