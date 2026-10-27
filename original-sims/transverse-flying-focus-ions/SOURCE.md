# SOURCE: LWFA of ions with a transverse flying focus (Gong et al., PRL 2024): no public inputs found

- **Paper:** Z. Gong, S. Cao, J. P. Palastro, M. R. Edwards, "Laser wakefield acceleration of ions with a transverse flying focus," Phys. Rev. Lett. 133, 265002 (2024).
  - DOI 10.1103/PhysRevLett.133.265002
  - arXiv:2405.02690v2
- **PIC code:** EPOCH (open source, GPL): https://github.com/Warwick-Plasma/epoch
- **Checked:** 2026-10-27
- **Result: no simulation input decks or code are publicly available.** Nothing was downloaded.

## What was searched

1. **arXiv e-print source for 2405.02690v2** (https://arxiv.org/e-print/2405.02690v2, 5.1 MB).
   - Contains only `main.tex`, `output.bbl` and five figure PNGs.
   - **No Supplemental Material, no animations, no input decks.**
   - Not kept: it is paper source under the default arXiv license, not simulation input.
2. **APS Supplemental Material page** (https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.133.265002).
   - Returned a login-gated page with no file links.
   - The SM holds the detailed PIC parameters, the optical configuration of the transverse flying focus, the Hamiltonian derivation, the optical-imperfection study and the efficiency comparison. **Get it via institutional access if needed.**
3. **GitHub** repository search ("flying focus", "axiparabola", "echelon laser") found nothing relevant to this paper.
4. **Zenodo** search ("flying focus") found nothing relevant.
5. **The paper has no data-availability statement** in the arXiv version.

## Key parameters for reproduction (from the main text; see `docs/research/flying-focus-and-tweac.md`, Source 7a)

- **Focus trajectory:** hyperbolic (constant proper acceleration), x_f = (c²/α0)[√((α0 t/c)² + 1) − 1].
  - Trapping condition: α0 < Λ ≈ Z_i m_e c² a0 (n_e/n_c)^{1/6}/(m_i σ0).
- **Case 1:** I0 = 1.1e20 W/cm², H plasma at n_e = 0.05 n_c, α0 = 2e-4 c/T0 (T0 ≈ 3.3 fs, λ ≈ 1 µm). Result: 230 MeV protons after 1 mm.
- **Case 2:** 0.8 kJ, 21 ps, 37.5 TW, I0 ≈ 3e20 W/cm², n_e ≈ 5.5e19 cm^-3. Result: 1.64 GeV, 3.7% spread, 23.1 pC after 4.4 mm.
- **2D scans** (Fig. 4): a0 = 9 and σ0 = 4 µm unless varied.
- **Related optics paper:** Cao et al., arXiv:2510.14195 ("Flying focus with arbitrary directionality"). Not checked for code.
