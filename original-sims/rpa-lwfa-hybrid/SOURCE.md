# SOURCE: Hybrid RPA (light-sail/foil) → LWFA proton schemes: no public inputs found

- **Checked:** 2026-10-27
- **Result: none of the papers below has published input decks, code or data.** Nothing was downloaded. The parameters needed to rebuild each setup are summarized below. Full notes are in `docs/research/proton-wakefield-and-nanoparticles.md` (S3–S6, S13, S14).

## Papers and codes

| Paper | Code | Availability |
|---|---|---|
| Shen, Zhang, Sheng, Yu, Cary, PRST-AB 12, 121301 (2009), DOI 10.1103/PhysRevSTAB.12.121301 | VORPAL 2D (commercial, Tech-X) | No data statement. No inputs. |
| Yu et al., NJP 12, 045021 (2010), DOI 10.1088/1367-2630/12/4/045021 | 1D/2D PIC (code not identified; abstract only) | None found. |
| Zheng et al., arXiv:1101.2350 / PoP 19, 023111 (2012), DOI 10.1063/1.3684658 | KLAP (PKU in-house) | None. |
| Liu et al., PoP 25, 063103 (2018), arXiv:1806.10839, DOI 10.1063/1.5033991 | OSIRIS 2D | None. |
| Isayama et al., PoP 28, 073101 (2021), DOI 10.1063/5.0049725 (dual-pulse RPA-LWFA-TNSA) | 2D PIC (abstract only) | None found. |
| Chen et al., EPJ D 79 (2025), DOI 10.1140/epjd/s10053-025-00977-0 (RPA+LWFA in modulated channels) | not read | Not checked (paywalled). |

**Searched:** Zenodo API ("radiation pressure wakefield proton", "proton wakefield laser"), GitHub repository search, arXiv listing pages, and the papers' own data statements where readable. The only related public deck found is the near-critical **bow-wake** EPOCH deck in `../bow-wake-isayama2026/`. It is a single-stage near-critical scheme, but it shares the slow-front trapping physics.

## Rebuild parameters

### Liu et al. 2018 (best template for a 6 GeV design: density-ramped near-critical LWFA after RPA)

- **Code and grid:** OSIRIS 2D. 70×70 µm moving window, 5600×4200 cells. 400 ppc in the foil, 100 ppc in the background.
- **Laser:** λ = 1 µm, CP. a(t, y) = a0 sin²(πt/2τ) exp(−y²/σ²) for 0 ≤ t ≤ 2τ, with τ = 10T and σ = 8λ.
  - Baseline: a0 = 50.
  - High-intensity case: a0 = 120.
- **Foil:** CH (C:H = 1:2), n_e = 20 n_c, thickness 0.4λ (1λ for a0 = 120), |y| ≤ 2.5λ.
- **Background:** carbon.
  - a0 = 50: n_e = 4 n_c exp(−x/20λ), or uniform 4 n_c for comparison.
  - a0 = 120: 1.2 n_c exp(−x/60λ).
  - Alternative: 3 n_c exp(−x²/(30λ)²).

### Shen et al. 2009

- **Code and grid:** VORPAL 2D. 50λ×200λ window, 2000×400 cells, 10 ppc per species.
- **Laser:** CP, λ = 0.8 µm, I = 2.14×10^23 W/cm², 12.5T duration, 20λ FWHM spot.
- **Target:** H micro-target, 10 n_c, 2λ×2λ, at x = 100λ.
- **Background:** tritium at 0.3 n_c, from x = 10λ to 800λ.

### Zheng et al. 2011

- **1D run (KLAP):** 12000λ, 20 cells/λ, 10 ppc in the gas, 20000 ppc in the foil.
  - Laser: CP, a0 = 250, λ = 1 µm, 20λ sin² rise + 15λ flat top.
  - Foil: H, 20 n_c, D = 0.5λ.
  - Gas: Z/A = 1/3, 0.01 n_c.
- **2D run:** 0.2 n_c. Super-Gaussian laser with r0 = 10 µm and τ = 55 fs.
