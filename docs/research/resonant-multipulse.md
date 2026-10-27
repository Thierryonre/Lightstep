# Resonant / multi-pulse laser wakefield excitation — literature notes

Compiled 2026-10-27 for the MCF project (efficient, inexpensive LWFA for protons to ~6 GeV,
possibly driven by several lower-power, high-efficiency lasers).

Labels: **[paper]** = read in full text; **[abstract only]** = from abstract/listing only;
**[inference]** = my own reasoning/derivation, not stated by the authors.

Status: complete (2026-10-27). Sections 1-4 were appended source by source, followed by Implications and Reproduction targets.

---

## 1. Ross et al., "Resonant excitation of plasma waves in a plasma channel" (2024)

- **Citation:** A. J. Ross, J. Chappell, J. J. van de Wetering, J. Cowley, E. Archer, N. Bourgeois,
  L. Corner, D. R. Emerson, L. Feder, X. J. Gu, O. Jakobsson, H. Jones, A. Picksley, L. Reid,
  W.-T. Wang, R. Walczak, S. M. Hooker, *Phys. Rev. Research* **6**, L022001 (2024).
- **DOI:** 10.1103/PhysRevResearch.6.L022001. **arXiv:** 2310.05097 (v1, 8 Oct 2023), CC BY 4.0.
- **Access:** full text read (arXiv HTML v1, including Supplemental Material/Appendices A–E).
  Published PRR version not compared line-by-line (possible minor changes vs v1).
- **Facility:** Astra-Gemini TA3 (Rutherford Appleton Lab), Ti:sapphire, two synchronised beams.

### Laser (drive pulse train) [paper]
| Quantity | Value |
|---|---|
| λ0 | 800 nm; transform-limited FWHM 31 fs per beam |
| Train generation | Michelson interferometer placed after final amplifier and *before* the compressor; compressor partially compressed so the two chirped copies beat → train of short pulses (negatively chirped). Dazzler used to trim TOD/FOD |
| Spacing formula | τ = φ⁽²⁾·2πc/δX_Mich (φ⁽²⁾ = residual GDD, δX_Mich = Michelson path offset) |
| N | ≈ 10 pulses |
| τ (spacing) | 170 fs (main data set), 200 fs (some figures) |
| Train energy on target | 2.5 ± 0.5 J (unmodulated reference: 2.7 J, ~1 ps) |
| "Effective" coupled energy | 0.8 J (used in fluid modelling; matches measured red-shift better) |
| Energy/pulse | not reported; ~0.25 J if equal split [inference] |
| Uniformity | U = 1 − (τmax − τmin)/(2τavg) ≈ 0.9 at TOD ≈ 1×10⁴ fs³ |
| Focus | f/40 OAP; 1/e² radius 45.5 ± 3.4 µm; zR = 7.9 mm; 65% of energy inside FWHM; pointing jitter ~25×37 µm rms |
| a0 per pulse | not reported. Estimate: 0.25 J, 40 fs FWHM, w0 = 45 µm → P ≈ 6 TW, a0 ≈ 0.4–0.5 [inference] |

### Plasma channel [paper]
| Quantity | Value |
|---|---|
| Type | HOFI (hydrodynamic optical-field-ionised) channel in H2, *conditioned* by the leading ~3 pulses of the train (ionise the neutral collar → deeper, lower-loss channel; per WarpX PIC) |
| Channel-forming beam | ~100 mJ, 80 fs, axicon (3.6° base, 1.6° approach angle), Bessel focus FWHM 9.8 µm; delay to drive 3.5 ns |
| Energy cost of channel | ~7 mJ per cm of channel (~3% of drive energy) |
| Length | 110 mm (~14 zR) and 70 mm; cell-jet hybrid target, 10–150 mbar H2 |
| On-axis density | 1×10¹⁷ – 1×10¹⁸ cm⁻³ scanned; resonance at n_e,res = 4.3 ± 0.3 ×10¹⁷ cm⁻³ (T_p ≈ 170 fs) |
| Matched spot | W_M ≈ 40 ± 3 µm |
| WarpX channel model | n_e0 = 4.3e17, n_max = 6.2e18, n_∞ = 3.2e18 cm⁻³; d0 = 45 µm, d1 = 16 µm, d2 = 8 µm, r_max = 50 µm |

### Results [paper]
- Guiding of ~1–2.5 J, ~1.7 ps trains over 110 mm. Coupling T0 = 64 ± 4 % (well-aligned shots), attenuation
  length L_att = 124 ± 20 mm (all guided shots: T0 = 32 %, L_att = 96 mm). Theoretical mode-overlap coupling 71 %.
- Resonance signature: strong red-shift of transmitted spectrum (>40 nm extension beyond 820 nm) when
  T_p ≈ τ. No such resonance for the unmodulated 1 ps pulse (which only red-shifts via self-modulation
  above ~5.5×10¹⁷ cm⁻³).
- Measured resonance FWHM δn_e0 ≈ 1.6×10¹⁷ cm⁻³; predicted δn_e0/n_e,res ≈ 8/(3N) ≈ 1.2×10¹⁷ cm⁻³.
- Wake amplitude (fluid model, not measured directly): ~3 GV/m (0.8 J) to ~10 GV/m (2.5 J) →
  "stage energy gain of order 1 GeV" (no derivation given; presumably ~10 GV/m × ~0.1 m).
- Laser-to-wake efficiency, charge, beam acceleration: **not reported** (no injection/witness).

### Simulation [paper]
- In-house 2D-cylindrical quasistatic *fluid* code (benchmarked against WarpX), parabolic fully-ionised
  channel, non-evolving envelope (retrieved train). WarpX PIC (ADK ionisation) for channel conditioning.
  code_saturne CFD for gas target. Grid/resolution not reported. No public input decks found (see
  original-sims/resonant-channel-2024/SOURCE.md).

### Implementable formulas [paper unless noted]
- ω_p = (n_e e²/m_e ε0)^½, T_p = 2π/ω_p; resonance τ ≈ T_p; spectral sidebands at ω0 ± mω_p.
- Parabolic channel: n_e(r) = n_e0 + Δn (r/w0)², matched when Δn = 1/(π r_e w0²).
- Linear fluid wake in a channel (δφ = φ − 1, ξ = z − ct):
  [(∂ξ² + k_p²)(Δ⊥ − k_p²) − (d ln n_e/dr) ∂ξ²∂r] δφ = k_p²(Δ⊥ − k_p²)|a|²/4 ;
  δn/n_e = k_p⁻²(Δ⊥ − k_p²)δφ + |a|²/4.
- Photon-acceleration frequency shift after length z_end:
  Δω(ξ)/ω0 = −z_end (2c²/(ω0² w0²)) ⟨∂ξ(δn/Δn)⟩⊥, ⟨f⟩⊥ = (4/w0²)∫ f e^(−2r²/w0²) r dr.
  (Lets the measured red-shift be converted to a wake amplitude.)
- Resonance width: δn/n_res ≈ 8/(3N) [paper]. Cross-check [inference]: N equal kicks with phase
  slip φ = 2π(τ/T_p − 1) per pulse add as |Σ e^{ikφ}| = |sin(Nφ/2)/sin(φ/2)|; with δT_p/T_p = −½ δn/n,
  the amplitude-FWHM is δn/n ≈ 2.4/N (energy-FWHM ≈ 1.8/N) — consistent in scaling with 8/(3N).
- Note: transverse plasma-frequency variation in a channel (k_p(r)) causes wavefront curvature of the
  wake, which grows with the number of plasma periods behind the train — a limit on N in channels [paper's model; implication = inference].

---

## 2. Hooker et al., "Multi-pulse laser wakefield acceleration ..." (2014)

- **Citation:** S. M. Hooker, R. Bartolini, S. P. D. Mangles, A. Tünnermann, L. Corner, J. Limpert,
  A. Seryi, R. Walczak, "Multi-pulse laser wakefield acceleration: a new route to efficient,
  high-repetition-rate plasma accelerators and high flux radiation sources", *J. Phys. B: At. Mol.
  Opt. Phys.* **47**, 234003 (2014).
- **DOI:** 10.1088/0953-4075/47/23/234003 (open access, CC BY 3.0). **arXiv:** 1401.7874 (v1, 30 Jan 2014)
  — note: *not* 1406.xxxx.
- **Access:** arXiv v1 full text read (pdftotext); published IOP page also fetched (summary of
  published text — adds hydrogen-ion numbers, guiding demonstrations, √(π/4) in hosing criterion).

### Design example (the only quantitative MP-LWFA case in the paper) [paper]
| Quantity | Value |
|---|---|
| Pulse energy | 10 mJ per pulse |
| Duration | 100 fs FWHM |
| λ0 | 1 µm (two spectral branches at 1020 nm and 1035 nm → beat period T = 2π/Δω) |
| w0 | 40 µm (30 µm for the betatron-source variant) |
| a0 | 0.052 (I ≈ 3.7×10¹⁵ W/cm², P ≈ 94 GW per pulse [inference check]) |
| Spacing | = plasma period T_pe (≈ 266 fs at 1.75e17 [inference]) |
| Density | n_e = 1.75×10¹⁷ cm⁻³ (chosen to maximise energy gain); λ_p ≈ 80 µm, k_p w0 ≈ 3.1, E0 = mcω_p/e ≈ 40 GV/m [inference] |
| N | ≈ 120 useful pulses (total 1.2 J, train ≈ 32 ps [inference]) |
| Rep. rate / average power | 10 kHz → 12 kW average laser power on target [inference: 1.2 J × 10 kHz] |
| Wake growth | E_max grows **linearly with N** (fluid); δn/n reaches 22 % on axis → only mildly nonlinear, so **no spacing adjustment for relativistic detuning was needed** |
| Wake amplitude | E_max = 4.7 GV/m at N ≈ 120 (mobile/immobile Xe⁸⁺; ≈ 0.12 E0); **≈ 2.5 GV/m with mobile hydrogen ions** (published version) |
| Length / gain | L_acc = L_d/2 = 260 mm (accelerating+focusing phase), W_max = (2/π) E_max L_acc = 0.75 GeV (Xe⁸⁺); ≈ 0.4 GeV for H plasma (published version) |
| Electron beam assumed | 0.75 GeV, 1 % rms spread, 50 pC, ε_n = 0.1 µm, 5 fs FWHM, 10 kA, 10 kHz |
| Codes | Weakly-relativistic electron fluid equations (Miano 1990) + OSIRIS PIC (2D/3D not stated in arXiv text); GENESIS 1.3 for FEL |

### Limits on N and tolerances [paper]
- **Ion motion** is the limiting effect found: the train duration N·T_pe becomes comparable to the ion
  plasma period T_pi = 2π/ω_pi, ω_pi = (Z² n_i e²/(m_i ε0))^½. PIC with mobile H⁺ saturates far earlier
  than with Xe⁸⁺. [inference: at 1.75e17, T_pi(H⁺) ≈ 11 ps vs train 32 ps — this is the core
  problem for a hydrogen (proton-source) plasma.]
- **Nonlinear (relativistic) frequency shift:** not limiting for δn/n ≈ 22 %; for stronger wakes the
  authors propose a chirped/non-uniform spacing via spectral-phase control of the two branches
  (Deutsch et al. 1991 chirped beat wave) and **autoresonance** by down-sweeping the beat frequency
  through ω_p (Lindberg et al. 2006) for robustness against density variation and tapering.
- **Hosing (transverse pulse offsets):** stable if the longitudinal spacing is (1 − α)λ_p with
  0 < α < α_t = [2(N − 1)]⁻¹ (i.e. pulses spaced *slightly less* than λ_p); for α > α_t, stabilise by
  guiding in a waveguide with ω_ch > √(π/4) ω_h0 (ω_h0 = hosing frequency of an off-axis trailing pulse).
  For N = 120: α_t ≈ 0.4 % → spacing tolerance ~1 fs on 266 fs [inference].
- Detuning tolerance for coherent build-up is not given explicitly; see the generic formula in §1
  (δn/n ~ 2–3/N) [inference] → for N = 120, δn/n ≈ 2 %, i.e. density uniformity ≲ 1 % along the stage.

### Laser technology & efficiency arguments [paper]
- Ti:sapphire CPA wall-plug efficiency "much less than 0.1 %"; fibre / thin-disc / slab DPSS lasers
  give >1 kW average but only few-GW peak; multi-pulse moves energy storage from the gain medium to
  the plasma → "wall-plug efficiencies two orders of magnitude higher" (no detailed budget).
- Conceptual fibre system (Fig. 3): oscillator → two spectral branches (1020/1035 nm) → stretch to ns →
  pick to 10 kHz → pre-amp → 16-amplifier coherent combination with 8-replica divided-pulse
  amplification → partial recompression → combine → 120 × 10 mJ × 100 fs at 10 kHz.
- Peak intensity on optics reduced by N → small-diameter, short-focal-length coupling optics, D ∝ 1/√N
  (compact staging, maybe no plasma mirrors).
- Linear/quasi-linear regime (P < P_c) → no self-focusing, reduced spectral shifts; **requires
  external guiding** (capillary or plasma channel) and **external injection** (no self-trapping → no
  dark current).
- Train generation by beam splitters/delay lines costs >50 % loss; beat-wave method avoids that.

### Derived efficiency estimate [inference]
- Linear-wake energy per unit length (field + electron kinetic, Gaussian spot):
  U/L ≈ (ε0/2) E_max² (π w0²/4) [1 + 8/(k_p w0)²] ≈ 0.22 J/m for E_max = 4.7 GV/m, w0 = 40 µm.
  Over L_acc = 0.26 m that is ≈ 58 mJ, i.e. only **~5 % of the 1.2 J train** is transferred to the
  wake in one dephasing-limited stage. Quasi-linear multi-pulse wakes have pump-depletion lengths ≫
  dephasing length, so high laser-to-wake efficiency needs laser recycling/energy recovery,
  much longer (tapered) stages, or higher a0 per pulse.

---

## 3. Plasma-modulated plasma accelerator (P-MoPA)

### 3a. Jakobsson, Hooker & Walczak, PRL 127, 184801 (2021) — the P-MoPA proposal
- **Citation:** O. Jakobsson, S. M. Hooker, R. Walczak, "GeV-scale accelerators driven by
  plasma-modulated pulses from kilohertz lasers", *Phys. Rev. Lett.* **127**, 184801 (2021).
- **DOI:** 10.1103/PhysRevLett.127.184801. **arXiv:** 2110.00417 (v2, 27 Oct 2021). Accepted
  manuscript also at https://link.aps.org/accepted/10.1103/PhysRevLett.127.184801
- **Access:** full text + Supplemental Material read (arXiv v2 PDF via pdftotext).

**Concept [paper]:** 3 stages. (1) *Modulator*: a short low-energy seed (τ ≲ T_p0/2) drives a weak
wake (δn/n ≈ 2 %) in a plasma channel; a long (τ ≫ T_p0) joule-class drive pulse co-propagates and
is phase-modulated → sidebands at ω0 + mω_p0 (temporal envelope stays smooth). (2) Seed removed by
polariser; *dispersive optic* (GDD) shifts red vs blue sideband trains by T_p0/2 → train of short
pulses spaced T_p0. (3) *Accelerator*: second channel, same on-axis density, resonantly driven.
Only **one** high-energy long-pulse laser needed (vs two-colour beat wave).

**Laser [paper]:** λ0 = 1030 nm (thin-disk Yb:YAG) for driver and seed (800 nm seed variant studied).
| Case | Driver | Seed | w0 = W_M (modulator) | Seed–driver delay |
|---|---|---|---|---|
| (i)/(iii) | 600 mJ, 1 ps FWHM | 50 mJ, 40 fs | 30 µm | 1.7 ps |
| (ii)/(iv) (headline) | 1.7 J, 1 ps | 140 mJ, 40 fs | 50 µm | (same intensities as (i)) |
Derived [inference]: driver a0 ≈ 0.18 (I ≈ 4×10¹⁶ W/cm²), seed a0 ≈ 0.25 (I ≈ 8×10¹⁶ W/cm²);
P_driver ≈ 1.6 TW ≪ P_c ≈ 73 TW at 2.5e17 → no relativistic self-focusing, linear modulator.

**Plasma [paper]:** n_e0 = 2.5×10¹⁷ cm⁻³ (T_p0 = 220 fs, λ_p ≈ 67 µm, E0 ≈ 48 GV/m [inference]);
steep-sided "leaky" channel n_ch(r) = n_e0 + (1/(π r_e W_M²))(r/W_M)^α, α = 10, for r < r0 = 1.2 W_M;
flat for Δr = 10 µm then linear ramp to 0 over 10 µm (finite losses damp higher-order modes →
suppresses forward-Raman/modulational instabilities). Modulator L_mod = 120 mm; accelerator 100 mm,
W_M,acc = 30 µm (train from the 50 µm modulator is focused into a 30 µm channel). Ions stationary.

**Results [paper]:**
- Optimal GDD ψ(2) = −1480 fs² (case i; 1D model predicts ±1485 fs²) and −1620 fs² (case ii).
- Compressed pulses as short as 15 fs; peak intensity of train ∝ L_mod; but wake amplitude saturates
  for L_mod ≳ 100 mm because for resonant short-pulse trains **wake amplitude depends only on total
  train energy** once individual pulses are ≲ 45 fs (≪ T_p0 = 220 fs).
- Accelerator: δn/n ≈ 15 % (case iii); peak E_z ≈ 5–6 GV/m (Fig. 3c, case i); case (iv) larger
  ("considerably larger than Fig. 2"), quasi-linear over the whole 100 mm.
- Witness: 1 pC, 35 MeV, 5 fs rms, 4 µm wide injected at peak field → ~500 MeV at z ≈ 50 mm (narrow
  spectrum), **0.65 GeV mean at 100 mm**, spectrum broadens beyond ~50 mm from dephasing.
- **Laser-to-plasma energy transfer in the accelerator stage: 9 %** (from photon-number vs
  energy-loss bookkeeping; leakage separated out). Witness charge 1 pC → wake-to-beam negligible.
- 800 nm seed + 1030 nm driver also works but needs 150 mm modulator (group-velocity walk-off).
- Tolerances: seed–bunch delay ~10 fs; seed/drive pointing < 10 µrad.

**Codes [paper]:** EPOCH 4.17.10, 2D Cartesian; Δz = λ0/50 (modulator), λ0/100 (accelerator),
Δy = λ0/2.5; CPML transverse boundaries; Yee solver; stationary ions; train re-injected from
vacuum by FFT + quadratic spectral phase and Gaussian-beam back-propagation. FBPIC (RZ, 2 azimuthal
modes) cross-check. 1D quasistatic fluid wake solved with RK4.

**Implementable formulas [paper]:**
- Phase modulation in modulator (1D, linear, v_g ≈ v_p):
  b(ζ,τ) ≈ |b0(ζ)| Σ_m i^m J_m(−β) exp[i m(ω_p0 τ + Δφ′)],  **β = ½ (ω_p0²/ω0)(δn/n0)(z/v_g)**
  (sideband m carries |J_m(β)|²; β ≈ 1.7 for δn/n = 2 %, z = 120 mm [inference check]).
  With walk-off Δv = v_g − v_p: modulation ∝ τ·sinc(½ ω_p0 Δv τ / v_p).
- Optimal GDD (valid for β ≲ 3.83):  ψ(2)_opt = ± [Σ_{m=1}^{N} |J_m(β)| m³ / Σ_{m=1}^{N} |J_m(β)| m⁴] · π/ω_p0².
- Pulse peaks: t_n = nT_p0 + z/v_p + Δφ/ω_p0 ∓ T_p0/4 (red/blue trains offset by T_p0/2).
- 1D quasistatic wake: ∂²φ/∂ξ² = (k_p²/2)[(1 + a²/2)/(1 + φ)² − 1], E_z = −(m_e c²/e) dφ/dz,
  δn/n0 = [1 + a²/2 + (1 + φ)²]/[2(1 + φ)²] − 1  (a = peak normalised vector potential, linear pol.).
- Energy bookkeeping: ΔT_plasma/T0 = ΔT/T0 − ΔN/N0 (photon-number loss = leakage; energy loss beyond
  that = wake excitation).

### 3b. van de Wetering, Hooker & Walczak, "Multi-GeV wakefield acceleration in a plasma-modulated plasma accelerator" (PRE 2024)
- **Citation:** J. J. van de Wetering, S. M. Hooker, R. Walczak, *Phys. Rev. E* **109**, 025206 (2024)
  [journal volume per search listing "PRE 109:2 (2024)"; article number to be confirmed — see §3e].
- **arXiv:** 2311.00471 (v1, 1 Nov 2023). **Input decks:** Zenodo 10.5281/zenodo.10061009 (WarpX).
- **Access:** full text read (arXiv v1 via pdftotext).

**Parameters [paper]:** λ_L = 1030 nm, τ_drive = 1 ps FWHM; W_drive = 1.2 J (Fig. 1), 2.4 J (Figs 3–5a,b),
5.0 J (Fig. 5c). Accelerator channel = quasi-square (CHOFI-like) profile, Eq. (7):
n0(r) − n00 = Δn (r/R)¹⁰/(1.2)¹⁰ for r < 1.2R; = Δn for 1.2R ≤ r < 1.2R + d; linear ramp to 0 over
next d; 0 beyond; Δn = 1/(π r_e R²), d = 10 µm.
| Case | W_drive | n00 (cm⁻³) | R | w0 | β | E_max/E_wb | L_d | ΔW (PIC) | Laser→plasma |
|---|---|---|---|---|---|---|---|---|---|
| Fig. 5a | 2.4 J | 2.5e17 | 30 µm (R∞,eff ≈ 46 µm, Δn = 1.26e17) | 30 µm | 1.2 | ≈ 0.5 (≈ 24 GV/m) | 93 mm | ≈ 1.5 GeV | 16 % |
| Fig. 5b | 2.4 J | 2.5e17 | 30 µm | 30 µm | 2.4 | ≈ 0.5 | 80 mm | ≈ 1.5 GeV | 19 % |
| Fig. 5c | 5.0 J | 1.0e17 | 36 µm | 36 µm | 1.2 | 0.46 (≈ 14 GV/m) | 300 mm (Eq. 3: 296) | ≈ 2.5 GeV (Eq. 4: 2.6) | n.r. |
- Witness: 1 pC, 35 MeV, x_rms = 4 µm, z_rms = 1.5 µm (×2.5 at 1e17), placed at peak field; no beam
  loading studied (explicitly left for future work).
- Fig. 1 snapshot: on-axis wake δn/n ≈ 50 % resonantly driven; strong wake also on the channel inner
  wall (steep gradient d ln n0/dr > k_p) → transverse wavebreaking may precede longitudinal.
- Codes: WarpX, 2D PIC (resolution in Zenodo decks). Paraxial weakly-relativistic envelope theory.

**Key physics / formulas [paper]:**
- Matched parabolic channel: n0(r) = n00 + Δn (r/w0)², Δn = 1/(π r_e w0²).
- Group velocity in channel: v_g/c = 1 − ω_p0²/(2ω_L²) − 2c²/(ω_L² w0²).
- Dephasing length: L_d = (λ_p0/4)[ω_p0²/(2ω_L²) + 2c²/(ω_L² w0²)]⁻¹.
- Energy gain (linear, sinusoidal wake): ΔW/(m_e c²) ≈ (2/π) eE_max L_d/(m_e c²)
  = 2 (E_max/E_wb) ω_L²/(ω_p0² + 4c²/w0²).
- Spot-size prescription: w0 ≳ 2c/ω_p0 = λ_p0/π. Scaling: W_drive ∝ w0²λ_p ∝ λ_p³, ΔW ∝ λ_p²,
  Q ∝ λ_p → laser-to-bunch efficiency has **no density scaling** (same as single-pulse linear LWFA).
- Pump depletion: L_pd = (π E_max/(8 E_wb))⁻¹ L_d (always > L_d in linear regime; trailing pulses
  deplete up to 2× faster). For E_max/E_wb = 0.5: L_pd ≈ 5.1 L_d [inference].
- **Channel limit on N:** in deep parabolic channels (½k_p0²w0² < 1) axial wake converts to radial
  within a few buckets; to use N pulses need ½k_p0²w0² ≫ N (e.g. w0 ≫ 75 µm at 1e17, N = 10 →
  10-J-scale drivers), *or* square-profile channels (CHOFI) which largely avoid it. Ion-motion
  modulational instability acts later (~40 λ_p for hydrogen).
- **P-MoPA pulse shape:** f_acc(ξ;β) = f_mod(ξ)[J0(β) + 2 Σ_{n≥1} J_n(β) cos(n k_p0 ξ)],
  β = 2Ω_s L_mod/v_g,mod, Ω_s = (ω_p0²/(8ω_L))(δn_s/n00). Peak amplitude max at β = j0,1 ≈ 2.405
  (f_acc = 2.47 f_mod). Use β ≤ 2.405; linear wake is optimised for β ≈ 1.1–1.6.
- **P-MoPA vs beat wave:** φ_P-MoPA/φ_PBWA = 4 Σ_{n≥0} J_n(β)J_{n+1}(β) = 2β[J0²(β) + J1²(β)];
  maximum 1.72 at β ≈ 1.43 (72 % more wake per joule than an ideal 1 + cos beat-wave train).
- **Rosenbluth–Liu detuning:** λ_p^NL ≈ λ_p(1 + 3φ_a²/16); beat-wave saturation E_sat/E_wb = (16a1a2/3)^{1/3}.
  For a Gaussian-envelope P-MoPA train (N_eff = 2τ_FWHM/T_p), requiring ≥ 90 % of energy before π/2
  detuning: E_max/E_wb < √(2.8/N_eff). Example: τ = 2 ps at 2.5e17 → N_eff = 18 → E_max < 32 GV/m
  (0.66 E_wb). For E_max/E_wb ≲ 0.5 → **N_eff < 30**. Detuning partly self-compensated because
  trailing pulses red-shift more (spacing grows). Quiver-relativistic detuning: use slightly higher
  density in the accelerator than the modulator.
- **Transverse mode beating (square channel radius R∞):** Bessel modes, w0,eff ≈ 0.66 R∞;
  spot-oscillation frequency ω_w ≈ 12.3 c²/(ω_L R∞²); R∞,eff = 46 µm → 2πc/ω_w ≈ 6.6 mm (matches PIC
  oscillation of on-axis E_z). Coupling coefficients d00 ≈ 0.57, d01 ≈ 0.27, d11 ≈ 0.48;
  γ(ξ) = (ω_p0²/(2ω_L))(δn_a(ξ)/n00 − |a0|² f_acc²/4).

### 3c. van de Wetering, Hooker & Walczak, "Stability of the modulator in a P-MoPA", PRE 108, 015204 (2023)
- **Citation:** J. J. van de Wetering, S. M. Hooker, R. Walczak, *Phys. Rev. E* **108**, 015204 (2023)
  (citation as given in ref. [16] of the 2023 accelerator-stage preprint).
- **arXiv:** 2303.14032 (v1, 24 Mar 2023). **Input decks:** Zenodo 10.5281/zenodo.7734261 (WarpX 22.07).
- **Access:** full text read (arXiv v1, incl. Supplemental Material).

**Parameters [paper]:** all runs n00 = 2.5×10¹⁷ cm⁻³, λ_L = 1030 nm, τ_seed = 40 fs, W_seed = 50 mJ
(w0 = 30 µm), L_mod = 110 mm; W_drive 0.6–2.4 J; τ_drive = 0.25, 1, 2, 4 ps; square vs parabolic
channels (w0 = 30 or 50 µm, wall thickness d = 10 µm); WarpX 22.07 2D, Δz = λ/50, Δx = λ/2.5,
Yee solver, PML, transverse window ≥ 2.67 w0. Square channel: n − n00 = Δn (r/1.2w0)¹⁰ for r < 1.2w0, etc.

**Findings [paper]:**
- 3D theory: spectral modulation is *independent of radius* (good for compression):
  Δω(ξ; L_mod)/ω_L = −L_mod (2c²/(ω_L² w0²)) ⟨∂_ξ(δn/Δn)⟩⊥.
- Wake phase-front curvature in **parabolic** channels suppresses modulation toward the drive-pulse
  tail; **square** channels (flat wavefronts) work much better; larger parabolic spot (50 µm) helps.
  3D curvature effect worse than 2D. 2D slab modulates ~√2 faster than 3D cylindrical.
- Instability regime: Mori parameter Γ = (P/1 TW)(τ_L/1 ps)(n_e/10¹⁹ cm⁻³)^{5/2}(λ_L/1 µm)⁴; RFS if Γ ≥ 3,
  envelope self-modulation (SM) if Γ ≤ 0.4. Jakobsson params: Γ = 6.3×10⁻⁵ → SM regime;
  γ_SM = (1/8) a0² (ω_p²/ω_L)(1 + a0²)^{-3/2}; ~1.3 e-folds in the 2021 design.
- **Transverse mode instability (TMI)**, analogous to fibre-laser TMI, limits drive energy.
  **Stability condition (Eq. 15):**
  [(δw/w0)/(δn_s/n00) + k_p0² w0²/8] · ω_p0 W_drive λ_L²/(π w0²) ≪ P_mod = 32π² m_e² ε0 c⁵/e² ≈ 220 GW.
  Jakobsson case (δn_s/n00 ≈ 2.5 %, δw/w0 ≈ 12 %): LHS = 37 GW (verified numerically [inference]);
  PIC remains usable up to LHS ≈ 70 GW. Condition is independent of τ_drive (confirmed for 0.25–4 ps
  at 1.2 J). → spot mismatch δw/w0 must be minimised; W_drive,max ∝ w0²/(λ_L² ω_p0 × ...).
- Stokes (red) sidebands defocus and go off-axis faster than anti-Stokes (non-paraxial asymmetry);
  at 2.4 J in a 30 µm square channel the drive pulse breaks up severely.
- Modulation needed: Ω_s τ_mod ≈ ½ (i.e. β ≈ 1) roughly reaches the accelerator wake plateau.
- Mitigations: deeper channels (but more curvature), leaky channels (lose energy in higher modes).

### 3d. Public P-MoPA simulation inputs (downloaded)
- `original-sims/pmopa/accelerator-zenodo-10061009/` — 4 WarpX 23.06 2D accelerator decks (1.2/2.4/5.0 J;
  β = 1.2/2.4; n = 2.5e17 / 1e17). The 268 MB pulse-train field files (*.txye) were **not** downloaded
  (>200 MB); they must be regenerated. Grid: 384 × 63872 cells, 160 µm × 1.5 mm, CKC, moving window.
- `original-sims/pmopa/modulator-zenodo-7734261/` — 8 WarpX 22.07 2D modulator decks (0.6–2.4 J,
  0.25–4 ps, square/parabolic, one with mobile protons).
- Details, checksums and caveats in `original-sims/pmopa/SOURCE.md`. [paper/deck]

### 3e. Published-version note
- Accelerator-stage paper confirmed as *Phys. Rev. E* **109**, 025206 (2024), DOI 10.1103/PhysRevE.109.025206
  (link.aps.org listing). Oxford group page lists no 2025–2026 P-MoPA journal paper (first page checked);
  Oxford news item reports the PRR 2024 experiment as the "accelerator stage" demonstration using a
  Michelson-generated train that *mimics* the modulator + compressor. [abstract only]
- No experimental demonstration of the full modulator→compressor→accelerator chain, and no
  kHz-thin-disk-driven P-MoPA experiment, was found in searches up to Oct 2026 (searches: arXiv/web
  "plasma-modulated plasma accelerator" 2025/2026, Hooker/Walczak 2025). [inference from search]

---

## 4. Other multi-pulse / pulse-train wake drivers and closely related physics (brief)

### 4a. Walter, Farmer, Turner, Jenko, "Influence of ion motion in a resonantly driven wakefield accelerator", arXiv:2512.14476 (Dec 2025)
- **Access:** full text (arXiv HTML) summary. Proton-beam (AWAKE) self-modulation, not laser:
  400 GeV, 49 nC, σ_z = 170 ps p⁺ bunch; 10 m plasma at 4.8×10¹⁴ cm⁻³; Xe, Ar, He compared; LCODE.
  Companion experiment: Turner et al., PRL 134, 155001 (2025).
- **Relevant physics [paper]:** ion motion driven by the time-averaged ponderomotive force of the
  wakefield itself, F_p,i = −(Z e²/(4 m_e ω_p²)) ∇Ê²; two damage channels — (i) loss of resonance
  (detuning from ion-density-induced plasma-frequency change) near the head, (ii) phase mixing via
  transverse wavebreaking toward the tail; both scale as **m_i^(−1/3)** (time to onset ∝ m_i^(1/3)).
- **Implication [inference]:** a long resonant train in a *hydrogen* plasma (needed if protons are
  the accelerated species/source) suffers the earliest ion-motion damage: relative to He the onset is
  (1/4)^(1/3) ≈ 0.63× earlier; relative to Ar ≈ 0.29×; relative to Xe ≈ 0.20×.

### 4b. Farmer & Zevi Della Porta, "Wakefield regeneration in a resonantly driven plasma accelerator", arXiv:2404.14175 (v2 Feb 2025)
- **Access:** abstract only. AWAKE-type drive-bunch train; periodically loading the wake with
  multiple witness bunches removes the limit on drive-to-plasma energy transfer; proof-of-concept
  simulations double accelerated charge using only a fraction of the drive train. [abstract only]
- **Implication [inference]:** the same "multi-witness / periodic beam loading" idea applies to a
  laser pulse train: in the quasi-linear multi-pulse regime the laser depletes slowly, so loading
  several buckets (or interleaving trains and witnesses) is a route to higher laser-to-beam efficiency.

### 4c. Jonnerby et al., "Measurement of the decay of laser-driven linear plasma wakefields", PRE 108, 055211 (2023)
- **Authors:** J. Jonnerby, A. von Boetticher, J. Holloway, L. Corner, A. Picksley, A. J. Ross, R. J. Shalloo,
  C. Thornton, N. Bourgeois, R. Walczak, S. M. Hooker. **arXiv:** 2306.06438 (CC BY 4.0).
  **DOI:** 10.1103/PhysRevE.108.055211. **Access:** full text (pdftotext, key sections).
- **Setup [paper]:** Astra-Gemini TA3, 1.68 J, 800 nm, 48.9 fs FWHM, f/40, w0 = 52.3 µm,
  I = 6.5×10¹⁷ W/cm², a0 = 0.54; gas cell H2 and D2, n_e0 = 8.4×10¹⁷ cm⁻³ (T_pe = 121 fs);
  1D linear wake δn/n ≈ 6 % (H), 4 % (D); measured by single-shot frequency-domain holography (TESS).
  Simulations: Smilei 2D PIC (8λ_p × 160 µm window, fixed), EPOCH for post-ionisation temperature.
- **Results [paper]:** 1/e wake lifetime τ_wf(H2) = 9 ± 2 ps (≈ 76 T_pe; ≈ 1.7 T_pi with
  T_pi(H⁺) = 5.2 ps), τ_wf(D2) = 16 ± 8 ps (≈ 134 T_pe; T_pi(D⁺) = 7.4 ps). Simulated ratio D/H = 1.76.
  Decay dominated by ion-coupled **modulational instability** (Mora et al. 1988), growth set by
  W = ε0|E_L|²/(2 n_e0 k_B T_e); faster than collisional/Landau damping (absent beam loading).
  Survey of earlier experiments: τ_wf/T_pe varies < 5× across >100× range of density & pulse length.
- **Authors' conclusion:** lifetime ~100 plasma periods ≫ N ≈ 10 pulses of ps-scale trains → not limiting
  for P-MoPA. **[inference for protons]** For ~100-pulse trains (Hooker 2014 fibre design) in hydrogen,
  the wake decays on the same timescale as the train (consistent with the 2014 PIC result that mobile H⁺
  cut E_max from 4.7 to ≈ 2.5 GV/m). Since T_pi ∝ (M/Z)^½ n^(−½), decay time in units of T_pe is
  roughly density-independent (~40·√(M/m_p) T_pe per T_pi); heavier/less-ionised gases (D2, He, N, Ar)
  extend it, but a pure-hydrogen plasma is the worst case. Lower total train length (fewer, stronger
  pulses; N ≲ 30) is the safe regime.

### 4d. Cowley et al., "Excitation and control of plasma wakefields by multiple laser pulses", PRL 119, 044802 (2017)
- **Authors:** J. Cowley, C. Thornton, C. Arran, R. J. Shalloo, L. Corner, G. Cheung, C. D. Gregory,
  S. P. D. Mangles, N. H. Matlis, D. R. Symes, R. Walczak, S. M. Hooker. **DOI:** 10.1103/PhysRevLett.119.044802.
  **arXiv:** 1708.04206. **Access:** full text (pdftotext). First MP-LWFA demonstration (pre-2020 but the
  experimental baseline for everything above).
- **Setup [paper]:** Astra-Gemini TA2 Ti:sapphire (600 mJ, 40 fs, 800 nm, 5 Hz standard); Michelson between
  final amplifier and compressor (same method as §1); f/18 OAP; pure H2 gas cell; linear wakes measured by
  frequency-domain holography and TESS.
  Cases: N = 1 (270 mJ, 43 fs); N = 2 (δτ = 365 fs, 160 mJ total); N ≈ 7 (δτ = 112 fs, 170 mJ, beat-wave-like
  chirped train). T_p0 = 90 ± 5 fs at 31 mbar.
- **Results [paper]:** clear constructive/destructive interference for N = 2 and a pronounced resonance for
  N ≈ 7 when T_p0 = δτ (fit δτ = 116 ± 2 fs). **Energy-recovery demo:** an out-of-phase trailing pulse
  reduced wake amplitude 0.60 % → 0.35 % (−40 %; ≈ 66 % of wake energy removed [inference, ∝ amplitude²]),
  energy leaves as blue-shifted photons in the trailing pulse. Wake observable ~2 ps (~20 T_p), limited by
  cell density non-uniformity: number of coherent periods ≈ n_e0/(2Δn_e0) → Δn/n ≈ 2.5 %.
  PIC: ion motion reduces wake only after ~80 T_p.
- **Formulas [paper]:**
  - Single Gaussian pulse (linear, 3D correction): δn/n|₁ = A ω_p0 τ0 [1 + (2√2 c/(ω_p0 w0))²] exp[−(ω_p0 τ0)²/(16 ln 2)],
    τ0 = intensity FWHM, A ∝ peak intensity.
  - **N identical pulses spaced δτ:** δn/n|_N = δn/n|₁ · sin(½ N ω_p0 δτ)/sin(½ ω_p0 δτ)
    (→ N·δn/n|₁ on resonance; this is the linear-superposition/detuning formula to implement).
  - Coherence-length rule: N_coh ≈ n_e0/(2Δn_e0) for a density spread Δn_e0 (applies to the pulse
    count as well [inference]).

### 4e. Maurya et al., "Wakefield amplification via coherent resonant excitation with two copropagating laser pulses in homogeneous plasma", arXiv:2603.21798 (Mar 2026)
- **Access:** abstract only. Seed + trailing pulse in uniform plasma; analytic + PIC; claims up to 3×
  single-pulse wake with separation ≈ λ_p/4. [abstract only]
- **Caution [inference]:** linear theory (§4d) gives constructive addition at δτ = T_p and at most 2× for two
  equal pulses; a λ_p/4 optimum and 3× gain must reflect a nonlinear regime, unequal pulses, or a different
  definition of separation. Low priority; do not use as a design input without reading the full text.

### 4f. Benedetti, Schroeder, Esarey, Leemans, "Plasma wakefields driven by an incoherent combination of laser pulses: a path towards high-average power laser-plasma accelerators" (LBNL, 2014)
- **Where:** OSTI accepted manuscript https://www.osti.gov/servlets/purl/1163658 (full text read via pdftotext).
  Journal: *Phys. Plasmas* **21**, 056706 (2014) [inference — citation recalled, not shown on the OSTI PDF text;
  verify]. Pre-2020 but the key reference for "many lower-power lasers" drivers.
- **Core result [paper]:** the linear wake behind the driver depends only on the time-averaged energy density
  ⟨a²⟩ over scales ≪ λ_p/c, so **phase-incoherent** combination of many beamlets drives a regular wake
  *behind* the driver equal (or nearly equal) to a single coherent pulse of the same energy, provided the
  incoherent structure is on time scales < ω_p⁻¹ and enough energy sits within ~λ_p³.
- Three schemes (ALaDyn PIC, 2D):
  1. **Spectral combining** (spectrally separated pulses overlapped by dichroics/gratings): wake = coherent
     pulse with the *same energy* (100 % equivalent). Limit: group-velocity dispersion between colours
     lengthens the driver (dispersion length ∝ 1/N); max N ~ 3/β (equal a0) or ~1.6/β² (equal energy),
     β = fractional spectral spacing ≫ k_p/k0. Example 10 GeV stage (30 J, 1 µm, A0 ≈ 1, k_p/k0 ≈ 0.01,
     β = 0.08): N ≈ 20 (equal a0, λ = 0.6–8.9 µm) or N ≈ 250 (equal energy, 120 mJ each, λ = 0.05–12 µm —
     impractical range). Polarisation multiplexing doubles N.
  2. **Longitudinal stacking of very short pulses** (ℓ0 ≈ 2λ0, random phases): wake equals flat-top coherent
     pulse; ~8 % more energy needed (37 pulses, a0 = 2.45 vs A0 = 1.5).
  3. **Mosaic of beamlets** tiling the λ_p-scale volume transversely and longitudinally (e.g. 208 = 13×8×2
     beamlets, a0 = 1.5, ℓ0 = 4 µm, d0 = 15 µm, 0.8 µm, n0 = 0.9e17, guided in a flat-bottom steep-wall
     channel n = n0 + ρ(|x| − R)⁸): regular wake behind driver, "a few %" more energy than coherent;
     energy guided over many beamlet Rayleigh lengths. 10 GeV-stage estimate: ~16 × 6 × 6 × 2 ≈ 10³
     beamlets of ~10 fs, 10 µm.
- **Relevance [inference]:** the resonant pulse train (§1–3) is the *longitudinal-period-λ_p* version of
  incoherent combination; spatial/spectral incoherent tiling is an alternative way to sum several
  independent lasers **without phase locking**, but needs either very short beamlets (≲ 10 fs) or broad
  spectral separation — both hard for efficient Yb/Tm lasers. Resonant trains need only timing to a
  fraction of T_p (tens of fs) — far easier than optical-phase locking.

### 4g. Sadler, Arran, Li, Flippo, "Overcoming the dephasing limit in multiple-pulse laser wakefield acceleration", PRAB 23, 021303 (2020)
- **arXiv:** 2001.09108. **Access:** abstract only (via mirrors).
- **Result [abstract only]:** density modulation switches a pulse-train wake on (resonant sections) and off
  (non-resonant drift sections in which the wake vanishes and electrons rephase). 2D PIC: **four 2.5 TW
  pulses → 50 MeV gain, 4× a uniform plasma**. Laser red-shift precludes the blowout regime; useful for
  linear-regime accelerators limited by laser power; minimising depletion → sub-relativistic intensities.
- **Relevance [inference]:** a multi-pulse-specific route past L_d without staging optics — relevant if a
  6 GeV proton stage would otherwise be dephasing-limited (but protons at < few GeV are far below c, so
  dephasing is dominated by the *proton* velocity, not the laser — see Implications).

### 4h. Vantaggiato, Labate, Tomassini, Gizzi, "Modelling of pulse train generation for resonant LWFA using a delay mask", NIM A (2018), DOI 10.1016/j.nima.2018.02.024
- **arXiv:** 1802.00826. **Access:** abstract only. Concentric-zone delay mask (different thicknesses)
  before the final parabola splits one pulse into a train (Resonant Multi-Pulse Ionisation injection,
  ReMPI, INO-CNR Pisa); central hole passes an undelayed injector pulse. [abstract only]
- **Relevance [inference]:** a mask-segmented aperture is optically equivalent to *several separate
  lasers sharing one focusing optic with staggered delays* — a template for combining N independent
  efficient lasers into a resonant train at a common focus (each annulus/sub-aperture = one laser;
  only timing at ≲ 0.05 T_p needed, no optical phase lock).

### 4i. Driver-laser status relevant to multi-pulse schemes (brief)
- Thin-disk ps lasers cited by the P-MoPA papers [paper refs]: 720 mJ, 920 fs, 1 kHz (Herkommer et al.,
  Opt. Express 28, 30164 (2020), TRUMPF Scientific, 4 thin-disk heads, room temperature); 1.1 J, ps, 1 kHz
  cryogenic Yb:YAG (Wang et al., Opt. Lett. 45, 6615 (2020), Colorado State); >10 kW near-fundamental-mode
  thin-disk (Nagel et al., Opt. Lett. 46, 965 (2021)); thin-disk optical-to-optical efficiency > 50 %
  (Jakobsson 2021). Searches (Oct 2026) found no confirmed 2024–2026 multi-J, kHz thin-disk record beyond
  these; 330 mJ/100 Hz and 500 mJ/1 kHz programmes reported 2023. [abstract only / search]
- Coherent fibre combination: 3.5 kW coherently-combined ultrafast fibre laser (arXiv:2101.08499, Jena);
  LBNL kBELLA fibre programme (coherent spatial + temporal combining of mJ beamlets at multi-kHz). No
  wake-driving experiment with a combined fibre array was found (2020–2026). [search / abstract only]
- Wall-plug numbers: Ti:sapphire < 0.1 % (all papers); "two orders of magnitude higher" for fibre/thin-disk
  (Hooker 2014, Cowley 2017), i.e. ~10 %; no paper gives an audited wall-plug budget. [paper]

---

## Implications for an efficient proton LWFA

All items below are **[inference]** unless tagged.

1. **The resonant-train toolbox is mature only for the linear/quasi-linear, luminal-wake regime.**
   Demonstrated: resonance with N ≈ 7–10 (Cowley 2017; Ross 2024), guiding of ~1–2.5 J, 1.7 ps trains in
   110 mm HOFI channels. Simulated: 0.65–2.5 GeV *electron* gains with 1.7–5 J ps drivers at
   1e17–2.5e17 cm⁻³ (E_max/E_wb ≈ 0.5, 14–24 GV/m). Nothing in this literature treats protons.
2. **Phase-velocity mismatch is the dominant obstacle for protons, not wake amplitude.** These wakes move
   at v_g ≈ c(1 − 1.8×10⁻⁴) (2.5e17, 1.03 µm, 30 µm spot). A proton at 1 GeV (β = 0.875) dephases in
   (λ_p/4)/(β_φ − β) ≈ 0.13 mm (≈ 2 MeV gain at 24 GV/m); at 6 GeV (β = 0.9908) in ≈ 1.9 mm (≈ 28 MeV).
   So a P-MoPA-type stage cannot accelerate protons from rest or from a ~100 MeV–1 GeV injector without
   **phase-velocity control**: (a) lower γ_φ ≈ ω0/ω_p to ~γ_p — γ_φ ≈ 7.4 needs n ≈ 2e19 cm⁻³ at
   1.03 µm (T_p ≈ 25 fs), which removes the main virtue of multi-pulse schemes (long T_p allows long,
   efficient-laser pulses); (b) longitudinal density up-ramps / tapering that slow the accelerating
   bucket (unexplored for trains; tapering conflicts with resonance, which needs δn/n ≲ 2.4/N);
   (c) flying-focus / spatiotemporal control of the driver velocity; or (d) pre-accelerate protons to
   γ ≫ γ_φ elsewhere (defeats the purpose). Any design study must start from the proton β(z) vs v_φ(z)
   matching problem.
3. **Pulse count N is bounded from several sides.** Design for **N ≈ 10–30**:
   - Resonance/detuning tolerance: amplitude FWHM δn/n ≈ 2.4/N (linear theory) ≈ 8/(3N) (Ross). Density
     uniformity along the stage and pulse-spacing jitter must be ≪ 1/N (N = 10 → ~±5 %; N = 120 → ±1 %).
   - Rosenbluth–Liu (relativistic) detuning: E_max/E_wb < √(2.8/N_eff) → N_eff < 30 for E/E_wb ≈ 0.5.
   - Hosing: spacing (1 − α)λ_p with α < 1/(2(N − 1)) (N = 120 → 0.4 % ≈ 1 fs) unless channel-guided.
   - Channel wake-front curvature: parabolic channels need ½k_p²w0² ≫ N; square-ish (CHOFI) channels relax it.
   - Ion motion: train duration must be ≪ wake lifetime (≈ 9 ps ≈ 75 T_p in H2 at 8.4e17; T_pi(H⁺) ≈
     43 T_p at any density). Hooker 2014's N = 120 train (32 ps) lost about half its field with mobile H⁺.
   ⇒ **Use D2/He or a heavier plasma rather than H2** if the plasma need not be the proton source
   (lifetime ∝ m_i^(1/3)–(1/2)); keep the train ≲ 10–30 T_p.
4. **"Several lower-power lasers" is physically allowed.** The linear wake is the coherent sum of each
   pulse's wake (Cowley Eq. 4), so independent lasers need only **timing synchronisation to ≲ 5 % of T_p
   (~10 fs at 2.5e17)** and pointing ≲ 10 µrad, not optical phase locking. Incoherent spatial/spectral
   tiling (Benedetti 2014) also works, but needs ≲ 10 fs beamlets or a huge spectral spread. A segmented
   aperture / delay mask (Vantaggiato 2018) or a Michelson cascade is the optical template. The P-MoPA
   modulator lets one *long-pulse* thin-disk laser make its own train, needing only one seed laser of
   50–140 mJ, 40 fs.
5. **Efficiency chain (best numbers in the literature):** laser → plasma 9 % (Jakobsson 2021, 1.7 J) to
   16–19 % (van de Wetering 2024, 2.4 J, quasi-square channel, over one L_d); ~5 % for the 2014 120-pulse
   design [inference estimate]. Wake → beam: **never studied** (1 pC test bunches; beam loading explicitly
   left as future work). Coupling into channels: 64 % (best shots, Ross 2024), L_att ≈ 124 mm.
   Channel-forming cost ~7 mJ/cm (~3 % of drive). In the linear regime L_pd = (π E_max/(8E_wb))⁻¹ L_d ≈
   5 L_d at E/E_wb = 0.5, so most laser energy exits a dephasing-limited stage unused. Routes up:
   **energy recovery** (an out-of-phase trailing pulse removed ~66 % of wake energy, Cowley 2017), re-use
   of the transmitted train in further stages, multiple witness bunches per train (Farmer 2024), heavier
   beam loading. With ~20–30 % wall-plug lasers × ~20 % laser→wake × ≤ 50 % wake→beam, plan around a
   ~2–3 % wall-plug-to-beam ceiling today.
6. **Density/energy scaling (van de Wetering 2024, linear theory):** W_drive ∝ λ_p³, ΔW ∝ λ_p², Q ∝ λ_p;
   laser-to-bunch efficiency is density-independent; ΔW ≈ 2(E_max/E_wb)(ω_L²/(ω_p² + 4c²/w0²)) m_e c².
   For luminal electron-like acceleration, 6 GeV per stage needs ~1e17 cm⁻³ and ≳ 5–10 J. For protons the
   binding limit is item 2.
7. **Code choice for reproduction:** WarpX decks are public (2D, ~2.5×10⁷ cells, ~10⁶ steps per 100 mm),
   but expensive. A quasistatic/envelope code (FBPIC, Wake-T, HiPACE-style) or the papers' 1D/2D fluid
   models is adequate for the linear-regime targets below.

## Reproduction targets (numbers)

| # | Target | Inputs | Expected output | Source |
|---|---|---|---|---|
| R1 | Linear N-pulse superposition | identical pulses, spacing δτ | δn/n_N = δn/n₁·sin(½Nω_pδτ)/sin(½ω_pδτ); on resonance = N·δn/n₁ | Cowley 2017 |
| R2 | Resonance width vs density | N pulses, fixed τ | amplitude FWHM δn/n ≈ 2.41/N (my calc: 0.242 for N = 10); paper formula 8/(3N) = 0.27; measured 1.6e17/4.3e17 = 0.37 | Ross 2024 |
| R3 | Resonant density | τ = 170 fs | n_res = 4.3(±0.3)×10¹⁷ cm⁻³ (T_p = τ) | Ross 2024 |
| R4 | MP-LWFA fibre design | 120×10 mJ, 100 fs, 1 µm, w0 = 40 µm, a0 = 0.052, n = 1.75e17, spacing T_p = 266 fs | E_max linear in N; 4.7 GV/m at N = 120 (immobile ions); my 1D linear estimate 5.0 GV/m; δn/n = 22 %; L_d/2 = 260 mm; ΔW = (2/π)E_max L = 0.75 GeV; mobile H⁺: ≈ 2.5 GV/m, ≈ 0.4 GeV | Hooker 2014 |
| R5 | Hosing threshold | N = 120 | α_t = 1/(2(N−1)) = 0.42 % (≈ 1.1 fs of 266 fs) | Hooker 2014 |
| R6 | P-MoPA modulator | 600 mJ/1 ps + 50 mJ/40 fs, 1030 nm, w0 = W_M = 30 µm, n = 2.5e17, α = 10 channel, L_mod = 120 mm | seed wake δn/n ≈ 2 %; β ≈ 1.7; optimal GDD −1480 fs² (1D theory ±1485); pulses down to 15 fs; T_p0 = 220 fs | Jakobsson 2021 |
| R7 | P-MoPA accelerator (PRL) | 1.7 J/140 mJ (w0 = 50 µm modulator) → 30 µm channel, 100 mm | δn/n ≈ 15 % (0.6 J case); 1 pC 35 MeV witness → ~0.5 GeV at 50 mm, 0.65 GeV mean at 100 mm; laser→plasma 9 % | Jakobsson 2021 |
| R8 | Wake saturation vs pulse length | resonant train | wake depends only on total train energy once pulses ≲ 45 fs (T_p0 = 220 fs) | Jakobsson 2021 SM |
| R9 | P-MoPA vs beat wave | — | φ_P-MoPA/φ_PBWA = 2β[J0²(β)+J1²(β)], max 1.723 at β = 1.435; peak f_acc = 2.47 f_mod at β = 2.405 | vdW 2024 |
| R10 | Multi-GeV stage A | 2.4 J, 1 ps, β = 1.2, n = 2.5e17, quasi-square R = 30 µm (R∞,eff = 46 µm, w0,eff = 30 µm) | E/E_wb ≈ 0.5; L_d = 93 mm (Eq. 3: 93.4 mm, my calc); ΔW ≈ 1.5 GeV (Eq. 4: 1.43 GeV); laser→plasma 16 % (19 % at β = 2.4, L_d 80 mm); spot-oscillation period 6.6 mm | vdW 2024 + Zenodo decks |
| R11 | Multi-GeV stage B | 5.0 J, n = 1e17, R = 36 µm, β = 1.2 | E/E_wb = 0.46; L_d ≈ 300 mm (Eq. 3: 296); ΔW ≈ 2.5 GeV (Eq. 4: 2.6; my calc 2.64) | vdW 2024 + Zenodo decks |
| R12 | Rosenbluth–Liu limit | τ_FWHM = 2 ps, n = 2.5e17 | N_eff = 18, E_max < 32 GV/m (0.66 E_wb); N_eff < 30 for E/E_wb ≲ 0.5 | vdW 2024 |
| R13 | Modulator TMI criterion | 0.6 J, w0 = 30 µm, δn_s/n = 2.5 %, δw/w0 = 12 % | LHS = 37 GW ≪ P_mod = 220 GW (my calc 36.8/219 GW); usable to ~70 GW | vdW 2023 |
| R14 | Wake lifetime (ion motion) | 1.68 J, 49 fs, w0 = 52 µm, a0 = 0.54, n = 8.4e17 | δn/n ≈ 6–7.5 %; τ_wf(H2) = 9 ± 2 ps (≈ 76 T_p), τ_wf(D2) = 16 ± 8 ps; sim ratio D/H = 1.76 | Jonnerby 2023 |
| R15 | Channel guiding of trains | 2.5 J, N ≈ 10, 110 mm HOFI, W_M ≈ 40 µm | coupling 64 ± 4 %, L_att = 124 ± 20 mm; wake 3 (0.8 J) to 10 (2.5 J) GV/m (fluid) | Ross 2024 |
| R16 | Energy recovery | 2 pulses, out of phase | wake 0.60 % → 0.35 % (−40 % amplitude) | Cowley 2017 |
| R17 | Proton dephasing sanity check [inference] | n = 2.5e17, 1.03 µm, w0 = 30 µm (β_φ = 0.99982) | L_d(λ_p/4) = 0.13 mm at 1 GeV, 0.58 mm at 3 GeV, 1.85 mm at 6 GeV; γ_φ = 7.4 requires n ≈ 1.9e19 cm⁻³ (T_p ≈ 25 fs) | this note |

---

## Source URLs
- Ross et al. 2024: https://arxiv.org/abs/2310.05097 ; https://doi.org/10.1103/PhysRevResearch.6.L022001 ; ORA https://ora.ox.ac.uk/objects/uuid:f11d11b5-e798-4cca-9945-b94f82add7ee
- Hooker et al. 2014: https://arxiv.org/abs/1401.7874 ; https://iopscience.iop.org/article/10.1088/0953-4075/47/23/234003
- Jakobsson et al. 2021: https://arxiv.org/abs/2110.00417 ; https://doi.org/10.1103/PhysRevLett.127.184801
- van de Wetering et al. 2024 (accelerator): https://arxiv.org/abs/2311.00471 ; https://doi.org/10.1103/PhysRevE.109.025206 ; decks https://doi.org/10.5281/zenodo.10061009
- van de Wetering et al. 2023 (modulator): https://arxiv.org/abs/2303.14032 ; decks https://doi.org/10.5281/zenodo.7734261
- Jonnerby et al. 2023: https://arxiv.org/abs/2306.06438 ; https://doi.org/10.1103/PhysRevE.108.055211
- Cowley et al. 2017: https://arxiv.org/abs/1708.04206 ; https://doi.org/10.1103/PhysRevLett.119.044802
- Walter et al. 2025: https://arxiv.org/abs/2512.14476
- Farmer & Zevi Della Porta 2024/25: https://arxiv.org/abs/2404.14175
- Maurya et al. 2026: https://arxiv.org/abs/2603.21798
- Benedetti et al. 2014: https://www.osti.gov/servlets/purl/1163658
- Sadler et al. 2020: https://arxiv.org/abs/2001.09108
- Vantaggiato et al. 2018: https://arxiv.org/abs/1802.00826
- Herkommer et al. 2020: https://opg.optica.org/oe/fulltext.cfm?uri=oe-28-20-30164&id=439952
- kBELLA fibre programme: https://atap.lbl.gov/research/berkeley-lab-laser-accelerator-bella-center/fiber-lasers-toward-kbella/
