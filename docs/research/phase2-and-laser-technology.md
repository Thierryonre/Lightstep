# Phase-2 optimisation papers and laser-driver technology for an efficient ~6 GeV proton LWFA

Compiled 2026-10-26/27 by a research agent for the MCF project, which aims at an energy-efficient, inexpensive laser-wakefield accelerator for ~6 GeV protons feeding muon production for muon-catalysed fusion.

**Provenance labels on every statement:**
- **[paper]**: read in the full text (published version and/or arXiv) or in the paper's Supplementary Information.
- **[abstract]**: only the abstract or listing was read.
- **[press]**: press release or news article.
- **[secondary]**: number taken from a report, talk slide or another paper that cites the primary source.
- **[my inference]**: my own calculation or judgement. Formulas derived by me are marked this way too.

The local copies of papers in `original-sims/*/` are listed in each folder's SOURCE.md.

Other notes in this folder cover related topics: `flying-focus-and-tweac.md`, `proton-wakefield-and-nanoparticles.md`, `resonant-multipulse.md` (Hooker 2014 and P-MoPA in depth), and `muon-production-and-mucf.md`.

---

## 0. Key points

1. **Lahaye et al. (PRR 2026).** A linear density **up-ramp** of 0.03 n0/mm (n0 = 9.1e18 cm^-3 background, about 3.4e18 cm^-3 on the HOFI channel axis) over a 12.8 mm guided plasma raised the cut-off energy from 1.1 to 1.6 GeV with about 1 J and 30 fs. FBPIC reproduces this through three effects: delayed injection, self-focusing, and slowing of the laser peak. [paper]
   - For **protons** the sign is reversed. Protons are slower than the wake, so the wake must be slowed: a down-ramp, a higher density, or spatiotemporal control. A density down-ramp alone cannot phase-lock protons over long distances (section 8). [my inference]
2. **DOI 10.1103/bpms-63ml is not an LWFA paper.** It is a differentiable-simulation inverse design of **ICF implosions**: a 500-parameter laser pulse, a JAX 1D Lagrangian hydrodynamics code, L-BFGS-B, and neural-network reparametrisation. Its code is **not public**. The method transfers to LWFA (gradient-based design of density profiles and pulse or beamlet timings). [paper]
3. **The "80% efficient palm-sized laser"** is a multipass **optical parametric amplifier** (Nature 2025). The 81% is a *photon conversion efficiency* inside the cell. The system photon efficiency is 52%, which is about 32% pump-to-signal power. It is **not** a wall-plug efficiency, and it ran at about 3 W, 76 MHz, roughly 40 nJ. It is not directly relevant to J-class drivers. [paper/SI] [my inference]
4. **Transversely Pumped Acceleration (Nat. Commun. 2026)** is a **plasma** scheme. Thousands of counter-propagating, delayed beamlets cross on a line focus and drive a wake whose phase velocity is set by the timing.
   - The authors simulated (2D OSIRIS) 95 MeV to 1.12 GeV protons in 3.6 mm (2 × 1200 beamlets of 290 mJ) and a 3D electron case with 7 mJ beamlets. [paper]
   - It explicitly allows an **arbitrary, accelerating, subluminal wake** and many low-energy lasers, which is what slow protons need. Its demonstrated laser-to-beam efficiency is only about 1e-5 (section 6). [paper] [my inference]
5. **Laser drivers.**
   - Ti:Sa sits at about **0.1% wall-plug**. [secondary]
   - Projected high-efficiency routes: coherently combined Yb fibre (Snowmass assumption **50% wall-to-laser**; ICAN target >30%), LLNL **Tm:YLF BAT** (**20% wall-plug** projected; 19% optical-to-optical measured in a burst; 1.59 J, 270 fs demonstrated), and thin-disk Yb (>50% optical-to-optical; ~1 J at 1 kHz, but ps pulses).
   - Best demonstrated combined-fibre results: 10 mJ/120 fs/1 kW (100 kHz) and 32 mJ/158 fs (20 kHz). [paper/abstract/secondary]

---

## 1. Lahaye et al. 2026: engineered density gradient plus optical (HOFI) guiding

### Citation and access
- R. Lahaye, I. A. Andriyash, J. Gautier, O. Kononenko, A. Leblanc, J.-P. Goddet, A. Tafzi, C. Thaury (LOA, ENSTA/CNRS/École polytechnique), "Experimental demonstration of dephasing reduction in an optically guided laser-plasma accelerator", **Phys. Rev. Research 8, 023274 (2026)**, published 10 Jun 2026. **DOI 10.1103/pc2y-hxj9**. **arXiv:2508.00145** (v1, 31 Jul 2025). Published version is CC BY 4.0.
- **I read the full text of both the published version and arXiv v1.** The published numbers differ in places; the published values are used below. Differences: n0 = 9.1e18 (arXiv: 8.6e18); 12° gradient 0.05 n0/mm (arXiv: 0.06); reference background density 1.7e19 (arXiv: 1.5e19); channel density 3.4e18 (arXiv: 3e18). [paper]

### Analytical model (implementable) [paper]
- Wake phase: φ(z,t) = π (z_L(t) − z)/r_B(z_L), with r_B ∝ n_e^{-1/2} and z_L the laser front.
- **Wake phase velocity in a density gradient (Eq. 2):**
  v_φ(ξ, z) ≈ v_g(z) [1 + (ξ/(2 n_e)) dn_e/dz],
  where ξ = z_L − z is the distance behind the laser front.
  - Validity: n_e/(dn_e/dz) ≫ λ_p and ≫ ξ, and r_B depends only on the local density. The authors call it "qualitative".
  - Consequences: an up-ramp gives v_φ > v_g; the excess grows with ξ; a steep up-ramp makes the wake superluminal (no injection).
- **Phase-locked ("optimal") profile (Eq. 3):** n_e(z) = n0/(1 − z/L0)^{2/3}, with L0 = (2/3) L_d0 and L_d0 the dephasing length at n0 (refs. Pukhov & Kostyukov 2008; Döpp 2016).
- **Electron phase (Eq. 4):** φ_e(z_e) = (π/r_B(z_e)) [∫_{z0}^{z_e} (v_g(z)/c − 1) dz + ξ0].
- **Bubble field (Eq. 5):** E_z = −(e n_e/ε0)(ξ_e − r_B).
- **Energy gain (Eq. 6):** Δγ = (q/mc²) ∫ E_z dz.
- **Linear profile (Eq. 7):** n_e(z) = n0 (1 + α z/L_d).
  - α = 1 is the best linear choice: Δγ ≈ 1.36 γ_max at z ≈ 0.88 L_d0.
  - α = 1.5 is initially superluminal, so injection is delayed to about 0.2 L_d, giving Δγ ≈ 0.94 γ_max.
  - α > 1 blocks early injection; α < 1 gives weaker dephasing mitigation.
- **Matched parabolic channel (Eq. 8):** n_e(r,z) = n0(z) + r²/(π r_e w0⁴), with w0 ≈ 21 µm (field waist radius).
  - Tapered-channel variant: w0 → w_m(z) = C(z) w0, with C(z) = (r_hole/f0) · z/(R e^{a(z − f0 − δ0)}) following the axiparabola-formed channel.
  - Ideal matching for a linear ramp needs a channel diameter ∝ z^{-1/2}. A constant-intensity axiparabola produces exactly this scaling.

### Experiment [paper]
| Item | Value |
|---|---|
| Laser | LOA "Salle Jaune". Driver 30 fs; 1.05 ± 0.05 J in the first zero ring (73% of total, so about 1.44 J total [my inference]); F/18 off-axis spherical mirror; D_FWHM = 26 µm; active pointing stabilisation (σ ≈ D_FWHM/6). Wavelength not stated; Salle Jaune is Ti:Sa, ~0.8 µm [my inference]. |
| Guiding | **HOFI** channel. Channel-forming beam 2.3 mJ, 30 fs, focused by an off-axis **axiparabola** (f0 = 200 mm, δ0 = 30 mm, R = 38.1 mm, r_hole = 6 mm, f(r) = f0 + (1/a) ln(r e^{aδ0}/R), a = ln(R/r_hole)/δ0) with deformable-mirror correction |
| Target | Slit gas jet (15 mm long for the reference and 8° cases; 20 mm for 12°) on a rotation stage; tilt angle sets the linear gradient. H2 + 1% N2. A 200 µm Si-wafer blade creates a shock for **shock-assisted ionisation injection** and sets the effective length. |
| Reference (flat) | Best cut-off **1.1 ± 0.06 GeV** at 27 bar, background n_e ≈ 1.7e19 cm^-3 (without channel); on-axis channel density ≈ 3.4e18 cm^-3. A 20 mm jet gave no further gain (depletion or guiding limit suspected). |
| **Best gradient (8° tilt)** | 26 bar, **n0 = 9.1e18 cm^-3** (background), **gradient 0.03 n0/mm**, **L_target = 12.8 mm**. Cut-off **1.6 ± 0.1 GeV** (×1.4). Charge above 1 GeV **4.2 ± 1.4 pC** (1.3 pC at 11.9 mm; 1.6 pC at 15.9 mm, where the cut-off falls to 1.2 GeV). Best single shot: electrons above **1.8 GeV**, 9.4 pC above 1 GeV, 3 pC above 1.5 GeV. |
| 12° tilt | n0 = 1.1e19, ≈0.05 n0/mm (non-linear profile). Cut-off < 1.15 GeV for all lengths (delayed injection from an initially superluminal wake). ≈15 pC above 200 MeV; 1.6 ± 0.9 pC above 1 GeV at 14.5 mm. Spectrum more peaked. |
| 3° tilt | Similar to 8° but slightly lower energy |
| Spectra | Continuous (ionisation injection and shock injection). Cut-off defined at 2.5 fC/MeV. Spectrometer resolution 2.1% at 1 GeV; total energy error 5.2% at 1 GeV and 7.9% at 1.6 GeV; charge error 28%. **No energy spread or emittance quoted** for the main result. |

### Simulations [paper]
- Code: **FBPIC** (pseudo-spectral, quasi-cylindrical; Lehe et al. CPC 203, 66, 2016). Numerical resolution, number of azimuthal modes and macroparticles are **not given**.
- Physical setup: Gaussian pulse, 1 J, intensity FWHM 25 µm, 25 fs, a0 ≈ 1.6; pre-ionised plasma with a preformed parabolic channel (Eq. 8).

| Case | Result |
|---|---|
| n0 = 6.2e17 cm^-3, flat vs. 0.06 n0/mm | Both reach 750–800 MeV. The gradient case does so in half the distance because the wake stays superluminal until z ≈ 10 mm, which delays injection. L_D0 ≈ 33 mm (Lu model); α_theo = δn·L_D0/n0 ≈ 2. |
| n0 = 1.0e18 cm^-3, flat vs. 0.08 n0/mm | L_D0 ≈ 15 mm, α_theo ≈ 1.2. The flat case dephases after ≈19 mm. The gradient case barely dephases for ≈10 mm and accelerates over ≈16 mm, reaching **≈1.4 GeV (+~20%)**. a0 nearly triples over 16 mm (self-focusing). |
| Same, but with the channel radius tapered as the axiparabola channel (w_m = C(z) w0) | Stronger self-focusing and more fully evacuated cavity give **≈1.6 GeV**, matching the experiment |

- **Mechanism claimed:** combined dephasing reduction through tapering; delayed injection (initially superluminal wake); nonlinear laser evolution, where the peak travels slower than v_g because of SPM, dispersion and etching; and self-focusing plus stronger guiding at higher density.
  - Self-focusing lengthens the nonlinear wavelength and slows the rear of the bubble, which lowers the effective α.
  - Pump depletion is mentioned only as a possible limit of the 20 mm flat target.
  - This is **not** a phase-velocity-locking demonstration with a designed nonlinear profile. The authors propose that as future work (laser-machined or multi-inlet gas jets).
- **Data and code:** not public; available on request (see `original-sims/lahaye-density-gradient/SOURCE.md`).

### Relevance to the proton design [my inference]
- The model in Eqs. 2–7 is reusable. Set v_φ at the proton position equal to v_p(z) instead of c, and solve for n_e(z).
- Because v_p < v_φ for protons, this requires **dn_e/dz < 0** (a down-ramp) or higher density (lower v_g). See section 8.
- The HOFI and axiparabola matching rule (channel diameter ∝ λ_p ∝ n^{-1/2}) is a practical constraint for any tapered, guided stage.

---

## 2. DOI 10.1103/bpms-63ml: differentiable inverse design with 500 laser-pulse parameters (ICF, not LWFA)

### Citation and access
- A. J. Crilly (Imperial College / I-X), P. Travis (Ergodic LLC), J. P. Brodrick (Pasteur Labs), J. B. Coughlin (Ergodic), A. S. Joglekar (Ergodic / Pasteur Labs), "High-dimensional inverse design of inertial fusion implosions via differentiable simulation", **Phys. Rev. Research 8, 033353 (2026)**, published 23 Sep 2026. **DOI 10.1103/bpms-63ml**. **arXiv:2606.08827** (7 Jun 2026). CC BY 4.0. [paper]
- **I read the full published text and the arXiv v1.** Published values are used where they differ: χ_noα = 0.529 vs 0.527; yield 1.94e15 vs 1.93e15.
- **Mismatch with the project brief:** this is not a joint laser–plasma *accelerator* optimisation. It optimises the **temporal power profile of a 25 kJ direct-drive ICF laser pulse** together with target geometry. [paper]

### What was parameterised [paper]
- **Bounded interpolated pulse: 500 trainable parameters θ.**
  - P̂(θ) = P_peak · ½(tanh θ + 1), with P_peak = 25 TW.
  - The time nodes are rescaled so that the trapezoid-integrated energy equals E_L = 25 kJ.
  - The power curve is linearly interpolated. The bounds −5 < θ < 5 correspond to 0.001–24.999 TW.
- Only the pulse is differentiated (purely **temporal power**; no spectral phase or spatial profile).
- Target outer radius (250–550 µm) and ice mass (5–20 µg) are Sobol-sampled (about 50 runs) in an outer, gradient-free loop, because rezoning is non-differentiable.
- **Neural-network pulse:** P(t) = MLP_θ(γ(t))·P_peak, with Fourier-feature encoding (K = 4 octaves), ReLU, and a final sigmoid.
  - Width 256 × depth 6, about 331,000 parameters.
  - The number of iterations needed to reach χ_noα > 0.2 scales as width^{-0.74}.

### Differentiable model [paper]
- 1D spherical **Lagrangian hydrodynamics** (von Neumann–Richtmyer staggered grid), written in **JAX** with equinox, lineax, optimistix, optax and diffrax.
- Physics: FEOS tabular EOS (differentiable interpolation and root-finding); separate electron and ion energy equations; flux-limited conduction (Epperlein–Haines and NRL coefficients), semi-implicit with tridiagonal solves; local DT bremsstrahlung loss.
- Laser drive is a reduced model: the laser is converted to an **external ablation pressure** applied to the unablated (stagnated) mass, Herrmann–Tabak–Lindl style:
  P_abl = 40 Mbar (I15/λ_µm)^{2/3},
  with I(t) = (P(t)/A0) · erf(A0/A_beam) and A_beam = π(358 µm)².
- Gradients come from reverse-mode AD ("discretise-then-optimise", which implicitly gives the adjoint) with checkpointing.
- Adjoint stability needed:
  - smooth artificial viscosity: min(0, Δu) → ½(Δu − √(Δu² + ε)), with ε ~ 1e-20;
  - a time step ≲ 0.1 of the forward CFL step.

### Objective, optimiser, results [paper]
- Objective: maximise the ignition metric χ_noα = (ρR/1 g cm^-2)^{0.61} (Y_DT/1e16 · 1 mg/M_stag)^{0.34}, together with a curvature (smoothness) regulariser λ Σ(θ_{i−1} + θ_{i+1} − 2θ_i)².
- Optimiser: **L-BFGS-B**.
  - Hyperparameters are scheduled piecewise: initial fuel temperature, λ, N_t, N_r and t_stop, from smooth/hot/coarse to sharp/cold/fine.
  - The NN variant uses Adam (lr 3e-3, cosine decay over 500 iterations, then fine-tuning at 1e-4 with an energy penalty λ ramped 0.1 → 10).
- Compute: about 1000 epochs to converge. Forward plus adjoint takes 10–15 min vs 2–3 min forward-only, on 4 CPUs (×5). Finite differences would cost 500× per gradient; ">100,000× speed-up" for the NN case.
- **Best design:** outer radius 400 µm, M_stag 7.76 µg, **χ_noα = 0.529**, Y_DT = 1.94e15, ρR = 190 (burn-averaged) and 221 (bang-time) mg/cm², v_imp = 645 km/s, adiabat ≲ 1.5.
  - The optimiser rediscovered a near-isentropic (Nuckolls-like) ramp to peak power without being given it. Fitted Gopalaswamy form: β1 = 5.4, β2 = 2.9, t_rise = 1.1 ns.
  - The paper gives **no "improvement vs baseline"** factor; the baseline was a linear ramp to 12.5 TW. NN pulses reached χ ≈ 0.4 in < 50 iterations but overshot and violated the energy budget by 2.6–59% before fine-tuning.
- **Code: not public.** The Data Availability statement says no public software. Related public code: **ADEPT** (MIT; https://github.com/ergodicio/adept); a snapshot is in `original-sims/differentiable-optimisation/related-code-adept-snapshot/`. ADEPT has no implosion or LWFA solver. [paper] [my inference]

### Transferable lessons for LWFA design [my inference]
- **Gradient-based design scales to hundreds of parameters** where Bayesian optimisation struggles. Candidate parameter sets:
  - a density profile n_e(z) at ~100–1000 nodes;
  - TPA beamlet delays and amplitudes (thousands of parameters; section 6);
  - laser spectral phase.
- A differentiable reduced LWFA model would be needed, for example a 1D/quasi-static fluid wake plus envelope driver in JAX. The paper's experience applies:
  - smooth all conditionals;
  - expect adjoint stiffness (time step ~10× smaller);
  - schedule hyperparameters from smooth to sharp;
  - use L-BFGS-B or Adam with bounded reparametrisations (tanh or sigmoid) and energy-budget penalties.
- Closest LWFA work found (not differentiable): B. Z. Djordjević, C. Benedetti, ..., C. B. Schroeder, "Bayesian optimization of laser-wakefield acceleration via spectral pulse shaping", arXiv:2512.09125 (Dec 2025); a Phys. Plasmas 33, 063101 (2026) listing appeared in search results. It uses PIC (WarpX per search snippet) and a Bayesian optimiser over spectral shaping plus OFI-channel parameters, giving about **10× charge** and higher mean energy vs a Gaussian pulse. [abstract]

---

## 3. "Palm-sized short-pulse laser sets new 80% efficiency record": multipass OPA

### Primary paper
- J. H. Nägele, T. Steinle, J. Thannheimer, P. Flad, H. Giessen (Univ. Stuttgart and SI Stuttgart Instruments GmbH), "Dispersion-engineered multipass optical parametric amplification", **Nature 647, 74–79 (2025)**, **DOI 10.1038/s41586-025-09665-w**. No arXiv version found.
- **Access:** paywalled. I read the **abstract, the Supplementary Information (efficiency definitions, coatings, simulation) and the peer-review file**, not the main text.

### What the 80% is [paper/SI]
- A **multipass OPA**. Dispersion-engineered mirrors refocus the beam repeatedly into one short nonlinear crystal (1 mm **PPLN**). After each pass the mirrors (i) compensate the pump–signal group delay (≈110 fs offset per pass) and (ii) transmit and discard the idler, suppressing back-conversion.
- **"Photon conversion efficiency up to 81%"**: η_phot = 1 − P_res/P_T, the fraction of pump photons *transmitted through the cell* that are converted to signal plus idler. Linear cell losses are excluded.
- **System conversion efficiency 52%**: η_sys = (P_sig,out/P_pump,in)(λ_sig/λ_pump), counting all losses (mirror R ≈ 98.5–99%; cell transmission ≈ 70%).
- With λ_pump = 1030 nm and λ_sig ≈ 1690 nm, the **pump-to-signal power efficiency ≈ 0.52 × 1030/1690 ≈ 32%** [my inference]. The authors deliberately avoid quoting this number; a referee asked for it.
- **None of these is electrical-to-optical or wall-plug.** The OPA needs a pump laser whose own wall-plug efficiency multiplies in.
- Other figures: gain ×1,500 over single-pass; 41 dB gain with 12 THz bandwidth; near-Fourier-limited output; M² preserved. [abstract]

### Operating point [SI/paper]
- Pump 1030 nm, 130 fs, **≈3 W at 76 MHz (≈40 nJ/pulse** [my inference]); seed ~1–40 mW at 1.6–1.7 µm.
- Output pulses "below 50 fs" [press]; device volume in the single-digit cm³ range. [abstract]
- Simulation: 1+1D pyNLO (parameters in `original-sims/multipass-opa-nagele2025/SOURCE.md`). Code available on request only.

### Can it scale to J-class pulses for LWFA? [paper] [my inference]
- The authors suggest Herriott-type multipass cells with large-aperture crystals could take the approach "to the kilowatt level". This is a statement, not a demonstration.
- At J level OPCPA is already used, but crystal aperture, damage fluence, thermal load and the pump laser (itself the efficiency bottleneck) dominate. Even a perfect OPA caps wall-plug efficiency at η_pump-laser × ~0.3–0.5.
- **Conclusion: not a route to an efficient J-class LWFA driver.** It could be useful for efficient wavelength conversion, for example to make broadband seeds for Tm (1.9 µm) amplifiers, or as a compact front end.

---

## 4. Laser-driver technologies for a high-repetition-rate, efficient LWFA

### 4.1 Baseline: Ti:sapphire
- Conventional LWFA drivers are limited to "less than approximately 1 Hz and 0.1%" in repetition rate and wall-plug efficiency, respectively (Hooker et al., J. Phys. B 47, 234003 (2014), arXiv:1401.7874). [abstract]
- BELLA PW: 40 J, 40 fs, 1 Hz; cost **O(10 M$) including auxiliaries, ca. 2007** (Snowmass ITF report, arXiv:2208.06030 / JINST 2023). [secondary]
- The ITF states that LWFA-collider drivers "will not be based on Ti:Sa laser technology owing to the fundamental quantum defect of Ti:Sa that restricts efficiency." [secondary]
- **L3-HAPLS** (diode-pumped pump laser, LLNL → ELI Beamlines): design ≥30 J, <30 fs, 10 Hz; achieved 13.3 J at 3.3 Hz (2021) and later 16 J at 3.3 Hz (~0.5 PW). No published wall-plug figure was found. [secondary/press]
- **KALDERA** (DESY; not LBNL): Ti:Sa CPA target 3 J, 30 fs, 100 TW, up to 1 kHz (kW level). First step 0.5 J at 100 Hz driving MAGMA. Started 2020; still under development. [secondary: DESY web page]
- **kBELLA** (LBNL proposal): 3 J, 30 fs, 1 kHz, 3 kW, described as a "$100M-class laser facility" (T. Zhou, LBNL seminar, 8 Sep 2023). [secondary]
- **EuPRAXIA** laser-driven site (per ITF): three Ti:Sa lasers (5 J/20 fs, 15 J/20 fs, 50 J/50 fs; 20 Hz, upgradable to 100 Hz). Total laser cost **73.5 M€** (41.5 M€ materials plus labour). [secondary]

### 4.2 Coherently combined Yb-fibre CPA (ICAN → XCAN, Jena, LBNL/UM)
- **ICAN concept** (Mourou, Brocklesby, Tajima, Limpert, Nat. Photon. 7, 258 (2013), DOI 10.1038/nphoton.2013.75):
  - Coherently add thousands of fibre amplifiers.
  - Demonstrator goal >10 J, >10 kHz, 100–200 fs (Southampton release 2013); later "tens of J, <50 fs, >100 kW, wall-plug >30%" (EPJ ST 2015 editorial and CERN Courier).
  - [secondary: press/editorial; full paper not read]
- **XCAN** (École polytechnique and Thales): tiled-aperture coherent combination of 61 fibre CPAs.
  - Fsaifes et al., Opt. Express 28, 20152 (2020): residual phase error λ/90 rms, **combining efficiency ≈50%**. [abstract via search]
  - System target **10 mJ, 350 fs, 50 kHz** (500 W). An earlier 7-fibre stage gave 71 W after compression; a 60-fibre combination was compressed to 225 fs. [secondary]
  - Tiled-aperture efficiency is limited (<~70%) by the fill factor and side-lobes. [secondary]
- **Jena (Limpert group):**
  - Stark et al., Opt. Lett. 46, 969 (2021), arXiv:2103.05614: **16 channels, 10 mJ, 120 fs, 1 kW** (so 100 kHz [my inference]). [abstract]
  - Stark, Benner, Buldt, Klenke, Limpert, Opt. Lett. 48 (11) (2023), DOI 10.1364/OL.488617: **32 mJ, 158 fs, 20 kHz** (≈640 W [my inference]); 8-pulse bursts in 16 amplifiers combined spatiotemporally. [secondary]
  - Müller et al., Opt. Lett. 45, 3083 (2020): **10.4 kW**, 12 channels, 254 fs, 80 MHz (≈130 µJ [my inference]). [secondary]
  - Earlier: 23 mJ at 674 W (25 kHz) by divided-pulse amplification (arXiv:2101.09686). [secondary]
  - Klenke et al., SPIE LASE 2025: multicore-fibre system with 1.75 mJ, 261 W, 330 fs, 148 kHz, 75% combining efficiency. [secondary]
- **LBNL / U. Michigan / LLNL** multidimensional combining (spatial ×~100, spectral ×~3, temporal stacking ×~100):
  - Funded intermediate goal 0.2 J, 30 fs, 5 kHz, 1 kW (2023 slides).
  - **AAC 2026 abstract (T. Zhou et al.): "150 mJ, 40 fs, 5 kHz, 1 kW" driver under construction.** Front end and amplifier chain complete. The 85 µm-core amplifier reached a record 8 mJ. Spectral combining gave 42 fs; stacking of 10 pulses was shown. Each of 3 spectral channels will feed an array of 9 amplifiers. [abstract]
  - Earlier: 22 mJ from three 85 µm CCC fibres; 81-beam diffractive combining. [secondary: Kiani et al. white paper]
  - Funding estimates (Kiani et al., arXiv:2204.10774 / JINST 2023): >100 mJ milestone at the "multi-$M" level; the next milestone at "few tens of $M"; multi-J kBELLA-class at the "$100M level". [paper]
- **Efficiency:**
  - Industrial CW fibre lasers reach >45% wall-plug (IPG 120 kW, cited in Zhou slides). [secondary]
  - Ultrafast industrial Yb-fibre lasers reach "up to 25%" wall-plug (Yusim et al., SPIE 9728 (2016), as cited by Nutting et al. 2026). [secondary]
  - Snowmass LPA-collider white paper (arXiv:2203.08366 / JINST 18 T06001 (2023)) assumes **50% wall-to-laser** = 65% (diode electrical-to-optical) × 90% (fibre optical-to-optical) × 85% (combining or stacking), calling it "challenging". [paper]
  - Combined fs fibre systems **have not demonstrated** system-level wall-plug numbers. [my inference]
- **Cost:** the ITF estimate for fibre-laser drivers of a **1 TeV LWFA collider is 1–6 B$**. The ITF R&D target is "5 J, 300 kW, ~40 fs" per driver. [secondary]
  - With a 105 MW site power at 50% wall-to-laser (≈52 MW of laser), that is **≈ $20–115 per W of average laser power** [my inference].

### 4.3 Big Aperture Thulium (BAT), Tm:YLF at ~1.9 µm (LLNL)
- Concept: diode-pumped (793 nm CW diodes) Tm:YLF in a HAPLS/Mercury-style gas-cooled slab.
  - 15 ms upper-state lifetime allows **multi-pulse extraction under CW pumping**, so repetition rate and energy can be freely exchanged.
  - "Two-for-one" cross-relaxation gives a low effective quantum defect.
  - Bandwidth supports <100 fs. [secondary: LLNL AAC 2022 and EUVL 2024 slides]
- Design points:
  - **30 J, <100 fs, 0.3 PW, 10 kHz, 300 kW** (gas-cooled head); variant 150 J, 1.5 PW, 100 Hz.
  - "EUV-BAT": **1 J, 100 kHz, 100 kW, wall-plug 20%, 500 kW electrical**.
  - [secondary]
- Demonstrated (LLNL):
  - **21.7 J, 20 ns** single shot (Tamer et al., Opt. Express 30, 46336 (2022)); >100 J in ms pulses; 38.1 J long pulse.
  - **Burst ~0.5 J/pulse at 6.8 kHz, 3.6 kW, 19% optical-to-optical**.
  - CPA: **1.59 J compressed to 270 fs (1.7 TW)**, single shot, compressor efficiency 42% (Opt. Lett. 49, 1583 (2024) reports >1.5 J, sub-300 fs). **10 J in a 10-pulse 1 kHz broadband burst.**
  - Gas-cooled heat extraction >20 W/cm².
  - MLD gratings at 1.9 µm with fs damage threshold >100 mJ/cm².
  - [secondary: slides; LLNL news 2023]
- LLNL explicitly lists **"laser-driven proton/electron acceleration ... and muon generation"** as target applications (AAC 2022 slide). [secondary]
- Note for LWFA [my inference]:
  - λ ≈ 1.9 µm gives a0 ∝ λ√I, so about 2.4× higher a0 at the same intensity than 0.8 µm.
  - It also gives about 5.6× lower critical density, which lowers the density needed for a given wake slow-down (relevant for protons; section 8).
  - Compressed pulses are still ~270 fs; LWFA wants ≲100 fs.

### 4.4 Thin-disk and cryogenic Yb:YAG (TRUMPF Scientific, LMU/MPQ, CSU)
- Thin-disk optical-to-optical efficiency exceeds 50%; about 1 J at 1 kHz demonstrated (Kiani et al. white paper). [paper]
- Herkommer et al., Opt. Express 28, 30164 (2020) (TRUMPF Scientific): 240 mJ regenerative amplifier, then a 4-head thin-disk multipass, giving **720 mJ, 1 kHz (720 W), 1030 nm, 920 fs**, M² ≈ 2.1. [secondary]
- Thin-disk regenerative amplifier: 200 mJ at 5 kHz (>1 kW) (2017); >2 kW average in ps multipass amplifiers. [secondary]
- CSU cryogenic Yb:YAG: Wang et al., Opt. Lett. 45, 6615 (2020): **1.1 J, 1 kHz**, 1.26 kW before compression, **4.5 ps** after compression (90% compressor efficiency). [abstract via search]
- These ps pulses are too long for direct LWFA. They need plasma modulation (**P-MoPA**: Jakobsson, Hooker, Walczak, PRL 127, 184801 (2021); see `resonant-multipulse.md`) or multipass-cell post-compression. [paper/secondary]

### 4.5 Reports that tabulate driver targets
- **European Strategy, Accelerator R&D Roadmap** (CERN Yellow Report CERN-2022-001, arXiv:2201.07895):
  - Plasma-collider drivers need O(10 kHz) and O(100 kW).
  - "Efficiency wall-plug to beam (includes drivers)" ≥10%.
  - Minimal-plan milestone: kW-average-power Ti:Sa (100 Hz × 10 J or 1 kHz × 1 J, <100 fs).
  - Far-term laser goal: "15 kHz rep rate, 100 Tera-Watt, 30% wall plug efficiency".
  - Candidate technologies: combined Yb fibre, Tm 2 µm, BAT, ps thin-disk with modulation.
  - [paper]
- **Snowmass 2021:**
  - LPA collider white paper (Benedetti, ..., Schroeder et al., arXiv:2203.08366):
    - quasi-linear stage of 6.5 J, 130 fs, 1 µm, 1e17 cm^-3, 1.7 m channel, 5 GeV per stage;
    - 1/3/15 TeV collider at 47 kHz with 105/315/1100 MW site power;
    - 50% wall-to-laser assumed;
    - bubble-regime γγ stage of 50 J, 70 fs, 0.8 µm, 3.1 cm, 1.2 nC, 3.2 GeV, wake-to-beam efficiency 43%.
    - [paper]
  - Laser white paper (Kiani, Zhou et al., arXiv:2204.10774): roadmap for fibre, BAT and thin-disk. Kiani/Zhou slides tabulate kBELLA 3 J/30 fs/1 kHz/3 kW → high-repetition driver 3 J/10 kHz/30 kW → collider driver 6 J/100 fs/50 kHz/300 kW, requiring "~10s %" wall-plug. [paper/secondary]
  - ITF report (arXiv:2208.06030): LWFA-LC cost driven by the lasers; fibre-laser estimate 1–6 B$ at 1 TeV; >10 years of R&D before a CDR. [paper]
- **ALEGRO** (input to ESPP 2019) was not separately read; its laser targets are absorbed into the 2022 roadmap above.
- **10 TeV pCM Wakefield Collider design initiative** (Gessner, Osterhoff, Lindstrøm et al., arXiv:2503.20214): abstract only, with no laser-efficiency numbers in the abstract. [abstract]

### 4.6 Table: laser driver options

Notes for reading the table:
- "WPE" = wall-plug (electrical-to-optical) efficiency.
- "o-o" = optical-to-optical.
- TRL values are my rough judgement for a *J-class, ≲100 fs, ≥kHz LWFA driver*. [my inference]
- Derived $/W figures divide quoted costs by average power. [my inference]

| Technology (example) | λ | Pulse energy | Duration | Rep rate | Avg power | WPE realised | WPE projected | Cost indicators | TRL (J-class kHz LWFA) | Sources |
|---|---|---|---|---|---|---|---|---|---|---|
| Ti:Sa PW, flashlamp/DPSS-pumped (BELLA) | 0.8 µm | 40 J | 40 fs | 1 Hz | 40 W | ≲0.1% (LWFA drivers generally) | n/a | O(10 M$) ca. 2007, ≈$250k/W | 9 at Hz; n/a at kHz | Hooker 2014 [abstract]; ITF [secondary] |
| Diode-pumped Ti:Sa PW (L3-HAPLS) | 0.8 µm | 30 J design (16 J achieved) | <30 fs | 10 Hz design (3.3 Hz achieved) | 300 W design (≈53 W achieved) | not published | not published | n/a | 7 at 10 Hz | ELI/LLNL releases [press] |
| kHz Ti:Sa (KALDERA, DESY) | 0.8 µm | 3 J target (0.5 J now) | 30 fs | 1 kHz target (100 Hz now) | kW target (50 W now) | not stated | not stated (Ti:Sa quantum defect) | n/a | 5 | DESY page [secondary] |
| kHz Ti:Sa or fibre (kBELLA, LBNL) | 0.8 µm | 3 J | 30 fs | 1 kHz | 3 kW | n/a | n/a | "$100M-class facility", ≈$33k/W at facility level | 4–5 (proposed) | Zhou 2023 slides [secondary] |
| EuPRAXIA Ti:Sa set | 0.8 µm | 5 / 15 / 50 J | 20 / 20 / 50 fs | 20 Hz (→100 Hz) | ≈1.4 kW total at 20 Hz | n/a | n/a | 73.5 M€ for 3 lasers: ≈€52k/W at 20 Hz, ≈€10k/W at 100 Hz | 6–7 at 20 Hz | ITF [secondary] |
| Coherently combined Yb fibre CPA (Jena) | 1.03 µm | 10 mJ; 32 mJ | 120 fs; 158 fs | 100 kHz; 20 kHz | 1 kW; ≈640 W | system WPE not reported; ultrafast Yb fibre ≈25%; CW fibre >45% | 50% (Snowmass assumption); >30% (ICAN) | collider estimate 1–6 B$ for ≈52 MW, ≈$20–115/W | 4 (J-class needs about 100× scale-up) | Stark 2021 [abstract]; Stark 2023 [secondary]; Snowmass WP [paper]; ITF [paper] |
| Coherently combined Yb fibre, high average power (Jena) | 1.03 µm | ≈130 µJ | 254 fs | 80 MHz | 10.4 kW | n/a | as above | n/a | n/a (too low energy) | Müller 2020 [secondary] |
| XCAN tiled 61-fibre (Polytechnique/Thales) | 1.03 µm | target 10 mJ | target 350 fs | target 50 kHz | target 500 W | combining efficiency ≈50% (tiled) | ICAN >30% | n/a | 3–4 | Fsaifes 2020 [abstract]; HAL [secondary] |
| LBNL/UM spectral+spatial+temporal fibre driver | 1.03 µm | target 150 mJ (8 mJ per amplifier now) | target 40 fs (42 fs shown) | 5 kHz | target 1 kW | n/a | "10s %" | multi-$M → $100M roadmap | 3–4 | AAC 2026 abstract [abstract]; Kiani WP [paper] |
| Tm:YLF BAT (LLNL) | 1.88–1.9 µm | 1.59 J compressed (single shot); ~0.5 J/pulse ns burst | 270 fs | 1 kHz burst (10 J/10 pulses); 6.8 kHz ns burst | 3.6 kW (ns burst) | 19% o-o (burst) | **20% WPE** (EUV-BAT 1 J/100 kHz/100 kW); concept 30 J/10 kHz/300 kW | n/a | 3–4 | LLNL slides 2022/2024 [secondary]; Tamer 2022 [secondary] |
| Thin-disk Yb:YAG multipass (TRUMPF Scientific) | 1.03 µm | 720 mJ | 920 fs | 1 kHz | 720 W | o-o >50% | n/a | commercial (prices not public) | 6 for ps; LWFA needs modulation or compression | Herkommer 2020 [secondary]; Kiani WP [paper] |
| Cryogenic Yb:YAG (CSU) | 1.03 µm | 1.1 J | 4.5 ps | 1 kHz | ≈1.1 kW | n/a | n/a | n/a | 5 (ps) | Wang 2020 [abstract] |
| Multipass OPA (Stuttgart) | pump 1.03 → signal 1.69 µm | ≈40 nJ pump | <50 fs | 76 MHz | ≈3 W pump | 81% photon (internal); 52% photon (system); ≈32% pump→signal power | kW claimed possible | n/a (patent; commercial) | 2 for J-class | Nägele 2025 [paper SI]; press |
| *Target:* LWFA collider driver | 1 µm | 5–6 J | 40–100 fs | 47–50 kHz | 300 kW | — | 30% (ESPP); 50% (Snowmass) | 1–6 B$ total (1 TeV) | — | ITF, Snowmass, ESPP [paper] |

### 4.7 Wall-plug chain to keep in the efficiency model [paper/secondary] [my inference]
- η_wall→beam = η_supply×diode (~0.65) × η_o-o (fibre ~0.9; Tm:YLF ~0.2–0.4 for the full chain) × η_combine/compress (~0.85 for fibre; 0.42–0.9 for grating compressors) × η_laser→wake × η_wake→beam.
- For electrons in optimised PIC: η_wake→beam ≈ 40% (Schroeder Table III).
- Depletion-limited η_laser→wake: 20% residual energy in the Schroeder bubble-regime example. Unused laser energy could be recovered with photovoltaics (proposed in the Snowmass white paper and in TPA).

---

## 5. Multi-pulse / multi-laser driving of one wake (brief; Hooker 2014 and P-MoPA are in `resonant-multipulse.md`)

- **Incoherent combination works in principle.** Benedetti, Schroeder, Esarey, Leemans, "Plasma wakefields driven by an incoherent combination of laser pulses: a path towards high-average power laser-plasma accelerators", Phys. Plasmas 21, 056706 (2014), arXiv:1404.4669 / OSTI 1163658. [paper: full OSTI preprint read]
  - Analysis plus PIC shows a regular wake behind an incoherent driver, provided the incoherent structure varies on time scales < ω_p^-1 and the time-averaged energy sits in a volume ~λ_p³.
  - Spectral combining is as efficient as a single pulse. A pulse stack or a beamlet mosaic needs only "a few percent" more energy.
  - Mosaic example for a 30 J, 10 GeV stage: about 3600 beamlets of about 8 mJ each, with polarisation multiplexing. **Phase locking is not required.**
- **Pulse trains:** resonant excitation by trains of about 7 pulses was shown experimentally (Cowley et al., PRL 119, 044802 (2017)). [secondary]
  - Oxford/CLF later guided about 2.5 J, N ≈ 10 pulse trains in a 100 mm HOFI channel with spectral evidence of resonant excitation (AAC 2022 and LPAW 2023 abstracts; no journal paper found). [abstract]
  - P-MoPA simulations: 0.65 GeV in 100 mm; multi-GeV in arXiv:2311.00471. [abstract]
- **2026 two-pulse studies** (Maurya et al., arXiv:2601.00298 (arXiv lists related DOI 10.1063/5.0320511) and arXiv:2603.21798): up to 3× wake amplitude with two co-propagating pulses. The two papers give inconsistent optimum separations (λ_p vs λ_p/4). Low weight. [abstract]
- **Fibre arrays as direct drivers:** I found no 2023–2026 PIC study of a tiled coherent fibre array driving an LWFA. The closest are TPA (section 6) and the LBNL multidimensional combining driver (section 4.2). [my inference from searches]
- **Transverse flying focus for ions** (Gong, Cao, Palastro, Edwards, PRL 133, 265002 (2024), arXiv:2405.02690; EPOCH 2D/3D). One laser with a focal spot moving transverse to propagation, matched to a uniformly accelerated ion.
  - Result: **1.64 GeV protons, 3.7% spread, 23.1 pC, 0.61° divergence, after 4.4 mm**.
  - Driver: 0.8 kJ, 21 ps, 37.5 TW, I0 ≈ 3e20 W/cm², n_e ≈ 5.5e19 cm^-3.
  - Laser-to-all-protons efficiency η ≈ 0.13% (3D).
  - Focus trajectory: x_f(t) = (c²/Π0)(√((Π0 t/c)² + 1) − 1), with Π0 = eZE_x/m_i.
  - [paper: arXiv full text read] TWEAC and flying focus are covered in `flying-focus-and-tweac.md`.

---

## 6. Nutting et al. 2026: "Transversely pumped laser driven particle accelerator" (TPA)

### Citation and access
- T. Nutting, N. Ernst, A. G. R. Thomas, K. Krushelnick (Univ. Michigan), **Nat. Commun. 17, 5949 (2026)**, published 8 Jul 2026, **DOI 10.1038/s41467-026-72697-x**, CC BY 4.0. No arXiv version.
- **Full text, SI and peer-review file read**; copies in `original-sims/transverse-pumping/`.

### Concept [paper]
- A **plasma** accelerator (underdense H plasma column or filament). It is not dielectric.
- Two or more **arrays of counter-propagating, focused beamlets** propagate *perpendicular* to the acceleration axis and cross on a shared line focus.
- Each neighbouring beamlet pair is delayed so that the **crossing point moves along the axis at a programmable, even accelerating, velocity**. That moving ponderomotive "intensity peak" drives a wake whose phase velocity is set by timing alone, sub- or superluminal.
- Adjacent beamlets are **cross-polarised** (or detuned in frequency) to suppress interference beating. The ponderomotive potential is then the *incoherent* sum ⟨A²⟩ = ½ Σ|A_i|², so no inter-beamlet phase locking is needed.
- Related to Debus's TWEAC (pulse-front-tilted crossing beams) but discretised. The authors argue it scales "only" by adding beamlets and lengthening a cylindrical focusing optic.

### Formulas to implement [paper]
- **Timing law** for beamlet i focused at z_i, for a particle under constant field E*:
  t_i = (mc/(qE*)) [√((γ0 + qE* z_i/(mc²))² − 1) − p0/(mc)].
  - Ultra-relativistic limit: t_i ≈ z_i/c.
  - Proton from rest: t_i = (z_i/c)√(1 + 2mc²/(qE* z_i)).
  - Non-relativistic: t_i ≈ √(2m z_i/(qE*)).
  - The general form is s^{-1}(z) = ∫ (v_z/V) dp_z/(qE_z).
- **Amplitude weighting** for a constant time-averaged ponderomotive peak U0 (SI Eqs. 11–15), with uniform spacing Δz and local velocity V_i:
  a_i² = (2/√π) · U0 Δz/(N_θ V_i τ0)  for Gaussian g = exp(−2z²/w0² − 2t²/τ0²),
  so the per-beamlet intensity is I_i ∝ Δz/(N_θ V_i τ0).
  - The (2/√π) prefactor is my reconstruction: the PDF square-root glyph was lost in text extraction, and it is consistent with ∫|g(0,t)|²dt = τ0√π/2.
  - **Slower structures need proportionally more energy per beamlet** (∝ 1/V_i) to keep the time-averaged drive constant. This matters for slow protons. [paper/SI] [my inference]
- **Feasibility scalings:**
  - number of beamlets N ≈ L/dx;
  - optic clear aperture d ≳ E/(F L) at damage fluence F ~ 1 J/cm²;
  - line-focus intensity I ≈ E/(w L τ);
  - sustainable length at fixed I: x = E/(I w τ).

### Simulation parameters and results (OSIRIS 4.0, modified for very long input decks) [paper]
| Case | Geometry and parameters | Result |
|---|---|---|
| **Protons (2D)** | Box 3.76 mm × 169 µm, 17.38 ps, static window. H plasma 1.8e18 cm^-3 (8th-order super-Gaussian column). **1200 beamlets per array**, dx = 3 µm, a0 = 8, w0 = 3 µm, τ = 25 fs, **290 mJ each**, cross-polarised. Structure starts at 0.42c. Injected RPA-like proton beam: 95 MeV ± 10 MeV (20 MeV FWHM), FWHM 4 µm, 1.5e16 cm^-3 (~10 pC if cylindrical). | **1.12 GeV max (0.98 GeV peak) after 3.6 mm at E* = 2.5 GV/cm**; spread grows from 20 to 40 MeV FWHM. Matches theory for several E*. Protons sit near the beamlet crossing (ponderomotive effects on emittance are flagged as an open issue). |
| Protons (2D, visualisation) | 682 × 253 µm, 4.1 ps, co-polarised in-phase beamlets | Streak plots confirm the accelerating structure |
| Electrons (2D) | Moving window 92.4 × 27.5 µm, 6.17 ps. dx = 1.3 µm, w0 = 1.64 µm, τ = 20 fs, a0 = 2.5 (**7 mJ**), λ = 1 µm, n = 1.2e18 cm^-3 (0.012 n_c), v_φ = c | Dephasingless. SI: **800 MeV, 1.9% spread, 1.38 mm·mrad** after 1525 µm (**0.52 TeV/m**), using 16.4 J total. An equal-energy conventional LWFA would dephase in 360 µm. |
| Electrons (3D) | 92.4 × 26.9 × 26.9 µm, 280 fs; 16 µm FWHM column; 7 mJ beamlets, two arrays | 20 MeV in 50 µm (0.4 TeV/m); 0.78 pC above 15 MeV. **Laser-to-beam efficiency 3e-5** ("not optimised"). |
| Electrons (3D, wide column) | 40 µm column, 830 µJ beamlets (a0 = 0.85) | Bubble narrower than the column |

### Efficiency and scaling claims [paper] [my inference]
- The authors claim:
  - bypasses dephasing, depletion and diffraction;
  - unlimited length scaling;
  - small optics, high repetition rate, ML-tunable;
  - spent beamlets can be collected and recycled;
  - fibre lasers at "up to 25%" wall-plug;
  - 1 TeV electrons in 2.5 m with about 2 million 7 mJ beamlets (~27 kJ), or 160,000 beams of 10 J (1.6 MJ) in 40 cm at 1e19 cm^-3 (2.5 TeV/m);
  - NSF-OPAL-class 500 J, 20 fs line focus giving x ≈ 17 cm and ~60–70 GeV per stage at ~0.4 TeV/m.
- **Laser-to-proton efficiency (my estimate from their numbers):**
  - laser energy 2 × 1200 × 0.29 J ≈ 696 J (2D-equivalent);
  - proton energy gain ≈ 10 pC × 0.885 GeV ≈ 8.9 mJ;
  - so **η ≈ 1.3e-5**. Their 3D electron case gives 3e-5.
  - Conventional LWFA reaches ~1–10% for electrons. TPA spends most energy on transverse pushing, with each beamlet crossing only microns of plasma. Transmitted energy recycling is essential, and is unproven.
- **Referee criticism (peer-review file):** Reviewer 3 says the major feasibility weaknesses remain. Timing and alignment complexity grows (possibly non-linearly) with beamlet number, and beam quality is not better than standard LWFA for 1–10 GeV electrons. The authors answered with a cylindrical-optic, shared-aperture layout and a staged experimental plan; no experiment yet. [paper]

### Suitability for slow protons [paper] [my inference]
- **Yes in principle.** TPA is one of very few schemes that explicitly produce a **subluminal, accelerating wake from many low-energy lasers**. The structure velocity is set electronically by delays, which is exactly what protons from about 0.4c to 0.99c need. The paper simulates this case directly.
- **Scaling to 6 GeV [my inference]:** at E* = 2.5 GV/cm, 95 MeV → 6 GeV needs ≈23.6 mm, i.e. ≈7,900 beamlets per array, about **4.6 kJ per shot** (2D-equivalent, constant 290 mJ). The 1/V_i weighting would raise energy where the structure is slow. With ~10 pC this gives about 59 mJ of beam, or η ≈ 1.3e-5.
  - Higher efficiency would need fewer, larger beamlets (the authors note larger spots reduce beam count), higher charge (beam loading), and energy recycling.
  - This is a key target for simulation-based optimisation (beamlet number, spot size, a0, density, charge), possibly with gradient-based or Bayesian methods (section 2).
- Inter-beamlet delays are fs-scale (4.3 fs for electrons; 10 fs quoted for the ion runs). Timing tolerances are looser than coherent combining because only the ponderomotive envelope matters. Coherent fibre arrays reach λ/90 (0.037 fs) phase error. [paper]

---

## 7. Other recent developments (2024–2026) relevant to efficiency and performance
- **Gas-jet tapering for 10 GeV stages:** R. Li, A. Picksley, C. Benedetti, ..., A. J. Gonsalves, Rev. Sci. Instrum. 96, 043306 (2025), arXiv:2411.17028. Simulated with 19 J in 30 cm: tapering raises energy from ~9 to >12 GeV and charge by about 10×. Profiles are set by nozzle throat width and jet angle. [abstract]
- Meter-scale supersonic gas jets for multi-GeV LPAs (Miao et al., RSI 96, 043003 (2025)) and 10 GeV-class channel-guided LPA (Picksley et al., PRL 133, 255001 (2024)) are cited by Lahaye as routes to tailored profiles and PW-scale tapered, guided stages. [secondary]
- **Transverse flying focus for ions** (Gong et al., PRL 2024): see section 5. It is a single-laser alternative to TPA, with 0.13% laser-to-all-protons efficiency (3D) [paper]. Only about 4.7e-5 goes into the 23 pC quasi-monoenergetic beam (my estimate: 23.1 pC × 1.64 GeV / 800 J), compared with about 1.3e-5 for TPA. It needs 21 ps, 0.8 kJ pulses. [my inference]
- **Bayesian optimisation with spectral pulse shaping** (Djordjević et al., arXiv:2512.09125): about 10× charge in OFI-channel LPAs. [abstract]
- **Fibre drivers:** LBNL 150 mJ/40 fs/5 kHz build (AAC 2026); Jena multicore 1.75 mJ/261 W (2025). [abstract/secondary]
- **BAT Tm:YLF:** J-level 270 fs CPA (2024); 2025 LLNL-led EUV project; gas-cooled head development. [secondary/press]

---

## 8. Implications for an efficient ~6 GeV proton LWFA [mostly my inference; formulas cited]

1. **Proton kinematics set the phase-velocity problem.**

   | Proton kinetic energy | γ | β |
   |---|---|---|
   | 95 MeV | 1.101 | 0.419 |
   | 1 GeV | 2.066 | 0.875 |
   | 3 GeV | 4.197 | 0.971 |
   | 6 GeV | 7.395 | 0.9908 |

   A standard LWFA wake moves at v_φ ≈ v_g ≈ c(1 − n/2n_c) ≈ c, so protons below a few GeV slip backwards out of the bucket in ~λ_p/(2(1−β)) of propagation. The wake must be **slowed and then accelerated** with the protons.

2. **Ways to slow the wake, ranked by flexibility:**
   - **(a) Spatiotemporal drivers:** TPA (section 6), transverse flying focus (Gong 2024), TWEAC. These give an arbitrary programmable v_φ(t), including strong acceleration from 0.4c.
   - **(b) High density:**
     - In the nonlinear regime the wake velocity is ≈ c(1 − 3n/(2n_c)) (Lu et al., PRSTAB 10, 061301 (2007)).
     - Matching β then needs n ≈ (2/3)(1 − β) n_c.
     - For β = 0.9908 (6 GeV): n ≈ 1.1e19 (0.8 µm), 6.4e18 (1.03 µm), 1.9e18 cm^-3 (1.9 µm).
     - For β = 0.875 (1 GeV): 1.5e20, 8.8e19, 2.6e19 cm^-3.
     - A *decreasing* density along z (higher n where protons are slow) can follow the proton velocity. Longer-wavelength drivers (Tm:YLF at 1.9 µm, CO2) need much lower densities. [my inference from Lu's formula; to be checked in PIC]
   - **(c) Density gradients (Lahaye Eq. 2):** set v_φ(ξ_p) = β_p c to get (1/n) dn/dz ≈ 2(β_p − v_g/c)/ξ_p < 0.
     - Example: n = 1e18 cm^-3 at 0.8 µm, ξ_p ≈ λ_p = 33 µm, β_p = 0.9908 gives a scale length L_n ≈ 1.9 mm. That steep exponential down-ramp cannot be maintained over tens of mm.
     - So gradients are a **fine-tuning tool** near β → 1, combined with (a) or (b). It is the mirror image of the electron up-ramp in Lahaye et al. [my inference]
   - **(d) HOFI/axiparabola-matched channels** with diameter ∝ n^{-1/2} keep guiding while the density is tapered (Lahaye). [paper]

3. **Many lower-power lasers are physically allowed.**
   - Incoherent combination (Benedetti 2014) and cross-polarised beamlet arrays (TPA) show that the wake responds to the *time-averaged* ponderomotive drive. Inter-laser phase locking is not essential, but **timing to a few fs** and pointing to µm-scale are. [paper]
   - This favours fibre-array or tiled-aperture drivers with electronic delay control, the same hardware as coherent beam combining but with relaxed phase requirements. [my inference]

4. **The efficiency gap is the main risk.**
   - Demonstrated laser-to-proton efficiencies in underdense proton schemes: TPA ≈1e-5 (2D, my estimate); TFF 1.3e-3 to all protons (3D).
   - Combined with a projected 20–50% wall-plug efficiency (BAT, fibre), wall-to-beam would be ~3e-6 to ~6e-4.
   - Wall-plug energy per 6 GeV proton is E_p/(η_wp · η_l→b). Examples: ≈1.2 PeV (η = 0.5 × 1e-5); ≈15 TeV (0.3 × 1.3e-3); ≈60 GeV (0.5 × 0.2, the electron-LWFA-like optimum).
   - Simulation must therefore target **laser-to-proton η ≥ 1e-2** for the concept to be competitive. Levers: beam loading with higher charge, energy recycling of transmitted beamlets, fewer and larger beamlets, and avoiding transverse energy waste.
   - Whether this is enough for muon-catalysed-fusion breakeven is covered in `muon-production-and-mucf.md`.

5. **Driver choice for simulation baselines.**
   - (i) **Yb-fibre arrays at 1.03 µm**: best projected WPE (~50% assumed); today ≤32 mJ per combined pulse; natural fit to TPA-style beamlets of mJ–100 mJ.
   - (ii) **Tm:YLF BAT at 1.9 µm**: J-class single aperture; 20% WPE projected; lower n_c helps slow wakes; current pulses ~270 fs.
   - (iii) **Thin-disk ps Yb** with P-MoPA: most mature high-average-power source; efficiency claims rest on >50% optical-to-optical.
   - Ti:Sa (~0.1%) should be used only for physics benchmarking, not efficiency claims.
   - Cost anchors for the economic model: ≈$20–115/W (ITF fibre collider estimate, my division); kBELLA ≈$33k/W (facility); EuPRAXIA ≈€10–52k/W.

6. **Suggested validation simulations:**
   - (1) Reproduce Lahaye's FBPIC case (1 J, 25 fs, 25 µm FWHM, n0 = 1e18 cm^-3, 0.08 n0/mm, parabolic channel w0 ≈ 21 µm) to validate our toolchain against ≈1.4–1.6 GeV.
   - (2) Rebuild the TPA 2D proton case (parameters above) in OSIRIS, WarpX or EPOCH, using the timing and amplitude laws, and verify 1.12 GeV in 3.6 mm before optimising efficiency.
   - (3) Build a reduced differentiable or BO loop over (density profile, beamlet delays and amplitudes, beamlet size and number), following Crilly et al. on adjoint smoothing and hyperparameter scheduling.

---

### Reading status summary
| Item | Read |
|---|---|
| Lahaye 2026 | Full text (published + arXiv) |
| Crilly 2026 | Full text (published + arXiv) |
| Nägele 2025 | Abstract + SI + peer-review file (main text paywalled) |
| Nutting 2026 | Full text + SI + peer-review file |
| Gong 2024 | Full arXiv text |
| Benedetti 2014 | Full OSTI preprint |
| ESPP roadmap, Snowmass LPA collider white paper, Kiani laser white paper, ITF | Full text, searched for laser sections |
| LLNL BAT | Talk slides (AAC 2022, EUVL 2024) + LLNL news |
| Jena, XCAN, thin-disk, cryo Yb, KALDERA, HAPLS, ICAN | Abstracts, search snippets or institutional pages only |
