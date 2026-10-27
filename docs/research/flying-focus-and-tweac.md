# Flying focus, dephasingless LWFA and TWEAC: literature notes

Purpose: these notes support the MCF project, which aims to design an energy-efficient LWFA for **protons up to about 6 GeV**. The key question is whether a wake's phase velocity can be made **subluminal and time-varying (accelerating)** so that it stays velocity-matched to protons that start slow.

Compiled: 2026-10-27. Each statement carries one of these labels:
- **[paper]**: read in the full text
- **[abstract only]**: taken from the abstract or listing
- **[press]**: from a press release or news piece
- **[inference]**: my own derivation or reasoning

Status log (appended as work proceeds):
- 2026-10-27: notes file created.
- 2026-10-27: all sources done.
  - Full text read: Sources 1b, 2, 3, 5, 6, 7a, 7b.
  - Press/standfirst only: Sources 1 and 4. nature.com is login-walled and no arXiv version exists.
  - original-sims folders created; see "Downloads".

**Bottom line [inference]:**
1. Wake phase velocity follows the drive's intensity-peak trajectory. Flying-focus optics (axiparabola plus echelon or DM), TWEAC tilt geometry (tan α = (1 − β0 cos φ)/(β0 sin φ)) and waveguide modal pulses can all, in principle, set *subluminal* speeds. The flying focus can also set *accelerating* trajectories.
2. Demonstrated velocity control is only about ±10^-3 around c.
3. For slow protons (β ≲ 0.9) an on-axis subluminal flying focus fails, because the drive duration is smeared by about Z_R(1/β − 1)/c. Gong et al. 2024 say the same and use a *transverse* flying focus, which reached 1.64 GeV protons in PIC with 0.8 kJ.
4. Laser energy is linear in acceleration length for every scheme. The electron cases need about 3–10 J per GeV of single-particle gain. The TFF proton case needs about 500 J/GeV.

---

## Source 1: Dephasingless LWFA of electrons using a flying focus (Nature Physics, 2026)

- **Citation:** C. D. Arrowsmith et al. (LLE, Univ. Rochester), "Dephasingless laser wakefield acceleration of electrons using a flying focus," *Nature Physics*, published online 10 July 2026. [press]
- **DOI:** 10.1038/s41567-026-03352-x
- **arXiv:** none found. I searched the arXiv API for `all:dephasingless` (8 hits, none of them this paper) and for `au:Arrowsmith_C` (5 hits, none of them this paper). nature.com redirects to the idp.nature.com login wall (one try only). **Access: abstract/press only.**
- **Sources actually read:**
  - LLE news page: https://www.lle.rochester.edu/news/flying-focus-laser-plasma-acceleration/
  - Univ. Crete listing: https://www.physics.uoc.gr/en/node/5210
  - thenote.app RSS mirror of the Nature standfirst
- **What is known:**
  - The experiment ran on the **MTW-OPAL** laser at LLE. [press]
  - The optics were an **axiparabola**, which has a radially dependent focal length and so produces an extended line focus, plus a **radial echelon**. The echelon's stepped mirror adds a radius-dependent time delay, which sets the speed of the intensity peak along the line focus. [press]
  - The flying focus was set to propagate at **c in the plasma** so that the electrons do not dephase. [press]
  - The press material describes the work as a "proof-of-concept experiment" and says "the dephasing limit can be overcome with a flying focus". [press: Nature standfirst]
  - The LLE page figure mentions "<25 fs" pulses, but only in a generic description of DLWFA, not as this shot's parameter. [press]
  - Next steps:
    - an NSF OPAL flagship experiment targeting **100 GeV electrons in a meter-long plasma**, with a stated path to the TeV scale
    - bespoke echelon optics made with a new in-house fabrication process, so that the focal velocity can be matched to the accelerating electrons [press]
- **Not available to me:** laser energy, plasma density and length, measured electron energy, charge, energy spread, and the comparison with a conventional focus. These need the full paper (institutional access) or a later arXiv posting.
- **Closest open-access proxies:**
  - Shaw et al., arXiv:2505.00157, "Path to a single-stage, 100-GeV electron beam via a flying-focus-driven LPA". It includes early MTW-OPAL axiparabola/echelon focus characterization. See Source 1b.
  - Palastro et al., arXiv:2606.20298 (Source 3), which shares several coauthors.
- **Relevance to protons:** the experiment demonstrates (per the press material) that the flying-focus intensity velocity is a real, controllable knob in a working LWFA. The demonstrated case is v = c (luminal). [inference]

## Source 1b (proxy for Source 1): Shaw et al., "Path to a single-stage, 100-GeV electron beam via a flying-focus-driven LPA" (2025)

- **Citation:** J. L. Shaw, M. V. Ambat, K. G. Miller, R. Boni, I. LaBelle, W. B. Mori, J. J. Pigeon, A. Rigatti, I. Settle, L. Mack, J. P. Palastro, D. H. Froula (LLE). Submitted to Phys. Plasmas.
- **arXiv:** 2505.00157 (30 Apr 2025)
- **DOI:** 10.48550/arXiv.2505.00157 (arXiv DOI; no journal reference listed)
- **Access: full text read [paper].**
- **Data/code:** data "available from the corresponding author upon reasonable request". No public inputs. [paper]

### Concept [paper]
- Two optics produce the flying focus:
  - The **axiparabola** is a parabola with deliberate spherical aberration. Near-field radius r maps to an on-axis focal position z(r) between f0 and f0 + L.
  - The **radial echelon** (a stepped mirror with λ/2 steps, so the phase fronts stay flat) adds a radius-dependent group delay τ(r). This sets the time at which each ring reaches its focus.
- Together they make the focal velocity v_f a design choice that is decoupled from plasma density.
- **An axiparabola alone gives an "uncontrolled and accelerating focal velocity"**. DLWFA needs the echelon to control it. [paper]
- **Optical demonstration of subluminal and superluminal focus:** Pigeon et al., Opt. Express 32, 576 (2024), used a broadband superluminescent diode, i.e. a CW all-optical test. [paper]
  - A **convex echelon gave v_f ≈ 0.9987c (subluminal)**.
  - A **concave echelon gave v_f ≈ 1.002c (superluminal)**.
  - The focal region spanned >50 Rayleigh ranges, with a diffraction-limited spot and a nearly transform-limited pulse, over cm scale.
- The Weizmann/LOA approach (axiparabola plus a refractive doublet that controls pulse-front curvature) measured superluminal and subluminal focal trajectories in 2024: Liberman et al., Opt. Lett. 49, 814 (2024). [paper]
- **Programmable trajectory:** the echelon is replaced by a deformable mirror plus an SLM. The DM sets the radial group delay and the SLM re-flattens the phase fronts. See Ambat et al., Opt. Express 31, 31354 (2023), demonstrated per ref [40] (CLEO 2025). This allows **arbitrary v_f(z) trajectories**, including accelerating ones. [paper]
- Related ref [39]: Palastro et al., "Arbitrary-velocity laser pulses in plasma waveguides," arXiv:2503.15690. [paper; to follow up]

### Scaling laws (Appendix, eqs. A1–A3) [paper; garbled PDF extraction reconstructed, see check below]
- Assumptions (A1):
  - λ = 1.054 µm
  - k_p w0 = k_p R = 2√a0 (matched bubble, Lu et al. 2007)
  - ω_p τ_laser = √a0
- **Traditional LWFA:**
  - L_deph ≈ (2/3)(ω0/ω_p)² R ∝ a0^{1/2} n^{-3/2}
  - U_e ∝ a0 n^{-1}
  - U_laser ≈ (π/2) I w0² τ ∝ a0^{7/2} n^{-3/2}
  - N ∝ a0^{3/2} n^{-1/2}
  - efficiency η = N U_e / U_laser ∝ a0^{-1}
- **DLWFA:** L is a free variable.
  - **U_e = m_e c² (k_pR/2)(k_pL/2) ∝ L a0^{1/2} n^{1/2}**
  - **U_laser ≈ 8 I w0² τ_laser (λ L / w0²) ∝ L a0^{5/2} n^{-1/2}**. The **laser energy is linear in the acceleration length L**: the line focus has to deposit a w0-sized, τ-long relativistic spot at every point along L.
  - N ∝ a0^{3/2} n^{-1/2}. This is the same as LWFA and **independent of L**.
  - **η = N U_e / U_laser ∝ n^{1/2} a0^{-1/2} λ^{-1}**. This is **independent of L** and rises with density, which shorter pulses allow.
  - **Check [inference]:** I w0² τ ∝ a0²·(a0/n)·(a0^{1/2} n^{-1/2}). Multiplying by λL/w0² ∝ L n / a0 gives L a0^{5/2} n^{-1/2}, which matches A3. So A1 really is k_p w0 = 2√a0 and ω_p τ = √a0 (the PDF dropped the square roots).
- **Crossover:** DLWFA needs **less laser energy than traditional LWFA when τ < 21.1 fs** (Fig. 3). For longer pulses DLWFA still reaches higher maximum energy but is less efficient. [paper]
- Fig. 3/4 curves assume a0 = 2. [paper]
- **m-stage LWFA comparison:** stage length = L/m, so density rises by m^{2/3}. [paper]

### Design numbers [paper]
- **OSIRIS DLWFA, MTW-OPAL-like case** (Miller et al., Sci. Rep. 13, 21306 (2023), arXiv:2308.13432):
  - Laser: λ = 1054 nm, 6.2 J, 15 fs
  - Optics: f/7 axiparabola with f0 = 0.7 m, 5 cm radius, and focal range L = 2 cm
  - a0 = 3 in vacuum, 2 in plasma
  - Plasma: n = 7×10^18 cm^-3, 2 mm plateau, 90% He / 10% Ar (pre-ionized to Ar8+, ionization injection)
  - **Result: 2.1 GeV max gain over 20 dephasing lengths, 25 pC, 1.8% average energy spread, 0.7% laser-to-beam efficiency.**
  - **Consistency check [inference]:** Shaw's text says the plateau "was 2 mm in length". But with a0 = 2 at 7e18 cm^-3 and 1054 nm, L_d ≈ (4/3)(n_c/n)R ≈ 1.1 mm, so 20 L_d ≈ 2 cm, which matches L = 2 cm. "2 mm" is probably a typo for 2 cm. Check against Miller et al., Sci. Rep. 2023 before reproducing.
- **Scaled OSIRIS runs** (7 mm, neutral H2 vs neutral He gas):
  - Plasma: n = 7×10^18 cm^-3 after full ionization
  - Laser: λ = 920 nm, 23.4 fs FWHM, 4.7 J (3.4 J after apodizing the inner 50% of radius)
  - Optics: f0 = 63 cm, L = 7.8 mm, 4.5 cm radius
  - **v_f slightly superluminal in plasma** so that the back of the bubble stays at fixed phase.
  - Findings:
    - **He: refraction at two ionization fronts splits the drive and wrecks the wake.**
    - **H2: minimal splitting.** H2 is recommended.
- **MTW-OPAL experiment** (activated summer 2024):
  - Laser: 6 J, 22 fs FWHM, 920 nm (OPCPA)
  - Optics: axiparabola designed for L_des = 7.8 mm at f0 = 630 mm with D = 90 mm. The **measured usable focal range was 3.7 mm** (FWHM of peak fluence), shortened because the real near field is an ~80 mm polygon. The spot was round to ~1 µm.
  - Predicted electrons: 500–800 MeV. The first DLWFA campaigns were planned from April 2025 and are presumably what the Nature Physics 2026 paper reports [inference].
- **Phase 3 (NSF OPAL Beta beam):** 30 J round, 20 fs, predicts **~7 GeV**. The plasma source is ~5× longer than in the 6 J design.
- **Phase 4 flagship:**
  - 375 J (round-apodized from 500 J), 20 fs, predicts **100 GeV in <1 m, 25 pC**.
  - Earlier scaling: 500 J / 20 fs gives 125 GeV in 1 m.
  - Needs meter-scale echelon/axiparabola optics, a ~1 m large-aperture plasma source, and a 100 GeV spectrometer.
- **Codes:**
  - OSIRIS: full PIC, flying focus implemented, plus the generalized structured-pulse method of Pierce et al., PRR 5, 013085 (2023)
  - QPAD: quasi-static, planned for 10 cm to 1 m scale runs
  - Planned: a Lorentz-boosted-frame flying focus in OSIRIS (~40× speedup)

### Limitations [paper]
- Ionization-front refraction is an open question.
- The usable focal range is sensitive to the near-field fill.
- The focal spot degrades at the far end because the outer rays carry exaggerated spherical aberration.
- Energy is bounded only by available laser energy, but **energy cost grows linearly with L**.
- The energy-scaling curve **efficiency is only ~0.7%** in the 6 J design.

### Relevance to protons [inference]
- Demonstrated optical v_f ranges from 0.9987c to 1.002c. For comparison, a 6 GeV proton has β = 0.9908 (γ = 7.40), and β = 0.9987 corresponds to a ~17 GeV proton (γ ≈ 19.6). The echelon/DM approach controls **group delay vs radius**, and in principle a delay τ(r) can map any z(r) onto any arrival time.
- **The axiparabola-alone case has an intrinsically accelerating focal velocity**, which is exactly the kind of trajectory a proton booster needs. It still has to be designed to the proton β(z).
- The fundamental issue for slow protons is **not the focus velocity but the plasma wake**:
  - The wake phase velocity follows the driver's intensity peak, v_wake = v_f, only if the plasma response is quasi-static and local.
  - If v_f ≪ c, the "driver" is a moving intensity spot made of different light rings, each of which still moves at ≈ c.
  - Wake excitation needs the spot duration (as seen by the plasma) to be about 1/ω_p.
  - These conditions need checking for β ≪ 1. Literature on that is sought in Source 7.

## Source 2: Liberman et al., "Electron Acceleration in a Flying-Focus Laser Wakefield Accelerator" (Weizmann, 2026)

- **Citation:** A. Liberman, A. Golovanov, S. Smartsev, A.-M. Talposi, S. Tata, V. Malka (Weizmann Institute).
- **arXiv:** 2604.05771v1 [physics.acc-ph], 7 Apr 2026. This is the long-form companion.
- **Companion letter:** "First electron acceleration in a tunable-velocity laser wakefield," Phys. Rev. Research (2026), arXiv:2509.21098.
- **Access: full text read [paper].**
- **Data/code:** "raw data ... as well as the code, can be made available upon reasonable request". Nothing is public. [paper]

### Laser and optics [paper]
- **Laser:** WIS HIGGINS 2×100 TW Ti:Sa, double CPA, **1.5 J, 27 fs, 800 nm, 30 nm bandwidth**. Near field ≈ 50 mm diameter, quasi-top-hat.
- **Axiparabola:**
  - Focal map **f(r) = f0 + δ (r/R)²**, with f0 = 480 mm (f/9.6) and focal depth δ = 5 mm.
  - 10° off-axis.
  - Produces a quasi-Bessel beam whose ring structure develops along the focal line.
- **Velocity control:** pulse-front curvature (PFC), written as a spatio-spectral phase **φ = α r² (ω − ω0)**. This is a radial group delay τ(r) = α r².
  - Set by moving a doublet lens inside the beam-expanding telescope.
  - Values used: **α = −0.0045, +0.0055, +0.0190 fs/mm²**.
  - The doublet shifts the focus by up to 400 µm, so the gas jet was moved to compensate. Pulse-front tilt was re-optimized at each position.
  - Measured with far-field beamlet cross-correlation.
- **Vacuum velocity of the intensity peak** (Eq. 1, from Liberman et al., Opt. Lett. 49, 814 (2024)): v_z(z)/c = 1 + [terms linear and quadratic in z that depend on R, δ, f0 and α].
  - **α < 0 is superluminal and α > 0 is subluminal (in vacuum)**. The measured v_z/c − 1 is of order 10^-3 (Fig. 4a). [paper]
  - The exact Eq. (1) was garbled in the PDF extraction. The first-order reconstruction below has the same structure. [inference]

### First-order formula, derived [inference]
- Setup: an axiparabola with focal map z(r) = f0 + δ r²/R² and an extra radial group delay τ(r). The paraxial geometric arrival time of the ray from radius r at its focus is
  - c·t(z) = const + z − R²(z − f0)²/(4 f0² δ) + c·τ(r(z)), with r(z)² = R²(z − f0)/δ.
- Axiparabola alone:
  - **v_f/c ≈ 1 + R²(z − f0)/(2 f0² δ)**. This is superluminal and *accelerating*, consistent with Shaw et al.'s "uncontrolled and accelerating focal velocity".
  - For WIS numbers, v/c − 1 goes from 0 to R²/(2f0²) ≈ 1.4×10^-3 over the 5 mm.
- With PFC τ = α r²: **v_f/c ≈ 1 + R²(z − f0)/(2 f0² δ) − c α R²/δ**.
  - For α = 0.019 fs/mm², R = 25 mm, δ = 5 mm: c α R²/δ ≈ 7×10^-4. This is the right order compared with Fig. 4a.
- **General design rule (any trajectory):** choose τ(r) = t_target(z(r)) − t_axi(z(r)), where t_target(z) = ∫dz/v_target(z). This is the principle behind echelons and DM/SLM programmable flying focus (Palastro 2020; Ambat 2023).

### Plasma [paper]
- Slit nozzle: 0.5 mm × 7 mm.
- Gas: 97% He / 3% N2 (ionization injection), 30 bar backing.
- Density **n_e ≈ 4×10^18 cm^-3** (Fluent CFD; up to 4.2×10^18 in the PIC runs).
- Laser height 3 mm above the nozzle. Plasma radius from shadowgraphy: 340 µm to 220 µm.

### Results [paper]
- 20 shots per α.
- Electrons reached hundreds of MeV with tens of pC above 150 MeV.
- **Cutoff energy depends on α:**

  | α (fs/mm²) | Wake speed | Cutoff energy |
  |---|---|---|
  | −0.0045 | fastest | ≈ 400 MeV |
  | +0.0055 | middle | in between |
  | +0.0190 | slowest | ≤ 350 MeV |

  - The **≈ 50 MeV difference** is significant: p = 0.0004 (>3.5σ) between −0.0045 and +0.0055.
  - Charge does not shift significantly between those two cases, so beam loading is ruled out as the cause.
- Pointing jitter 5.5 mrad RMS. Divergence 1.5 mrad RMS. Energy uncertainty at cutoff ≈ 12 MeV.
- The faster wake is also more stable: 2/20 failed shots, versus 4–5/20 for the slowest.

### Simulations [paper]
- **Pipeline:** Axiprop (axisymmetric optical propagation through the axiparabola, on-axis version) → LASY file → **FBPIC** (quasi-3D spectral PIC). This is open-source tooling that I can reproduce.
- **Initial beam:** 16th-order super-Gaussian, 48 mm intensity-FWHM diameter, 1.5 J, 30 fs Gaussian. PFC applied as a phase before the axiparabola.
- **FBPIC settings:**
  - 2 azimuthal modes
  - box 558 µm (r) × 150 µm (z)
  - dz = 0.04 µm, dr = 0.24 µm
  - Lorentz-boosted frame γ = 3, with Galilean coordinates against numerical Cherenkov
  - focal line starts 4 mm into the gas
  - I_max = 1.32×10^19 W/cm²
  - neutral He + N2 gas (32+32 macroparticles per cell within r < 30 µm, 8+8 outside)
- **Simulated cutoffs:** 485 MeV (α = −0.0045) and 440 MeV (α = +0.019). This reproduces the ~50 MeV gap. Absolute cutoff and charge are higher than in the experiment because the simulation assumes an ideal optic.
- **In-plasma wake velocity does NOT simply equal the vacuum focal velocity plus a group-velocity correction.** The accumulated wake shift differs strongly from the analytic laser-peak shift (Fig. 4b). Causes:
  - different path lengths of the annular segments through the gas
  - different ionization times
  - evolving bubble size
- Even so, the wake-velocity ordering is preserved, with a >1 µm relative shift at 2 mm into the focal line.

### Analytic model (Sec. V) [paper]
- Bubble field: E_z(ξ) = (m ω_p²/2e) ξ = (e n_e/2ε0) ξ, with ξ = z − z0(t).
- Laser group velocity: v_gr = c(1 − n_e/n_c)^{1/2}, giving 0.9989c at 4×10^18 cm^-3.
- Wake phase velocity: **v_ph(z) = v_gr + Δv(z)**, where Δv is the vacuum flying-focus velocity correction.
- Electron phase evolution: dξ/dt = c − v_ph, so ξ(z) = ξ_min + ∫0^z (1 − v_ph/c) dz'.
- Momentum gain: p_z(z) = −(e² n_e/2ε0 c) ∫0^z ξ(z') dz'.
- The model overestimates the absolute energy, but predicts the right sign: about +70 MeV for the faster wake.
- **I can implement this as a 1D dephasing integrator for any v_ph(z)**, including subluminal proton matching. [inference]

### Limitations [paper]
- The mapping from vacuum v_f to in-plasma wake velocity is "highly non-trivial". It likely needs in-situ measurement.
- Ionization and refraction effects are significant.
- Only partial mitigation of dephasing was shown. The velocity changes are small (~10^-3).

### Explicit mention of ions [paper]
- The discussion says these techniques "can be extended to ... the laser-wakefield acceleration of ions [57]".
- **Ref [57] is Z. Gong, S. Cao, J. P. Palastro, M. R. Edwards, "Laser wakefield acceleration of ions with a transverse flying focus," Phys. Rev. Lett. 133, 265002 (Dec 2024).** This is a key paper for the proton design and is followed up in Source 7.

## Source 3: Palastro et al., "Dephasingless laser wakefield acceleration in a plasma waveguide" (2026)

- **Citation:** J. P. Palastro, K. G. Miller, C. D. Arrowsmith, R. Almeida, M. R. Edwards, A. L. Elliott, A. Kiewel, A. Konzel, L. S. Mack, D. Ramsey, D. Singh, A. G. R. Thomas, J. Vieira.
  - Affiliations: LLE, IST Lisbon, Stanford, Univ. Michigan.
- **arXiv:** 2606.20298v2 [physics.plasm-ph], 18 Jun 2026; v2 22 Jun 2026. No journal reference yet.
- **Access: full text read [paper].**
- **Data/code:** no availability statement. The code is OSIRIS (not open source; licensed via UCLA/IST).

### Concept [paper]
- A pulse is built from N radial (Laguerre-Gaussian) modes of a parabolic plasma waveguide, each at a different, sharply peaked frequency ω_q.
- Their interference makes an ultrashort on-axis intensity peak that travels at **any prescribed velocity v_a**, with constant spot size, while the overall envelope moves at v_g.
- The theory comes from ref [46], Palastro et al., "Arbitrary-velocity laser pulses in plasma waveguides," arXiv:2503.15690.

### Formulas [paper]
- **Waveguide profile:** ω_p²(r) = ω_p0² + 4c² r²/w⁴, where w is the matched spot size.
- **Mode dispersion:** k_q(ω) = (1/c)[ω² − ω_p0² − 4(1+2q)c²/w²]^{1/2}.
- **Arbitrary-velocity condition (Eq. 8):** **ω_q = ω0 + (k_q(ω_q) − k0) v_a**.
  - It is an intersection of each mode's dispersion hyperbola with the line ω = k v_a + κ, so in principle **any v_a, including subluminal**. [paper: general; this paper uses v_a = c]
- **Luminal case (v_a = c), with ω_p0 w/(2c) ≫ 1:**
  - Mode spacing Δ ≈ 2ω0 [2c/(ω_p0 w)]², and ω_q = ω0 + qΔ.
- **On-axis intensity (Eq. 14):** |a|² = (1/N²)|ψ(t − z/v_g)|² · sin²[NΔ(t − z/c)/2] / sin²[Δ(t − z/c)/2].
  - The peaks move at c and the envelope at v_g.
- **Peak timing:**
  - Recurrence period T_R = 2π/Δ.
  - Peak FWHM τ = πη/(NΔ), with η going from 1 to 0.88.
- **Stage length** (a peak slips through the envelope of duration T):
  - L_D = c v_g T/(c − v_g) ≈ 2 (ω0/ω_p0)² cT.
  - **Design** (τ = π/ω_p0 and T_R ≈ T): matched w = (2c/ω_p0)(ω0/ω_p0)^{1/2} N^{1/2}.
  - FWHM spot: w_F = (2c/ω_p0)(ω0/ω_p0)^{1/2}(2 ln2/η)^{1/2}.
  - **L_D = (2πc/ω_p0)(ω0/ω_p0)² 2N/η**.
- **Linear-regime wake** (a0 ≲ 0.5, τ = π/ω_p0): **e|E_z|/(m c ω_p0) = (π/8) a0²**.
- **Energy gain:**
  - DLWFA: Δγ_D = (π²/4)(2N/η)(ω0/ω_pD)² a0²
  - Standard: Δγ_S = (π²/4)(ω0/ω_pS)² a0², with L_S = L_d = 2πc ω0²/ω_pS³
- **Pulse energy:**
  - **U_D/(mc²) = (π c N/(4 r_e ω0 η))(ω0/ω_pD)⁴ a0²**. This is **linear in N, and hence linear in stage length L_D**.
  - U_S/(mc²) = (π c/(4 r_e ω0))(ω0/ω_pS)³(ω0/ω_pD) a0².
- **Ratios:**
  - Fixed density: Δγ_D/Δγ_S = N/η, U_D/U_S = N/η, and **energy per GeV is the same as standard LWFA**.
  - Fixed stage length: gain ratio = (N/η)^{1/3}, with equal U.
  - Fixed energy gain: L_D/L_S = (η/N)^{1/2} and U_D/U_S = (η/N)^{1/2}. **The pulse-energy saving equals the length reduction**, because DLWFA runs at higher density.
  - Key quote: "the energy required in the DLWFA pulse scales proportionally with the stage length, such that, in principle, the pulse does not incur an energy penalty relative to standard LWFA". [paper]
- **Peak power:** P/P_cr is identical to the standard pulse (Eq. 29), because w_F is the same.
- **Depletion length:** L_pd = c N ω0²/(a0² ω_p0³).
- **Plasma volume:**
  - Flying focus with an axiparabola: **V ≈ πL³/(12 f#²)**, because the plasma must fill the f-number cone to avoid refraction. This is a critical challenge for a 1 m stage.
  - Waveguide: V ≈ π N w² L = (ω_p0/ω0)³ L³/π, much smaller since ω_p0/ω0 ≪ 1.

### Simulation (Table I, App. B) [paper]
- **Code:** OSIRIS, quasi-3D (azimuthal modes m = 0, 1), moving window, customized dispersion-corrected solver.
- **Laser:** λ0 = 1 µm, a0 = 0.25/0.5/0.75, τ = 23 fs, w_F = 20 µm.
- **Plasma:** n(0) = 6×10^18 cm^-3 (1/ω_p0 = 7.24 fs, c/ω_p0 = 2.17 µm), 152 µm upramp.
- **Standard case:** w = 17 µm, L_d = 2.5 mm.
- **DLWFA case:** N = 10, Δλ = 13 nm (mode spacing), w = 54 µm, L_D = 2.8 cm. Envelope: 36 fs rise, 258 fs flattop, 36 fs fall (286 fs FWHM).
- **Grid:** window 178 µm × 323 µm, 4980 × 1490 cells, dt = 70.9 as, 109 ps total, 16 particles per cell.
- **Results:**
  - Externally injected 100 MeV electrons. At a0 = 0.5 the **gain is 660 MeV (DLWFA) vs 58 MeV (standard)**, the predicted 11× enhancement.
  - At a0 ≈ 0.75, self-focusing, depletion and redshift slow the peak and dislocate the wake phase. This is a stated limit.
- **Example 100 GeV design** (a0 = 0.5, 1 µm):
  - Standard: 10 stages × 10 GeV at 3.5×10^16 cm^-3 with L_S = 5.7 m each.
  - DLWFA (N = 10): 5 stages at 2×10^17 cm^-3 with L_D = 4.7 m each. **Total pulse energy is 2.4× lower.**
  - Spot sizes: w_D = 690 µm vs w_S ≈ 160 µm.

### Limitations [paper]
- Needs a highly structured multi-frequency, multi-mode pulse. Suggested routes: metasurface/SLM per frequency band, coherently combined fiber lasers, or plasma/gas diffractive optics. **This has not been demonstrated at high power.**
- Restricted to the linear or mildly nonlinear regime (a0 ≲ 0.5).
- Bandwidth grows with (N − 1)Δ.

### Relevance to protons [inference]
- Eq. 8 allows **any v_a**, so a subluminal luminal-peak design is formally possible. The ω_q spacing for v_a < c changes sign and structure and must be re-derived.
- **Time-varying (accelerating) v_a is not covered:** the mode frequencies fix one constant v_a.
- The energy scaling U ∝ L at fixed density carries over: the laser energy has to cover every metre of acceleration.

## Source 4: "Electrons surf farther on plasma waves," Nature Physics (21 Aug 2026)

- **DOI:** 10.1038/s41567-026-03410-4. Published online 21 August 2026. [press: Univ. Crete RSS listing https://www.physics.uoc.gr/en/node/5269]
- **Type:** almost certainly the News & Views piece on Source 1. Authors are not listed in the mirror. [inference]
- **Standfirst:** the energy gain of LWFAs is tied to the distance over which electrons are accelerated, and flying-focus pulses let electrons ride the plasma wave over longer distances. [press]
- **Access: standfirst only.** No numbers are available. nature.com is behind a login wall and was not retried.

## Source 5: Palastro et al., "Dephasingless laser wakefield acceleration," PRL 124, 134802 (2020)

- **Citation:** J. P. Palastro, J. L. Shaw, P. Franke, D. Ramsey, T. T. Simpson, D. H. Froula (LLE), Phys. Rev. Lett. 124, 134802, published 31 Mar 2020.
- **DOI:** 10.1103/PhysRevLett.124.134802
- **Erratum:** Phys. Rev. Lett. 130, 159902 (2023). I could not read its content. It probably concerns the nonlinear-regime scaling, which the later Miller et al. 2023 bubble-regime study revised to ~125 GeV in <1 m for 500 J [inference]. **Treat the "TeV in 4.5 m" claim as superseded.**
- **arXiv:** none found. I searched the arXiv API by title and author.
- **Access: full text read [paper]**, from the accepted manuscript via CHORUS: https://link.aps.org/accepted/10.1103/PhysRevLett.124.134802

### Concept [paper]
- Axiparabola (spherical aberration) plus a cylindrically symmetric **echelon** (λ/2-deep steps, so the phase fronts stay coherent) give an ultrashort pulse whose intensity peak travels **"at any velocity over any distance"**.
- The wake phase velocity equals the velocity of the ponderomotive force.
- Single cylindrically symmetric pulse, unlike TWEAC's two crossed tilted pulses.
- Explicitly: **"by adjusting the profile of the echelon, the ponderomotive force can be made to follow a dynamic trajectory, with either accelerations or decelerations"**. [paper]

### Linear-regime scalings [paper]
- **Energy gain:**
  - DLWFA: **W_D = (π/8)(k_pl L) a0²**, with k_pl = ω_pl/c and ω_pl = π/τ_l. The density is set by the pulse duration: **n_max = π² m ε0/(e² τ_l²)**, i.e. ω_p τ_l = π.
  - Traditional: W_T = (π/8)(k_p L_d) a0², with L_d = 2k0²/k_p³.
  - At the same length: W_T = (ω0 τ_l/π)^{2/3}(2cτ_l/L)^{1/3} W_D.
- Energies are in units of m_e c².

### Optics [paper]
- **Axiparabola focal map** (equal intensity per ring): f(r) = f0 + (r/R)² L. Phase ≈ −(k r²/2f0)[1 − L r²/(2 f0 R²)].
- **Echelon delay** τ(r) is chosen from ray optics to give v_f (Eq. 1; the exact form was garbled in extraction). Its structure is dτ/dr = (2Lr/(cR²))·[c/v_f − 1 + (geometric axiparabola term)], consistent with my Source 2 derivation. [paper/inference]
- **Echelon profile:** ech(r) = (1/4)[ceil(cτ/λ0)λ0 + floor(cτ/λ0)λ0]. The extra factor of 1/2 accounts for reflection, so the step depth is λ0/2 and each step is many λ wide, giving negligible diffraction loss.
- **Group-velocity correction:** for v_f = c in plasma, the **vacuum focal velocity is set to v_f/c = 1 + ω_p²/(2ω0²)**. The finite-spot correction δv_g = −1/(16 f#²) ≈ −1×10^-3 is neglected.
- Each ring sees different plasma dispersion on its way to focus. This is compensated with a **radially varying linear chirp**, e.g. chirped coatings on the echelon.
- **Density tolerance:** δω_p² < 2ω0²/(k_p L).

### Simulation, linear regime [paper]
- Laser: λ0 = 1 µm, τ_l = 30 fs, a0 = 0.5.
- Plasma: n0 = 3.5×10^18 cm^-3 (uniform).
- Optics: f# = f0/2R = 7, L = 8 cm.
- Method: modified-paraxial wave-equation propagation, Green's-function linear wake, test electrons injected at γ0 = 60.
- **Result: 1.3 GeV over 16 dephasing lengths**, versus 75 MeV for the v_f = v_g emulation of traditional LWFA. The paper also quotes 1.3 GeV in 8 cm vs 28 cm (~3.5× shorter).
- The laser energy for this run is **not stated**.
- **My estimate [inference]:**
  - Achromat at f/7: w0 ≈ 4.5 µm, z_R ≈ 63 µm.
  - Achromat-focus energy ≈ 3 mJ, times L/z_R ≈ 1270, gives **≈ 4 J for L = 8 cm**. That is ≈ 50 J/m, or ≈ 3 J per GeV at a0 = 0.5.
  - Cross-check: the paper says a "30 fs, 3 J kHz laser ... ~2 GeV" (linear regime).

### Laser-energy cost vs length (the key tradeoff) [paper]
- "Because the axiparabola distributes the energy density of the pulse over a length L, the pulse must contain **L/z_R more energy** for the same peak intensity (or a0) as a pulse focused by an achromatic lens".
- So **U_D ∝ L**: laser energy is linear in acceleration length at fixed a0, spot and density. This agrees with Shaw's U_laser ∝ L a0^{5/2} n^{-1/2}.
- Example: a **10 GeV gain needs one tenth of the distance but U_D ≈ 6 U_T**.
- Efficiency η = N W/U:
  - For that example U_D L_d ≈ 2 U_T L, giving η_D ≈ 2(A_D/A_T) η_T, where A is the accelerated-beam cross-section.
  - With w_T = π/k_p: **η_D ≈ 32 f#²(λ0/L_d)^{2/3} η_T ≈ 0.05 η_T**, i.e. about 5% of traditional-LWFA efficiency in this linear-regime example. The extraction is ambiguous on whether "0.05" is relative or absolute; I read it as relative.
- **Why:** most of the light at any instant is in rings that are not at focus, and the Bessel-like focus puts much of the energy into side lobes. The local power is moderate, and each ring is intense only within its own Rayleigh range.

### Trapping control with an accelerating focus [paper]
- Linear DLWFA traps electrons with initial momentum above
  - **p_th = γ_f β_f (1 + γ_f E_max) − γ_f [(1 + γ_f E_max)² − 1]^{1/2}**
  - where γ_f = (1 − v_f²/c²)^{-1/2}, β_f = v_f/c and E_max ≈ π a0²/8 (normalized).
- Starting at **v_f = 0.9c** traps slow electrons (γ0 ≈ 1.5). Accelerating v_f to c then stops further trapping, with p_th → 1 + 2/(π a0²).
- **This is the first explicit proposal of a subluminal, accelerating flying-focus wake trajectory** (for electrons). [paper]
- **Proton analogue [inference]:** apply the same Hamiltonian trapping threshold with m_p in place of m_e. For a proton, the normalized wake potential is reduced by m_e/m_p (E_max in units of m_p c² is 1836× smaller), so trapping protons from rest requires v_f very low, or pre-acceleration.

### Nonlinear (bubble) regime [paper, superseded per erratum]
- W_D = (1/2)(k_pl L) a0^{1/2}, with k_pl ≈ a0^{1/2}/(cτ_l).
- Claims: TeV in 4.5 m (a0 = 4, 15 fs, 1 µm), and "15 fs, 500 J → 100 GeV in a half-meter stage".
- Later LLE documents use 500 J/20 fs → 125 GeV in 1 m, and 375 J → 100 GeV.

### Limitations stated [paper]
- Higher laser energy is required for the same gain.
- Lower laser-to-beam efficiency.
- Needs a radially varying chirp to correct dispersion.
- Uniform density is required, with the stated tolerance.

## Source 6: Debus et al., "Circumventing the dephasing and depletion limits of laser-wakefield acceleration" (TWEAC), PRX 9, 031044 (2019)

- **Citation:** A. Debus, R. Pausch, A. Huebl, K. Steiniger, R. Widera, T. E. Cowan, U. Schramm, M. Bussmann (HZDR / TU Dresden), Phys. Rev. X 9, 031044, published 10 Sep 2019 (received 5 Mar 2018).
- **DOI:** 10.1103/PhysRevX.9.031044
- **License:** CC-BY 4.0, open access.
- **arXiv:** I could not find an arXiv version via the API (searched au:Debus AND au:Bussmann, and the title phrase). The open-access PRX PDF downloaded directly from journals.aps.org/prx/pdf/10.1103/PhysRevX.9.031044.
- **Access: full text read [paper].**

### Geometry [paper]
- Two ultrashort pulses, each line-focused by a **cylindrical mirror** onto the electron axis (y), arrive obliquely at **±φ** to the axis in the y–z plane.
- Each pulse carries a **pulse-front tilt α**. The overlap region, which carries the ponderomotive driver, slides along the line focus.
- The laser field is **continuously replenished from the side**. Each part of the pulse only crosses the interaction zone over the cycling distance
  - **L_cyc ≈ L_trans/sin φ**, with L_trans = min(Z0, R_p)
  - so depletion and self-phase modulation are bounded by L_cyc < L_dep, not by the total stage length L_int.
- The overlap moves at c, so self-injection is suppressed. Injection must be external, ionization, optical or density-ramp. The paper uses a density shock followed by a 620 µm downramp.
- **Pulse synthesis:** two extra gratings after the compressor (refs [38,42], the TWTS papers). The main challenge is pre-compensating group-delay dispersion from angular dispersion. **Below φ ≈ 10° little or no pre-compensation is needed.**

### Velocity formula: subluminal allowed [paper, Eq. A1]
- General matching condition (ref [39], Steiniger et al., the traveling-wave Thomson-scattering work):
  - **α = arctan[(1 − β0 cos φ)/(β0 sin φ)]**, where β0 is the target speed of the overlap region along the axis.
  - For β0 = 1 this reduces to **α = φ/2**.
- **Derivation check [inference]:** a tilted front translating along k̂ at c intersects the axis at speed
  - **β = 1/(cos φ + sin φ tan α)**
  - so any β0 > 0 can be reached by choosing α. **Subluminal and even very slow overlap speeds are geometrically allowed.**
  - Examples:
    - β0 = 0.43 (≈ 100 MeV proton): α ≈ 86° at φ = 5°, α ≈ 65° at φ = 60°, α ≈ 67° at φ = 90°.
    - β0 = 0.9908 (6 GeV proton): at φ = 5°, tan α = (1 − 0.9908·0.99619)/(0.9908·0.08716) ≈ 0.01297/0.08636 ≈ 0.150, so α ≈ 8.5°. Compare α = φ/2 = 2.5° for β = 1.
- **The paper does not discuss v ≠ c except as a pointing-error tolerance.** No ion or proton acceleration is mentioned (grep for "proton", "ion accel" and "hadron" found nothing). [paper]
- **Accelerating trajectory [inference]:** β0(y) varying along the axis needs a tilt α(y) that varies across the beam aperture, i.e. a non-planar (curved) pulse front, or a varying φ(y) from a non-cylindrical mirror. Neither is discussed in the paper.
- **Pointing tolerance (Eq. A2):** L_max < λ_p/(2 δφ tan(φ/2)).
  - For φ = 5°, n = 3.2×10^18, δφ = 10 µrad: L_max ≈ 21.4 m.
  - Slippage s = ∂β0/∂(angle) × δ; the slippage distance is d_s = s·L.
- **The overlap velocity is independent of plasma density** for a slit target that is translationally symmetric along the axis (App. A2). Refraction changes the arrival time but not the overlap speed. [paper]

### Laser energy vs length [paper, Eq. 4; reconstructed]
- Total energy for both pulses:
  - **W0 ≈ 2 × [2π² ε0 m_e² c⁵ a0²/(e² λ0²)] × √(π/(4 ln2)) τ0 × √(π/2) w_x × L_int sin φ**
  - ≈ 52.7 (ε0 m_e² c⁵/(e² λ0²)) a0² τ0 w_x L_int sin φ
- **Check [inference]:** a0 = 3.5, τ0 = 10 fs, λ0 = 0.8 µm, w_x = 1.2 µm, φ = 60°, L = 12.7 mm gives 92 J, matching the paper's 92 J. The 5° case gives 9.2 J, also matching.
- **W0 ∝ L_int sin φ**: linear in accelerator length, and smaller incidence angles are cheaper. Physically, the beam width needed is D = L_int sin φ.
- The minimum angle is set by L_cyc = L_dep: **φ_min ≈ 0.2°** for their parameters (Fig. 5b).
- At a given target energy: **W0 ∝ E_e n_e^{-1/2}**, the same as LWFA. "TWEAC and LWFA ... ultimately can only achieve the same energy efficiency."
- Characteristic metric: driver energy per LWFA depletion length.

### PIC simulations [paper]
- **Code:** PIConGPU 3D3V (beta-rc6, 0.3.1, 0.4.0).
  - Laser: Eq. (6) of ref [38], a TWTS pulse with tilt dispersion, injected via a total-field/scattered-field scheme.
  - Numerics: TSC shape, Vay pusher, Esirkepov deposition. Pre-ionized plasma.
  - Grid: 880 × 2304 × 2784 cells, cell size λ/12 × λ/20.9 × λ/20.9 (λ = 0.8 µm), box 58.5 × 88.4 × 106.8 µm.
  - Duration: 5×10^5 steps = 41.9 ps.
- **Baseline (Figs. 2–4):**
  - n_e = 3.2×10^18 cm^-3 plateau after a shock at 6.4×10^18.
  - τ0 = 10 fs FWHM, λ = 800 nm, φ = ±60°, tilt 30°, a0 = 3.5 per arm (7 in the overlap).
  - Line-focus height w_0,x = 1.2 µm, strongly over-focused, P/P_c = 0.06, Z0 = 20.1 µm.
  - Reference lengths: L_d = 5.7 mm, L_dep = 4.9 mm, L_int ≈ 12 mm.
- **Baseline results:**
  - **TWEAC:** linear energy gain to **984 MeV mean**, 17.1% rms spread, **177 pC**, with constant gradient over more than 2 L_d.
  - **LWFA reference:** 769 MeV peak, falling to 594 MeV with 13.5% spread and 78 pC.
  - TWEAC laser duration is constant to 3%. Laser drift < 4×10^-3 plasma periods.
  - **Cavity diameter (Eq. 3):** D_TWEAC ≈ max[λ_p/sin(φ/2), cτ0/sin(φ/2)]. This is 26.4 µm at 6.4×10^18 cm^-3, consistent with the simulation.
- **Table I** (4 cases; the column alignment was reconstructed from garbled layout text and checked for internal consistency):

  | Case | n_e (cm^-3) | a0 | Driver energy (J/L_dep) | Gradient (GeV/cm) | Charge (nC) | Laser energy per GeV | Laser→beam efficiency |
  |---|---|---|---|---|---|---|---|
  | LWFA | 3.2e18 | 7 (w0 = 7.9 µm) | 3.28 | 1.44 | 0.078 | 4.65 J/GeV | 1.68% |
  | TWEAC 60° | 3.2e18 | 7 | 35.6 | 0.752 | 0.177 | 96.6 J/GeV | 0.18% |
  | **TWEAC 5°** (crossed polarization) | 3.2e18 | 7 | 3.58 | 0.799 | 2.52 | 9.15 J/GeV | **27.6%** |
  | **TWEAC 3.5°** (App. C) | 2.5e18 | 6 | 2.36 | 0.995 | 1.77 | 3.78 J/GeV | **46.8%** |

  - The 5° case used 9.2 J over 12.6 mm, i.e. ≈ **0.73 kJ/m** at 0.8 GeV/cm.
  - The 3.5° case reached 330 MeV with 18.9% spread and a 2.2 × 4.8 × 13 µm bunch (rms).
  - The high efficiencies come from very heavy beam loading of the large, flat cavity (≈60 µm wide in z).
- **Polarization:** parallel linear polarization works for 30°–70°. Outside that range, use orthogonal linear or counter-rotating circular polarization to avoid optical-lattice transmissive modes.
- **Depletion along the approach (App. D):**
  - Etching speed v_etch ≈ c ω_p²/ω0² × f(a0); it scales as a0^-2 for a0 < 2.
  - For φ = 5° with a 1 mm-wide gas target, depletion and filamentation along L_cyc are < 5%.
  - **Constraint: the target width, not its length, sets the approach-path depletion.**

### Scaling and outlook claims [paper]
- A 1 PW laser could reach the 100 GeV level in a single stage at 10^19 cm^-3 (44 pC), versus 10 GeV/440 pC for LWFA at 10^17 cm^-3 with the same energy.
- **TeV at 1 GeV/cm over 10 m.**
- 10 TW-scale lasers would suffice for 1 GeV, which makes kHz operation plausible.

### Limitations [paper]
- Needs µm-scale line foci with high Strehl ratio.
- Needs tilt-dispersion pre-compensation.
- Parasitic injection into side cavities C1/C2.
- 3D PIC becomes expensive for long stages.
- Pointing-induced slippage.
- Large energy spread with heavy beam loading.
- Not yet demonstrated experimentally (as of 2019). I did not find a TWEAC experimental demonstration in this search. [inference]

## Source 7a (key for protons): Gong, Cao, Palastro, Edwards, "Laser wakefield acceleration of ions with a transverse flying focus," PRL 133, 265002 (2024)

- **Citation:** Z. Gong (Stanford; ITP-CAS), S. Cao (Stanford), J. P. Palastro (LLE), M. R. Edwards (Stanford), Phys. Rev. Lett. 133, 265002 (Dec 2024).
- **DOI:** 10.1103/PhysRevLett.133.265002
- **arXiv:** 2405.02690v2 (21 Dec 2024)
- **Access: full text read [paper]** (main text). The Supplemental Material (SM) holds the PIC parameters, optical design, Hamiltonian derivation, imperfection study and efficiency comparison, and was **not read**.
- **Code:** EPOCH (open-source PIC). No input decks are public as far as I found.

### Why a longitudinal subluminal flying focus fails for slow ions [paper]
- "**for subrelativistic flying-focus velocities, the finite Rayleigh length makes light field gradients in the longitudinal direction small [74], preventing the formation of the strong, slow-moving electrostatic fields required for ion acceleration**". The SM shows this.
- Ref [74] is Ramsey et al., PRA 107, 013513 (2023), "Exact solutions for the electromagnetic fields of a flying focus".
- **This is a direct negative result for the "slow on-axis flying-focus wake" idea for protons from rest.** [paper]
- Other routes they dismiss for ion LWFA:
  - near-critical density to slow v_g: hard plasma profiles
  - ions relativistic within one pulse: needs >300 PW
- **Physical reason [inference]:** in a longitudinal flying focus each ring of light still moves at c. When v_f ≪ c the intensity peak is a slowly sliding interference or focal pattern whose axial extent is about a Rayleigh length, so the axial ponderomotive gradient is weak, of order a0²/Z_R rather than a0²/(cτ). Equivalently, in 1D the cold-wake field limit scales like m ω_p v_p/e, which shrinks with β_p.

### Their solution: the transverse flying focus (TFF) [paper]
- The focal spot moves **perpendicular** to the laser k-vector, along x. The sharp transverse intensity gradient (spot size σ0) creates a strong charge-separation field E_x at the channel edge, and the spot motion can be **sub-relativistic and accelerating**.
- **Optics (axisymmetric):** axicon lens, spherical lens and axicon mirror with a chirped pulse. Chromatic dispersion makes ring foci of different radii per colour, and the axicon mirror collapses each ring onto the x axis at a colour-dependent position.
  - Alternatives: echelons, or time-varying-index optics.
  - **Not yet demonstrated experimentally.**
- **Focus trajectory (Eq. 1):** constant proper acceleration (hyperbolic motion), x_f(t) = (c²/α0)[√((α0 t/c)² + 1) − 1].
  - Matching requires α0 = e Z_i E_x/m_i.
- **Co-moving Hamiltonian (Eq. 2):** H(ξ, ξ̇) = ½ m_i ξ̇² + (e Z_i φ(ξ) + m_i α0 ξ)/γ̃³, with ξ = x − x_f and γ̃ = [(α0 t/c)² + 1]^{1/2}.
  - Trapping needs a local minimum of the total potential e Z_i φ + m_i α0 ξ.
  - **Trapping criterion: α0 < Λ ≡ e Z_i E_max/m_i.**
- **Analytic threshold (Eq. 3):**
  - **α0 < Λ ≈ Z_i m_e c² a0 (n_e/n_c)^{1/6}/(m_i σ0)**
  - It follows from e E_x ≈ F_p ≈ a0² m_e c²/(γ_e σ0) with γ_e ≈ a0 (n_e/n_c)^{-1/6} (PIC fit).
  - Validated in 2D PIC over a0, σ0, n_e and m_i (Fig. 4). The best energies come just below threshold.

### Numbers [paper]
- **Case 1 (2D/3D):**
  - Laser: I0 = 1.1×10^20 W/cm², λ ≈ 1 µm (T0 ≈ 3.3 fs).
  - Plasma: H, n_e = 0.05 n_c.
  - Focus acceleration α0 = 2×10^-4 c/T0.
  - **Result: 230 MeV protons after 1 mm**, 3.9% spread, 0.89° divergence.
- **Case 2 (3D):**
  - Laser: **0.8 kJ, 21 ps, 37.5 TW**, peak I0 ≈ 3×10^20 W/cm².
  - Plasma: H, **n_e ≈ 5.5×10^19 cm^-3**.
  - **Result: 1.64 GeV after 4.4 mm (6400 T0)**, 3.70% spread, 0.61° divergence, **23.1 pC**.
- **2D case (Fig. 3):**
  - Threshold Λ ≈ 7.8×10^-4 c/T0.
  - With α0 = 4×10^-4 c/T0, the measured mean gradient was **4.0 GeV/cm**, versus the predicted m_i α0 ≈ 4.1 GeV/cm.
  - With α0 = 1.2×10^-3 > Λ, ions slide and are not accelerated.
- **Efficiency:**
  - Laser to all protons: **≈ 0.13%**.
  - Effective monochromatic/collimated metric ≈ 10^-4 msr^-1 (SM).
- **Energy cost [inference]:**
  - 0.8 kJ/4.4 mm ≈ **180 kJ/m** of acceleration, or ~0.5 kJ per GeV of proton energy.
  - The 1.64 GeV × 23.1 pC beam carries ≈ 38 mJ, i.e. ≈ 0.005% of the laser energy in the monoenergetic peak.
  - The pulse duration has to cover the acceleration time (t ≈ L/⟨v⟩), so **at fixed power the energy is ∝ L**. Extrapolating to 6 GeV at ~4 GeV/cm gives L ≈ 1.5 cm, t ≈ 55–60 ps, and **≈ 2–3 kJ at ~40 TW**.

### Limitations [paper/inference]
- The optics (axicon, lens and axicon mirror with a chirped pulse) are only a concept.
- Robustness: moderate optical imperfections were checked in the SM.
- Wall-plug efficiency is very low.
- The plasma is near-critical-ish (0.05 n_c, ~5×10^19 cm^-3).
- Proton energy up to 1.6 GeV has only been simulated.

## Source 7b: Palastro et al., "Arbitrary-velocity laser pulses in plasma waveguides" (2025)

- **Citation:** J. P. Palastro, K. G. Miller, M. R. Edwards, A. L. Elliott, L. S. Mack, D. Singh, A. G. R. Thomas.
- **arXiv:** 2503.15690 (19 Mar 2025). No journal reference in the listing.
- **Access: full text skimmed [paper]**, targeted sections only.

### Velocity range and frequency rule [paper]
- "The peak intensity can travel **subluminally, superluminally, or backward**". The demonstrated cases are v_a = −c and 1.05c.
- **Prohibited velocities:** only a narrow subluminal interval around v_g0 (Eq. 12).
- **At v_a = 0 all modes share one frequency**, so there is no moving peak.
- Paraxial mode frequencies (Eq. 13): Δω_q ≈ ω0·v_a W_q^-2/[2(v_a − v_g0)].
- Recurrence period:
  - **T_R = (ω0 w²/2c²)|(v_a − v_g0)/v_a|**
  - Recurrence distance L_R = v_a T_R = ω0 w²/2c, about 2.2 mm in their example.

### Effective peak duration: the key constraint for slow peaks [paper]
- **Eq. 19: τ_eff ≈ (ω0 w²/(4c² q_max))·|(v_a − v_g0)/v_a|**
- The 1.05c peak is 20× shorter than the −c peak.
- **Consequence for slow (proton-matched) peaks [inference]:** the ratio τ_eff(β_a)/τ_eff(1) ≈ [(1 − β_a)/β_a]/(ω_p²/2ω0²).
  - For n = 4×10^18 cm^-3 at 0.8 µm (n/n_c ≈ 2.3×10^-3) and β_a = 0.5, the peak is ≈ 870× longer than a luminal peak with the same mode count.
  - To drive a wake you need τ_eff ≈ π/ω_p. That would require ~10³× more modes or bandwidth, or a much smaller w.
  - This is the waveguide version of the Gong et al. statement that slow on-axis foci have weak longitudinal gradients.
  - **Fundamental reason:** a slow-moving envelope built from light that moves at ≈ c needs enormous bandwidth to be temporally short in the lab frame.

### Simulations and outlook [paper]
- **Code:** QPAD (quasi-static, open source), zeroth azimuthal mode only.
  - Window: 10.3 ps × 96 µm (12288 × 8192 cells), Δs = 20 µm, 32 particles per cell.
  - Pulse: 7.7 ps FWHM (1.8 ps rise, 6.4 ps plateau, 1.8 ps fall).
- **Corrugated waveguides** could add luminal or subluminal *phase* velocity control. [paper]

## Source 7c: other related items found (abstract level)

- **Cao, Singh, Mack, Palastro, Edwards, "Flying focus with arbitrary directionality for spatiotemporal control of laser pulses"**
  - arXiv:2510.14195 (v2 Apr 2026). DOI 10.1103/fwcp-pv5c (a new-style APS DOI; the journal was not identified). [abstract only]
  - Method: a chirped pulse goes through a diffractive lens plus grating. Focal length, grating period and chirp set the direction and velocity of the focus, which can be **longitudinal or transverse**.
  - A holographic, gas/plasma-pumped grating is proposed for high power.
  - Lists **LWFA of ions** as an application. This is the optical route to Gong et al.'s transverse flying focus. [abstract only]
- **Pierce, Miller, Li, Palastro, Mori, "Laser wakefield acceleration driven by a discrete flying focus"**, arXiv:2506.19824 (Jun 2025). [abstract only]
  - A sequence of pulses with staggered foci and delays.
  - **150 J total gives 40 GeV per electron to 50 pC in a single 30 cm stage (50 dephasing lengths).**
  - Implied [inference]: ≈ 500 J/m, ≈ 3.75 J/GeV, and laser-to-beam efficiency ≈ 2 J/150 J ≈ 1.3%.
  - **A discrete sequence of pulses could in principle be timed to any v(z) trajectory**, including an accelerating proton trajectory. [inference]
- **Ambat et al., "Programmable and arbitrary-trajectory ultrafast flying focus pulses"**, arXiv:2307.05313; Opt. Express 31, 31354 (2023). [abstract only]
  - Design method for **arbitrary focal trajectories** with an axiparabola plus an echelon or a deformable mirror/SLM.
  - The web-search summary says it argues for starting subluminal (to trap) and then accelerating to luminal. That matches the Palastro 2020 trapping-control idea.
- **Miller et al., "Dephasingless laser wakefield acceleration in the bubble regime"**, Sci. Rep. 13, 21306 (2023), arXiv:2308.13432. [abstract and LLE summaries only]
  - OSIRIS run with 6.2 J/15 fs gives 2.1 GeV, 25 pC, 0.7% efficiency.
  - Projects 125 GeV in a sub-meter stage with 500 J.
  - An author correction (2024) fixed a figure misalignment.
- **Searches with no proton-specific flying-focus or TWEAC paper beyond Gong et al. 2024:**
  - arXiv API: `all:"flying focus" AND (ion OR proton)`, which returned only Gong 2024 and Cao 2025.
  - arXiv API: `all:"transverse flying focus"`.
  - Web searches: "flying focus proton acceleration subluminal wakefield 2025 2026" and "Nature Physics News & Views flying focus".
  - **I found no paper on TWEAC for ions or protons, and none on a subluminal on-axis flying-focus wake for protons.** [inference from search]
- **Older slow-light ion LWFA ideas** (cited by Gong et al.):
  - Brantov et al., PRL 116, 085004 (2016), "Synchronized ion acceleration by ultraintense slow light", which uses near-critical plasma
  - Shen et al., PRE 76, 055402 (2007), "Bubble regime for ion acceleration", which needs >300 PW
  - Not read here.

## Downloads (original-sims)

| Folder | Content | Public inputs? |
|---|---|---|
| `original-sims/tweac-picongpu/` | PIConGPU **TWEAC-FOM benchmark** (3.5° TWEAC .param/.cfg) plus the TWTS tilted-pulse laser model sources and PICMI wrapper. GPLv3+. 52 files, 0.4 MB. **The TWTS model has a `BETA_0` parameter for the overlap speed, so subluminal TWEAC can be set up directly.** Note: the benchmark scales a0 by 0.01 and uses n = 1.6e17 cm^-3, so it is not the PRX physics case. | Yes |
| `original-sims/flying-focus-lwfa-weizmann/` | **Axiprop** (Andriyash; BSD-3-style), the code used in Source 2. **axiprop_utils** (Golovanov; no license, local use only), with axiparabola models and `add_constant_velocity_phase(dv)` for any constant focal velocity. The paper's own FBPIC inputs are not public. | Partial (tools only) |
| `original-sims/flying-focus-dlwfa-lle/` | SOURCE.md only: no public inputs for LLE DLWFA (Sources 1, 1b, 3, 5, 7b). | No |
| `original-sims/transverse-flying-focus-ions/` | SOURCE.md only: Gong et al. EPOCH inputs not public. The arXiv source has no SM, and the APS SM is login-gated. | No |

Nothing was executed.

---

## Implications for slow-proton acceleration

Everything in this section is **[inference]**, built on the cited [paper] results unless marked otherwise.

### 1. Proton kinematics set the required wake-velocity trajectory

Python-computed table (m_p c^2 = 938.272 MeV):

| T (MeV) | gamma | beta | 1/beta - 1 |
|---|---|---|---|
| 10 | 1.0107 | 0.1448 | 5.90 |
| 100 | 1.1066 | 0.4282 | 1.335 |
| 200 | 1.2132 | 0.5662 | 0.766 |
| 500 | 1.5329 | 0.7579 | 0.319 |
| 1000 | 2.0658 | 0.8750 | 0.143 |
| 2000 | 3.1316 | 0.9476 | 0.055 |
| 6000 | 7.3947 | 0.99081 | 0.0093 |

- For constant gradient G, the required wake velocity is v(z) = c·β(T0 + G z).
- The required "focal acceleration" is a = G/(m_p γ³) in the lab frame, or a proper acceleration of eG/m_p. Gong's α0 = 2×10^-4 c/T0 corresponds to eG/m_p at G ≈ 190 GV/m.
- **Trapping and synchronism condition** (Gong Eq. 3; Palastro 2020 p_th): the drive must not accelerate faster than the wake field can push the proton, i.e. α0 < eE_max/m_p. This is the plasma analogue of the synchronous phase in an RF linac.

### 2. Can a wake be subluminal and accelerating? Yes in principle; it is a matter of optics

- **Longitudinal flying focus** (axiparabola plus echelon, or DM/SLM):
  - Any trajectory t(z) can be programmed with τ(r) = t_target(z(r)) − t_axi(z(r)) [paper: Palastro 2020; Ambat 2023].
  - Optically demonstrated so far: only 0.9987c to 1.002c [paper: Pigeon 2024], and α-tuned shifts of about 10^-3 in plasma [paper: Liberman 2026].
  - An axiparabola alone already gives an **accelerating** focus, v/c ≈ 1 + R²(z − f0)/(2f0²δ), but a superluminal one.
- **Delay budget** for an echelon or DM, total Δt = ∫(1/β − 1)dz/c (Python):

  | Start (T0) | G (GV/m) | Length L | Δt | c·Δt (reflective step depth = c·Δt/2) |
  |---|---|---|---|---|
  | 100 MeV | 10 | 0.59 m | 177 ps | 53 mm |
  | 100 MeV | 50 | 0.118 m | 35 ps | 10.6 mm |
  | 1 GeV | 10 | 0.50 m | 60 ps | 18 mm |
  | 10 MeV | 10 | 0.60 m | 249 ps | 75 mm |

  - This is far beyond DM stroke (tens of µm). It needs a deep stepped echelon or a discrete multi-pulse flying focus (Pierce 2025).
- **TWEAC** (Debus Eq. A1, [paper]):
  - The overlap speed is set by **tan α = (1 − β0 cos φ)/(β0 sin φ)**, so any β0 is possible.
  - PIConGPU's TWTS model exposes `BETA_0`.
  - Required pulse-front tilt α (deg):

    | Proton energy (β) | φ = 5° | φ = 30° | φ = 60° | φ = 90° |
    |---|---|---|---|---|
    | 10 MeV (0.145) | 89.2 | 85.3 | 82.3 | 81.8 |
    | 100 MeV (0.428) | 86.3 | 71.2 | 64.7 | 66.8 |
    | 1 GeV (0.875) | 59.3 | 29.0 | 36.6 | 48.8 |
    | 6 GeV (0.991) | 8.5 | 16.0 | 30.5 | 45.3 |

  - Large tilts mean large angular dispersion, and the GDD pre-compensation gets harder as tan²α.
  - An **accelerating** β0(y) needs a pulse-front tilt that varies across the aperture (a curved or chirped pulse front). It has not been proposed in the literature found.
- **Waveguide modal pulses** (Palastro 2025/2026, [paper]): any constant v_a (even backward), but no built-in acceleration. Slow peaks need enormous bandwidth (see point 3).
- **Transverse flying focus** (Gong 2024, [paper]): the only published scheme that actually accelerates **protons from rest** in underdense plasma (in 3D PIC), using a hyperbolic (accelerating) focal trajectory.

### 3. The physics obstacle for slow wakes is drive duration, not focus speed

- Gong et al. [paper]: with a subluminal *longitudinal* flying focus, "the finite Rayleigh length makes light field gradients in the longitudinal direction small", so a strong slow electrostatic field never forms.
- Waveguide analogue [paper, Eq. 19]: τ_eff ≈ (ω0 w²/4c²q_max)·|(v_a − v_g)/v_a|. The peak duration grows like (1 − β)/β.
- **My criterion [inference]:** for an axiparabola-type focus, light reaching a given z comes from a range of radii whose foci are blurred over an axial length Z_eff (a few f#²λ). Its arrival times are spread over **Δt ≈ Z_eff(1/β_f − 1)/c**. Resonant wake drive needs Δt ≲ 1/ω_p, so
  - **Z_eff ≲ (c/ω_p)·β/(1 − β)**
  - For n = 10^18 cm^-3 (c/ω_p = 5.3 µm):

    | T | β | Z_eff limit | Feasibility |
    |---|---|---|---|
    | 10 MeV | 0.145 | ≤ 0.9 µm | impossible |
    | 100 MeV | 0.43 | ≤ 4 µm | essentially impossible |
    | 1 GeV | 0.875 | ≤ 37 µm | needs ≈ f/2 to f/3 |
    | 6 GeV | 0.991 | ≤ 570 µm | easy |

  - Lower density relaxes this as n^{-1/2}. For example, at 10^17 cm^-3 and 1 GeV the limit is ≤ 118 µm.
  - **Conclusion: an on-axis (axiparabola) subluminal flying-focus wake is plausible only above roughly 1–2 GeV (β ≳ 0.9–0.95). Below that, a different geometry is needed.**
- **TWEAC-type geometry may evade this [inference, needs PIC check]:**
  - In the plane containing the axis and k, the beams are *collimated*. Axial position maps one-to-one onto the beam's lateral coordinate, so there is no Rayleigh-length blur.
  - A tilted pulse front keeps the local duration at τ0 at every point while the overlap slides at β0c. The overlap's axial length is β0·cτ0, which shrinks together with the slow-wake wavelength β·λ_p.
  - So subluminal TWEAC can in principle keep ω_p τ0 ≈ 1 at any β0.
  - Testable with the downloaded PIConGPU TWTS model by setting BETA_0 < 1.
  - Open issues: 3D cavity shape at φ > 30°, extreme tilt angles, and the polarization/lattice effects that Debus noted for φ outside 30°–70°.

### 4. Slow-wake field, potential and trapping limits [inference]

- **Cold 1D non-relativistic wave-breaking** at phase velocity v_p: E_WB ≈ m_e ω_p v_p/e = β_p E_0, where E_0 = m_e c ω_p/e ≈ 96 GV/m × (n/10^18 cm^-3)^{1/2}.
  - At 10^18 cm^-3: ≈ 41 GV/m at 100 MeV, 84 GV/m at 1 GeV, 95 GV/m at 6 GeV.
  - **The gradient is still huge, but the wake wavelength shrinks to β λ_p** (14 µm at 100 MeV and 10^18 cm^-3).
- **Potential well depth:** eΦ ~ m_e v_p² ≈ 0.5 MeV·β² (non-relativistic). This is tiny compared with the proton kinetic energy.
  - **Velocity acceptance:** δβ/β ~ √(2m_e/m_p) ≈ 3.3%. A slow wake can capture only protons already velocity-matched to within a few percent.
  - **Protons cannot be picked up from rest by an electron-plasma wake.** You need injection from a TNSA or RF source at the matching β, or the Gong transverse-flying-focus mechanism, which uses the channel-edge charge-separation field rather than a resonant wake.
- **Background-electron trapping:** with the Palastro 2020 threshold, p_th → small or negative as γ_f → 1. A wake with β_p ≲ 0.9 will trap copious plasma electrons. That means beam loading, dark current, and an energy sink.
  - This argues for **low a0 (linear regime)** at low β, or for the ion-specific TFF mechanism. TWEAC's luminal self-injection suppression does not carry over to slow wakes.

### 5. Energy cost vs acceleration length (all schemes: U ∝ L)

- **Flying focus (axiparabola):**
  - **U_laser ∝ L a0^{5/2} n^{-1/2}** at fixed a0 and n [paper: Shaw App. A].
  - "the pulse must contain **L/z_R more energy**" than an achromatic focus [paper: Palastro 2020].
  - η ∝ n^{1/2} a0^{-1/2} λ^{-1} is independent of L.
  - η_D ≈ 0.05 η_T in Palastro's 10 GeV linear example. The 6.2 J MTW-OPAL design gives 0.7%.
  - Plasma volume V ≈ πL³/(12f#²) [paper: Palastro 2026], which is cubic in L.
- **TWEAC:**
  - **W0 ≈ 52.7 (ε0 m_e² c⁵/(e²λ²)) a0² τ0 w_x L sin φ** [paper Eq. 4, reconstructed and checked].
  - Linear in L and in sin φ.
  - Efficiencies in PIC: 27.6% (5°) and 46.8% (3.5°), with nC-level beam loading [paper Table I].
- **Waveguide modal DLWFA:** U_D ∝ N ∝ L_D. "No energy penalty relative to standard LWFA" at fixed density [paper].
- **Discrete flying focus:** 150 J for 30 cm, i.e. 500 J/m [abstract].
- **Transverse flying focus (ions):** U = P·t_acc ≈ P·L/⟨v⟩. 0.8 kJ over 4.4 mm is about 180 kJ/m, and 0.13% of laser energy goes into all protons [paper].
- **Laser energy per GeV of single-particle gain** (from the cited numbers):

  | Scheme | Laser energy per GeV |
  |---|---|
  | LLE DLWFA OSIRIS case (6.2 J → 2.1 GeV) | ≈ 3 J/GeV |
  | Palastro 2020 linear case (≈ 4 J → 1.3 GeV, my estimate) | ≈ 3 J/GeV |
  | NSF OPAL flagship (375 J → 100 GeV) | ≈ 3.75 J/GeV |
  | Discrete flying focus | ≈ 3.75 J/GeV |
  | TWEAC 3.5° | 3.8 J/GeV |
  | TWEAC 5° | 9.2 J/GeV |
  | **Gong TFF protons** | **≈ 490 J/GeV** |

- **6 GeV proton estimate:**
  - Electron-like wakes, if velocity matching worked at the same gradient: tens of J to ~60 J.
  - The demonstrated-in-simulation TFF route: ~2–3 kJ (≈ 1.5 cm, ≈ 55 ps at ~40 TW).
  - The 100× gap is the cost of building a slow, strong electrostatic structure for heavy particles.

### 6. Suggested architecture to evaluate [inference]

1. **Low-β section (0 to ~1–2 GeV):**
   - Gong-type transverse flying focus (only published proton-from-rest scheme). Or an injector (TNSA or RF) followed by a **subluminal TWEAC** with β0(y) ramped by spatially varying tilt.
   - Must be tested in PIC: PIConGPU TWTS with BETA_0 < 1 first at constant β0, then piecewise-constant β0 stages.
2. **High-β section (β ≳ 0.9–0.95, T ≳ 1–2 GeV to 6 GeV):**
   - Axiparabola/echelon flying focus or TWEAC tuned to the proton β(z). Here the axial-blur criterion is satisfiable.
   - At 6 GeV the required 1/β − 1 = 0.0093 is ≈ 10× the demonstrated vacuum velocity tuning range (≈10^-3), so it needs a purpose-built echelon (delay span ~tens of ps).
3. **Energy-efficiency levers:**
   - small TWEAC angle φ (energy ∝ sin φ)
   - short τ (DLWFA is more efficient than LWFA for τ < 21 fs [paper: Shaw])
   - heavy beam loading
   - in the flying-focus case, a tighter f# and higher n
   - Avoid long axiparabola focal lines at low density: plasma volume and energy grow with L.

## Reproduction targets (numbers)

| # | Target | Key inputs | Expected result | Source |
|---|---|---|---|---|
| R1 | Palastro 2020 linear DLWFA (test electrons) | λ = 1 µm, τ = 30 fs, a0 = 0.5, n = 3.5e18 cm^-3, f/7 axiparabola, L = 8 cm, v_f(vacuum)/c = 1 + ω_p²/2ω0², test electrons at γ0 = 60 | 1.3 GeV over 16 L_d. The v_f = v_g emulation gives 75 MeV. W_D = (π/8)k_pl L a0². | [paper] |
| R2 | Miller 2023 / Shaw 2025 bubble DLWFA | λ = 1054 nm, 6.2 J, 15 fs, f/7 axiparabola (f0 = 0.7 m, R = 5 cm), L = 2 cm, a0 = 3 vacuum / 2 plasma, n = 7e18 cm^-3, He + 10% Ar (Ar8+ pre-ionized) | 2.1 GeV, 25 pC, 1.8% spread, 0.7% efficiency | [paper] |
| R3 | MTW-OPAL optics | 920 nm, 6 J, 22 fs (sim: 4.7 J/23.4 fs, 3.4 J after 50% apodization), f0 = 630 mm, L_des = 7.8 mm, D = 90 mm | measured focal range 3.7 mm. H2 avoids ionization-refraction splitting (He does not). Predicted 500–800 MeV. | [paper] |
| R4 | Weizmann flying-focus LWFA | 800 nm, 1.5 J, 27 fs (sim 30 fs, 16th-order super-Gaussian, 48 mm FWHM); axiparabola f0 = 480 mm, δ = 5 mm; PFC α ∈ {−0.0045, 0.0055, 0.019} fs/mm²; n ≈ 4e18 cm^-3, 97% He / 3% N2. FBPIC: 2 modes, 558 × 150 µm box, dz = 0.04 µm, dr = 0.24 µm, γ_boost = 3 | cutoff ≈ 400 vs ≤ 350 MeV in experiment, 485 vs 440 MeV in simulation, ~50 MeV gap | [paper] |
| R5 | Waveguide DLWFA | λ = 1 µm, a0 = 0.5, τ = 23 fs, w_F = 20 µm, n = 6e18 cm^-3, N = 10, Δλ = 13 nm, w = 54 µm, 286 fs envelope | L_D = 2.8 cm (vs L_d = 2.5 mm). Injected 100 MeV electrons gain 660 MeV vs 58 MeV standard. | [paper] |
| R6 | TWEAC 60° | 800 nm, 10 fs, a0 = 3.5 per arm, w_x = 1.2 µm, tilt 30°, n = 3.2e18 cm^-3 (shock 6.4e18 plus 620 µm downramp), 12 mm | 984 MeV mean, 17.1% spread, 177 pC. W0 = 92 J. | [paper] |
| R7 | TWEAC 5° (crossed polarization) | as R6 but φ = 5° | 9.2 J for 12.6 mm, 0.799 GeV/cm, 2.52 nC, 27.6% efficiency | [paper] |
| R8 | TWEAC 3.5° | a0 = 3.0 per arm, n = 2.5e18 cm^-3, 120 µm upramp to 5e18 cm^-3, 240 µm plateau, then shock | 0.995 GeV/cm, 1.77 nC, 330 MeV, 18.9% spread, 46.8% efficiency. PIConGPU TWEAC-FOM is this geometry. | [paper] |
| R9 | Gong TFF protons (3D) | 0.8 kJ, 21 ps, 37.5 TW, I0 ≈ 3e20 W/cm², H plasma n_e ≈ 5.5e19 cm^-3, hyperbolic x_f(t) with α0 below threshold | 1.64 GeV, 3.7% spread, 0.61°, 23.1 pC at 4.4 mm. Trapping threshold Λ = Z m_e c² a0 (n_e/n_c)^{1/6}/(m_i σ0). | [paper] |
| R10 | Gong TFF protons (2D) | a0 = 9, σ0 = 4 µm, n_e = 0.05 n_c, α0 = 4e-4 c/T0 (Λ ≈ 7.8e-4) | 4.0 GeV/cm average, vs predicted 4.1 GeV/cm | [paper] |
| R11 | Formula checks | TWEAC W0 formula; Shaw DLWFA scalings; Liberman analytic dephasing integrator ξ(z) = ξ_min + ∫(1 − v_ph/c)dz, p_z = −(e²n_e/2ε0c)∫ξ dz | R6/R7 energies (92 J, 9.2 J); η ∝ n^{1/2}a0^{-1/2}λ^{-1} | [paper/inference] |
| R12 | New test (proposed) | PIConGPU TWTS with BETA_0 = 0.9, 0.95, 0.99 at φ = 5–30° | wake phase velocity vs BETA_0; field amplitude vs β·E0; background-electron trapping | [inference] |
