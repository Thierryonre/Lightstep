# SOURCE: LLE dephasingless LWFA (flying focus, axiparabola + echelon, plasma-waveguide DLWFA): no public inputs found

- **Papers covered:**
  1. C. D. Arrowsmith et al., "Dephasingless laser wakefield acceleration of electrons using a flying focus," Nature Physics (10 Jul 2026), DOI 10.1038/s41567-026-03352-x. MTW-OPAL experiment.
  2. J. P. Palastro et al., "Dephasingless laser wakefield acceleration," PRL 124, 134802 (2020), DOI 10.1103/PhysRevLett.124.134802. Erratum: PRL 130, 159902 (2023).
  3. K. G. Miller et al., "Dephasingless laser wakefield acceleration in the bubble regime," Sci. Rep. 13, 21306 (2023), arXiv:2308.13432.
  4. J. L. Shaw et al., "Path to a single-stage, 100-GeV electron beam via a flying-focus-driven LPA," arXiv:2505.00157; Phys. Plasmas 32, 083107 (2025).
  5. J. P. Palastro et al., "Dephasingless laser wakefield acceleration in a plasma waveguide," arXiv:2606.20298 (2026).
  6. J. P. Palastro et al., "Arbitrary-velocity laser pulses in plasma waveguides," arXiv:2503.15690 (2025).
- **Codes used:**
  - OSIRIS (full PIC, with flying-focus / arbitrarily structured pulse implementations)
  - QPAD (quasi-static PIC)
  - modified-paraxial wave-equation solver plus Green's-function wake (PRL 2020)
- **Checked:** 2026-10-27
- **Result: no simulation input decks, optics design files or data are publicly available.** Nothing was downloaded.

## What was searched

- **Data statements:**
  - Shaw et al. 2025: "data ... available from the corresponding author upon reasonable request".
  - Palastro et al. 2020 (accepted manuscript via CHORUS) and Palastro et al. 2026: no data/code statement or repository link.
- **Nature Physics 2026 paper:** nature.com is behind a login wall (one attempt only), so the data-availability and code-availability sections could not be read. **Check these via institutional access**, since Nature journals require such statements.
- **Zenodo API:** "dephasingless", "flying focus" and "axiparabola" returned nothing from LLE. The only related hit is the Marquardt thesis (Zenodo 10.5281/zenodo.18695682, HZDR, LASY → PIConGPU flying focus).
- **GitHub repository search:** "flying focus", "axiparabola" and "echelon laser" returned nothing from LLE.
- **arXiv:** no arXiv version of the Nature Physics paper was found (API searches `all:dephasingless` and `au:Arrowsmith_C`).

## Open-source paths to reproduce (not downloaded)

- **OSIRIS** is open source (https://github.com/osiris-code/osiris; AGPL). Whether it contains the flying-focus pulse initialization of Pierce et al., PRR 5, 013085 (2023), was not verified.
- **QPAD:** https://github.com/UCLA-Plasma-Simulation-Group/QPAD
- **Alternative pipeline:** LASY (axiparabola plus radial group-delay echelon) feeding FBPIC, WarpX or PIConGPU. See the `../flying-focus-lwfa-weizmann/` and `../tweac-picongpu/` SOURCE.md files.
- **Design numbers for reproduction** are tabulated in `docs/research/flying-focus-and-tweac.md` under "Reproduction targets (numbers)".
