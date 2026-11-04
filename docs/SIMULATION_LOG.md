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
  - wave phase velocity (**corrected 2026-11-03**, cross-correlating on-axis E_z between successive snapshots near the envelope, 11 pairs): **0.979 ± 0.006c**, vs 0.971c needed and **0.980c predicted** by the LP01 guided-mode dispersion of the hollow channel (both colours in the fundamental mode; V = ω_pw R/c = 3). *The first version of this entry reported 1.05c and 1.10c: that zero-crossing estimate was wrong — it picked up noise behind the envelope and mixed in three stale snapshots (steps 50/100/200) from the earlier clipped attempt.* So the beat is sub-luminal and only ~1 % too fast (dephasing length ≈ 0.3 mm);
  - behind the envelope the field falls from 6.4 GV/m (period 1) to 2–3 GV/m noise level by period 5–10 — no persistent surface wave;
  - protons (75 µm behind the envelope centre, i.e. in the decayed region): mean ΔT = +0.003 MeV, energy spread unchanged (σ_T 0.391 → 0.391 MeV; the per-particle "±2.5 MeV" first quoted was an artefact — particle order is not preserved between GPU snapshots), r_rms 0.335 → 0.339 µm, 100 % stay inside R — **no measurable acceleration**, no break-up.
- **Conclusion:** first test negative/inconclusive, for an identifiable reason: the bunch sat behind the laser, where the wave had decayed — a 0.971c proton falls back relative to a ≈c envelope, so it must start inside the beat and the envelope must be long enough to hold it over the stage. (A second suggested fix in the first version of this entry — a beat with Δk > Δω/c from different guided modes — was based on the wrong speed measurement and is not needed: a small radius change, R = 3 → 2.4 c/ω_pw, retunes the fundamental-mode beat to 0.972c.) Does **not** beat the guided train at 3 GeV on this evidence; follow-up S045.

### S045 ✅ FBPIC surface-plasmon follow-up (protons inside the beat, speed retuned) — Modal GPU — 2026-11-04
- **Set-up:** `modal_fbpic_sp.py --steps 12000 --diag-every 1000 --extra "--R_cwp 2.4 --wsp 0.705 --w0_R 1.10 --tau_fs 150 --bunch centre" --out fbpic_sp2_out` (8882 s on GPU, ≈ $3; log `sims/phase2/fbpic_sp2_run_modal.log`) · analysis `analyse_fbpic_sp.py fbpic_sp2_out FBPIC_surface_plasmon_followup` · data `results/data/FBPIC_surface_plasmon_followup_analysis.json` · figure `results/figures/FBPIC_surface_plasmon_followup.png`. Fixes from S044: (i) proton bunch at the envelope centre, inside the beat; (ii) channel radius 3 → 2.4 c/ω_pw (R = 1.26 µm) so the LP01 guided-mode beat moves at 0.972c (3 GeV protons 0.971c); surface-mode frequency 0.705 ω_pw (S040 dispersion); laser waist matched to the LP01 mode (1.10 R). Wall 1.0×10²⁰ cm⁻³, two colours 1.00 + 1.27 µm, a0 = 0.4 each, 150 fs, ≈ 1.7 mJ total [est from a0, w0, τ].
- **Results (t = 1.33 ps, ≈ 0.36 mm of proton travel inside the beat):**
  - wave speed (cross-correlation, 11 snapshot pairs): **0.971 ± 0.007c** — matched to the protons (target 0.9712c);
  - wall E_z 30–90 GV/m over the run; on-axis E_z similar but noisy (macro-particle noise on axis inflates the axis peak, so the 1.38 axis/wall ratio is not reliable); field behind the envelope only 5–9 GV/m — the surface wave again does not persist behind the light;
  - **protons:** energy spread grows steadily, σ_T 1.15 → **8.97 MeV**, range 2996.5–3003.3 → **2984.4–3015.0 MeV**, with the energy modulated along the bunch at the surface-wave period (≈ 4.6–4.8 µm): a coherent, phase-locked interaction, no saturation within the run. Best-phase protons gained ≈ +15 MeV in ≈ 0.36 mm ⇒ **≈ 40 GV/m effective gradient** on the protons. Mean +0.26 MeV (the bunch spans all phases). r_rms 0.27 → 0.30 µm, 100 % stay inside the channel;
- **Conclusion:** with both fixes the beat-driven surface plasmon accelerates 3 GeV protons at ≈ 40 GV/m in quasi-3D PIC — comparable to the guided train's 22–51 GV/m design range. Not yet a design candidate because: (a) efficiency was not measured (test bunch carries no charge; needs a beam-loaded run); (b) the wave lives only under the light, so a stage needs an envelope ≳ (1/β − 1)L/c (≈ 2.4 ps for a 1 GeV, 25 mm stage); (c) the channel is 1.26 µm in radius, so the bunch must have ~2×10⁻¹⁰ m rad normalised emittance — ~500× smaller than the guided-train test bunch (S043) and far below today's proton beams. Scaling R up at fixed physics means lower density and longer laser wavelength, with fields falling ∝ 1/R.

### S046 ✅ "Electric flying focus" — electric analogue of Mach-Batlle et al. (PRL 125, 177204) for protons
- **Scripts:** `sims/phase1/e1_electric_flying_focus.py` (parts A–D, ~2 min on the laptop), figure `sims/phase1/e1_figure.py` · data `results/data/E1_electric_flying_focus.json` · figure `results/figures/E1_electric_flying_focus.png` · write-up `docs/research/electric-flying-focus.md`
- **Model:** a pattern moving rigidly at v obeys Laplace's equation in the proton frame (exact in vacuum); wall-field Fourier modes reach the axis with factor 1/I₀(ka/γ). Tracking: 6D, paraxial quasi-static fields recomputed every step from discrete ring electrodes (each fires the pattern at its own centre with its own random timing error); smooth external focusing; no space charge (handled in Part D as an estimate).
- **A (replicator):** reproducing a virtual ring charge at r_v inside the bore (inward Mach-Batlle replica) to ≤3 % needs wall/axis peak field 12× (r_v = 0.75a), 28× (0.5a), 2×10⁴× (0.25a), ~10¹¹× (0.1a, 5 % error); grows like e^{k_max(a − r_v)}; axis field never exceeds wall field (maximum principle).
- **B:** a moving flat-top transmits 0.30/0.55/0.84/0.99/1.00 of the wall field to the axis for lengths 0.5/1/2/4/8 γa.
- **C (tracking 1 → 100 MeV):** a = 2 mm, 2 mm electrode pitch, 50 MV/m wall, 20 mm flat-top/10 mm edges: synchronous field 32.6 MV/m, 3.04 m, 100 % captured, ΔT/T 0.1 %; timing jitter 0/2/10/30 ps: no measurable effect; no external focusing: 100 % lost to the wall; required focusing at 1 MeV ≈ 10.6 T solenoid or ~200 T/m smooth quadrupole equivalent.
- **D (estimate):** field energy 0.14 J/m (bore), ~0.56 J/m (vacuum-gap rings), ~8 J/m (DWA insulator wall); space-charge-limited bunch 29 pC (1 MeV) … 2.3 nC (1 GeV); wall-plug→beam 0.12 % (section from 1 MeV, vacuum gaps) / 0.6 % with 80 % field-energy recovery / 0.008 % DWA-style; 10–31 % for a section starting at 1 GeV.
- **Conclusion:** the programmable-velocity part works (robust phase lock from 1 MeV, jitter-tolerant); the "virtual source in an inaccessible region" part gives no acceleration gain (on-axis ≤ wall field; concentrating costs exponentially). As a non-RF front end to 0.5 GeV feeding the guided train: system 0.9 % (1.9 % with recovery) vs all-optical 1.0 % and RF + train 2.9 % [est].

### S047 ✅ Electric flying focus — how short can 1 → 100 MeV be? (gradient / pattern / ramp scan)
- **Script:** `sims/phase1/e1_electric_flying_focus.py --parts S --Np 1000` · data `results/data/E1_shorter_scan.json`. Same tracking as S046 (10 ps jitter); the external focusing is now programmed to the smooth pattern's defocusing (3×), not to electrode-to-electrode spikes. Efficiency estimate: field energy per energised metre 0.56 J/m × (E_w/50 MV/m)² (vacuum-gap rings), 70 % pulsed power, no recovery, bunch charge either fixed at 29 pC or set by the focusing margin at 1 MeV.

| case | length | mean gradient | captured | quad gradient (solenoid) needed at 1 MeV | wall-plug→beam, 29 pC / focusing-limited charge |
|---|---|---|---|---|---|
| 50 MV/m, S046 pattern | 3.03 m | 33 MV/m | 100 % | 194 T/m (10.6 T) | 0.12 % / 0.31 % (75 pC) |
| 50 MV/m, 40 mm flat-top, sync at 92 % | 2.24 m | 44 MV/m | 100 % | 104 T/m (7.7 T) | 0.16 % / 0.22 % (40 pC) |
| 100 MV/m | 1.52 m | 65 MV/m | 100 % | 388 T/m (15 T) | 0.06 % / 0.31 % (150 pC) |
| 200 MV/m | 0.76 m | 131 MV/m | 100 % | 775 T/m (21 T) | 0.03 % / 0.31 % (300 pC) |
| 200 MV/m, 40 mm flat-top, sync at 92 % | 0.56 m | 177 MV/m | 100 % | 414 T/m (15.5 T) | 0.04 % / 0.22 % (160 pC) |
| ramp 50 → 200 MV/m by 20 MeV, 20 mm edges | 0.88 m | 113 MV/m | 100 % | 98 T/m (14.6 T) | 0.03 % / 0.04 % (38 pC) |

- **Conclusion:** length scales as 1/gradient and the dynamics stay clean at every gradient tried (100 % capture, ≤ 0.6 % spread). The price: field energy per metre grows as E², so at a fixed bunch charge the efficiency falls as 1/E; it holds only if the focusing (and with it the space-charge-limited charge) is scaled up with the gradient, which at 200 MV/m means ~400–800 T/m quadrupoles at 1 MeV. The cheapest shortening is free: a longer flat-top with the protons higher on the edge (3.0 → 2.2 m at the same 50 MV/m, with *weaker* focusing). Whether 100–200 MV/m survives on ns-pulsed electrodes is an assumption, not checked here.

### S048 ✅ FBPIC surface-plasmon long run (2 mm) — Modal GPU, detached — 2026-11-04
- **Why:** in S045 the light pulse's own speed inside the 1.26 µm-radius channel was 0.966c vs proton 0.971c (protons stayed within ±4 µm of the pulse centre); the 0.36 mm of S045 was a compute limit.
- **Run:** same as S045, 60000 steps (≈ 1.94 mm of proton travel), `modal run --detach sims/phase2/modal_fbpic_sp_long.py --steps 60000 --diag-every 2000 --extra "--R_cwp 2.4 --wsp 0.705 --w0_R 1.10 --tau_fs 150 --bunch centre" --out fbpic_sp3_out` (17420 s ≈ 4.8 h, ≈ $9) · analysis `analyse_fbpic_sp.py fbpic_sp3_out FBPIC_sp_2mm` + history `results/data/FBPIC_sp_2mm_history.json` · figure `results/figures/FBPIC_sp_2mm.png`.
- **Results (energy-modulation amplitude of the 3 GeV test bunch, sinusoid fit):** 3.1 / 7.6 / 11.3 / 13.8 / 15.3 / 16.3 / 17.1 / 17.8 / 18.2 MeV at 0.06 / 0.19 / 0.32 / 0.45 / 0.58 / 0.71 / 0.84 / 0.97 / 1.10 mm, then **flat at 18.2 MeV to 1.94 mm** (best protons +18 MeV, worst −17 MeV). Effective gradient ≈ 31 GV/m over the first 0.3 mm, 17 GV/m averaged to saturation at ~1.1 mm.
- **Why it saturates (three effects, all measured):** (i) the wave slows from 0.971c to a steady **0.9675–0.968c** after ~0.3 mm (laser evolution), so the protons (0.9712c) outrun it by half a period (2.3 µm) in ~0.6 mm; (ii) the laser depletes — peak a 0.63 → 0.28, on-axis laser energy 38 % of initial at 1.94 mm, wall field 84 → ~20 GV/m; (iii) the protons drift ahead of the pulse centre by ~24 µm (pulse ≈ 0.966c). Bunch r_rms 0.27 → 0.78 µm, 93 % still inside R = 1.26 µm.
- **Conclusion:** ≈ 18 MeV per ~1 mm of hollow channel per 1.7 mJ (two colours) at 3 GeV before refreshing. To go further: taper the channel radius so the wave speed tracks the protons (as for the train), and re-supply laser energy every ~1 mm (staging) — a 1 GeV gain would need ~50 such refreshes or a tapered, continuously fed channel. Efficiency measured next (S053, beam-loaded).

### S049 — combined staged accelerator: surface-plasmon speed limits, slow-light matching, staged efficiencies (calculation)
- **Script:** `sims/design/combined_stages.py` · data `results/data/combined_stages.json`
- **Surface plasmon at low speed (exact S040 dispersion, best over all channel radii):** best on-axis/wall field 6×10⁻²¹ (10 MeV), 6×10⁻⁷ (30 MeV), 0.03 (100 MeV), 0.38 (300 MeV), 0.80 (1 GeV), 0.96 (3 GeV). The field of a slow surface wave is tied to the wall by the same proton-frame Laplace physics as the electric flying focus (decay over ~βγλ/2π); a flying focus changes the drive's speed, not this, so it cannot extend the SP below ~0.3–1 GeV.
- **Slow light in the hollow channel (two colours in the LP01 mode, beat matched to the protons):** 3 GeV — pulse speed 0.977c vs 0.971c (slip 0.6 %; FBPIC S045 measured 0.966c); 1 GeV — pulse 0.926c vs 0.875c (slip ≈ 6 %: here a flying-focus-type envelope control or a longer pulse would be needed); 300 MeV — no match. So slow light keeps the pulse with the protons only above ~1–2 GeV.
- **Staged efficiencies [est; SP efficiency is a scenario — not yet simulated]:** projected fibre lasers, train 0.5→1.5 GeV, SP 1.5→6 GeV: RF front end 2.6–4.9 % (2.9–5.4 % with PV); electric-flying-focus front end 1.4–1.8 % without / 2.0–3.0 % with 80 % field-energy recovery (+0.06–0.15 points from PV); RF to 1.5 GeV then SP only: 3.1–6.8 % (3.4–7.4 % with PV). Lower bound = SP as efficient as the train (wake→beam 0.25); upper = SP free of the train's left-behind-wave loss (0.585, S024), plausible because its pulse moves with the protons — to be tested.
- **Addendum (2026-11-04): per-section efficiencies and PV** (`combined_stages.py` part 4). Wall-plug→beam per section, today / projected fibre lasers: RF linac 15 % [lit]; electric flying focus 0.23 % (0.6 % with 80 % recovery) [est on S046/S047]; laser slow section (self-injection) 0.068 / 0.135 %; guided train 1.23 / 2.46 %; surface plasmon 1.23–2.88 / 2.46–5.76 % (scenario). Laser light left unused: 60 % of the laser energy (38 % never coupled into the channel + 22 % leaving after driving the wave). Recovering *all* of it at 69 % would raise the laser sections ×1.09 (today) / ×1.20 (projected); with realistic cells (S039) ×1.09. Energy-bill shares (slow/train/SP) for non-RF versions are 27–69 % / 8–20 % / 21–60 % — the slow section is the largest share only when the electric front end has no energy recovery; **this corrects the statement in the first S049 entry and § 14 that it dominates in every non-RF version.**

### S050 ✅ Guided train with a low-emittance 1 GeV proton bunch — first measured train gradient on protons (FBPIC quasi-3D, Modal GPU) — 2026-11-04
- **Run:** `modal_fbpic_generic.py --script fbpic_waveguide_train.py --args "--steps 6000 --diag_every 500 --protons --zb_um -85 --p_sigr 1.0e-6 --p_emit 1e-8 --p_sigz 8e-6" --out fbpic_train_p1_out` (904 s, ≈ $0.5) · analysis `analyse_train_protons.py` · data `results/data/FBPIC_train_protons_analysis.json` · output bunch `sims/phase2/bunch_from_train.npz`. Same train as S043 (3 lines, LG₀,₃,₆, n₀ = 3.09×10¹⁸ cm⁻³, pattern 0.875c); proton bunch 10× lower emittance than S043 (1×10⁻⁸ m rad, σ_r 1 µm, σ_z 8 µm), placed 14 µm ahead of the envelope centre so it slips back through the drive.
- **Results:** on-axis wake up to 115 GV/m inside the train (≈ 0.68 E₀), 67–92 GV/m later; the proton energy is modulated along the bunch with period **16.2 µm** (= the 0.875c pattern wavelength) — phase-locked; sinusoid amplitude **3.9 MeV over ≈ 243 µm in plasma ⇒ 16 GV/m effective gradient** on the protons (same metric gives **31 GV/m** for the surface plasmon, S045); best bin +4.3 MeV. Bunch passed from +14 µm ahead to −24 µm behind the envelope centre (slip 12.5 %). r_rms 1.4 → 3.1 µm (growing: the focusing region is r ≲ 3 µm); emittance preserved (1.13×10⁻⁸).
- **Meaning:** the 22–51 GV/m quoted before was a design-density range, not a simulation. Measured on protons at 3.1×10¹⁸ cm⁻³: 16 GV/m averaged over the bunch's passage through the drive (peak wake 0.36–0.68 E₀ = 60–115 GV/m). The protons pass through the drive in ~0.3 mm, after which only the decaying left-behind wave remains (S043).

### S051 ✅ "Train + surface plasmon in one channel": 3-line comb vs 2 colours at equal laser energy (FBPIC quasi-3D, Modal GPU) — 2026-11-04
- **Run:** `modal_fbpic_generic.py --script fbpic_surface_plasmon.py --args "--steps 12000 --diag_every 1000 --R_cwp 2.4 --wsp 0.705 --w0_R 1.10 --tau_fs 150 --bunch centre --nlines 3 --equal_energy" --out fbpic_sp_comb3_out` (8132 s, ≈ $4) · analysis `analyse_fbpic_sp.py fbpic_sp_comb3_out FBPIC_sp_comb3` · comparison `results/data/FBPIC_sp_comb3_vs_2colour.json`. Lines 0.824 / 1.00 / 1.272 µm (equally spaced by the surface-wave frequency), a0 = 0.24 / 0.29 / 0.37 so that total energy = S045's two colours (a0 0.4 each).
- **Results:** wave speed 0.969 ± 0.009c (matched). Peak fields higher at first (106–115 GV/m vs 80–90) but falling to 30–40 GV/m. Proton energy-modulation amplitude (sinusoid fit, MeV) at 32…388 µm: comb 1.7 3.6 5.1 6.0 6.7 7.2 7.7 8.0 8.3 8.6 8.9 9.2 vs two colours 1.5 3.1 4.6 5.7 6.7 7.6 8.5 9.5 10.4 11.3 12.0 12.7. The comb leads by ~15 % for the first ~100 µm, ties at ~160 µm and then saturates; at 0.39 mm the two-colour drive is 38 % ahead.
- **Conclusion:** as predicted from the guided-mode dispersion (all lines share the single LP01 mode, so a 3-line comb cannot stay rigid; dephasing estimate ≈ 0.23 mm), extra lines help only over the first ~0.1–0.2 mm. In this single-mode hollow channel the two-colour drive is the better choice. A multi-line drive would need lines in different guided modes (as the train uses LG₀,₃,₆), which a channel this narrow (V = 2.4, single-mode) does not support.

### S052 ❌ Consecutive stages: train output bunch → surface plasmon tuned for 1 GeV (FBPIC quasi-3D, Modal GPU) — 2026-11-04
- **Runs:** `modal_fbpic_generic.py --script fbpic_surface_plasmon.py --args "--steps 12000 --diag_every 1000 --T_MeV 1000 --w_ratio 1.79 --R_cwp 2.45 --wsp 0.706 --w0_R 1.085 --tau_fs 150 --bunch centre --bunch_dz_um 15" --bunch sims/phase2/bunch_from_train.npz`. Surface plasmon designed from S049 for 1 GeV: wall 3.5×10²⁰ cm⁻³, R = 0.70 µm, colours 1.00 + 1.65 µm. Incoming bunch = S050's final bunch (ε_n = 1.13×10⁻⁸ m rad), demagnified (emittance-preserving) to σ_r = 0.15R.
  - *First attempt (`fbpic_sp_handoff_out`, 3008 s) invalid — my error:* the mapping kept the train bunch's position–angle correlation (it was expanding) and magnified it 20×, so the protons left at ≈ 0.13 rad. Its field data are still valid (see below).
  - *Corrected (`fbpic_sp_handoff2_out`, 7521 s):* ideal thin lens removes the correlation first (beam brought to a waist). Remaining intrinsic divergence 60 mrad at σ_r = 0.10 µm.
- **Results:** protons leave the 0.70 µm channel within the first ~30 µm (r_rms 2.5 µm at 33 µm, 30 µm at the end; 99.9 % outside R); no energy change (mean +0.001 MeV). Surface plasmon at this design: laser a 0.55 → 0.3 within ~70 µm (strong loss in the dense wall), pulse speed 0.908c (S049 predicted 0.926c; protons 0.875c), no coherent wave (snapshot cross-correlations 0.15–0.41, below the 0.5 acceptance; S045 gave 0.75–0.94).
- **Conclusion:** the train → surface-plasmon hand-off fails at 1 GeV for two reasons: (i) emittance — the channel needs ε_n ≲ 1×10⁻⁹ m rad (10× below the train's output, ~1000× below today's proton beams) unless the plasmon itself focuses strongly; (ii) the 1 GeV surface plasmon needs such a dense wall that the light is lost in < 0.1 mm and no clean wave forms. Consistent with S049: the surface plasmon is a ≳ 3 GeV option, and its acceptance (R ~ 1 µm at 10²⁰ cm⁻³) is the main obstacle to combining it with any upstream stage. Scaling up R means lower density and longer-wavelength lasers, with fields ∝ 1/R.
