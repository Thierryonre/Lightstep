# Results: energy-efficient laser wakefield acceleration of protons to ~6 GeV

*Status: 2026-10-27. Every number is tagged **[sim]** (simulated in this repository, ID in
`docs/SIMULATION_LOG.md`), **[lit]** (published value, see `docs/research/`) or **[est]**
(our estimate / assumption, not a simulation result).*

> **Revision 2026-11-03 (S031–S041).** Follow-up simulations showed that in a plasma channel the
> laser's energy envelope runs ahead at ≈ c and the protons ride the wave it leaves behind. With
> that physics the best 1D wake→beam efficiency of the guided train so far is **25 %** (not 58.5 %),
> and its long-stage phase stability is not yet solved (S038). Revised wall-plug efficiencies:
> RF injector + guided train **1.5–2.9 %** (protons), **2.5–4.6 %** (deuterons); designs without an
> RF injector **≤ 0.5–1.2 %** (§ 10). Sections 1–8 below keep the original numbers for the record;
> the multipliers vs conventional LWFA fall by ≈ 2.3× (≈ 150× instead of ≈ 340× with the same
> lasers).

## 1. Bottom line

1. **A conventional LWFA cannot accelerate protons from any practical injector** [sim S009,
   S021]. Its wake moves at the laser group velocity, so protons slip out within a few c/ω_p:
   best-phase gain per stage is 0.2 MeV (10 MeV injection), 0.8 MeV (100 MeV) and 8 MeV
   (1 GeV), at every density tested. Laser→proton efficiency per stage is 5×10⁻⁵–4×10⁻⁴
   because protons use only ~10⁻³ of the driver's depletion length.
2. **What works is a wake whose phase velocity is matched to the protons and programmed to
   follow them** (the proton version of the dephasingless flying focus). In 1D kinetic
   simulations a phase-locked, beam-loaded wake takes protons from 30 MeV, 100 MeV, 300 MeV or
   1 GeV to **6 GeV in a single continuous stage**, with **35–53 % wake→beam efficiency** and
   sub-percent energy spread [sim S015, validated by PIC to ≈3 % in S012/S014].
   Joint (differentiable) optimisation of pulse shape and bunch profile raises wake→beam
   efficiency to **60–71 %** at 1–6 GeV [sim S016].
3. **The decisive question is how the slow, moving drive is made optically.** Free-space
   flying foci waste most light (each focal zone used once) and cannot form slow, short drivers
   below β ≈ 0.9; side-pumped/transverse schemes are very inefficient in 3D [lit].
   **Best embodiment found: a guided, resonant flying-focus train** — 3–5 narrow-band laser
   lines spaced by ω_p, each in a different radial mode of a matched plasma channel. Their
   beating forms a rigid train of intensity peaks spaced by one plasma period (resonant
   excitation, Phase 1.3) that travels at a programmable sub-luminal velocity (flying focus,
   Phase 1.1); tapering the channel *width* sweeps the velocity from 0.875c to 0.983c with
   fixed lasers (Phase 2.1). The light stays guided and is reused until absorbed.
   [sim optics S022, S025; 1D PIC with protons S024: 58.5 % wake→beam]
4. **Best design (D2):** RF injector to 1 GeV + three guided resonant-train stages (≈18 cm of
   plasma, 22–51 GV/m) driven by efficient Yb-fibre lasers. **Estimated wall-plug efficiency
   3.3–6.4 %** (today's → projected fibre lasers) [est on sim ratios, incl. a quasi-3D FBPIC
   correction f_3D ≈ 0.62, S029]. That is **≈300× better than a
   conventional staged LWFA with the same lasers and ≈10⁵× better than a Ti:Sa conventional
   LWFA** — but still **below a conventional RF proton accelerator (~10–18 %)** [lit].
5. **For muon-catalysed fusion the accelerator is not the limiting factor.** With demonstrated
   μCF physics (~150 fusions per muon) no accelerator efficiency reaches energy break-even [lit];
   our best LWFA design would return ≈1 % of its wall-plug power as fusion power [est].

## 2. Evidence base and its limits

| Tool | What it simulates | Validation |
|---|---|---|
| 1D cold-fluid quasi-static wake (`fluid1d.py`), JAX version (`jax_wake.py`) | nonlinear wakes for any phase velocity, beam loading | analytic linear theory to 10⁻⁴ (S001); JAX = numpy to 10⁻¹¹ |
| 1D envelope PIC (`pic1d_env.py`) | kinetic plasma, mobile ions, programmed driver trajectories, exact energy budget | fluid (S003), full-EM PIC and gridless sheet model (S006–S008) |
| 1D full-EM PIC (`pic1d_em.py`) | resolved laser, depletion, etching, red-shift | envelope PIC/fluid (S008) |
| Quasi-static proton tracker (`track1d.py`) | 0.03→6 GeV accelerations in seconds | kinetic PIC to ≈3–4 % incl. ion motion (S012, S014) |
| Linear optics of channel modes (`p1e_*`) | rigid-comb flying-focus trains, channel tapers | exact modal dispersion |
| FBPIC quasi-3D (WSL) | multi-D check of the guided train | see §6 |

**Reproductions of published results** [sim vs lit]:

| Paper | Quantity | Published | This work |
|---|---|---|---|
| Palastro et al. PRL 124, 134802 (2020) — flying-focus DLWFA | conventional vs dephasingless energy, 8 cm | 75 MeV vs 1.3 GeV | **75 MeV vs 1.22 GeV** (S028) |
| Hooker et al. J. Phys. B 47, 234003 (2014) — multi-pulse | wake after 120 pulses | 4.7 GV/m (2.5 with mobile H) | **5.01 GV/m** (4.28 mobile H; transverse ion motion not in 1D) (S017) |
| Ross et al. PRR 6, L022001 (2024) — resonance in a channel | resonance density / width | 4.3×10¹⁷ / 0.37 (meas.), 8/(3N)=0.27 (theory) | **4.3×10¹⁷ / 0.21** (S011) |
| Lahaye et al. PRR 8, 023274 (2026) — density up-ramp | energy gain vs flat | +20 % (FBPIC, 0.08 n₀/mm); ×1.4 experiment | **+12.6 % at 0.08 n₀/mm, +14.7 % at 0.04** (1D mechanism; no self-focusing) (S027) |

Main limitations: most plasma physics here is 1D (no diffraction, self-focusing, transverse
beam dynamics or hosing); the laser coupling of each optical embodiment is either computed with
energy accounting (guided train) or taken from the literature (free-space and side-pumped
schemes). These are labelled throughout.

## 3. Conventional LWFA baseline [sim]
(S009, S021, figure `results/figures/summary_gain_per_stage.png`)

| Injection energy | best gain / stage | wake→proton η (best stopping point) | laser→proton η per stage | stages to 6 GeV |
|---|---|---|---|---|
| 10 MeV | 0.18 MeV | — | — | ~33 000 |
| 100 MeV | 0.78 MeV | 0.18 | 4.5×10⁻⁵ | ~7 700–12 000 |
| 1 GeV | 7–8 MeV | 0.36 | 4.3×10⁻⁴ | ~600–1 100 |
| 6 GeV (γ = γ_p) | 0.93 GeV | — | — | — |

## 4. Phase 1 — individual techniques and combinations

| ID | Technique(s) | Key simulated result | Improvement vs conventional |
|---|---|---|---|
| FF | velocity-matched (flying-focus-type) wake, single stage | 0.1→6 GeV (and 0.03, 0.3, 1 GeV starts) with 35–53 % wake→beam (S015) | per-stage gain ×600 (1 GeV start) to ×7 000 (100 MeV start); laser→wake coupling limited by the optical embodiment |
| NP | nanoparticle-like dense H layer, conventional wake | no capture possible (protons from NP are far below γ_p) (S009 logic) | none alone |
| RE | resonant pulse trains (multi-pulse) | trains of ¼-power pulses equal/beat one pulse in the quasi-linear regime: η 0.54 vs 0.52 (100 MeV), 0.55 vs 0.50 with 1.6× field (1 GeV); fail at a0 ≈ 3 (S016); Hooker/Ross reproduced (S011, S017) | enables low-peak-power, high-efficiency lasers; does not solve proton velocity matching alone |
| FF + NP | slow accelerating driver from rest + dense layer | self-injection of background protons; 317 MeV at 28.6 % (no layer) → 321 MeV, 7× charge, 74 % (with layer) laser→proton in 1D (S018) | removes the injector; but the slow-driver optics are ~10⁻³–10⁻⁵ efficient in 3D [lit] |
| FF + RE (+ channel) | guided resonant flying-focus train | rigid trains for ≥ 0.75–1 GeV (S022); 3→3.2 GeV at 58.5 % wake→beam, 18-bunch train 49.9 % (S024) | **best overall**; guided light reused → laser→wake set by depletion (design value 50 %) |
| NP + RE | — | NP gives no velocity matching; same limitation as NP alone | none for protons |
| FF + NP + RE | all-optical: self-injection (FF+NP) to ~1 GeV, then guided train | D3: 0.7 % wall-plug with transverse-flying-focus coupling [est from lit], 0.008 % with transverse pumping | limited by the low-energy optics |
| (dense matched) | laser group velocity matched by density (no flying focus) | wake slows below v_g by etching (S019), but a single guided pulse transfers only ~84 MeV to protons, wake unsteady (S020) | rejected |

## 5. Phase 2 — optimisations

- **Engineered density gradients and guiding.** Lahaye mechanism reproduced in 1D (S027):
  a linear up-ramp raises the dephasing-limited electron energy from 793 MeV (flat) to 909 MeV
  (+15 %, 0.04 n₀/mm) and 892 MeV (+13 %, 0.08 n₀/mm), reached in a shorter distance.
  For protons the useful version is the **channel-width taper** of the guided train: velocity
  0.875c → 0.983c at fixed laser frequencies, coherence ≥ 120 mm, resonance preserved (S025).
  Density changes detune the resonance and are avoided.
- **Joint differentiable optimisation** (JAX + L-BFGS-B, 112 parameters: pulse shape + bunch
  profile + phase, constraints on spread, gradient, wave breaking and a0): wake→beam efficiency
  ×1.41 (1 GeV) and ×2.46 (6 GeV) at equal gradient with the field flattened to ±5 % (S016).

## 6. Multi-D check of the guided resonant train (FBPIC quasi-3D) [sim, partial]
(S029, figure `results/figures/FBPIC_guided_train_partial.png`)
- Three LG modes (p = 0/3/6) at the designed frequencies, injected into a matched channel,
  form the designed rigid-comb train inside the plasma: main peaks every 16.4–16.6 µm (design
  16.62 µm), secondary maxima at the expected 1/3 amplitude, peak a = 0.89 (design 0.9).
- The on-axis wake grows resonantly and matches the 1D wake for the same on-axis drive in shape
  and phase, at **0.79×** the 1D field (**f_3D ≈ 0.62** in energy) — used in the efficiency chain.
- Caveat: the run was stopped by the host (low system memory) after the front half of the train
  had entered the channel; velocity inside the channel, cm-scale guiding of the p = 6 mode, proton
  focusing and long-train ion motion remain to be checked in a full run.

**Kinematic caveat found in the follow-up (S031–S032).** In a channel only the beat pattern moves
at v_a; the light's energy envelope travels at the modes' group velocity (≈ c). Protons therefore
ride the plasma wave *left behind* by the envelope, whose phase velocity is imprinted by the peak
timing. In 1D this works (3000 → 3043 MeV in 600 c/ω_p, same field as the rigid model), but the
pattern velocity must follow the proton velocity *as a function of position*: with a fixed velocity
the protons dephase within ~10³ c/ω_p (S031), while an open-loop static channel-width taper
v_pat(z) = v_proton(z) kept them accelerating at/above the design rate over the 900 c/ω_p
simulated before the host stopped the run (S032). Consequences for D2: (i) the channel taper is
mandatory, not optional; (ii) the imprinted wave must survive the delay between envelope and
protons, ≈ (1/β − 1)·L/c ≈ 5–7 ps for the designed stages — comparable to the measured wake
lifetime in hydrogen/deuterium (≈ 9–16 ps, Jonnerby 2023 [lit]), and channel-induced phase-front
curvature may shorten it; mitigations are longer envelopes (multi-ps trains from thin-disk/fibre
lasers, which also keep the drive near the protons) or shorter stages. This is the main open
physics risk of the recommended design and the purpose of the pending full FBPIC run.

**Follow-up 2 (S036–S037).** Full 3000 c/ω_p runs of the static-taper design gave different
outcomes for identical drives: success in hydrogen plasma (3000 → 3172 MeV, design 3189), but
dephasing in deuterium plasma and with immobile ions. Probable cause: the rigid 3-line comb has
unequal spacings (0.981/1.019 ω_p), so the free wave left behind the c-moving envelope is a sum of
components with slightly different phase velocities. Candidate fix: **two lines spaced by exactly
ω_p** (a beat wave in two channel modes, rigid by construction) — on design over the first
600 c/ω_p before the host stopped the run. Until confirmed, the long-stage stability of the guided
train is an open issue on top of the injector bunch-length problem.

## 7b. Deuterium (S034–S035)
- **Deuterium plasma:** in 1D the wake loss to ion motion in a 120-pulse train drops from 15 %
  (H) to 3 % (D); the measured wake lifetime is ≈ 16 ps in D vs ≈ 9 ps in H [lit]. Recommended
  in all designs; no efficiency cost.
- **Deuteron beams (3.6 GeV, 1.8 GeV/u):** same wake→beam efficiency as protons (33–50 %), plasma
  section 2–3× shorter, but injection must start at 1.5–2 GeV. With literature muon yields,
  wall-plug energy per stopped muon falls from ≈ 104–360 GeV (protons) to ≈ 59–119 GeV
  (deuterons) [est on sim]; RF-only deuterons ≈ 33–40 GeV. Each muon still returns only
  ≈ 2.6 GeV of fusion heat at 150 fusions/μ [lit].

## 7. Rankings

Wall-plug efficiencies from `sims/design/design_calc.py` (S030); multipliers are relative to a
conventional LWFA (group-velocity wake, staged at every proton dephasing, RF injector to the same
energy) using **the same laser technology** unless stated. Figure:
`results/figures/summary_efficiency_ranking.png`.

| Rank | Design | 1. Energy efficiency (wall-plug → 6 GeV) | 2. Acceleration multiplier vs conventional | 3. Ease of construction | 4. Construction cost (1 MW, 6 GeV beam) | 5. Operating power (1 MW beam) | 6. Proton output / muon suitability |
|---|---|---|---|---|---|---|---|
| 1 | **D2 — RF injector (1 GeV) + guided resonant flying-focus train** (FF + RE + channel-width taper + joint optimisation) | **3.3 % (today's fibre) – 6.4 % (projected)** [est on sim]; LWFA section 2.9–5.8 % | per-stage gain ≈ 200× (≈1.7 GeV/stage vs 8 MeV); efficiency ≈ 320–340× (same lasers, whole machine / LWFA section), ≈ 1.4×10⁵× vs Ti:Sa conventional | Hard: HOFI channels ~18 cm with width taper, 3–5 narrow-band fibre lines into radial modes (p ≤ 6), ~10 fs injector–laser synchronisation; HOFI channels and fibre combining are demonstrated, guiding of high-order modes (p ≥ 3) in plasma channels is not | lasers $0.15–0.85 B (projected $20–115/W) or $7–74 B at today's prices; + 1 GeV RF injector $0.3–1 B [est] | 20 MW (projected) / 38 MW (today) [est] | 4×10⁷ p (7 pC)/shot, < 1 % spread [sim 1D]; 1 MW needs 24 MHz × 0.31 J = 7.4 MW of laser (≈10⁴× today's ~1 kW fibre systems); a 1 kW demonstrator needs ~7 kW; beam quality ample for pion targets |
| 2 | D3 — all-optical: slow accelerating driver from rest + nanoparticle-like H layer (self-injection) to 1 GeV, then D2 | 0.68 % (transverse-flying-focus coupling) / 0.008 % (transverse pumping) [est on sim + lit] | no injector needed; 1D: 0 → 317 MeV in one stage (28.6 %), 7× charge with NP layer (74 %) | Very hard: slow, steep drivers need transverse flying focus or ~10³–10⁴ timed beamlets (not demonstrated) | dominated by the inefficient low-energy section: ~10× D2 laser power | ~150 MW [est] | high charge per shot in 1D; 3D charge/efficiency unverified |
| 3 | D1 — free-space (on-axis) flying focus, velocity-matched, RF injector to 1 GeV | 0.14–0.43 % (fibre), 10⁻⁵ (Ti:Sa) [est on sim] | per-stage gain ≈ 600× (single 1 → 6 GeV stage) [sim 1D]; efficiency ≈ 20× (same lasers) | Hard: axiparabola/echelon or chromatic optics, tight foci, limited to β ≳ 0.9; energy ∝ L/Z_R | very high laser power (~95 MW optical, ~$2–11 B at projected $/W) | ~235 MW [est] | as D2 per shot; poor wall-plug |
| 4 | D4 — near-critical RPA + wake / light-spring (single multi-PW laser) | 6×10⁻⁵ (Ti:Sa) [lit, not simulated here]; ~1 % if a 20 %-efficient PW laser existed | multi-GeV in one stage [lit] | Very hard: 5–10 PW, ultra-thin targets, ≲ 1 Hz | multi-PW facility ($0.1–0.5 B) for ≲ 10¹⁰ p/s | n/a at 1 MW | ~10⁹–10¹⁰ p/shot at ≤ 1 Hz → 10⁵× short of a muon factory |
| 5 | D0 — conventional LWFA (baseline) | 2×10⁻⁴ (fibre), 5×10⁻⁷ (Ti:Sa) [sim + est] | 1 (reference): 8 MeV/stage from 1 GeV, ~600–1 100 stages | Impractical (thousands of stages) | — | ~5 GW (fibre) | — |
| ref. | RF proton accelerator (SC linac / RCS) | ~10–18 % [lit] | — | Mature | ~$1–2 B, 300–800 m | ~7–10 MW | 1–2 MW beams exist today |

**Overall:** among LWFA options the guided resonant flying-focus train (D2) is best on every
criterion that matters for a muon source; it is the only one within an order of magnitude of RF
efficiency, and its advantage over conventional LWFA comes from (i) velocity matching (no
dephasing), (ii) guided light reused until absorbed, (iii) resonant drive from narrow-band,
efficient lasers, (iv) beam-loading/pulse-shape optimisation. It does **not** beat RF on
efficiency; its potential advantages are compactness (≈18 cm of plasma vs hundreds of metres)
and, at projected fibre-laser costs, capital cost.

## 8. Recommended design (D2) — summary sheet [est on sim]
- Injector: 1 GeV RF (cyclotron/linac), bunches synchronised to the laser train (~10 fs).
- Three plasma stages, λ = 1 µm fibre lines (N = 3 per stage, radial modes p = 0/P/2P):
  1→2 GeV (n₀ = 3.1×10¹⁸ cm⁻³, W = 6.8 µm), 2→3.5 GeV (1.2×10¹⁸, 11 µm),
  3.5→6 GeV (6×10¹⁷, 12.6 µm); channel width tapered ×1.5–2 inside each stage to keep the
  train velocity on the proton velocity; ≈18 cm of plasma at 22–51 GV/m.
- Per shot: 4×10⁷ protons (7 pC), 0.31 J of laser at the plasma; laser→beam 11 %
  (coupling 0.62 × laser→wake 0.64 × wake→beam 0.585 × f_3D 0.62); joint optimisation can lift
  wake→beam to ≈0.7 (S016).
- Muon production at 1 MW (1×10¹⁵ p/s): 24 MHz, 7.4 MW laser, 20–38 MW wall-plug →
  ≈0.5–0.9×10¹⁵ stopped μ⁻/s [lit yield]; with 150 fusions/μ this is ≈0.3 MW of fusion power,
  ≈1–1.5 % of the wall-plug power: μCF break-even needs far more fusions per muon (≥ 400–1000),
  whatever the accelerator [lit].

## 9. What would change the conclusions / next steps
1. A full FBPIC run of the guided train with protons (≈3 h, ≈2–3 GB RAM; two attempts were
   stopped by the host on low memory) — to measure the imprinted-wave phase velocity and lifetime
   behind the envelope in a real channel, the proton accelerating+focusing phase, and proton
   energy gain; plus the full static-taper 1D run (S032).
2. Experimental guiding of LG_{p≥3} modes in HOFI channels and multi-line fibre drivers.
3. The low-energy section (< 1 GeV) is the efficiency bottleneck of any all-optical design: an
   efficient slow-wave drive would remove the RF injector.
4. Deuteron beams (≈1.6–1.9× more pions per GeV [lit]) would improve the muon cost directly.


## 9b. Full multi-D check of the guided train (S043, FBPIC on a GPU)
- Confirmed: the beat pattern travels at the designed 0.875c in the channel while the energy
  envelope runs at ≈ c; protons have an accelerating-and-focusing region (24–34 % of each period,
  r ≲ 3 µm); on-axis wake = 0.72× the 1D prediction (0.52× in energy).
- **Not viable as first conceived:** the wave left behind the light halves within ~6 plasma periods
  (~350 fs) — 15–20× shorter than a cm-scale stage needs. The drive must stay with the protons:
  a multi-picosecond envelope (duration ≳ (1/β − 1)L/c, e.g. ~10 ps for a 2 cm stage at β = 0.875).
  That is compatible with efficient ps fibre/thin-disk lasers but costs more laser energy per shot;
  the efficiency of that long-envelope regime has not yet been simulated, so the § 7–8 efficiency
  figures for the guided train remain upper estimates.

## 10. Designs without an RF injector (all-optical)

Requested view: only designs in which every stage is laser-driven. Numbers from
`design_calc.revised_designs()` (S041): simulated 1D plasma/beam physics (S018 self-injection,
S038 guided train), literature coupling for the slow low-energy driver, estimated laser and
channel-coupling factors. "PV" = with photovoltaic recovery of leftover light (S039).

| All-optical design | Wall-plug → 6 GeV (today's → projected fibre) | with PV (projected) | Wall-plug GeV per muon (projected) | Share of energy spent below hand-off |
|---|---|---|---|---|
| Self-injection from rest (slow accelerating driver, transverse-flying-focus coupling) **+ nanoparticle-like H layer**, hand-off to guided train at **0.5 GeV** | 0.51 % → 1.01 % | 1.16 % | 660–1 190 | 62 % |
| same, hand-off at 1 GeV | 0.32 % → 0.64 % | 0.74 % | 1 050–1 890 | 78 % |
| same without nanoparticle layer, hand-off 0.5 GeV | 0.25 % → 0.51 % | 0.59 % | 1 320–2 370 | 81 % |
| slow section by transverse pumping (many beamlets), with NP layer, hand-off 0.5 GeV | 0.008 % → 0.016 % | 0.019 % | ~4×10⁴–7×10⁴ | 99 % |
| Near-critical RPA + wake (single multi-PW Ti:Sa laser) [lit, not simulated here] | ~6×10⁻⁵ | — | ~10⁵ | — |
| **Conventional LWFA (baseline)** | **cannot capture protons from rest** (S009: 0.2 MeV per stage even from 10 MeV) | — | — | — |

- **Multiplier vs conventional:** a conventional LWFA has no all-optical route to 6 GeV protons at
  all (its wake cannot trap slow protons), so the all-optical designs are the only options in this
  class; against the conventional LWFA *with* an injector (2×10⁻⁴ with the same fibre lasers) the
  best all-optical design is ≈ 25–50× more efficient.
- **What limits them:** below ~0.5–0.75 GeV no guided embodiment exists (S022), and the
  side-pumped drivers that do work couple ~10⁻³ (transverse flying focus) to ~10⁻⁵ (transverse
  pumping) of the laser energy into protons [lit]. Even though this section adds < 10 % of the final
  energy, it consumes 60–100 % of the wall-plug energy. The nanoparticle layer helps (7× charge,
  2× efficiency of that section in 1D, S018). Surface plasmons (S040) cannot fill this gap (field
  confined to the wall at low β).
- **Advantage:** no RF machine (hundreds of metres) and no femtosecond bunch-compression problem —
  self-captured protons are born short and phase-locked to the driver.

## 11. Additional ideas evaluated (2026-11-03)
- **Laser-beat-driven surface plasmons in a hollow channel** (Lei et al., PRL 137, 105002 (2026),
  electron simulations, 10 MeV in 40 µm): our dispersion analysis (S040) shows slow, proton-matched
  surface modes exist only in tubes ≳ 3 c/ω_p, with a usable on-axis field only for protons above
  ~1 GeV (0.75–0.94 of the wall field) and ≤ 5×10⁻⁶ at 100 MeV. A possible alternative high-energy
  structure; does not solve the slow section. Amplitudes/efficiency need PIC.
  *First quasi-3D PIC test at 3 GeV (S044, FBPIC on GPU) [sim]:* the two-colour beat is guided and
  gives ~17 GV/m on axis (~0.02 of the wall wave-breaking field), moving at 0.979c (0.971c needed;
  0.980c predicted by guided-mode theory — an earlier version of this note wrongly said 1.05–1.1c).
  The wave did not persist behind the laser, and test protons placed there gained no energy. It does
  not yet beat the guided train; follow-up (S045) puts the protons inside the beat with the speed
  retuned by a smaller channel radius.
- **Monochromatic photovoltaic recovery** (68.9 % GaAs at ~0.85 µm; 55–59 % demonstrated at
  ~1.07 µm, the relevant wavelength here): light that drove the wake is spread out of the cell band
  (S039), so recovery works mainly on light that never interacted. Gain ≤ 1/(1 − η_laser η_PV f):
  ×1.04–1.09 for the guided train, ×1.08–1.18 for free-space/side-pumped schemes; ≤ ×1.5 even with
  ideal cells. Included in § 10.

## 12. Optical-only accelerator — plain-language summary

*This section restates the all-optical (no RF accelerator) design in simple terms. It changes no
numbers above. Labels: **[simulated]** = we ran a simulation; **[estimate]** = calculation or
assumption; **[literature]** = published value.*

### What it is
A machine that takes protons from **rest** to **6 GeV** using only lasers and plasma — no
conventional (RF) accelerator at all.

### How it works, step by step
1. **Catch protons from rest (0 → ~0.5 GeV).** A laser focus is made to sweep sideways across a
   thin gas jet, starting slowly and speeding up (a *transverse flying focus*). Its light pressure
   pushes electrons aside, and the resulting electric field drags nearby protons along with it.
   A tiny hydrogen-rich layer (standing in for nanoparticles) supplies extra protons to catch.
2. **Hand over to a guided plasma accelerator (0.5 → 6 GeV).** Two or three fibre-laser beams of
   slightly different colours are sent down a plasma "fibre" (channel). Where they overlap they
   beat into a train of bright pulses spaced exactly one plasma wave apart, which builds a strong
   plasma wave. By choosing which channel mode each colour uses, and by slowly widening the channel,
   the pulse train is made to travel at the protons' speed (slower than light), so the protons
   never fall out of step.

### Numbers
| | Value | Basis |
|---|---|---|
| Protons caught from rest in step 1 (1D) | to 321 MeV, 74 % of the driver's energy into protons | [simulated, 1D] |
| Same, real optics (transverse flying focus) | ~0.3 % laser → protons | [estimate from literature: Gong et al. 2024 got 0.13 % in 3D] |
| Step 2 speed matching | peak train moves at the designed 0.875c in a 3D simulation | [simulated, quasi-3D] |
| Step 2 field strength | ~0.4 of the plasma's natural limit (≈ 60 GV/m at the design density) | [simulated, quasi-3D] |
| Step 2 protons focused as well as accelerated | yes, in ~¼ of each plasma wave | [simulated, quasi-3D] |
| **Overall wall-plug efficiency** | **≈ 0.5 % (today's fibre lasers) to ≈ 1 % (projected); ≈ 1.2 % with solar-cell-style light recovery** | [estimate, chain of simulated + literature factors] |
| Conventional laser accelerator, same job | **cannot do it** — it cannot catch protons from rest | [simulated, 1D] |
| Conventional RF accelerator, for comparison | ≈ 15 % | [literature] |

### Where 100 J of electricity goes (projected fibre lasers)
| Destination | Step 1 (catching, ~62 J) | Step 2 (guided, ~38 J) |
|---|---|---|
| Lost inside the lasers | ~37 J | ~23 J |
| Light that never enters/couples into the plasma | most of the remaining ~25 J (passes through the sweeping focus) | ~6 J |
| Light that crosses the plasma unabsorbed | — | ~3 J |
| Left in the plasma (heat, unused wave) | — | ~5 J |
| **Ends up in the protons** | **~0.08 J** | **~0.9 J** |
| **Total in protons** | **≈ 1 J out of 100 J (≈ 1 %)** | |

Step 1 adds less than 10 % of the protons' final energy but uses most of the electricity — it is
the weak link.

### What is proven and what is not
- **Proven by simulation:** protons can be caught from rest by a speeding-up focus (1D); a laser
  pulse train can be made to travel slower than light inside a plasma channel and drive a wave
  that both accelerates and focuses protons (quasi-3D); the pulse train needs only two or three
  narrow-band fibre lasers.
- **Not yet proven:** that real optics can make the speeding-up focus efficiently (efficiency is
  borrowed from another group's 3D result); that the guided stage works over centimetres — the 3D
  run showed the plasma wave fades within ~6 waves once the light has passed, so the laser pulses
  must be several picoseconds long to stay with the protons, and that version has not been simulated.
- **Advantages over the RF-injector version:** no large RF machine, and no need to compress proton
  bunches to femtoseconds (protons caught in step 1 are automatically short and in step).
- **Bottom line:** ~0.5–1 % efficient on current evidence — far better than a conventional laser
  accelerator (which cannot do this at all), but well below RF accelerators (~15 %).

## 13. "Electric flying focus" — proposals only (not simulated)
From the literature review in `docs/research/electric-field-tailoring.md` (prompted by
Mach-Batlle et al., PRL 125, 177204 (2020)). **Nothing in this section has been simulated yet.**
- **Key physics [inference, checked against a published design]:** a field pattern moving with
  the proton is electrostatic in the proton's frame, so it cannot be "projected" into empty space:
  it decays away from the structure over βγλ/2π, and a single structure cannot both accelerate and
  focus in 3D without time-alternation (alternating-phase focusing). Hence a "wavelength ladder":
  the driver wavelength must grow as protons get slower (RF below ~3 MeV; mm-wave/THz/pulsed walls
  ~3–100 MeV; mid-IR near fields above ~0.1–0.2 GeV; dielectric-laser or plasma above ~1 GeV).
- **Programmable speed is real:** set by the firing times of the surrounding sources (precedents:
  LLNL dielectric-wall accelerator, travelling-wave Stark decelerators, pulse-front-tilted
  dielectric laser accelerators).
- **Proposed concepts (estimates, not results):** C1 laser-switched dielectric-wall accelerator
  (2–200 MeV, ~20–50 MV/m); C2 timed THz-emitter array (1–100 MeV); C3 inverse-designed
  alternating-phase-focusing proton dielectric laser accelerator with tilted pulse fronts
  (0.2–3 GeV, ~0.2–1 GV/m); C4 hollow plasma channel with a chirped laser-imprinted grating
  (0.3–6 GeV, unverified 3–20 GV/m); C5 hybrid ladder of the above.
- **Assessment:** below ~100 MeV none is expected to beat RF quadrupole/drift-tube linacs on
  efficiency; the concept is most promising as a programmable-speed booster at β ≈ 0.5–0.95 — the
  same range where the laser-plasma options here are weakest.
- **Proposed first simulations:** (0) a laptop model of required wall field per unit gradient
  vs speed, wavelength and aperture; (1) 2D adjoint inverse design + FDTD + proton tracking of
  concept C3 (~2–24 CPU-h, plus ~$5–30 of GPU for a 3D check).
