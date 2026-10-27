# SOURCE: Subluminal-driver, density-tailored LWFA for slow/heavy particles (Badiali et al. 2026): no public inputs found

- **Paper:** C. Badiali, R. Almeida, B. Malaca, R. Fonseca, T. Silva, J. Vieira, "Tailored laser wakefield acceleration for decaying particles", *Phys. Rev. Research* 8, 023077 (2026).
  - DOI: 10.1103/1pp8-qx35. Open access, CC-BY 4.0.
- **Code used:** OSIRIS, quasi-3D (azimuthal modes m = 0, 1). OSIRIS is open source (AGPL): https://github.com/osiris-code/osiris
- **Checked:** 2026-10-27
- **Result: no input decks or data are public.** The data-availability statement says the data are "available from the authors upon reasonable request". Nothing was downloaded.

## What was searched

- The paper's data-availability section (full text read).
- Zenodo API: "proton wakefield laser", "flying focus", "space-time wave packet wakefield".
- GitHub repository search: "flying focus", "space-time wave packet wakefield", "wakefield proton". The GitHub API rate limit was hit after a few queries.
- No arXiv preprint with source files was found.

## Parameters to rebuild the PIC setup (from Appendix B of the paper)

- **Plasma:** n0 = 4×10^18 cm⁻³ (c/ω_p = 2.55 µm, ω0/ω_p = 20). The density profile n(z) is solved from Eqs. (1a, 1b); the formulas are in `docs/research/proton-wakefield-and-nanoparticles.md`, S12.
- **Window:** co-moving at c. 344 µm (135 c/ω_p) × 51 µm radial (20 c/ω_p). 27000 × 400 cells (dξ = 0.005 k_p⁻¹, dr = 0.05 k_p⁻¹). dt = 3.5×10⁻³ ω_p⁻¹ (0.030 fs). Open field boundaries at large r, absorbing for particles. Dynamic load balancing every 100 steps.
- **Driver:** space-time flying-focus wave packet.
  - λ0 = 0.8 µm. a0 = 3 (nonlinear cases) or 0.8 (linear cases). w0 = 1.4 k_p⁻¹ (3.56 µm). Envelope length 108 k_p⁻¹ (275 µm).
  - The intensity peak moves rigidly at the prescribed v_f (0.7c to 0.97c), while the envelope moves at c.
  - The field is injected with a plane-wave-injection method that is exact for non-paraxial packets.
- **Witness:** flat-top, length 75 k_p⁻¹ (0.2 mm), radius 0.26 k_p⁻¹ (0.5 µm), n_b = 10⁻³ n0. Masses tested: 264, 207, 100 and 50 m_e (π, μ, μ/2, μ/4). Protons were treated only in theory.

## Related folders

- `../transverse-flying-focus-ions/`: Gong et al. PRL 2024 (transverse flying focus for ions; no inputs public).
- `../flying-focus-dlwfa-lle/` and `../tweac-picongpu/`: electron flying-focus and TWEAC tools.
