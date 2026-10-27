# SOURCE: Bow-wake acceleration (BWA) of protons in near-critical foam — Isayama et al. 2026

- **Paper:** S. Isayama et al., "Bow-wake acceleration of ions toward a relativistic regime", *Communications Physics* 9 (2026). DOI: 10.1038/s42005-026-02749-7 (open access, CC-BY 4.0).
- **Data/code record:** Zenodo, "Supplementary Data and Code for 'Bow-Wake Acceleration of Ions Toward a Relativistic Regime'" by Shogo Isayama.
  - Concept DOI 10.5281/zenodo.20821422; version DOI 10.5281/zenodo.20821423.
  - URL: https://zenodo.org/records/20821423
- **License:** CC-BY-4.0, per the Zenodo metadata.
- **Published on Zenodo:** 2026-06-24. **Downloaded:** 2026-10-27, unmodified. None of the files have been executed.
- **Code needed:** EPOCH 3D, which is not included and must be obtained from the EPOCH developers.

## Contents (`zenodo-20821423/`)

| File | Size (B) | SHA-256 | What it is |
|---|---|---|---|
| `Supplementary Code 3_input.deck` | 3376 | 60c0c480…bbfd | **EPOCH 3D input deck** for the 17 n_c filamentary-foam case (case B). |
| `Supplementary Code 1_filament_3D_17nc.py` | 16530 | d411865e…b094 | Python script: 3D random-walk filament density, mean 17 n_c, split into H⁺/C⁶⁺/O⁶⁺, written as EPOCH `.bin` density files. |
| `Supplementary Code 2_filament_3D_high.py` | 22118 | a5f5ad83…90c7 | Python script: the same, with a locally overdense focus region (0 < x < 10 µm, \|y\|, \|z\| < 4 µm) for case A. |
| `Descriptions of Supplementary Codes.txt` | 2691 | 42f3edad…04f1 | Authors' descriptions. **Note:** the descriptions for "Code 2" and "Code 3" are swapped relative to the filenames. Code 3 is the deck. |
| `Fig2_Fig6_data_with_description.xlsx` | 490629 | dac4c41e…d0b9 | Measured TOF data (Fig. 2) and simulated versus experimental maximum proton energies (Fig. 6). |

## Key deck parameters (read, not run)

- **Grid:** nx, ny, nz = 2500×250×250 over x ∈ [−10, 190] µm and y, z ∈ [−10, 10] µm (dx = 80 nm). t_end = 3000 fs. MPI layout 50×4×4.
- **Boundaries:** `simple_laser` at x_min, open at x_max, periodic in y and z.
- **Laser:** λ0 = 0.81 µm, FWHM spot 1.6 µm, Gaussian focus at x = 0, τ_FWHM = 45 fs, I = 5.48×10^21 W/cm², linear polarization (pol_angle = 0).
- **Species:** electrons, C⁶⁺, H⁺, O⁶⁺, each with 10 ppc and T = 10 keV. Densities are read from **absolute HPC paths** (`/vol0004/...fil3d_n17_1/*.bin`); edit these before use.
- `restart_snapshot = roll0001.sdf` is set. **Remove it for a fresh run.**
- **Outputs:** Ex, Ey, Bz, number density, particle px/py/pz/id/energy every 80 fs; rolling restart every 40 fs.

## Notes for reuse in MCF

- Case A (5 n_c, 3.07×10^21 W/cm²) uses the same deck with a different intensity and density files.
- This is a full-3D, 1.56×10^8-cell problem, i.e. HPC scale. The authors' absolute paths point to a large shared HPC file system. For MCF, a 2D or quasi-3D reduction of the same physics (near-critical slab, slow laser front, proton trapping in the bow wake) is the practical starting point.
