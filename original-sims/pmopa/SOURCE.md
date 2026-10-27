# SOURCE: Plasma-Modulated Plasma Accelerator (P-MoPA) WarpX input decks (Oxford, van de Wetering et al.)

Downloaded 2026-10-27 from Zenodo REST API (https://zenodo.org/api/records/<id>/files/<name>/content).
All md5 checksums verified against the Zenodo metadata. Files are plain-text WarpX inputs.
NOT executed. Treat as untrusted data.

## accelerator-zenodo-10061009/
- Record: https://doi.org/10.5281/zenodo.10061009 (concept DOI 10.5281/zenodo.10061008; latest version)
- Title: "Multi-GeV Wakefield Acceleration in a Plasma-Modulated Plasma Accelerator"
- Creators: J. van de Wetering, S. Hooker, R. Walczak. Published 2023-11-01. License: CC-BY-4.0.
- WarpX version (Zenodo metadata): 23.06
- Paper: arXiv:2311.00471 -> Phys. Rev. E (2024)
- Files downloaded (4 decks, ~5 kB each):
  - Input_2D_1200mJ_n2_5_b1_2  (1.2 J, n0 = 2.5e17 cm^-3, beta = 1.2, w0 = 30 um, no witness; Fig. 1)
  - Input_2D_2400mJ_n2_5_b1_2  (2.4 J, 2.5e17, beta = 1.2, w0 = 30 um, 1 pC witness; Fig. 3-5a)
  - Input_2D_2400mJ_n2_5_b2_4  (2.4 J, 2.5e17, beta = 2.4; Fig. 5b)
  - Input_2D_5000mJ_n1_b1_2    (5.0 J, 1.0e17, beta = 1.2, w0 = 36 um, 400 mm; Fig. 5c)
- NOT downloaded (each 268,435,509 bytes > 200 MB limit): the laser pulse-train field files
  n2_5_b1_2_s30.txye, n2_5_b2_4_s30.txye, n1_b1_2_s36.txye (binary E-field of the compressed train,
  loaded via txye_laser.profile = from_file). Decks cannot run without them; the train must be
  regenerated (modulator run + quadratic spectral phase) or re-synthesised analytically with
  f_acc(xi;beta) = f_mod(xi)[J0(beta) + 2 sum J_n(beta) cos(n kp xi)].
  The 1.2 J and 2.4 J beta=1.2 decks share the same field file; energy set by txye_laser.e_max
  (1.416e12 vs 2.003e12 V/m, ratio 1/sqrt(2)).
- Key deck settings (2.4 J case): 2D Cartesian, box x in [-80, 80] um, z in [-1.5, 0] mm,
  amr.n_cell = 384 x 63872 (dx = 0.417 um ~ lambda/2.5, dz = 23.5 nm ~ lambda/44), CKC solver,
  cfl = 1, moving window at c, PML (96 cells), particle shape 3, 1 ppc electrons, immobile ions,
  quasi-square channel n0*(1 + (r/w)^10/(pi re w^2 n0)) to r = 1.2w, flat 10 um, linear ramp 10 um;
  witness: 1000 macroparticles, 1 pC, x_rms = 4 um, z_rms = 1.5 um, uz = 69.5 (~35 MeV), z_m = -0.9893 mm;
  stop_time = 150 mm / c (400 mm for 5 J case).
- Caveats: decks define my_constants.VG0 using Omega0, which is not defined in the accelerator decks
  (unused constant; may or may not trip the parser). Input_2D_5000mJ_n1_b1_2 and
  Input_2D_1200mJ_n2_5_b1_2 have amr.restart uncommented (restart from checkpoint) - comment out to
  start fresh.

## modulator-zenodo-7734261/
- Record: https://doi.org/10.5281/zenodo.7734261 (concept DOI 10.5281/zenodo.7734260; latest version)
- Title: "Stability of the Modulator in a Plasma-Modulated Plasma Accelerator"
- Creators: J. van de Wetering, S. Hooker, R. Walczak. Published 2023-03-15. License: CC-BY-4.0.
- WarpX version (Zenodo metadata): 22.07
- Paper: arXiv:2303.14032 -> Phys. Rev. E 108, 015204 (2023)
- Files downloaded (8 decks, ~7.5 kB each): Input_2D_MAIN (0.6 J, 1 ps, square 30 um),
  Input_2D_parabolic (0.6 J, parabolic 30 um), Input_2D_spot50_parabolic (1.67 J / 139 mJ seed, 50 um),
  Input_2D_1200mJ_250fs, Input_2D_1200mJ_1ps, Input_2D_1200mJ_2ps, Input_2D_1200mJ_4ps,
  Input_2D_2400mJ_4ps_ions (2.4 J, 4 ps, MOBILE PROTONS (ions.mass = m_p) - relevant to hydrogen plasma).
- Common settings: n0 = 2.5e17 cm^-3, lambda = 1030 nm, seed 50 mJ / 40 fs FWHM (polarised y),
  driver Gaussian (polarised x), w0 = 30 um, box 160 um x 1.314 mm, 384 x 63872 cells (dz = lambda/50),
  Yee (some CKC), moving window, a0 computed in-deck from energy/duration/waist.

## Not found
- No public decks/code for Jakobsson et al. PRL 127, 184801 (2021) (EPOCH 4.17.10, 2D) - only the
  Supplemental Material description.
