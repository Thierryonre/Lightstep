# SOURCE: Proton bubble/wake acceleration with vortex (LG) and light-spring drivers (Shen/Zhang group): no public inputs found

- **Checked:** 2026-10-27
- **Result: no input decks, code or data are public** for any of the papers below. Nothing was downloaded. Full notes are in `docs/research/proton-wakefield-and-nanoparticles.md` (S1, S2, S9).

## Papers and codes

| Paper | Code | Availability |
|---|---|---|
| Shen, Li, Yu, Cary, PRE 76, 055402(R) (2007), DOI 10.1103/PhysRevE.76.055402 | VORPAL 3D (likely) | Paywalled. No inputs. |
| Zhang et al., NJP 16, 123051 (2014), DOI 10.1088/1367-2630/16/12/123051, arXiv:1407.6467 | VORPAL 3D | No inputs. |
| Guo, Zhang, Shen, Tajima, HPLSE 12, e72 (2024), DOI 10.1017/hpl.2024.72 (CC-BY) | EPOCH 3D | No data statement or repository link in the PDF. |
| Willim, Vieira, Malka, Silva, PRR 5, 023083 (2023), DOI 10.1103/PhysRevResearch.5.023083 | 3D PIC (likely OSIRIS) | Not checked in detail. |

**Searched:** Zenodo API ("light spring proton", "proton wakefield laser"), GitHub repository search, and the papers' data-availability statements where readable.

## Rebuild parameters

### Guo et al. 2024 (EPOCH 3D; "light spring" → 8.7 GeV self-injected, 10.6 GeV witness)

- **Box and grid:** 80×60×60 µm moving window, 1000×800×800 cells, 1 ppc.
- **Plasma:**
  - Self-injection case: tritium with an H dopant (T:H = 70:1), n_e = 1.23×10^27 m⁻³, x = 10–800 µm, |y|, |z| < 27 µm.
  - Witness case: tritium, n0 = 6.9×10^26 m⁻³. Witness beam 4×2×2 µm, starting at x = 5 µm with E = 0.11 GeV.
- **Laser:** two symmetric light-spring pulses, 4.81 PW total. Each is a coherent sum of 7 LG modes:
  - l = 1…7, ω_n = (0.85…1.15) ω0, λ0 = 0.8 µm.
  - w0n = 16, 11.314, 9.238, 8, 7.155, 6.532, 6.047 µm, keeping w0n√l_n constant.
  - Sub-beam a_LG = 15, giving a_LS ≈ 100. Duration T = 16 µm.
  - The intensity profile follows their Eqs. (1)–(2).
  - The imperfect-LS case uses random beamlet phases and a_LG = 24, for 12.3 PW total.

### Zhang et al. 2014 (VORPAL 3D; LG10 → 1 to 7 GeV witness)

- **Box and grid:** 60×100×100 µm, 600×300×300 cells, 1 ppc.
- **Plasma:** tritium, 2.4×10^20 cm⁻³, 12–1000 µm, |y|, |z| < 35 µm.
- **Laser:** CP LG10. a = a0 (2r/r0) exp(−r⁴/r0⁴) e^{ilφ} sin²(πt/2t0), with r0 = 7 µm and t0 = 12.5T. Power equals a super-Gaussian pulse at 2.14×10^22 W/cm² (a0 = 70.7, λ = 0.8 µm).
- **Witness:** 3×1×1 µm, 160 pC, at x = 5 µm, 1 GeV.

## Open-source starting points (not downloaded)

- **EPOCH** (GPL, https://github.com/Warwick-Plasma/epoch). Laser blocks can superpose several LG modes using `profile`/`phase` expressions.
- An EPOCH deck structure close to these runs, for near-critical plasma, is in `../bow-wake-isayama2026/zenodo-20821423/`.
