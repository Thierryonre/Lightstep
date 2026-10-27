# Crilly et al. 2026: differentiable inverse design with a 500-parameter laser pulse

**Important:** the DOI the user supplied, 10.1103/bpms-63ml, resolves to an **inertial-confinement-fusion (ICF) implosion** paper. It is not an LWFA or laser-plasma-accelerator paper:

A. J. Crilly, P. Travis, J. P. Brodrick, J. B. Coughlin, A. S. Joglekar,
"High-dimensional inverse design of inertial fusion implosions via differentiable simulation",
Phys. Rev. Research **8**, 033353 (2026), published 23 Sep 2026. DOI: 10.1103/bpms-63ml. arXiv: 2606.08827 (v1, 7 Jun 2026).

- Retrieved: 2026-10-27.
- Licence of the published article: CC BY 4.0.

## Contents
| Path | What it is | Source URL | Licence | SHA-256 |
|---|---|---|---|---|
| `Crilly2026_PRResearch_8_033353_CC-BY.pdf` | Published paper | https://journals.aps.org/prresearch/pdf/10.1103/bpms-63ml | CC BY 4.0 | 0d0d5a8a2ad50b0d983b514da479cbac9fbfcac828a5c83aa55e69665b6cd749 |
| `related-code-adept-snapshot/adept-c0a8ef0.zip` | Snapshot of **ADEPT** ("Automatic-Differentiation-Enabled Plasma Transport", JAX), commit `c0a8ef023f763a764e94962c066198a196a30353`. 834 entries, 17.8 MB uncompressed. Left as a zip, not extracted and not executed. | https://github.com/ergodicio/adept (zip from codeload.github.com) | MIT | 67244f9e60fa5766a4c9916ba24aba7f7bdf3915548e3f85d01a0d3944265d07 |

## The paper's own code is NOT public
- Data Availability statement in the published version: "There are no publicly available research data or software supporting this manuscript. Requests for further information or data should be sent to the authors." Contact: ac116@ic.ac.uk.
- The implosion code is described as written in JAX with equinox, lineax, optimistix, optax and diffrax. It is not in ADEPT.
- **ADEPT is related code only.** It is maintained by Ergodic LLC, the employer of co-authors A. S. Joglekar and P. Travis. It is a set of differentiable plasma solvers (1D/2D Vlasov, 1D electrostatic PIC, 1D two-fluid, 2D laser-plasma envelope for TPD/SRS, Vlasov-Fokker-Planck). ADEPT has no radiation-hydrodynamics or implosion module and no LWFA module. It was downloaded as a public, MIT-licensed starting point in case a differentiable reduced plasma model is wanted for LWFA optimisation.
- What was searched: the paper's data statement; the arXiv listing (no ancillary files); GitHub (`differentiable implosion`, `inverse design implosion jax`, the user repositories of joglekara and acrilly, the ergodicio organisation).
