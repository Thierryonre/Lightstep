# Simulation Log

Every simulation attempt is recorded here — including failures, bugs and dead ends — with
parameters, results and conclusions. IDs are sequential (S###). Units: unless stated, lengths in
c/ω_p, times in 1/ω_p, fields in E₀ = m_e c ω_p/e, densities in the reference density n_ref
(see `sims/codes/*.py` docstrings). "a0" is the peak normalised vector potential (linear
polarisation, ⟨a²⟩ = a0²/2).

**Status tags:** ✅ validated / result accepted · ⚠️ result with caveats · ❌ failed / bug found ·
🔁 superseded.

Codes (all in `sims/codes/`):

| Code | What it is | Validated by |
|---|---|---|
| `fluid1d.py` | 1D nonlinear cold-fluid quasi-static wake, arbitrary phase velocity β_p (incl. sub-luminal), beam-loading term, energy densities | S001 |
| `pic1d_env.py` | 1D relativistic electrostatic PIC, prescribed ponderomotive envelope driver(s) moving on any programmed trajectory, density profiles, mobile ions, loaded proton beams, exact energy budget | S003–S008 |
| `pic1d_em.py` | 1D relativistic full-EM PIC (laser resolved, dt = dx, implicit plasma current), moving window at c; includes laser depletion/red-shift | S006, S008 |
| `tests/sheet_model.py` | gridless Dawson sheet model (exact 1D electrostatics), used as an independent check | S007 |

---

## Phase 0 — Code validation

### S001 ✅ fluid1d vs analytic linear theory — 2026-10-27
- **Script:** `sims/tests/test_fluid1d.py`
- **Setup:** Gaussian ⟨a²⟩ = A exp(−ξ²/2σ²), A = 10⁻³. Luminal (β_p = 1): σ = 0.5, 1, 2. Sub-luminal: β_p = 0.3, 0.6, 0.9 with σ = β_p/2.
- **Theory:** luminal E_max = (A/2) σ √(2π) e^(−σ²/2); sub-luminal linear limit φ'' = (a²/2 − φ)/β_p² ⇒ wavelength 2πβ_p and E amplitude |∫a² e^{iξ/β_p} dξ| / (2β_p²).
- **Result:** luminal ratio num/theory = 0.99975, 0.99961, 1.00001. Sub-luminal ratio = 1.0015, 1.0001, 0.9998; wavelength exact to 4 digits.
- **Failure noted:** the first version of the test used a wrong reference formula (extra 1/β_p) and showed ratio = β_p exactly; the reference was corrected, the solver was not changed.
- **Conclusion:** fluid solver correct in the linear regime for luminal and sub-luminal wakes.

### S002 ✅ fluid1d nonlinear wake amplitudes and depletion length — 2026-10-27
- **Setup:** luminal, Gaussian σ = 1 (intensity FWHM 2.355 c/ω_p), a0 = 0.5, 1, 2, 3, k0/kp = 20.
- **Result:** E_max = 0.091, 0.319, 0.897, 1.439 E₀ (no breaking). Wake energy density u = 0.0041, 0.0505, 0.405, 1.057 n m_e c²; implied pump-depletion length U_L/u = 30600, 9920, 4950, 4270 c/ω_p.
- **Conclusion:** provides the nonlinear reference for S003–S008.

### S003 ✅ pic1d_env vs fluid1d — 2026-10-27
- **Script:** `sims/tests/test_pic1d_vs_fluid.py` (dx = 0.02, ppc = 16, dt = 0.5 dx·max(β,0.2), window 40, propagation 60)
- **Result (rel. RMS difference of E_z behind driver):** a0 = 0.5 luminal 0.66 %; a0 = 1 luminal 1.5 % (E_max 0.327 vs 0.319); a0 = 0.3, β = 0.5: 2.1 %; a0 = 0.5, β = 0.9: 0.87 %. a0 = 2 luminal: amplitude identical (0.8975 vs 0.8969) but RMS diff 20 % → investigated in S005–S007.
- **Conclusion:** envelope PIC agrees with fluid theory for linear/mildly nonlinear and sub-luminal wakes.

### S004 ❌→✅ Energy diagnostic bug — 2026-10-27
- **Problem:** the laser→plasma work was first accumulated as Σ F_pond·v_particle, giving an 11 % imbalance (work 16.99 vs field + kinetic 18.88).
- **Fix:** in the ponderomotive model the energy given by the envelope is Σ (∂⟨a²⟩/∂t)|ₓ /(2γ) dt (for a rigid driver = −v_d·F_pond); kinetic energy must include the quiver term √(1+u²+a²).
- **Check:** with all plasma kept inside the window (Lx = 120): laser work 22.074 vs field + kinetic 22.071 (0.01 %).
- **Conclusion:** exact energy accounting in `pic1d_env.py` — used for every efficiency number below.

### S005 ⚠️ a0 = 2 wake decays behind the driver (investigation) — 2026-10-27
- **Observation:** with a sharp vacuum–plasma edge, the PIC wake equals the fluid wake for ~1.5 periods, then decays (0.74 → 0.48 → 0.43 → 0.36 E₀ over 40 c/ω_p) and electrons reach u ≈ 30.
- **Convergence tests** (`tests/debug_numerics.py`): identical results for dx = 0.02/0.01/0.005, ppc = 16/32/64, dt = 0.5/0.1 dx, and with/without a small initial temperature → not numerical noise.
- **H = γ − u − φ** (conserved for a rigid luminal driver in steady state) is violated by a subset of electrons (`tests/debug_H.py`).
- Figure: `results/figures/validation/S005_sharp_edge_wake_decay.png`.

### S006 ⚠️ Independent full-EM PIC shows the same decay — 2026-10-27
- **Script:** `sims/tests/test_em_vs_env.py` (k0/kp = 10, dx = λ/32, ppc = 8; envelope PIC with β = v_g)
- **Result:** EM amplitudes 0.86/0.66/0.36/0.29 vs envelope 0.73/0.47/0.39/0.29 vs fluid 0.90 in successive 10 c/ω_p windows → decay is not an artefact of the envelope model.
- Figure: `results/figures/validation/S006_em_vs_env_sharp_edge.png`.

### S007 ✅ Gridless sheet model confirms; root cause = edge injection — 2026-10-27
- **Script:** `sims/tests/sheet_model.py` (exact 1D electrostatics by sorting; 100 and 400 sheets per c/ω_p)
- **Result:** same decay (0.75/0.48/0.42/0.31), converged in sheet number → physical behaviour of the model.
- **Root cause test** (`tests/test_ramp.py`): plasma entrance ramp (sin²) of length L_r:
  - L_r = 0: 0.739/0.481/0.433/0.357, max u = 44
  - L_r = 10: 0.897/0.851/0.625/0.467
  - L_r = 30: 0.897 in all windows (a few injected electrons further back)
  - L_r = 60: 0.897 in all windows, max u = 1.0 (no trapped electrons) — fluid 0.901
- **Conclusion:** electrons injected at the sharp vacuum–plasma boundary are accelerated and beam-load (damp) the wake. Not a bug. **Design rule adopted:** entrance ramps ≥ 30–60 c/ω_p in all subsequent runs unless injection is wanted.

### S008 ✅ Full-EM PIC vs envelope PIC vs fluid with smooth ramp; depletion — 2026-10-27
- **Script:** `sims/tests/test_em_vs_env_ramp.py` (60 c/ω_p sin² ramp + 60 c/ω_p plateau)
- **a0 = 2, k0/kp = 10:** amplitudes EM 1.13/1.09/0.91/1.00, envelope 0.90/0.90/0.91/0.91, fluid 0.90. Laser energy lost: EM 43.5, envelope work 37.5, fluid estimate 36.5.
- **a0 = 1, k0/kp = 20:** EM 0.346, envelope 0.320, fluid 0.320 (all windows). Energy lost: EM 4.1 (diagnostic accuracy ~±1), envelope 5.0, fluid 4.6.
- **Conclusion:** envelope PIC ≡ fluid in the regime of validity. The full-EM laser self-steepens/compresses in 1D and drives an 8–25 % stronger wake while losing ~16 % more energy. The prescribed-driver model therefore slightly **underestimates** wake amplitude (conservative) and gets energy transfer within ~20 %.
- Figures: `results/figures/validation/S008_em_vs_env_ramp_a1.png`, `..._a2.png`.

---

## Baseline — conventional LWFA

### S009 ✅ B2: conventional LWFA acting on injected protons — 2026-10-27
- **Script:** `sims/baseline/b2_conventional_protons.py` · data `results/data/B2_conventional_protons.json`
- **Model:** 1D fluid wake + test-proton tracking (`track1d.py`). Driver Gaussian, a0 = 2, intensity FWHM 2.355 c/ω_p (resonant), moving at the laser group velocity (γ_p = k0/kp). 400 test protons spread over one full wake period; maximum gain of the best-phase proton recorded until it slips out.
- **Scan:** γ_p = 5, 7.4, 10, 20, 40 (n/n_c = 1/γ_p²) × T_inj = 10, 100, 1000, 3000, 6000 MeV.
- **Result (best-phase gain):**
  - T_inj = 10 MeV: 0.17–0.18 MeV for every γ_p
  - T_inj = 100 MeV: 0.75–0.78 MeV
  - T_inj = 1 GeV: 7.1–8.4 MeV
  - T_inj = 3 GeV: 35–127 MeV (largest at γ_p = 5)
  - T_inj = 6 GeV: 89 MeV (γ_p = 5), **928 MeV (γ_p = 7.4 ≈ γ_proton)**, 259 MeV (γ_p = 10), 114–128 MeV (γ_p = 20–40)
- **Wake:** E_max = 0.90 E₀, potential depth 1.0 MeV (electron-scale), i.e. Δφ_p = eΔΦ/m_pc² ≈ 1.1×10⁻³.
- **Check vs Hamiltonian theory:** bucket height Δγ ≈ 2γ_pβ_p√(2γ_pΔφ_p) → 1.73 GeV at γ_p = 7.4; a proton injected at the bucket centre gains ≈ half of it (0.93 GeV simulated vs 0.87 GeV estimate). Protons outside the bucket (|γ − γ_p| ≳ Δγ/2) are not trapped.
- **Conclusion:** a conventional LWFA (wake phase velocity = laser group velocity) cannot accelerate protons from any practical injector energy: gains are 10⁻³–10⁻² of the injection energy unless protons are already within the bucket around γ ≈ γ_p (≥ ~5 GeV for n ≈ n_c/55). **Conventional-LWFA baseline for protons: ΔT ≈ 0.2 MeV (10 MeV injection), 0.8 MeV (100 MeV), 8 MeV (1 GeV) per stage.**

---

## Phase 1 — primary concepts

### S010 ✅ P1a: maximum wake behind a velocity-matched driver — 2026-10-27
- **Script:** `sims/phase1/p1a_matched_wake_scan.py` · data `results/data/P1a_matched_wake_scan.json`
- **Model:** 1D cold-fluid wake with β_p equal to the proton velocity; scan a0 (0.1–6) and drive duration at a point τ (1.5–4 /ω_p; spatial FWHM β_pτ); keep the wake unbroken and |E| ≤ 0.8 E_wb, E_wb = √(2(γ_p − 1)).
- **Result (best proton-accelerating field E⁺, wake energy per unit length u):**

  | T (MeV) | β_p | E_wb (E₀) | best E⁺ (E₀) | a0 | τ | u (n m_ec²) |
  |---|---|---|---|---|---|---|
  | 10 | 0.145 | 0.146 | 0.101 | 0.2 | 1.5 | 0.0052 |
  | 30 | 0.247 | 0.253 | 0.158 | 0.4 | 4.0 | 0.0124 |
  | 100 | 0.428 | 0.462 | 0.347 | 0.7 | 3.0 | 0.060 |
  | 300 | 0.653 | 0.800 | 0.631 | 1.2 | 2.355 | 0.193 |
  | 1000 | 0.875 | 1.460 | 1.157 | 2.2 | 2.0 | 0.679 |
  | 3000 | 0.971 | 2.529 | 2.021 | 4.1 | 2.355 | 2.150 |
  | 6000 | 0.991 | 3.576 | 2.823 | 5.9 | 2.0 | 3.846 |
- **Conclusion:** a slow wake is limited by cold wave breaking, E⁺ ≲ 0.7 E_wb ≈ 0.7β_p E₀ for slow protons; slow drivers need only modest a0 because they are spatially short. Wake energy per unit length rises ~700× from 10 MeV to 6 GeV — so for a fixed loaded charge a constant (not growing) gradient is the efficient choice.

### S011 ✅ R1: reproduction of Ross et al. PRR 6, L022001 (2024) resonance — 2026-10-27
- **Script:** `sims/phase1/r1_ross2024_resonance.py` · data `results/data/R1_ross2024.json` · figure `results/figures/R1_ross2024_resonance.png`
- **Setup:** 10 pulses, 31 fs FWHM, 170 fs spacing, 800 nm, w₀ = 45.5 µm; a0 per pulse from train energy (0.01 J → a0 0.021; 0.8 J → 0.187; 2.5 J → 0.330); 1D nonlinear fluid, density scan 1.5–8×10¹⁷ cm⁻³.
- **Result:** resonance at **4.3×10¹⁷ cm⁻³** (measured 4.3±0.3×10¹⁷ ✔). Amplitude-FWHM δn/n = **0.21** (paper's theory 8/(3N) = 0.27; measured 0.37). Peak wake 5.9 GV/m (0.8 J) and 18.6 GV/m (2.5 J) vs paper's 2D fluid 3 and 10 GV/m (1D/2D ≈ 1.9, the expected transverse-geometry factor). No resonance shift up to a0 = 0.33.
- **Conclusion:** resonance position reproduced exactly; width within 25 % of their theory; measured broadening (×1.8) plausibly from pulse-spacing non-uniformity (U ≈ 0.9), jitter and the red-shift diagnostic — not reproduced in 1D.

### S012 ✅ P1c-v1: kinetic PIC vs fluid tracker, beam-loaded matched segment — 2026-10-27
- **Script:** `sims/phase1/p1c_pic_check_matched.py` (v1, fixed-ξ lock) · log `results/data/P1c_run_T1000.log`
- **Setup:** T_inj = 1 GeV, τ = 2.355, a0 = 1.709 (E⁺ = 0.82 E₀), beam load 0.4×E⁺ (areal weight 0.33), 2000 macro-protons, σ_ξ = 0.04λ, mobile hydrogen ions, 60 c/ω_p entrance ramp, 2000 c/ω_p of acceleration; PIC dx = 0.02, ppc = 16.
- **Result:** gain PIC 159.3 MeV vs tracker 153.7 MeV; energy spread 15.27 vs 15.26 MeV; wake→beam efficiency 15.6 % vs 14.6 %; laser work per length 0.326 vs 0.337; 100 % beam survival; negligible background-electron trapping.
- **Conclusion:** the quasi-static tracker reproduces the kinetic PIC (incl. ion motion and beam loading) to ≈ 4 % → used for long accelerations. (Low gain here was due to the v1 lock bug, S013; the code-to-code comparison is unaffected because both used the same lock.)

### S013 ❌→✅ P1b-v1 phase-lock bug — 2026-10-27
- **Problem:** v1 locked the beam centroid at a fixed distance ξ behind the driver. The wake wavelength 2πβ_p grows as protons speed up, so the beam drifted towards a field zero: field at the beam fell 0.60 → 0.17 E₀ over Δβ = 0.02 (`sims/tests/debug_lock.py`); the full 1→6 GeV run never finished (stalled), and was stopped.
- **Fix (v2):** lock to a fixed phase of the *first* proton-accelerating lobe (front, phase-stable side, E = 0.8 E_peak), re-located from the current unloaded wake whenever β changes; stall detector added.
- **Check:** 1.0 → 1.5 GeV: 2223 c/ω_p, mean gradient 0.44 E₀, **wake→beam efficiency 40.7 %**, energy spread 0.5 % rms, 99.7 % captured (runtime 6 s).

### S014 ✅ P1c-v2: kinetic PIC validation of the corrected (phase-locked) design — 2026-10-27
- **Script:** `sims/phase1/p1c_pic_check_matched.py --Tinj 300` · log `results/data/P1c_run_T300_lockv2.log`
- **Setup:** T_inj = 300 MeV (β = 0.65), a0 = 0.971, E⁺ = 0.448 E₀, load 0.4, phase lock v2 (first bucket), 2000 c/ω_p, mobile H ions, PIC dx = 0.02, ppc = 16.
- **Result:** gain PIC 214.3 MeV vs tracker 213.3 MeV; wake→beam efficiency 44.2 % vs 45.7 %; laser work/length 0.0849 vs 0.0818; energy spread PIC 1.6 MeV vs tracker 4.5 MeV; beam survival 99.95 %; no background-electron trapping.
- **Conclusion:** velocity-matched, beam-loaded proton acceleration is reproduced kinetically to ≈ 3 %; the tracker is conservative on energy spread.

### S015 ✅ P1b: velocity-matched acceleration to 6 GeV, scan — 2026-10-27
- **Script:** `sims/phase1/p1b_scan.py` (v2 lock, K = 0.05, lock at 0.8 E_peak, τ = 2.355, f = 0.7, 1000 macro-protons, σ_ξ = 0.03λ, ΔT/T = 0.5 %) · data `results/data/P1b_scan.json`, trajectories `results/data/P1b_traj_*.npy`
- **'const' field program (E⁺ = 0.56 E_wb(T_inj) held constant):**

  | T_inj | load | length (c/ω_p) | mean gradient (E₀) | wake→beam η | final spread | captured |
  |---|---|---|---|---|---|---|
  | 1000 MeV | 0.3 | 19 263 | 0.508 | 35.3 % | 0.2 % | 99.7 % |
  | 1000 MeV | 0.5 | 22 916 | 0.427 | 49.5 % | 0.2 % | 99.7 % |
  | 300 MeV | 0.3 | 39 565 | 0.282 | 37.4 % | 0.1 % | 99.9 % |
  | 300 MeV | 0.5 | 47 188 | 0.236 | 52.3 % | <0.1 % | 99.9 % |
  | 100 MeV | 0.3 | 70 533 | 0.164 | 38.0 % | <0.1 % | 99.9 % |
  | 100 MeV | 0.5 | 84 167 | 0.137 | 53.1 % | <0.1 % | 100 % |
  | 30 MeV | 0.3 | 129 648 | 0.090 | 38.2 % | <0.1 % | 100 % |
- **'track' program (E⁺ = 0.56 E_wb(β), growing with energy):** ❌ every case stalled at ≈ 2.0–2.2 GeV with η = 5–17 % (wake breaking flagged in the 1 GeV and 300 MeV cases): at fixed beam charge a growing field is weakly loaded and eventually breaks.
- **Conclusion:** in 1D, a phase-locked velocity-matched wake accelerates protons from 30 MeV–1 GeV to 6 GeV with 35–53 % wake→beam efficiency and sub-% spread. Length ∝ 1/E_wb(T_inj): starting slower costs length, not efficiency. Physical length = L × c/ω_p (e.g. 100 MeV start, load 0.3: 37 cm at 10¹⁸ cm⁻³, 12 cm at 10¹⁹ cm⁻³).
- **Acceleration multiplier vs conventional LWFA (S009, same injection energy):** 100 MeV start: 5900 MeV vs 0.8 MeV per stage (≈ 7 000×); 1 GeV start: 5000 MeV vs 8 MeV (≈ 600×).

### S016 ⚠️ P2b: differentiable joint optimisation (driver shape + beam profile) — 2026-10-27
- **Script:** `sims/phase2/p2b_joint_optimisation.py`, model `sims/codes/jax_wake.py` (JAX solver identical to fluid1d to 10⁻¹¹; laser-work formula W' = −∫(n_e/2γ)∂_ξ⟨a²⟩ dξ checked against the wake energy density to < 0.6 %). L-BFGS-B, 64 driver + 48 beam amplitudes (112 parameters), constraints: field spread over the bunch ≤ 5 %, mean field ≥ hand design, unbroken wake, |E| ≤ 0.8 E_wb, a0 cap.
- **Failures on the way:** (i) v1 basis too coarse for the bunch and a sqrt-clamp exploit gave unphysical "fields" ≈ 18 E₀; (ii) the first train run started with zero beam (bunch not shifted behind the last pulse); (iii) barrier weights too weak let broken-wake solutions win (η = 550, flagged infeasible) → weights raised ×100, finer bucket-local beam basis, dimensionless bounded parameters.
- **Results — single-pulse window, a0 ≤ 1.3 × hand design** (`results/data/P2b_joint_opt_free.json`, figure `results/figures/P2b_joint_opt_free.png`):
  - 100 MeV: η 0.523 → 0.531 (field spread 0.21 → 0.05); marginally below the gradient constraint
  - 1 GeV: η 0.503 → **0.710 (×1.41)**, same mean field 0.41 E₀, field spread 0.39 → 0.05
  - 6 GeV: η 0.245 → **0.601 (×2.46)**, field 1.11 → 1.13 E₀, spread 0.086 → 0.05
- **Results — "lower-power lasers": peak a0 ≤ 0.5 × hand design, 5-period window** (`..._lowpower_train.json`): a greedy hand-designed nonlinear-resonant train of 5 pulses (each ¼ of the single-pulse peak power) gives η = 0.542 (100 MeV, spacings 0.98/0.98/0.81/1.49 λ_lin) and η = 0.548 with 1.6× higher loaded field (1 GeV, spacings 1.00/1.04/1.11/1.34 λ_lin) — equal or better than the single pulse. At 6 GeV (a0 ≈ 3.3 per pulse) stacking failed (η = 0.033): nonlinear detuning. Local optimisation from the train starts did not improve on them under the 5 % flatness constraint (multimodal landscape).
- **Conclusion:** joint optimisation of pulse shape + beam loading raises wake→beam efficiency 1.4–2.5× at 1–6 GeV while flattening the field; resonant trains of quarter-power pulses are as efficient as one pulse in the quasi-linear regime (a0 ≲ 1–2 per pulse).

### S017 ✅/⚠️ R2: reproduction of Hooker et al. J. Phys. B 47, 234003 (2014) — 2026-10-27
- **Script:** `sims/phase1/r2_hooker2014_multipulse.py` · data `results/data/R2_hooker2014.json` · figure `results/figures/R2_hooker2014_multipulse.png`
- **Setup:** 120 pulses × a0 = 0.052, 100 fs FWHM, λ = 1 µm, spacing = plasma period, n = 1.75×10¹⁷ cm⁻³ (E₀ = 40.2 GV/m), 1D envelope PIC (dx = 0.05, ppc = 8), immobile ions and mobile protons. (A first run was stopped after 3 h — CPU shared with other jobs and an inefficient driver evaluation; driver evaluation was then restricted to each pulse's support, ~10× faster.)
- **Result:** linear growth 1.36 / 2.76 / 5.01 GV/m after 30 / 60 / 120 pulses (immobile) vs paper **4.7 GV/m** ✔ (7 %). Mobile H: 4.28 GV/m vs paper ≈ 2.5 GV/m.
- **Conclusion:** the multi-pulse resonant build-up is reproduced; the ion-motion saturation reported in the paper is only partly captured in 1D (−15 % vs −47 %), i.e. it is mostly transverse ion motion (multi-D) — a known limitation of our 1D models for long trains in hydrogen.

### S018 ✅ P1d: proton self-injection from rest by a slow, accelerating driver (FF from rest; + NP layer) — 2026-10-27
- **Script:** `sims/phase1/p1d_scan.py` (1D envelope PIC, hydrogen with mobile protons, dx = 0.02, ppc = 8, dt = 0.01) · data `results/data/P1d_scan.json`
- **Setup:** Gaussian driver a0 = 3, FWHM ℓ = 1 c/ω_p, ramped on at rest over 20/ω_p, then constant proper acceleration α₀ (1D analogue of the transverse-flying-focus scheme of Gong et al. 2024). Λ = eE_max/m_p with E_max = 1.73 E₀ (adiabatic front-slope estimate) → Λ = 9.44×10⁻⁴ c ω_p. Target 300 MeV.
- **Result:**

  | case | trapped areal charge (n c/ω_p) | final T (MeV) | laser→trapped-proton efficiency |
  |---|---|---|---|
  | α₀ = 0.5 Λ | 0.70 | 317 ± 5 | **28.6 %** |
  | α₀ = 0.8 Λ | 0.0025 | 278 | 0.16 % |
  | α₀ = 1.2 Λ | 0 | — | 0 |
  | α₀ = 0.5 Λ + dense H layer (10× n, 0.5 c/ω_p thick, "nanoparticle-like") | **4.85** | 321 ± 11 | **74 %** |
- **Conclusion:** a slow accelerating driver can pick up background protons from rest without an injector; the trapping threshold lies between 0.5 Λ and 0.8 Λ (below the ideal α₀ < Λ because the captured charge loads the field). A local hydrogen-rich layer (the 1D stand-in for a nanoparticle/cluster) raises the captured charge 7× and the 1D efficiency to 74 %. **Caveats:** 1D (the layer is an infinite sheet, no transverse loss), prescribed non-depleting driver; the optical embodiment of a slow, steep driver (transverse flying focus / transverse pumping) is very inefficient in 3D per the literature (Gong 2024: 0.13 %; Nutting 2026: ~10⁻⁵).

---

## Phase 2 — additional optimisations / alternative embodiments

### S019 ✅ P2a-explore: wake phase velocity and depletion in dense plasma (full-EM 1D PIC) — 2026-10-27
- **Script:** `sims/phase2/p2a_explore_dense_em.py` · data `results/data/P2a_explore_dense_em.json`
- **Idea tested:** make the laser's own group velocity match the protons (n ≈ n_c/γ_p²) so that a guided pulse is reused until depleted — no flying-focus optics.
- **Result:** the wake moves markedly slower than the linear group velocity (pulse-front etching and red-shift):

  | n/n_c | a0 | linear γ_g | measured wake γ_φ | E_max (E₀) | depletion length (c/ω_p) | energy lost in 400 c/ω_p |
  |---|---|---|---|---|---|---|
  | 1/16 | 1 | 4.0 | 2.43 | 0.17 | 1375 | 47 % |
  | 1/16 | 2 | 4.0 | 2.15 | 0.29 | 973 | 86 % |
  | 1/55 | 1 | 7.4 | 5.76 | 0.39 | 897 | 38 % |
  | 1/55 | 2 | 7.4 | 2.85 | 1.15 | 447 | 76 % |
- **Conclusion:** in dense plasma the phase velocity can be lowered by a0 at fixed density (n_c/55 with a0 = 2 matches ~1.7 GeV protons on average). Important constraint (analytic): with ω/ω_p ≈ γ_p a resonant pulse is only ≈ γ_p/2 optical cycles long → few-cycle drivers are required.

### S020 ❌ P2a: single density-matched, depletion-limited stage with protons (full-EM 1D PIC) — 2026-10-27
- **Script:** `sims/phase2/p2a_dense_stage.py --k0 7.4 --a0 2 --Tc 1700` · data `results/data/P2a_stage_k7.4_a2.0.json`
- **Setup:** k0/kp = 7.4, a0 = 2, 2.8-cycle pulse; 1140 test protons over 1.3 wake periods × T = 1.0–2.55 GeV; then loaded bunches σ_b = 0.05/0.15/0.3.
- **Result:** 64 % of the laser energy is lost in the first 260 c/ω_p and the wake keeps slowing; best-phase proton gain only **84 MeV** (at the 2.55 GeV edge of the scanned grid). Loaded runs invalid: protons slipped out of the c-moving window (survival 0) — reported efficiencies (≤ 1.5 %) are not meaningful.
- **Conclusion:** a single guided pulse at matched density gives an unsteady wake (velocity evolves with depletion) and transfers little energy to protons. Not pursued further (the planned 6–12 h FBPIC check was not run). Better route: keep the light guided but control velocity optically (next study).
- **Also tested:** FBPIC 0.27.1 (quasi-3D) installed in WSL; timing for this case 1.9 s/step → 12.6 h per mm at λ/24 (CPU shared with other jobs).

### S021 ✅ B3: conventional LWFA with a loaded proton bunch — efficiency baseline — 2026-10-27
- **Script:** `sims/baseline/b3_conventional_protons_loaded.py` · data `results/data/B3_conventional_protons_loaded.json`
- **Setup:** fluid tracker; group-velocity wake (a0 = 2, resonant Gaussian), γ_p = 7.4 / 20 / 41.7; bunch 0.4 E_peak, 9 injection phases; efficiency evaluated at the point of maximum beam energy (stage ended exactly at dephasing — best case).
- **Result:** wake→proton efficiency 0.18 (100 MeV), 0.36 (1 GeV), 0.40 (3 GeV), essentially independent of γ_p; but the mean gain is only 0.49–0.50 MeV (100 MeV), 4.6–5.0 MeV (1 GeV), 22–33 MeV (3 GeV) because the protons dephase within a few c/ω_p.
- **Derived (sim + energy accounting):** the guided driver's depletion length at 10¹⁸ cm⁻³/0.8 µm is ≈ 2.15×10⁴ c/ω_p (S002 scaled ∝ (k0/kp)²) while a stage lasts only ≈ 5.5 c/ω_p (100 MeV) or ≈ 25 c/ω_p (1 GeV) → laser→wake coupling 2.6×10⁻⁴ / 1.2×10⁻³ → **laser→proton efficiency per stage ≈ 4.5×10⁻⁵ (100 MeV) / 4.3×10⁻⁴ (1 GeV)**, and ~12 000 / ~1 100 separately-driven stages to reach 6 GeV.
- **Conclusion:** the conventional baseline loses not on beam loading but on laser→wake coupling: protons use only a tiny fraction of the driver's depletion length. This defines the efficiency baseline for the multipliers.

### S022 ✅ P1e: optics of the guided resonant flying-focus train (FF + resonant excitation) — 2026-10-27
- **Scripts:** `sims/phase1/p1e_waveguide_train_optics.py`, `p1e_feasibility_boundary.py` · data `results/data/P1e_*.json` · figure `results/figures/P1e_waveguide_train_optics.png`
- **Concept:** N laser frequencies ≈ ω_p apart, each launched into a different radial mode LG_{p=qP,0} of a matched parabolic channel. With all components placed exactly on the line ω = v_a k + ω_c (exact modal dispersion, solved numerically) the on-axis intensity is a *rigid* train of peaks moving at v_a < c, spaced by one plasma period (resonant). First attempt with the first-order rule (uniform ω_p spacing) failed at 1 GeV: higher modes cut off and the comb decohered in ~0.1 mm (logged) → replaced by the exact rigid design with W chosen so the mean spacing is ω_p.
- **Result (λ = 1 µm):**
  - 3 GeV protons (β = 0.971): N = 3–5, P = 1–2, n = 0.35–1.2×10¹⁸ cm⁻³, W = 10.7–20.5 µm, k_pW ≈ 2.2–2.3, Δn/n₀ ≈ 0.76–0.82, bandwidth 3.5–13 %, spacings 0.89–1.13 ω_p; peaks N× the mean intensity, FWHM 0.18–0.31 T_p, radius 0.31–0.53 W.
  - 6 GeV protons (β = 0.9908): n = 1.0–1.4×10¹⁷ cm⁻³, W = 32–49 µm, bandwidth 1.9–4.5 %, spacings 0.97–1.04 ω_p.
  - Feasibility boundary (N = 3): k_pW ≥ 2.2 down to **1.0 GeV** (P = 3, n = 3.1×10¹⁸, W = 6.8 µm, Δn/n₀ = 0.78); k_pW ≥ 1.8 down to 0.75 GeV; k_pW ≥ 1.4 down to 0.5 GeV (Δn/n₀ ≈ 1.9).
- **Conclusion:** a guided, arbitrary-velocity, resonant drive exists for protons above ≈ 0.75–1 GeV using only 3–5 narrow-band, long (≥ 100 fs) pulses — compatible with efficient fibre/thin-disk lasers (no few-cycle pulses). Below ~0.75 GeV only side-pumped geometries remain.

### S023 ❌ P1f-v1: multi-bunch train, overloaded — 2026-10-27
- **Script:** `sims/phase1/p1f_waveguide_train_multibunch.py` (v1) · log `results/data/P1f_a0.35.log`
- **Setup:** 3 GeV, k0/kp = 28.5, spacings 0.963/1.037 (P = 1 design), a_avg = 0.35, 12-period envelope, 18 bunches **each** loaded with 0.4 E_peak.
- **Result:** protons *lost* energy (3000 → 2835 MeV): the cumulative loading of 18 bunches reversed the wake; additionally ±3.7 % spacing non-uniformity accumulates ~3 rad of drive/wake phase error over 12 periods. Laser used: 5.6 % in 3000 c/ω_p (depletion length ≈ 6×10⁴ c/ω_p).
- **Fix:** total (not per-bunch) loading = 0.4 E_peak; use the more uniform P = 2 design.

### S024 ✅ P1f-v2: guided resonant train driving velocity-locked protons (1D PIC) — 2026-10-27
- **Setup:** 3 GeV design P = 2, N = 3 (spacings 0.981/1.019 ω_p), k0/kp = 56.4 (n = 3.5×10¹⁷ at 1 µm), a_avg = 0.35, 12-period Gaussian envelope, mobile ions, energy-consistent depletion, velocity lock (K = 0.02), 3000 c/ω_p.
- **Single bunch behind the train** (`results/data/P1f_single_v2.json`): 3000 → **3215 MeV** (0.14 E₀), **wake→beam 58.5 %**, laser energy used 0.65 % (depletion length ≈ 5.4×10⁵ c/ω_p at this dilute design point).
- **18 bunches in the train's buckets (total load 0.4 E_peak)** (`P1f_multi_v2.json`): 3000 → **3252 MeV** (0.16 E₀), **wake→beam 49.9 %**, laser used 0.87 %.
- **Energy-accounting scaling (derived):** in the linear regime, the fraction of laser energy absorbed per unit proton-energy gain ∝ ΔT/(k0/kp)², independent of drive amplitude → denser plasma (enabled by larger k_pW in the rigid-comb design) raises laser→wake coupling towards depletion. Used in the design calculator.

### S025 ✅ P2c: programming the train velocity with a channel-width taper (Phase 2.1) — 2026-10-27
- **Script:** `sims/phase2/p2c_channel_taper_velocity.py` · data `results/data/P2c_channel_taper.json`
- **Setup:** fixed laser frequencies of the 1 GeV rigid design (λ = 1.000/1.052/1.118 µm, modes p = 0/3/6); vary channel spot W and on-axis density n₀; compute peak velocity, comb rigidity (coherence length) and resonance (mean spacing/ω_p).
- **Result:** at constant n₀, W/W₀ = 1 → 1.25 → 1.5 → 2 → 3 gives β = 0.875 → 0.916 → 0.940 → 0.965 → 0.983 (matched proton energy 1.0 → 1.4 → 1.8 → 2.6 → 4.2 GeV) with coherence length ≥ 120 mm and spacing/ω_p = 1.000. Changing n₀ instead detunes the resonance (spacing/ω_p = 1.12 at 0.8 n₀, 1.29 at 0.6 n₀).
- **Conclusion:** the train velocity can be programmed along the accelerator purely by tapering the channel *width* (engineered optical guiding) with fixed lasers. Caveat: at fixed train power the on-axis intensity falls ∝ 1/W² → use 2–3 stages with modest tapers.

### S026 ⚠️ R3 (Wake-T) attempt — too slow on this machine — 2026-10-27
- **Script:** `sims/phase2/r3_lahaye_gradient_waket.py` (Wake-T 0.9.1, quasistatic_2d, laser evolution, matched channel; Lahaye FBPIC parameters).
- **Result:** fixed two set-up errors (ParticleBunch takes weights, not charge; zero density at z = 0 causes a division by zero in Wake-T's bunch deposition → ramp from 2 % n₀). Still > 550 s for 0.5 mm at n_xi = 600 and > 580 s for 2 mm at n_xi = 300 on the shared CPU (≈ 2–6 h per 24 mm case) → replaced by the kinetic 1D mechanism study (S027).

### S028 ✅ R4: reproduction of Palastro et al. PRL 124, 134802 (2020) — dephasingless LWFA (flying focus) — 2026-10-27
- **Script:** `sims/phase1/r4_palastro2020_dlwfa.py` · data `results/data/R4_palastro2020.json` (tracker generalised to electrons: `track1d.Tracker(species='electron')`)
- **Setup:** λ = 1 µm, 30 fs, a0 = 0.5, n = 3.5×10¹⁸ cm⁻³ (k0/kp = 17.8), 8 cm; conventional driver at the linear group velocity vs ideal flying focus at v = c; 800 test electrons over two periods, 10 MeV injection; 1D (diffraction-free, as provided by the flying focus).
- **Result:** conventional maximum **75 MeV** (paper 75 MeV); dephasingless **1216 MeV** after 8 cm (paper 1.3 GeV, −6.5 %).
- **Conclusion:** the flying-focus acceleration multiplier (×16 for electrons in this case) is reproduced quantitatively by our 1D models.

### S027 ✅ R3-1D: Lahaye et al. density up-ramp mechanism, kinetic 1D PIC — 2026-10-27
- **Script:** `sims/phase2/r3_lahaye_mechanism_1d.py` · data `results/data/R3_lahaye_mechanism_1d.json` · log `results/data/R3_1d.log`
- **Setup:** n₀ = 10¹⁸ cm⁻³, 0.8 µm (k0/kp = 41.7), a0 = 1.6, 25 fs; driver at the etching-corrected velocity c√(1 − 3n/n_c) (Lu 2007) so that the flat-density dephasing length is bubble-like; sin² entrance ramp 60 c/ω_p then n₀(1 + g z[mm]); 3000 test electrons over the first bucket (50 MeV); dx = 0.02, ppc = 12.
- **Result:** peak energy (distance) — flat 793 MeV (20.8 mm); g = 0.04/mm: 909 MeV (16.9 mm, **+14.7 %**); g = 0.08/mm (paper's value): 892 MeV (14.0 mm, **+12.6 %**); g = 0.12/mm: 859 MeV (12.2 mm, +8.3 %).
- **Comparison:** paper's FBPIC +20 % at 0.08 n₀/mm (≈1.4 GeV; experiment ×1.4). Our 1D model reproduces the sign and size of the dephasing-mitigation effect and the shorter distance to peak energy; the remaining difference is consistent with self-focusing, laser evolution and delayed injection, which are absent in 1D.
- **Conclusion:** density up-ramps give a modest (~10–15 %) electron-energy gain in 1D; for protons the relevant Phase-2 lever is the channel-width taper (S025), since protons need the wake *slowed*, not sped up.

### S029 ⚠️ FBPIC quasi-3D check of the guided resonant train (partial run) — 2026-10-27
- **Scripts:** `sims/phase2/fbpic_waveguide_train.py` (WSL, FBPIC 0.27.1 CPU, 6 threads), analysis `sims/phase2/analyse_fbpic_train_partial.py` · data `results/data/FBPIC_train_analysis_partial.json` · figure `results/figures/FBPIC_guided_train_partial.png`
- **Setup:** 1 GeV rigid-comb design (S022): three LG_{p,0} components p = 0/3/6 at λ = 1.000/1.052/1.118 µm, a0 = 0.3 each, intensity FWHM 2.5 plasma periods, all focused at the entrance of a matched parabolic channel (n₀ = 3.09×10¹⁸ cm⁻³, W = 6.83 µm, Δn/n₀ = 0.78, 10 µm entrance ramp); grid 3985×136, 2 modes, dz = λ/16, dr = 0.2 µm, mobile ions, moving window at c.
- **What happened:** the run (4000 steps planned, ~2.1 s/step) was **stopped by the host at ~step 1500–2000 because the system ran critically low on memory** (other jobs were running); not restarted. Snapshots at steps 500/1000/1500 (t = 313 fs) were saved — at t = 313 fs the front half of the train is inside the channel.
- **Normalisation check:** FBPIC's azimuthal decomposition gives Er_{m=1} = E_x/2 on axis → a = 2|Er₁|/E₀; peak a = 0.89 at the entrance vs design 3×0.3 = 0.9 ✔ (first analysis attempt missed the factor 2).
- **Result (in the channel, z > 17 µm):** the on-axis envelope is the designed rigid-comb pattern — main peaks every **16.4–16.6 µm** (design β_aλ_p = 16.62 µm) with the expected one-third-amplitude secondary maxima (measured ratio 0.34). The on-axis wake grows resonantly peak by peak and matches the 1D fluid wake driven by the *same measured on-axis drive* in shape and phase; amplitude ratio FBPIC/1D = **0.79** (field), i.e. **f_3D ≈ 0.62** in energy terms (the value used in the design calculator). The wake is confined to r ≲ 5 µm (designed peak radius 0.46 W).
- **Not established by this partial run:** peak-train velocity inside the channel (too short a window), guiding of the p = 6 mode over cm lengths, proton focusing, ion motion over long trains. A full run needs ~2.5 h and ~2 GB RAM in WSL.

---

## Design synthesis (estimates built on the simulated ratios)

### S030 — design calculator — 2026-10-27
- **Script:** `sims/design/design_calc.py 0.62` · data `results/data/design_calc.json`, `results/data/D2_physical_sheet.json` · figures `results/figures/summary_efficiency_ranking.png`, `summary_gain_per_stage.png`
- Every factor is tagged sim/lit/est in the JSON. Wall-plug → 6 GeV proton efficiency: RF reference 15 % [lit]; **D2 guided resonant train 3.3 % (today's fibre) – 6.4 % (projected fibre)**; D3 all-optical 0.68 % (transverse-flying-focus coupling) / 0.008 % (transverse pumping); D1 free-space flying focus 0.14–0.43 % (fibre), 10⁻⁵ (Ti:Sa); D4 near-critical RPA 6×10⁻⁵ [lit]; D0 conventional staged 2×10⁻⁴ (fibre), 5×10⁻⁷ (Ti:Sa).
- LWFA section only (1 → 6 GeV): D2 5.8 % / 2.9 % vs conventional 1.7×10⁻⁴ (fibre) / 4.2×10⁻⁷ (Ti:Sa) → **efficiency multiplier ≈ 340× (same lasers), ≈ 1.4×10⁵× vs Ti:Sa conventional LWFA**.
- D2 physical sheet [est]: 3 stages (1→2→3.5→6 GeV, n₀ = 3.1×10¹⁸ / 1.2×10¹⁸ / 6×10¹⁷ cm⁻³, 22–51 GV/m) ≈ 18 cm of plasma; 4.4×10⁷ protons (7 pC) and 0.31 J of laser per shot; a 1 MW beam needs 24 MHz, 7.4 MW laser average power, 19.6 MW (projected) / 38 MW (today) wall-plug.

---

## Follow-up (full multi-D check requested) — 2026-10-27

### S031 ⚠️ P1g: guided train with physically correct kinematics (envelope at ~c, pattern at v_a), fixed velocity — 2026-10-27
- **Why:** in a plasma channel only the beat pattern moves at v_a; the energy envelope travels at the modes' group velocity (≈ 0.9995c here). S024/P1f moved the envelope with the pattern (optimistic). Protons at v_a therefore fall behind the envelope and ride the free plasma wave it leaves, whose phase velocity is imprinted by the peak timing.
- **Script:** `sims/phase1/p1g_two_velocity_train.py` (TwoVelocityDriver; window moves with the envelope so the imprinted wave is kept) · data `results/data/P1g_nenv12.json` · log `results/data/P1g_nenv12.log`
- **Setup:** 3 GeV design (P = 2, N = 3, spacings 0.981/1.019 ω_p), a_avg = 0.35, 12-period envelope, mobile ions, bunch (load 0.4 E_peak) in the first bucket behind the envelope; pattern velocity **fixed** at the injection velocity (no taper, no feedback).
- **Result:** protons ride the imprinted wave and gain 3000 → 3043 MeV in the first 600 c/ω_p (≈ 0.14 E₀ — same as the rigid model), then dephase and **lose** energy (2795 MeV after 2700 c/ω_p): a 1.4 % energy change at 3 GeV changes β by 7×10⁻⁴, i.e. ~⅓ wake period of slip over 3000 c/ω_p.
- **Conclusion:** the free imprinted wave works as an accelerating structure (the driver need not stay with the protons), but the pattern velocity must follow the proton velocity *as a function of position*. Physical implementation: a **static** channel-width taper with v_pat(z) = v_proton(z) (open loop; tested in S032).

### S032 ⚠️ P1g static channel-taper (open-loop) test — partial (stopped by host, low memory) — 2026-10-27
- **Script:** `sims/phase1/p1g_two_velocity_train.py --taper --G 0.07` (TaperedTwoVelocityDriver: pattern is a function of t − τ(z), τ(z) = ∫dz/v_pat(z), v_pat(z) = velocity of a proton gaining G = 0.07 MeV per c/ω_p — fixed before the run, no feedback) · log `results/data/P1g_taper_G0.07.log`
- **What happened:** stopped by the host's memory-pressure safeguard after 900 of 3000 c/ω_p (another heavy job had started); not restarted.
- **Partial result:** ⟨T⟩ = 3034 / 3072 / 3088 MeV at 300 / 600 / 900 c/ω_p (design 3021 / 3042 / 3063), spread ±9–14 MeV — still accelerating where the fixed-velocity case (S031) had already turned to deceleration; protons ride the imprinted wave 88–114 c/ω_p behind the envelope centre.
- **Conclusion (provisional):** an open-loop static channel taper keeps protons on the imprinted wave; the gain slightly exceeds the design rate, so a second iteration of v_pat(z) would be needed for long stages. Full run pending.

### S033 ❌ FBPIC guided-train rerun with proton bunch — stopped by host (low memory) at step ~500–750 — 2026-10-27
- **Script:** `sims/phase2/fbpic_waveguide_train.py --steps 4500 --protons` (adds a 1 GeV, 16 fC proton bunch, mode-0 E_r/B_θ maps for the proton focusing force, snapshots every 250 steps after step 1500) · log `sims/phase2/fbpic_train_run2.log`
- **What happened:** reached step 500 (t = 104 fs, train still in vacuum; max RSS 2.0 GB) before the host stopped it; no new physics information. Not restarted. The first (partial) run's snapshots are preserved in `sims/phase2/fbpic_train_out_v1partial/` (analysis S029 unchanged).
- Analysis scripts for the full run are ready: `sims/phase2/analyse_fbpic_train_full.py`, `sims/phase2/fbpic_vs_1d_two_velocity.py`.

---

## Deuterium studies — 2026-10-29

### S034 ✅ Multi-pulse wake with mobile deuterium ions (Hooker 2014 case) — 1D envelope PIC
- **Script:** `sims/phase1/r2_hooker2014_multipulse.py 120 D` · data `results/data/R2_hooker2014_mobileD.json`
- **Result:** wake behind the 120-pulse train: immobile 5.01 GV/m (S017), mobile H 4.28 GV/m (−15 %), **mobile D 4.85 GV/m (−3 %)**.
- **Conclusion:** deuterium plasma removes ≈ 80 % of the (longitudinal) ion-motion loss in 1D; transverse ion motion (the larger effect in multi-D) is expected to improve in the same direction but is not simulated.

### S035 ✅ Velocity-matched acceleration of deuterons to 3.6 GeV (1.8 GeV/u) — fluid tracker
- **Script:** `sims/phase1/p1b_deuteron_scan.py` (tracker species = deuteron) · data `results/data/P1b_deuteron_scan.json`
- **Sanity check:** deuterons 2.0 → 2.5 GeV vs protons 1.0 → 1.5 GeV (same initial β): length 2256 vs 2223 c/ω_p, gradient 0.435 vs 0.441 E₀, wake→beam 40.6 % vs 40.7 %.
- **Result:** 2.0 → 3.6 GeV: 6455 / 7593 c/ω_p, 0.49 / 0.41 E₀, **η 33 % / 47 %** (load 0.3 / 0.5), spread 0.4 %; 1.5 → 3.6 GeV: 9641 / 11389 c/ω_p, η 36 % / 50 %. Protons 1 → 6 GeV: 19263 / 22916 c/ω_p, η 35 % / 50 %.
- **Conclusion:** same wake→beam efficiency, plasma section 2–3× shorter (only 1.6–2.1 GeV to add). Injection must start at 1.5–2 GeV for deuterons (same β threshold of the guided train).
- **Energy per muon (estimate, `design_calc.energy_per_muon`, `results/data/energy_per_muon.json`):** deuterons (RF 2 GeV + train to 3.6 GeV) 99–119 GeV (today's fibre) / 59–71 GeV (projected) wall-plug per stopped μ⁻, overall efficiency 5.0 % / 8.5 %; protons (RF 1 GeV + train to 6 GeV) 200–360 / 104–187 GeV, 3.3 % / 6.4 %; RF-only 33–40 (d) / 44–80 (p) GeV. Muon yields are literature values.

### S036 ⚠️ Static channel taper (open loop) — full runs in H, D and immobile ions; 3-line comb
- **Script:** `sims/phase1/p1g_two_velocity_train.py --taper --G 0.07 [--ion H|D|none]` · data `results/data/P1g_taper_G0.07_{Hplasma,Dplasma,immobile}.json`
- **Result (⟨T⟩ at 900 / 1800 / 2700 c/ω_p; design 3063 / 3126 / 3189 MeV):** H plasma 3088 / 3147 / **3172**; D plasma 3070 / 3004 / **2951**; immobile ions 3010 / 2821 / **2794**.
- **Correction to S032:** the provisional "taper keeps protons accelerating" (H run stopped at 900 c/ω_p) does **not** hold generally: identical drives succeed in H but dephase in D and with immobile ions → the protons sit at the edge of phase stability.
- **Diagnosis (hypothesis, not confirmed):** the rigid 3-line comb has unequal spacings (0.981/1.019 ω_p). Behind an envelope moving at ≈ c, each near-resonant component leaves a free wave with a slightly different phase velocity, 1/v ≈ (ω_d/ω_p)/v_pat + (1 − ω_d/ω_p)/v_env, so the composite wave's phase drifts by ~π over ~3000 c/ω_p. In the rigid-envelope model (P1f) this cannot occur, which is why S024 succeeded.

### S037 ⚠️ Fix candidates — stopped by host (low memory) at 600 c/ω_p
- **Two lines spaced by exactly ω_p** (N = 2 beat wave in two channel modes — rigid by construction, exactly resonant), D plasma (`P1g_taper_N2_Dplasma.log`): 3030 / 3052 MeV at 300 / 600 c/ω_p (design 3021 / 3042) — on design so far.
- **Three equally spaced lines** (diagnostic, immobile ions; `P1g_taper_N3uniform_immobile.log`): 3004 / 3008 MeV — weak gain (bunch probably in a weak phase); inconclusive.
- Both runs stopped by the host's memory-pressure safeguard (other jobs running); not restarted. The diagnosis therefore remains unconfirmed.

---

## Follow-up 3 — 2026-11-03

### S038 ⚠️ Guided train, left-behind wave: line-spacing diagnosis and taper iteration (1D envelope PIC, D plasma)
- **Script:** `sims/phase1/p1g_two_velocity_train.py --taper --ion D [--spac ...] [--G ...]` · logs `results/data/P1g_taper_*`
- **Two lines spaced by exactly ω_p, G = 0.07** (`P1g_taper_N2_Dplasma`): monotonic gain 3000 → 3067 / 3082 / 3094 / 3106 / **3116 MeV** at 900 / 1500 / 2100 / 2400 / 2700 c/ω_p, spread narrowing to ±12 MeV, wake→beam **25 %** — no reversal, unlike the 3-line (0.981/1.019) D-plasma run (S036: 2951 MeV).
- **Three equally spaced lines** (`P1g_taper_N3uniform_Dplasma`): weak wake behind the envelope (E_peak 0.066 E₀ vs ~0.27), no net gain (2997 MeV) — probably nonlinear saturation of the exactly resonant 3-line drive; inconclusive as a diagnostic.
- **Two lines, taper re-designed for the measured gain rate G = 0.045** (`P1g_taper_N2_G0.045_Dplasma`): rises to 3051 MeV by 900 c/ω_p then oscillates (synchrotron-like) around it; final 3051 MeV — worse than the first iteration.
- **Conclusion:** two lines (exact resonance) remove the phase-drift failure seen with the 3-line comb, but the left-behind-wave accelerator is a delicate phase-stability problem: the taper must be designed RF-linac style (stable synchronous phase, taper set from the measured imprinted-wave amplitude at that phase), not from a guessed gain rate. Best 1D result so far: +116 MeV over 2700 c/ω_p, wake→beam 25 % (vs 58.5 % in the rigid-envelope model S024). Design numbers revised accordingly (S041).

### S039 ✅ Photovoltaic recovery: spectrum of the light leaving the plasma (full-EM 1D PIC)
- **Script:** `sims/phase2/p2d_pv_recovery_spectrum.py --case beat|single` (k0/kp = 10) · data `results/data/P2d_pv_spectrum_{beat,single}.json`
- **PV model [lit]:** best monochromatic laser power converters at ~1.07 µm 55–59 % (Broadcom multijunction InGaAsP, 2025), ~45 % at 1.55 µm, 68.9 % GaAs record near 0.85 µm (GaAs cannot absorb 1 µm light); cell bandgap 5 % below the lowest drive line, photons above it converted at η_max ω_g/ω.
- **Two-line beat drive:** in-band (±10 %) fraction of the remaining light 77 % → 26 % → 11–15 % as absorption rises 0 → 16 % → 49–56 %; PV efficiency on the remaining light 49 % → 30 % → 21–24 %.
- **Single resonant pulse (a0 = 1.5):** in-band 96 % → 5 %, PV efficiency on the remaining light 44 % → ~2.5 % once ≳ 25 % is absorbed (caveat: part of the up-shifted spectrum may be harmonics/numerical high-k noise; the in-band fraction is the robust number).
- **Conclusion:** light that has driven the wake is spread far out of a PV cell's band (photon deceleration plus up-shift); only light that never interacted (coupling losses, free-space/side-pumped schemes) stays near-monochromatic. Upper bound on the wall-plug gain: 1/(1 − η_laser η_PV f_rec) ≲ 1.2× for 40 %-efficient lasers with 55 % cells (≲ 1.5× even with ideal cells). Design calculator: guided train ×1.04–1.09, free-space / side-pumped ×1.08–1.18.

### S040 ✅ Beat-driven surface plasmon in a hollow channel (Lei et al., PRL 137, 105002 (2026)) — can it match protons?
- **Script:** `sims/phase1/p1h_surface_plasmon_dispersion.py` · data `results/data/P1h_surface_plasmon_dispersion.json` (exact TM₀ dispersion of a vacuum tube of radius R in a cold plasma wall; linear, no amplitudes)
- **Check:** large-R limit reproduces the planar result (β = 0.875: ω = 0.46 vs 0.436 ω_p; β = 0.43: 0.675 vs 0.671).
- **Result:** curvature pushes the mode towards c, so narrow tubes (R ≤ 1 c/ω_p) carry no slow surface mode. Matched modes and on-axis/wall field ratio: 1 GeV (β 0.875) R = 3 c/ω_p → 0.75; 3 GeV → 0.94; 300 MeV → 0.32 (R = 3); 100 MeV only for R ≳ 10 c/ω_p where the on-axis field is 5×10⁻⁶ of the wall field; none for 10 MeV in the scanned range.
- **Conclusion:** the surface-plasmon scheme cannot serve the slow low-energy proton section (field confined to the wall); it is a possible alternative structure above ~1 GeV, but slow-plasmon drive (beat with Δk > Δω/c), field per GW, efficiency and hollow-channel beam break-up would need PIC.

### S041 — design calculator revision (estimates on simulated ratios)
- **Script:** `sims/design/design_calc.revised_designs()` · data `results/data/design_calc_revised.json`
- With wake→beam 0.25 (S038) and PV recovery (S039): RF injector + guided train, protons 1.5 % (today's fibre) / 2.9 % (projected), 3.1 % with PV; deuterons 2.5 % / 4.6 % (4.9 % with PV). All-optical (no RF injector): best 0.5 % / 1.0 % (1.2 % with PV) — self-injection with NP-like layer, transverse-flying-focus coupling [lit], hand-off to the train at 0.5 GeV; the slow section uses 62–100 % of the energy.

### S042 ❌ FBPIC full guided-train run with protons — stopped by host (low memory) after step ~500, 2026-11-03
- Third attempt (log `sims/phase2/fbpic_train_run3.log`); only the step-500 snapshot (train still in vacuum, max RSS 2.0 GB) was saved; no new physics. Not restarted.


### S043 ✅ FBPIC quasi-3D guided-train run with protons — completed on a Modal GPU — 2026-11-03
- **Scripts:** `sims/phase2/modal_fbpic_train.py` (Modal, NVIDIA A10 via GPU fallback list, FBPIC 0.27.1 CUDA with numba-cuda + NVIDIA bindings; 4500 steps in 427 s, ≈ 0.09 s/step, ≈ $0.2), analysis `analyse_fbpic_train_full.py`, `fbpic_vs_1d_two_velocity.py` · data `results/data/FBPIC_train_analysis_full.json`, `FBPIC_vs_1D_two_velocity.json` · figure `results/figures/FBPIC_guided_train_full.png`
- **GPU set-up failures on the way (logged):** Avast HTTPS interception blocked the Modal client (fixed with a launcher trusting the Windows root store); no L4 capacity (GPU fallback list); segfault in numba 0.60's legacy CUDA driver binding on driver 610.57 (fixed with numba-cuda + NVIDIA bindings); missing pyfftw; an unnecessary GPU→CPU copy in our diagnostics.
- **Results (t = 938 fs, train fully in the channel):**
  - beat-pattern velocity in the channel: mean **0.875c** (design 0.875c; snapshot scatter 0.83–0.91); energy envelope ≈ c (two-velocity kinematics confirmed in multi-D);
  - accelerating **and** focusing region for protons exists in every period: 24–34 % of the period, within r ≲ 3 µm;
  - on-axis wake vs the 1D two-velocity model with the same drive: **f_3D = 0.72 (field), 0.52 (energy)**;
  - **wake left behind the envelope decays quickly:** 0.36 / 0.31 / 0.24 / 0.23 / 0.24 / 0.18 E₀ in periods 1–6 behind it, with the waveform degrading — the imprinted wave halves within ~6 plasma periods (~350 fs), versus the ~5–7 ps the left-behind-wave design needs (most likely channel-induced phase-front curvature; absent in 1D).
  - proton test bunch: inconclusive — its emittance (normalised 1e-7 m rad at σ_r = 1.5 µm ⇒ ~37 mrad divergence) spread it to 13 µm before it reached the plasma; mean energy unchanged within 0.3 MeV.
- **Conclusion:** the guided resonant train's optics and drive are confirmed in multi-D, and protons get a focusing+accelerating phase; but a stage cannot rely on the wave left behind the light. The drive must stay with the protons — a long (multi-ps) envelope of duration ≳ (1/β − 1)L/c — which suits ps fibre/thin-disk lasers but raises the laser energy per shot. This is now the governing design constraint.

### S044 ⚠️ FBPIC quasi-3D test of beat-driven surface plasmons for 3 GeV protons (hollow channel) — Modal GPU — 2026-11-03
- **Scripts:** `sims/phase2/fbpic_surface_plasmon.py` (run via `modal_fbpic_sp.py`, 6000 steps, 2434 s on GPU; log `sims/phase2/fbpic_sp_run_modal.log`), analysis `analyse_fbpic_sp.py` · data `results/data/FBPIC_surface_plasmon_analysis.json`, raw `sims/phase2/fbpic_sp_out/` · figure `results/figures/FBPIC_surface_plasmon.png`
- **Set-up (from S040):** wall n = 1.02×10²⁰ cm⁻³ (E₀,wall = 973 GV/m), vacuum core R = 3 c/ω_pw = 1.58 µm, two colours 1.00 µm + 1.25 µm (beat = 0.662 ω_pw, target wave speed 0.971c), a0 = 0.4 each, 100 fs, w0 = 0.65R, launched already focused inside the channel (an earlier attempt launched from vacuum clipped the 1-µm-waist beam); 3 GeV proton test bunch (σ_r = 0.15R, normalised emittance 2×10⁻¹⁰ m rad) placed behind the laser.
- **Results (t = 667 fs, ≈ 200 µm of channel):**
  - beat is guided; on-axis E_z in the train 13–30 GV/m over the run (17 GV/m at the end) = **~0.02 E₀,wall**; axis/wall ratio 1.1 (field fills the core, as predicted for R = 3 c/ω_p at this speed);
  - wave phase velocity: only two usable snapshot-pair estimates, **1.05c and 1.10c** (target 0.971c). Superluminal values point to the measured E_z being dominated by the laser-driven/guided-mode beat rather than a free slow surface wave; the slow mode is **not** demonstrated;
  - behind the envelope the field falls from 6.4 GV/m (period 1) to 2–3 GV/m noise level by period 5–10 — no persistent surface wave;
  - protons (75 µm behind the envelope centre, i.e. in the decayed region): mean ΔT = +0.003 MeV, per-particle ±2.5 MeV, r_rms 0.335 → 0.339 µm, 100 % stay inside R — **no measurable acceleration**, no break-up.
- **Conclusion:** first test negative/inconclusive. The design flaws are identifiable: (i) the bunch should sit inside the beat, but a 0.971c proton slips back relative to a ≈c envelope, so the drive must be long (same constraint as S043); (ii) a co-propagating two-colour beat in a hollow guide moves at ≈ the guided group velocity (> 0.99c here), so matching 0.971c needs Δk > Δω/c (e.g. different guided modes or a counter-/oblique geometry), not just a frequency difference. Does **not** beat the guided train at 3 GeV; not added to the design. A follow-up would need a mode-mismatched beat and a multi-ps envelope.
