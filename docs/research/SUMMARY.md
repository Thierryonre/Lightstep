# Literature synthesis — what the papers imply for a 6 GeV proton LWFA

Condensed from the five topic notes in this folder (each statement there is labelled
[paper]/[abstract only]/[inference]). Numbers here are **literature values**, not our simulations.

## 1. The core obstacle: protons are slow, wakes are fast
- A conventional LWFA wake moves at the laser group velocity, γ_p = ω/ω_p ≈ 10–50. Trapping a
  proton from rest needs a wake potential ≈ (1 − 1/γ_p) m_pc²/e ≈ 1 GV, whereas laser wakes have
  potentials of order m_ec²/e × a few (MV). Protons must therefore be injected with γ ≈ γ_p or the
  wake must be slowed. [proton-wakefield notes, S1–S6]
- Positive particles are *defocused* by the ion cavity of a blowout wake; they need quasi-linear
  wakes (a focusing + accelerating quarter period exists), hollow channels or donut drivers.
- Multi-GeV proton results in the literature are simulation-only and use ultra-intense
  (10²¹–10²³ W/cm², multi-PW) single lasers: RPA + near-critical wake (Liu 2018: ~2 GeV, 6 %;
  Shen 2009: 38 GeV at 18 kJ), "light-spring" twisted pulses (Guo 2024: 8.7 GeV, 11 %).
  The only experimental proton-in-wake evidence is ~60 MeV (Isayama 2026, near-critical foam).

## 2. Phase-velocity control (Phase 1.1 and relatives)
- **Flying focus (on-axis)**: dephasingless electron LWFA demonstrated experimentally (Nature
  Physics, 10 Jul 2026; Weizmann arXiv:2604.05771). Palastro 2020 linear example: 1.3 GeV vs
  75 MeV conventional — but laser energy ∝ L/Z_R (each focal zone used once); efficiency ~5 % of
  conventional in that example; LLE bubble design 6.2 J → 2.1 GeV, 0.7 % laser→beam.
- **Slow on-axis flying focus fails for ions** (Gong et al. PRL 2024): for v_f ≪ c the drive at
  a point lasts ~Z_R(1−β)/(βc), so longitudinal gradients are weak. Their *transverse* flying
  focus reaches 1.64 GeV protons from rest (3D PIC) with 0.8 kJ, 0.13 % laser→protons.
- **Flying focus in a plasma waveguide** (Palastro 2025/2026): guided multimode pulses with
  arbitrary peak velocity; luminal case uses the same laser energy per GeV as standard LWFA.
  Slow peaks need many modes/bandwidth (τ_eff ∝ |(v_a − v_g)/v_a|).
- **TWEAC** (Debus 2019): side-coupled tilted pulse fronts, overlap velocity set by geometry
  (any v < c allowed: tan α = (1 − β cos φ)/(β sin φ)); 3D PIC laser→electron efficiency 27.6 %
  (φ = 5°), 46.8 % (3.5°), but 0.18 % at 60°. Not applied to ions in the literature.
- **Transverse pumping** (Nutting, Nat. Commun. 2026): thousands of timed beamlets give an
  arbitrary, accelerating, sub-luminal wake from many low-energy lasers; 2D OSIRIS: protons
  95 MeV → 1.12 GeV in 3.6 mm, but laser→proton ≈ 10⁻⁵.

## 3. Resonant / multi-pulse excitation (Phase 1.3)
- Hooker 2014: 120 × 10 mJ pulses, a0 = 0.052 → 4.7 GV/m (linear growth); ion motion in hydrogen
  roughly halves it (2.5 GV/m); spacing tolerance ~1/(2(N−1)).
- Ross 2024 (PRR 6, L022001): ~10-pulse train guided 110 mm in a HOFI channel, resonance at
  4.3×10¹⁷ cm⁻³, width 8/(3N), 64 % coupling (best shots).
- P-MoPA (Jakobsson 2021, van de Wetering 2023/24): ps thin-disk pulse modulated into a train,
  2.4 J → 1.5 GeV electrons (16–19 % laser→plasma) in simulation; relativistic detuning small
  below ~30 pulses. Enables efficient long-pulse lasers.

## 4. Nanoparticles (Phase 1.2)
- No paper matches the exact phrase. Closest title: Vallières et al. PRAB 22, 091303 (2019):
  10 nm Au/Ag particles on foils, ≈ 2× TNSA energy and yield (sheath acceleration, no wake).
- Nanoparticle-triggered *electron* injection into LWFA: Aniculaesei 2019/2024 (10 GeV, 340 pC),
  Xu 2022 (>90 % injection). Hydrogen-cluster / CH-nanoparticle proton sources: ~300–450 MeV
  in simulation with intense lasers (Matsui 2019, Nishihara 2016).

## 5. Phase 2 papers
- Lahaye et al. PRR 8, 023274 (2026): linear density up-ramp + HOFI channel, 1.1 → 1.6 GeV
  electrons (×1.4); mechanism = delayed injection + reduced dephasing + self-focusing.
- "Differentiable 500-parameter optimisation" (DOI 10.1103/bpms-63ml) is Crilly et al. PRR 8,
  033353 (2026): ICF pulse shaping with a JAX 1D hydro code + L-BFGS-B — method transferable,
  code not public.

## 6. Laser technology and cost
| Driver | Wall-plug | Notes |
|---|---|---|
| Ti:Sa | ≲ 0.1 % | ~$33k–250k per W average (facility level) |
| Coherently combined Yb fibre | ~25 % today (ultrafast), 30–50 % projected | 10–32 mJ demonstrated; $20–115/W projected for collider scale |
| Tm:YLF (BAT) | 20 % projected | 1.6 J / 270 fs demonstrated |
| Thin-disk Yb | > 50 % optical-to-optical | ~1 J, kHz, but ps pulses (needs modulation/trains) |
- The "80 % efficiency" palm-sized laser (Nägele, Nature 2025) is 81 % internal photon
  conversion of a multipass OPA at 40 nJ/76 MHz — not a wall-plug figure, not J-class.

## 7. Muon production and μCF energetics
- π⁻ yield per unit beam power is flat from ~2 to 11 GeV (≈ 0.018 π⁻/GeV/proton on graphite);
  estimate 0.5–0.9 stopped μ⁻ per 6 GeV proton in an optimised thick target; deuterons are
  ~1.6–1.9× better per GeV. Energy cost per μ⁻: 5–6 GeV classic, 3–4.7 GeV best claims.
- Record 150 ± 20 fusions per muon; alpha sticking caps it at ~180–330. Electrical break-even
  needs ≳ 400–1000 fusions/μ even with a perfect accelerator → **no accelerator efficiency alone
  closes the μCF energy balance with demonstrated physics.**
- Benchmarks: PSI cyclotron 18 % (accelerator-only), SNS ~9 %, J-PARC ~3 % wall-plug → a 6 GeV
  LWFA would need ≳ 10 % wall-plug to be competitive on efficiency.
