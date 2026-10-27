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
