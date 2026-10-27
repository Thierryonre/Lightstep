# Nutting et al. 2026: Transversely Pumped Acceleration (TPA)

**Paper:** T. Nutting, N. Ernst, A. G. R. Thomas, K. Krushelnick (G. Mourou Center for Ultrafast Optical Science, Univ. of Michigan),
"Transversely pumped laser driven particle accelerator", Nature Communications **17**, 5949 (2026). Version of record 08 Jul 2026.
DOI: 10.1038/s41467-026-72697-x. No arXiv version was found.

- Retrieved: 2026-10-27.
- Licence: Creative Commons Attribution 4.0 (article, Supplementary Information and the Transparent Peer Review file are all marked CC BY 4.0).

## Contents
| File | What it is | Source URL | SHA-256 |
|---|---|---|---|
| `Nutting2026_NatCommun_TPA_article.pdf` | Main article (10 pp.) | https://www.nature.com/articles/s41467-026-72697-x.pdf | e095b3309192f536388550ca1cbf7d9c1ce051213bb4e41ed72624deed55002c |
| `Nutting2026_NatCommun_TPA_SI.pdf` | Supplementary Information: (I) derivation of the per-beamlet amplitude weighting for a programmable-velocity intensity peak; (II) monoenergetic 800 MeV, 1.9% electron case with localized injection | https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-026-72697-x/MediaObjects/41467_2026_72697_MOESM1_ESM.pdf | ab6f731c89b6a924866f6e9c9a88ff07fa19e08dd88f794830c06fbe243d421c |
| `Nutting2026_NatCommun_TPA_PeerReview.pdf` | Transparent peer-review file. Reviewer 3 is strongly critical of feasibility and scalability. | https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-026-72697-x/MediaObjects/41467_2026_72697_MOESM2_ESM.pdf | d3dfb51b60cb76243a96044cca0133d283d379ba41adafc0de89d5a7a9c5e4b3 |

## Simulation inputs and data: NOT public
- Data availability (quoted from the article): "The raw simulation outputs generated during this study comprise approximately 4 TB of data and are not publicly available due to their size ... The input files and processed datasets underlying all figures are available from the corresponding author upon request."
- Code availability (quoted): "The simulations were performed using a modified version of the OSIRIS 4.0 framework to enable exceptionally long input configurations required for this study. The modified source code is available from the corresponding author upon request."
- Public base code: OSIRIS is open source at https://github.com/osiris-code/osiris (AGPL-3.0). It was not downloaded. The modification for very long input decks (thousands of individually defined beamlets, produced by an "automated text file generator") is not public.
- What was searched: the article's data and code statements, the SI, GitHub (`transversely pumped`, `TPA wakefield`, `transverse pumped acceleration osiris`, user search for Nutting), and arXiv (no preprint found).
- All physical simulation parameters needed to rebuild the decks are in the Methods section. They are transcribed in `docs/research/phase2-and-laser-technology.md`, section 6.
