# SOURCE: Nanoparticle / cluster / microsphere-assisted proton acceleration and NP-assisted LWFA injection: no public inputs found

- **Checked:** 2026-10-27
- **Result: no input decks, code or data are public** for any of the papers below. Nothing was downloaded. Full notes are in `docs/research/proton-wakefield-and-nanoparticles.md` (N1–N13).

## Papers and codes

| Paper | Topic | Code | Availability |
|---|---|---|---|
| Vallières, Barberio, Scisciò, d'Humières, Antici, PRAB 22, 091303 (2019), DOI 10.1103/PhysRevAccelBeams.22.091303 | **"Enhanced laser-driven proton acceleration using ultrasmall nanoparticles"** (10 nm Au/Ag NPs on Al; TNSA) | PICLS 2D3V (not public) | No data statement. No inputs. |
| Mehrangiz, PoP 28, 123103 (2021), DOI 10.1063/5.0072087 | Au-NP-layered gas-filled nanosphere | EPOCH 2D | Paywalled. Not found. |
| Jinno et al., Sci. Rep. 12, 16753 (2022), DOI 10.1038/s41598-022-18710-x | micron H₂ clusters, J-KAREN-P | EPIC3D (in-house) | No inputs. |
| Matsui, Fukuda, Kishimoto, PRL 122, 014804 (2019), DOI 10.1103/PhysRevLett.122.014804 | 300 MeV from H cluster (shock + RIT) | 3D PIC (EPIC3D presumably) | Paywalled. Not found. |
| Nishihara et al., J. Phys. Conf. Ser. 688, 012076 (2016) | 450 MeV from 700 nm CH particle, a ≈ 100 | 3D PIC | Not found. |
| Hilz et al., Nat. Commun. 9, 423 (2018), DOI 10.1038/s41467-017-02663-1 | levitated 1 µm PMMA sphere, PHELIX | PIConGPU 3D (open source, GPLv3) | No per-paper deck found on Zenodo or GitHub. |
| Ostermayr et al., PRE 94, 033208 (2016) | isolated spheres, Texas PW | 3D PIC | Not found. |
| Cho, Pathak, Kim, Nam, Sci. Rep. 8, 16924 (2018) | NP-assisted electron injection | JoPIC (in-house) | No inputs. |
| Aniculaesei et al., PR Applied 12, 044041 (2019); MRE 9, 014001 (2024) | NP-assisted LWFA (electrons) | OSIRIS (2019) | No inputs. Patent 17/845,223. |
| Xu et al., Sci. Rep. 12, 11128 (2022) | Cu-NP insertion injection (electrons) | VORPAL 3D | No inputs. |

**Searched:** Zenodo API ("nanoparticle wakefield", "nanoparticle proton acceleration", "isolated proton bunch PIConGPU", "hydrogen cluster proton PIC", "Hilz Ostermayr sphere"), GitHub repository search ("nanoparticle wakefield"), and data statements in the open-access papers.

## Rebuild parameters

### Vallières 2019 (PICLS 2D3V)

- **Laser:** p-polarized, 5×10^20 W/cm² (a0 ≈ 15), τ = 25–300 fs.
- **Grid:** dx = dy = 2 nm (1 nm for the size scans), dt = 6.6 as. 24200×420 cells, periodic transverse boundaries, 20 ppc.
- **Target:** a layer of 20 nm Au spheres (diameter scanned 5–100 nm, gap scanned 0–400 nm) on a 500 nm Au foil (2500 n_c), with a 20 nm H layer (15 n_c) at the rear.

### Hilz 2018 (PIConGPU 3D3V)

- **Box and grid:** 104×139×104 µm, 30 nm cells (3456×4624×3456), dt = 57.5 as.
- **Target:** PMMA (C5O2H8) Gaussian plasma, peak 0.8 n_c, σ = 3.06 µm.
- **Laser:** a0 = 17, 13.5 µm spot, 500 fs, linear polarization, λ = 1.054 µm.

### Jinno 2022 (EPIC3D)

- **Box:** 10.24×20.48×10.24 µm.
- **Target:** a single H cluster (0.33–2.0 µm diameter) at n_e = 4.6×10^22 cm⁻³ (26.8 n_c), in 0.024 n_c H gas.
- **Laser:** λ = 810 nm, a0 ≈ 7.8.

### Cho 2018 (JoPIC 3D)

- **Grid:** 1500×313×313 cells, dz = λ/40, dx = dy = λ/5. 2 ppc in the plasma, 8000 ppc in the NP.
- **Plasma:** n0 = 7×10^18 cm⁻³ with a 100 µm ramp.
- **NP:** 100 nm, 2×10^23 cm⁻³, at 400 µm.
- **Laser:** a0 = 1, 16 fs, W0 = 17.6 µm.

### Xu 2022 (VORPAL 3D)

- **Grid:** 200×160×160 µm window, 2000×800×800 cells. 1 ppc background, 10^4 ppc in the NP.
- **Plasma:** n0 = 3.5×10^17 cm⁻³.
- **Laser:** 2×10^19 W/cm², 35 fs, 70 µm FWHM.
- **NP:** 100 nm, 100 n_c, at x = 100 µm.

## Open-source starting points (not downloaded)

- **PIConGPU** (https://github.com/ComputationalRadiationPhysics/picongpu, GPLv3+). It is already partly mirrored in `../tweac-picongpu/` by another task. A mass-limited-sphere setup would have to be written; none ships with the code.
- **EPOCH** (GPL) can load arbitrary density files, as in the bow-wake deck in `../bow-wake-isayama2026/`. Nanoparticle arrays or clusters can be generated with a script and loaded the same way.
