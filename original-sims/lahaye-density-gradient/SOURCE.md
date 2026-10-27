# Lahaye et al. 2026: density taper plus HOFI guiding (no simulation files are public)

**Paper:** R. Lahaye, I. A. Andriyash, J. Gautier, O. Kononenko, A. Leblanc, J.-P. Goddet, A. Tafzi, C. Thaury,
"Experimental demonstration of dephasing reduction in an optically guided laser-plasma accelerator",
Phys. Rev. Research **8**, 023274 (2026). DOI: 10.1103/pc2y-hxj9. arXiv: 2508.00145 (v1, 31 Jul 2025).

- Retrieved: 2026-10-26/27 by a research agent.
- Licence of the published article: CC BY 4.0 (stated on the article). The arXiv v1 is CC BY-NC-SA 4.0.

## Contents of this folder
| File | What it is | Source URL | SHA-256 |
|---|---|---|---|
| `Lahaye2026_PRResearch_8_023274_CC-BY.pdf` | Published version (12 pp., includes Appendices A and B: spectrometer and density profiles) | https://journals.aps.org/prresearch/pdf/10.1103/pc2y-hxj9 | bbf2a2d98067cca541a8a34afef8f7bf2e8dbf212920e83db1238662288f1c20 |

## Simulation inputs and data: not public
- The paper's Data Availability statement says: "The data that support the findings of this article are not publicly available ... The data are available from the authors upon reasonable request." Contacts: ronan.lahaye@ensta.org, cedric.thaury@ensta.fr.
- The simulations were run with **FBPIC**, an open-source pseudo-spectral quasi-cylindrical PIC code (https://github.com/fbpic/fbpic, BSD-3-Clause-LBNL). The paper does not give the numerical parameters (grid, modes, particles per cell). It does give the physical parameters (see `docs/research/phase2-and-laser-technology.md`, section 1).
- What was searched: the arXiv listing (v1 only, no ancillary files); the APS article page and its supplemental material (in the published version the supplemental figures became Appendix B); GitHub (`lahaye fbpic`, `pc2y-hxj9`, `dephasing density gradient fbpic`); and the GitHub account of co-author I. Andriyash (`hightower8083`). That account has no repository for this paper.
- A related public tool from the same group is **axiprop** (https://github.com/hightower8083/axiprop), an optical propagation code used for axiparabola focal-line modelling, which matters for HOFI channel-forming beams. It was not downloaded because it is not the paper's simulation.
