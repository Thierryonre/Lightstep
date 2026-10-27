# Muon production and muon-catalysed fusion (μCF): energy-budget literature notes

Compiled 2026-10-27 for the MCF project (6 GeV proton LWFA -> pions -> muons -> dt μCF).

Labels: [paper] = full text read; [abstract only] = only abstract/summary seen; [report] = technical/lab report read;
[inference] = my own derivation or background knowledge not verified against the cited text in this session.

Status: notes are appended source-by-source as the search proceeds (topics 1-6), with the summary table and LWFA
requirements at the end.

---

## 0. Background framing (to be checked against sources) [inference]

- dt fusion releases 17.6 MeV (3.5 MeV alpha + 14.1 MeV neutron).
- Classic accounting: energy cost per negative muon E_μ (beam energy at wall-plug inverted by efficiencies), number of
  fusions per muon X_c (limited by alpha sticking ω_s and cycle rate vs muon lifetime 2.197 μs).
- Scientific break-even: X_c * 17.6 MeV >= E_μ (beam energy deposited per muon).
- Engineering break-even: X_c * 17.6 MeV * η_th(*blanket gain) * η_acc >= E_μ(beam) i.e. η_wallplug * η_thermal * Q >= 1.
- Frequently quoted numbers (to verify below): best-case beam cost ~5 GeV per μ- (Petitjean/Jändel), X_c ~ 100-150
  achieved (LAMPF/PSI/RAL), ω_s ~ 0.4-0.9 % effective, theoretical ceiling X_c ~ 1/ω_s ~ 200-300.

---

## Sources (appended as read)

### S1. Kelly, Hart & Rose (2021), "An investigation of efficient muon production for use in muon catalyzed fusion" [paper]
- J. Phys.: Energy 3, 035003 (2021). DOI 10.1088/2515-7655/abfb4b (open access; read via IOP HTML). Imperial College.
- Topics 1, 2. Geant4-type simulation (5000 beam particles) of d/t beams on long thin targets inside LiPb breeding shell.
- Literature muon cost quoted: ~5-6 GeV per μ- (their ref. 6, Petitjean et al.).
- Optimum found: **deuteron beam 3.61 GeV total (~1.8 GeV/u) on tungsten rod 652 mm long x 5.1 mm diameter**
  -> **0.77 (π-/μ-) per deuteron** -> **3.61/0.77 = 4.70 GeV per muon** (beam energy only, before accelerator efficiency).
- Energy ledger per beam deuteron (MeV): fusion from muons (150 f/μ) 2991; recoverable secondaries (p,n,d KE etc.) 2664
  (42 particles); π+ 23; heat in target 526; tritons bred in shell 110 per deuteron (530 MeV); subtotal 6734 vs beam 3606.
- Q-dependence on beam energy: Q rises steeply up to ~2 GeV (total d energy) and is flat to ~5 GeV. Tritons only marginally
  better than deuterons.
- Physics inputs: τ_μ = 2.2 μs; ω_s ≈ 0.47 %; t_c/τ ≈ 0.18 % at LHD -> X_c ≈ 1/(ω_s + t_c/τ) ≈ 154. Heat per fusion 26 MeV
  (17.6 + 8.4 MeV from 1.75 Li breeding reactions per neutron).
- Gains: Q(total heat incl. recovery)/beam = 1.87; fusion-only Q = 0.83 at 150 f/μ.
- Efficiencies assumed: η_acc = 18 % (PSI 590 MeV HIPA wall-plug), η_heat->elec > 60 %, muon delivery η_μ = 50 %.
  Q_elec = 0.108 x (F/2 + H)/B -> **Q_elec ≈ 14 %** at 150 f/μ (my recomputation from their table gives ~15.7 %).
  Claimed factor ~2.5 improvement over earlier muon-cost estimates via energy recovery + breeding.
- [inference] Electrical break-even would need ~7x improvement in (η_acc x X_c x energy recovery) relative to this case;
  with η_acc -> 50 % and X_c -> 300 one gets roughly Q_elec ≈ 0.14 x (0.5/0.18) x ~1.8 ≈ 0.7.

### S2. Yin, Kou & Chen (2026), "Muon-Catalyzed Nuclear Fusion: Physical Mechanism, Bottleneck Breakthroughs, and an Engineering Pathway" [paper, HTML skim]
- arXiv:2605.26432 [hep-ph], v1 26 May 2026. IMP-CAS Lanzhou + Shenzhen Haihean Science Research Co.
- Topic 2 (and 1 marginally). Uses <E_μ> ≈ 5 GeV per μ- "average effective cost at PSI / J-PARC MUSE pion beamlines,
  including pion production, transport, decay and collection" (sourced only to their own manuscript in preparation - weak).
- Q = X_μ x 17.6 MeV / 5 GeV -> **Q = 1 needs X_μ ≈ 284 dt fusions per muon** (scientific, beam-energy accounting).
- Their scenario table (projections, NOT measured): unpolarised X_μ 148 (ω_s 0.45 %, λ_c 2.0e8 /s) Q≈0.53;
  polarised conservative 193 (ω_s 0.342 %) Q 0.68; polarised optimistic 292 (ω_s 0.315 %) Q 1.03; "multi-technology"
  300-350 (ω_s 0.18-0.20 %); "engineering limit" 500-600 (ω_s 0.08-0.10 %); "ultimate" 873 (ω_s 0.06 %, Q≈3.07).
- Rates: λ_0 = 4.55e5 /s; resonant dtμ formation at 800 K ~1-1.5e10 /s (claim); λ_c 2-5.5e8 /s.
- Mentions planned CiADS/HIAF "EMuS" (Huizhou) muon source: >= 1e8 μ-/s after 2028 (with polarised target studies).
- No accelerator-efficiency or wall-plug analysis. Treat scenario numbers as speculative.

### S3. Kou & Chen (2026), "A Lawson-inspired Cycle-Closure Criterion for D-T Muon-Catalyzed Fusion" [abstract only]
- arXiv:2607.10989 [nucl-th], 13 Jul 2026, 7 pp.
- Useful implementable formulae (topic 2):
  - Cycle strength L_μ = Λ_c τ_μ (Λ_c = effective cycling rate, normalised to LHD density φ as needed).
  - Fusions per useful muon N_fus = L_μ / (1 + ω_s^eff L_μ)  (equivalently 1/X_c = 1/(Λ_c τ) + ω_s^eff).
  - One-muon gain G_μ = η_sys E_use N_fus / E_μ^cost ; N_L ≡ E_μ^cost/(η_sys E_use).
  - Required L_μ^req = G N_L / (1 - ω_s^eff G N_L); sticking boundary ω_s^eff < 1/(G N_L).
- [inference] With E_μ^cost = 5 GeV, E_use = 17.6 MeV, η_sys = 1: N_L = 284; any ω_s^eff >= 0.35 % makes G=1 impossible
  regardless of cycling rate. With η_sys = 0.4 (thermal->elec) and E_μ^cost at wall-plug = 5 GeV/η_acc(0.5) = 10 GeV:
  N_L = 1420, needs ω_s^eff < 0.07 %. This is the core "engineering break-even" obstacle.

### S4. Parisi & Rutkowski (2025), "Isotope Production in Muon-Catalyzed-Fusion Systems" [abstract only]
- arXiv:2511.20951 (physics.plasm-ph / acc-ph), v2 25 Dec 2025. (J.F. Parisi - Marathon Fusion / ex-PPPL [inference].)
- Topic 3/6: non-electric μCF market. Example: 1e12 μ-/s steady, ~0.5 kW fusion power, 10 g Ra-226 feed -> 20 mg Ac-225/yr
  (~400x 2024 world supply). Requirements on X_c and muon cost relaxed "by several orders of magnitude" vs power.
- [inference] 1e12 μ/s x 150 fusions x 17.6 MeV = 0.42 kW, consistent. 1e12 μ/s at 5 GeV/μ needs ~0.8 MW beam power.

### S5. Europhysics News 20(5) (1989), μCF review article, p.63 (last page only) [paper, partial - 1 page]
- URL: https://www.europhysicsnews.org/articles/epn/pdf/1989/05/epn19892005p63.pdf (WebFetch 403; curl worked).
  Author not on the retrieved page (article begins on earlier page).
- Scientific break-even: E_μ < E_out = Y x 17.6 MeV (Y = fusion neutrons per muon).
- "current estimation is some **5 GeV in beam power per muon**, although the **theoretical limit is below 2 GeV**. Present
  muon factories are far from the optimal efficiency."
- LAMPF: **150 fusions/muon**, "energy liberation just short of 3 GeV/muon"; indications ~300 f/μ might be possible.
- Effective sticking 0.3-0.5 % at 1.2 LHD (measured indirectly); theoretical **initial sticking ω_s0 = 0.886 %**.
- Pure fusion design "not possible today"; fusion-fission hybrids with spallation breeder need only ~100 f/μ and work even at
  5 GeV/μ. "Synergetic" systems: D/T mixture is both pion-production target and μCF fuel (no intermediate beams).

### S6. Eliezer & Henis (1994), "Muon-catalyzed fusion: an energy production perspective" [abstract only]
- Fusion Technology 26(1) (Aug 1994); OSTI ID 105359 (https://www.osti.gov/biblio/105359). Soreq NRC. 95 refs.
- Muon cost with current technology **~5000 MeV per μ**; 17.6 MeV per dt fusion.
- **X_μ ≈ 250 = "significant demonstration of scientific breakeven"**; practical power needs **X_μ ~ 1e4 with standard
  technology, ~1e3 with advanced physics/technology** (i.e. includes accelerator and thermal conversion efficiencies).
- Needs D-T near liquid density and ~1000 K for practical power. Conclusion: muon production energy cost must fall
  substantially before reactors are seriously considered.
- [inference] X=1e4 implies they assumed effective overall conversion factor ~ 5 GeV/(1e4 x 17.6 MeV) ≈ 3 % (e.g.
  η_acc ~ 0.1, η_th ~ 0.35, plus recirculating-power margin ~ 1/0.8 → Q_eng ≈ 1).

### S7. Jändel, Danos & Rafelski (1988), "Active target production of muons for muon-catalyzed fusion" [abstract only]
- Phys. Rev. C 37, 403-406 (1988). DOI 10.1103/PhysRevC.37.403. (Abstract via U. Arizona experts page.)
- Monte Carlo of high-energy deuteron beam into an *infinite* D-T target ("active target": fuel = pion-production target);
  energy efficiency of muon production vs target density and beam energy; **secondary (shower) muon production plays a key
  role**; derives constraints on μCF power-reactor feasibility. Numbers not in abstract.
- Related: M. Jändel, CERN-TH-4810/87 (1987) - per F. Ignatov's 2025 slide (S10): "theoretical lowest cost 5 GeV/muon ...
  needs 300 fusion/muon assuming 100% power-conversion efficiency"; another Jändel scenario "needs >700 fusion/muon but
  requires low density". [abstract-level / secondary citation]

### S8. Newburg (Acceleron Fusion / NK Labs), "Developing muon-catalyzed fusion as an abundant new source of energy" [report - slides]
- ARPA-E Fusion Programs Annual Meeting, 8-9 Jul 2025. https://arpa-e.energy.gov/sites/default/files/2025-08/Day2_09_Newburg.pdf
- Topic 3. ARPA-E awards: DE-AR0001798? / 2020 OPEN-type award **$2.28 M "Conditions for High-Yield Muon Catalyzed Fusion"**
  (NK Labs; sites NK Labs Cambridge MA, CUNY, LLE Rochester, Fermilab); Sep-2023 ARPA-E CREATE **$0.5 M "Active-target Muon
  Source"** (ML/Bayesian-optimised GEANT4 target design "to further reduce beam energy per muon").
- **Acceleron's target energy ledger per muon** (slide 5, "Our core innovation"):
  - Accelerator + muon production target: **3 GeV per muon** (GEANT4 active-target simulation currently gives
    **3.0 GeV beam energy per negative pion + muon exiting the target**; "design can likely be improved").
  - Sticking-imposed limit **300 fusions/muon x 25 MeV (fusion + breeding blanket) = 7.5 GeV** heat per muon,
    plus **2.5 GeV heat recycled** from the target/beam dump -> 10 GeV heat.
  - **64 %-efficient balance of plant** (Brayton cycle) -> 6.4 GeV electric; 3 GeV recirculated to accelerator ->
    3.4 GeV net; **47 % recirculating power fraction**.
  - [inference] The ledger only closes if the 3 GeV per muon is essentially the *wall-plug* energy, i.e. it implicitly
    assumes a very high-efficiency superconducting accelerator (slide 21: "using a superconducting accelerator, Brayton
    cycle balance of plant, and revenue from heat sales"), with most accelerator losses + beam energy recovered as heat.
- Target LCOE ~ $0.025/kWh (aspirational); "Energy breakeven test at Brookhaven in five years" (i.e. ~2030).
- Experimental: diamond-anvil-cell (DAC) DT target at PSI piE1; liquid DT compressed to solid then heated; preliminary DT
  cycling-rate data to **2.2 LHD** (Oct 2024, 60/40 DT, 50 K solid). Mechanism slide: ~1 % sticking per fusion.

### S9. Knaian for MuFusE collaboration, "Status of muon-catalyzed fusion experiments at PSI" [report - slides]
- Int. Conf. on μCF and Future Applications, Liverpool, 2-3 Jul 2026.
  https://indico.ph.liv.ac.uk/event/2421/contributions/10930/attachments/5293/7469/ (pptx.pdf)
- MuFusE @ PSI piE1 (HIPA). Goal: DT cycling rate and sticking at high density/temperature; open-source GEANT4 μCF models.
- **First tritium operation in DAC Oct 2024; world-record static DT pressure 990 MPa (~3x previous); first μCF data at
  > 1.45 LHD**; densities up to 2.2 LHD. 2025: 3 DD + 2 DT compressions; DD neutrons > 5σ; DT cycling observed, "50 %
  tritium compression exhibits fastest absolute cycling rate observed in an equilibrated isotopologue mixture" (preliminary,
  no numbers shown). Losses still being analysed (wall losses of μα, hot muonic atoms, He-3, impurities).
- Cites Nagamine (2008) compilation: measured sticking at high density is lower than theory -> sticking limit X ~ 170-330
  plotted vs density. Related arXiv: 2606.19304 (DT gas system, Koukina...Antognini...Knaian, Jun 2026) and 2606.05333
  (MuFusE large-volume DAC: up to 1 GPa, > 400 K).

### S10. Ignatov (Liverpool), "Muon Catalyzed Fusion" overview talk, 9 Jun 2025 [report - slides]
- https://indico.ph.liv.ac.uk/event/2009/contributions/9639/attachments/4465/6245/mucf.pdf
- Cycle rate ~ few 1e8 /s at LHD vs λ_0 = 0.45e6 /s; sticking loss ~0.5 %; **100-200 dt fusions/muon** typical.
- Stripping/reactivation R ~ 0.35 at high density.
- Quotes Iiyoshi (AIP Conf. Proc. 2179, 020010, 2019) in-flight μCF concept: 1e16 μ/s x 1000 fusions -> 28 MW fusion,
  8.5 MW electricity; "most μCF papers cite theoretical lowest cost 5 GeV/muon -> 8 MW beam for 1e16 μ/s; with 100 %
  power conversion needs 300 fusion/muon" (Jändel CERN-TH-4810/87).
- Present muon sources: Mu2e/COMET ~1e11 μ/s (-> 17 MeV x 100 x 1e11 = 30 W fusion); future muon collider ~1e13 μ/s
  (3 kW fusion) at price of ~10 MW proton driver (another x10 for wall-plug). "1-10 MW proton driver -> 1e12-1e13 μ/s"
  (Stratakis, Muons4Future 2025). Conclusion: **μCF needs a 3-4 orders of magnitude more intense and 3-4 orders cheaper
  muon source** than particle-physics designs (which optimise muon *collection in a beam*, not total stopped μ- per GeV).
- [inference] Important distinction: particle-physics muon yields (1e-3 - 1e-2 captured μ per proton in a beamline) are NOT
  the relevant metric; μCF needs nearly all π- produced to decay and the μ- to stop in fuel (active-target/solenoid capture),
  giving ~0.2-0.8 μ- per GeV-scale nucleon.

### S11. Strait, Mokhov & Striganov (2010), "Towards the optimal energy of the proton driver for a neutrino factory and muon collider" [paper]
- Phys. Rev. ST Accel. Beams 13, 111001 (2010). DOI 10.1103/PhysRevSTAB.13.111001; arXiv:1011.2537. Fermilab.
- Topic 1 (energy dependence, per unit beam power). HARP thin-target Ta π± double-differential data (3-12 GeV/c),
  folded with MARS15 NF/MC front-end acceptance (20 T target solenoid, r = 7.5 cm, p_T < 225 MeV/c, captured μ with
  40 < T < 180 MeV at 50 m), corrected for unmeasured θ < 350 mrad and thick-target (2 λ_I) showering.
- **Result: captured-muon yield at constant beam power peaks at T_p ≈ 7 GeV; within 10 % of max for 4-11 GeV; still
  85 % of optimum at 2 GeV.** Uncorrected (thin target): max at 4.1 GeV; π- yield per GeV max at 2.2 GeV and ~equal at
  4.1 GeV, down 12-20 % at 7.1 GeV (π- favours lower energy than π+).
- Table II (MARS15, Ta, ~1 cm diam; reading of garbled PDF table, columns T, Y_P(0.05 λ), Y_P(2 λ), R_t, R_t/R_t(4.1)):
  2.2 GeV: 0.057, 0.050, 0.874, 0.908 | 4.1: 0.056, 0.054, 0.963, 1.000 | 7.1: 0.053, 0.057, 1.079, 1.122 |
  11.1: 0.042, 0.050, 1.186, 1.233.  Y_P = captured μ (μ+ + μ-) per interacting proton per GeV of beam KE
  (normalisation as I read it - verify against original). Thick-target shower amplification grows with energy
  (~+12 % at 7 GeV, +23 % at 11 GeV relative to 4 GeV).
- [inference] For our purpose: ~0.055 captured μ± per proton-GeV in a *narrow-acceptance* beamline means ~18 GeV per
  captured μ± (~35-40 GeV per captured μ-). μCF designs that stop *all* π-/μ- inside a solenoid-confined fuel/active
  target do ~10x better (3-5 GeV per μ-). The energy-dependence conclusion (flat 4-11 GeV per unit beam power, high-Z
  optimum ~5-8 GeV) carries over: **6 GeV protons sit at/near the optimum per unit beam power for heavy targets**; for
  low-Z (C, Be) targets the optimum shifts down to ~3 GeV (Breton/Le Couedic/Soler, NuFact10, GEANT4 corrected to HARP).

### S4b. Parisi & Rutkowski (2025) - full text skim (update to S4) [paper, HTML skim]
- arXiv:2511.20951v2 (Marathon Fusion, San Francisco). Muon-source facts quoted: J-PARC MUSE ~2-4e7 μ-/s (25 Hz);
  PSI ~2e7 μ-/s CW; MuSIC (Osaka) ~4e7 μ-/s; PSI/J-PARC upgrades > 1e8 μ-/s.
- E_μ: "~5 GeV/muon" (Jändel), "3.0 GeV per negative muon" active-target modelling (Newburg/Acceleron, ARPA-E 2025, not
  demonstrated); their Fig. 2 assumes E_μ = 3 GeV.
- Energy per dt cycle incl. blanket: E_comb ≈ 20.4 MeV (Sawan & Abdou) -> ~3.1 GeV per muon at 150 f/μ; blanket
  multiplication M ≈ 1-1.2; f_n = 4/5, f_α = 1/5.
- X_c formulas: N = 1/(t_c/τ + p); N = φλ_c/(λ_0 + ω_s φ λ_c). Experiments: N ≈ 150 ↔ t_c ≈ 4 ns; p ≈ 0.5 %.
- **Electricity break-even (their Eq. 26):** N_fus ≥ (E_μ/E_fus) · 1/(η·K) · (1+ξ_circ) · (1 - η·η_μ),
  η = 0.4 thermal->electric, η_μ = 0.8 (fraction of beam power recovered as useful heat->electricity), K = 1.1 blanket,
  ξ_circ = 0.1 auxiliary recirculating fraction. Quoted result **N_fus ≳ 415** (consistent with E_μ = 5 GeV,
  E_fus = 20.4 MeV by my check [inference]; with E_μ = 3 GeV it would be ~250).
  NB: E_μ here is treated as electrical energy per muon (no separate η_acc) - i.e. it implicitly assumes η_acc ~ 1 or that
  E_μ is already a wall-plug number. [inference]
- Isotope (Ac-225) break-even needs N ≳ 5e-7 (economics dominated by product value); Mo-99 ~0.4; Pm-147 ~70; Au-197 ~195.
- Isotope design: 1e12 μ/s, N = 200 -> 564 W fusion; P_μ = R_μ E_μ / f_stop.

### S12. ARPA-E award DE-AR0001798, NK Labs LLC, "Active Target for Muon-Catalyzed Fusion Energy" [report - award abstract]
- https://www.highergov.com/grant/DEAR0001798 ; $500k, 22 Sep 2023 - 21 Sep 2025, DE-FOA-0002785 (Exploratory Topics C).
- Statements: >100 f/μ observed; alpha sticking gives probable limit **200-500 f/μ**. Floor of muon cost = m_μc² = 105 MeV
  (scientific break-even at ~5-6 f/μ at that floor). **State of the art: carbon rod/plate target requires 5 GeV of beam
  energy per muon -> ~300 f/μ for (scientific) breakeven.** Their software found a target needing **3.3 GeV beam energy
  per muon**: stack of plates with **electric fields between plates plus perpendicular magnetic field** (suppresses
  electron avalanche) so more pions exit and form a collimated pion beam. Goal: MW-scale breakeven experiment.
  (By July 2025 ARPA-E talk this had improved to 3.0 GeV per μ- - see S8.)
- Ion species not specified in abstract. [inference: likely deuterons or protons ~1-3 GeV/u]

## Topic 4: laser-driven muon / pion sources

### S13. Terzani et al. / BELLA (LBNL), "Measurement of directional muon beams generated at the Berkeley Lab Laser Accelerator" [paper, HTML]
- arXiv:2411.02321 (v3). Topic 4 (LWFA-electron route).
- ~21 J, ~40 fs BELLA PW, 0.1 Hz; 30 cm H2 jet at ~1e17 cm^-3; e-beam ~80 pC above 2 GeV (45-250 pC), tails to ~8 GeV,
  divergence 0.1-0.5 mrad.
- No dedicated converter: beam dump (40.5 cm Pb + 1 m steel + 1.8 m concrete, ~142 X0). Measured 126 ± 12 muons over
  ~760 shots in two scintillators; Geant4 agrees; ≳20 muons/shot within 100 mrad on 2x2 m² (≳10 m^-2 per shot).
  Pair (Bethe-Heitler) muon yield peaks at ~6-10 X0 of converter.
- [inference] ~20-100 muons per shot per ~21 J laser -> ~1-5 μ/J of laser, ~0.25 μ per pC (both signs, mostly GeV-energy
  muons that do NOT stop in a small fuel target). Equivalent cost ~1e-9 ... 1e-8 of what is needed: 1 μ per J =
  6.2e9 GeV per muon vs ~5 GeV per μ- for proton/pion route.

### S14. Babjak, Pouyez, Badiali, Grismayer & Vranic (2026), "Kilojoule-scale laser acceleration enabling efficient generation of electron-positron and muon beams" [abstract only]
- arXiv:2609.18775 (physics.plasm-ph), 16 Sep 2026. IST Lisbon (GoLP) [inference from authors].
- kJ-class PW lasers -> tens of nC at GeV-scale electrons; high-Z converter -> up to 3e12 e+ per shot and
  **6.5e5 Bethe-Heitler muons per shot, up to 580 μ/J of laser** (search snippet: ~330 μ/J at 1 PW, ~580 μ/J at 10 PW;
  pion-decay muons "far fewer" than BH muons).
- [inference] 580 μ/J = 1.7e-3 J per muon = 1.1e7 GeV of laser energy per muon (both signs, relativistic). Even with
  perfect stopping, that is ~2e6 x worse than the ~5 GeV/μ- of hadronic production. **Electron-driven muon production is
  ruled out for μCF energy balance**: BH pair production cross-section is suppressed by (m_e/m_μ)² ~ 2.3e-5 relative to e+e-,
  and photo-pion production (γN -> πN, threshold ~150 MeV) yields ~1e-3 π per GeV of photon energy [inference, order of
  magnitude].

### S15. Calvin, Tomassini, Doria, Martello, Deas & Sarri (2023), "Laser-driven muon production for material inspection and imaging" [paper]
- Front. Phys. 11:1177486 (2023). DOI 10.3389/fphy.2023.1177486 (open access). QUB / ELI-NP.
- Simulated ELI-NP 10 PW: 110 J on target, 24 fs -> LWFA e-beam 4.2 GeV peak, 15 % FWHM spread, >12 nC; 2 cm Pb converter.
- **Muons per electron (BH pair, 2 cm Pb): 7e-8 at 2 GeV; 1.85e-6 at 5 GeV; ~quadratic in E_e.** ~1e4 μ+ per shot
  (12 nC) at detector. Muon spectrum: relativistic Maxwellian peaking at ~1/4-1/5 of E_e (0.6-0.7 GeV).
- [inference] At 5 GeV: 1 nC = 6.2e9 e- -> ~1.2e4 μ per shot from ~31 J of electron-beam energy -> ~2.7e6 GeV of
  e-beam per muon. Confirms electron route is ~6 orders of magnitude worse than hadronic π production for μCF.

### S16. Laser-driven proton state of the art (context for "laser-driven proton -> pion" route) [abstract only / news]
- Record laser-accelerated proton energy ~**150 MeV** (Ziegler et al., HZDR DRACO-PW, Nature Physics 2024; HZDR press
  release 13 May 2024); >110 MeV from multi-PW on nm foils (Nature Communications, Feb 2025). No confirmed > 150 MeV
  result found in this search (to Oct 2026).
- Free-nucleon π production threshold ~ 280-290 MeV (pp -> ppπ0 / pn -> ppπ-; sub-threshold in nuclei is tiny)
  [inference/standard]. So no laser-driven proton has yet produced pions efficiently; 6 GeV is ~40x beyond the record.
- Simulation proposals for GeV-class laser protons exist, e.g. arXiv:1112.1816 (PIC: >10 GeV quasi-monoenergetic protons
  from mass-limited target + preformed channel, 60 fs CP laser at ~1e22 W/cm²) [abstract only]; laser-to-proton energy
  efficiency for such regimes is typically a few-10 % in 1D/2D PIC, unverified experimentally [inference].
- Pion production by laser *electron* bremsstrahlung: Schumaker et al., New J. Phys. 20, 073008 (2018): ~150 ± 50 pions
  per shot with a 300 TW laser (via 27Mg activation) [abstract only] - again negligible for μCF.

## Topic 5: conventional proton accelerator efficiency benchmarks

### S17. Kovach, Parfenova, Grillenberger & Seidel (2017), "Energy efficiency and saving potential analysis of the High Intensity Proton Accelerator HIPA at PSI" [paper]
- Proc. IPAC2017, paper TUPVA129, pp. 2399-2402. https://accelconf.web.cern.ch/IPAC2017/papers/tupva129.pdf
- HIPA: Cockcroft-Walton -> Injector-2 (72 MeV) -> Ring cyclotron 590 MeV, 2.2 mA (1.3 MW; max 1.4 MW). Commissioned 1974.
- **Whole facility 12.5 MW at 1.3 MW beam -> 10.4 % grid-to-beam** (incl. all beamlines, SINQ, UCN, cryo for moderators).
  Split: RF 5.3 MW (42 %), magnets 3.6 MW, cooling 1.65 MW, auxiliaries/infrastructure 1.95 MW (cryo 1.21 MW).
- **"Minimum full beam" accelerator-only consumption 7.12 MW -> 18.3 % grid-to-beam efficiency.**
- RF chain: AC-DC ~90 %, tetrode amplifier chain ~60 %, grid-to-RF ~55 %; RF base load ~2.2 MW at zero beam.
- Efficiency model: η_acc = P_beam / (P_beam/η_RF + P_wall-loss/η_RF + P_aux); Joho's law I_max ∝ U_acc³ while wall
  losses ∝ U_acc² -> efficiency rises with current: 2.2 mA (850 kV, 186 turns) η ≈ 0.18; planned 3.0 mA (1 MV, 160 turns)
  η ≈ 0.20.

### S18. Seidel & Mezger (2010), "Performance of the PSI high power proton accelerator" [paper]
- IAEA conference paper AT/RD-10 (IAEA P1433 proceedings). https://www-pub.iaea.org/MTCD/Publications/PDF/P1433_CD/datasets/papers/at_rd-10.pdf
- Zero-beam facility load (magnets + RF on) ~8 MW; **measured differential power dP/dI = 0.81 MW/mA vs beam
  0.59 MW/mA -> differential (marginal) grid-to-beam efficiency 73 %.** Proton accelerator uses ~10 MW total.
  1 GeV / 10 MW cyclotron proposal referenced (their ref. 7).
- [inference] Key lesson for any driver: at MW scale, fixed overheads dominate; at 10-100 MW beam power, the marginal
  RF-to-beam efficiency (~55-75 % for CW machines) is what governs η_wallplug -> asymptotic η ~ 40-60 % achievable for
  CW SRF linacs/cyclotrons (to be checked against ADS studies).

### S19. Yakovlev et al. (EuCARD-2 Proton Driver Efficiency WG), "The Energy Efficiency of High Intensity Proton Driver Concepts" [report - talk]
- IPAC2017 talk FRXCB1 (V. Yakovlev, Fermilab; WG incl. Grillenberger PSI, Kim SNS, Yoshii J-PARC, Seidel).
  https://proceedings.jacow.org/ipac2017/talks/frxcb1_talk.pdf (paper version exists: IPAC2017 FRXCB1).
- Definition: delivered beam power / accelerator consumption (RF + magnets + cooling/cryo), excluding experimental facilities.
- **PSI HIPA cyclotron, 0.59 GeV, 1.4 MW: ~18-19 %** (RF: AC/DC 90 %, DC/RF 64 %, RF->beam 55 %; RF chain overall 32 %;
  magnets 2.6 MW = 34 % of losses; RF 4.5 MW; cavity ohmic 1.2 MW). Up to **24 % at 3 mA**.
- **SNS (SRF pulsed linac), 1 GeV, 1.4 MW: 16.3 MW -> ~9 %** (another slide: 26.3 MW total incl. site, linac 8.6 %).
  Pulsed operation (60 Hz, ~6 % duty) + 2 K cryo + HVCM modulators dominate losses.
- **J-PARC linac + 3 GeV RCS, 1 MW: 32.6 MW -> ~3 %** (400 MeV H- linac 25 Hz + RCS magnets).
- Recommendations: SC sector magnets, high-efficiency klystrons/magnetrons, FFAG, CW SRF for ADS (>10 MW beams).
- Klystron facts (Seidel et al. IPAC'15 WEXC3 "Improving the energy efficiency of accelerator facilities" [paper]):
  klystron electronic efficiency ~65 % at saturation, usable ≲50 % below saturation; IOT ~70 %; high-efficiency
  klystron R&D (bunch-core-oscillation, HEIKA) targets ~90 %; CLIC drive beam RF->beam > 90 %.

### S20. ESS energy figures [news/secondary - abstract-level]
- ESS design: 5 MW, 2.0 GeV (originally 2.5 GeV), 62.5 mA peak, 2.86 ms, 14 Hz, SRF linac; >150 high-power RF sources
  (RF system cost > 200 M€, 2015 ESS talk). Modulator efficiency ~82 %, klystron ~50 % -> grid-to-RF ~40 % [inference
  from neutronsources.org "How do you power the world's most powerful linac?"].
- Site consumption estimate **~265-270 GWh/yr** (2015 Danish press; arXiv:2501.14979 sustainability guidelines), with
  ~253 GWh/yr of waste heat to Lund district heating. [inference] 270 GWh/yr ≈ 31 MW year-average; at ~5000-6000 h beam/yr
  ≈ 45-55 MW during operation for 5 MW beam -> **~10 % site-level grid-to-beam** (accelerator-only probably ~15-20 %).
  Note ESS initially operates at 2 MW / 800 MeV.
- China C-ADS/CiADS: CW SRF linac concept 1.5 GeV, 10 mA (15 MW), CAFe front end 20 MeV, 10 mA CW (205 kW) demonstrated
  (CERN Courier). No published wall-plug numbers found in this search.
- [inference / from memory, unverified this session] Rubbia's Energy Amplifier (CERN/AT/95-44) assumed a 1 GeV, ~10-12 mA
  three-stage cyclotron at ~40-45 % grid-to-beam; such ≥40 % values are design targets, never demonstrated at MW scale.

## Topic 1 (cont.): pion/muon yields vs proton energy

### S21. IMCC / MuCol, "MuCol Milestone Report No. 5: Preliminary Parameters" (Nov 2024) [report]
- arXiv:2411.02966. Section 4.1 Target & front end (FLUKA).
- Proton driver baseline for muon collider: **2 MW, 5 GeV (range 2-10 GeV), 5 Hz, 5e14 p/pulse, 1 bunch, 2 ns, beam
  σ_xy = 5 mm (range 1-2 mm quoted too)**, option 2: 4 MW at 10 GeV. Target: isostatic graphite rod Ø30 mm x 800 mm in
  He, inside 20 T-class HTS solenoid (700 mm inner radius), heavy W shielding.
- **Table 4.4 - FLUKA yield per unit beam energy [1e-2 per GeV per proton], captured if p < 500 MeV/c entering chicane,
  graphite rod r = 15 mm, beam σ = 5 mm (column reading of the PDF: T_p = 3,4,5,6,7,8,9,10 GeV):**

  | T_p (GeV) | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
  |---|---|---|---|---|---|---|---|---|
  | π+ | 2.8 | 2.6 | 2.4 | 2.3 | 2.2 | 2.1 | 1.9 | 1.9 |
  | π- | 1.8 | 1.8 | 1.8 | 1.8 | 1.7 | 1.7 | 1.7 | 1.7 |
  | μ+ | 1.3 | 1.2 | 1.1 | 1.1 | 1.0 | 0.98 | 0.92 | 0.90 |
  | μ- | 0.84 | 0.81 | 0.84 | 0.82 | 0.83 | 0.80 | 0.80 | 0.81 |

  -> **π- per GeV is flat (0.017-0.018 /GeV/p) from 3 to 10 GeV on graphite**; π+ per GeV falls with energy.
  At 6 GeV: 0.108 π- + 0.049 μ- ≈ **0.16 (π- + μ-) per proton captured below 500 MeV/c** -> ~38 GeV per captured
  negative. Outgoing muon beam after front end: 0.018 μ+ per GeV per p (Table 4.7).
- [inference] This is a *collider-acceptance* number (forward, p < 500 MeV/c, partially decayed). It is the most
  reliable modern energy-dependence data point: **per unit beam power, π- production is flat between 3 and 10 GeV, so
  6 GeV is fine; no gain from going higher, small gain (~0-10 %) from going lower to 3-4 GeV for low-Z targets.**
  The gap between ~38 GeV/negative (collider capture) and 3-5 GeV/μ- (μCF claims) is the total-vs-captured distinction
  plus the use of high-Z / long targets and whole-solid-angle capture; it has to be confirmed by our own Geant4/FLUKA run.

### S22. MiniBooNE Collaboration (2009), "The Neutrino Flux prediction at MiniBooNE" - Sanford-Wang π± parametrisation [paper]
- Phys. Rev. D 79, 072002 (2009); arXiv:0806.1449. Section "Sanford-Wang Fit to the Pion Production Data", Tables V-VI.
- **Implementable parametrisation (Sanford & Wang, BNL 11299, 1967):**
  d²σ/dp dΩ = c1 p^c2 (1 - p/(p_B - c9)) exp[-c3 p^c4 / p_B^c5 - c6 θ (p - c7 p_B cos^c8 θ)]  [mb/(GeV/c sr)],
  p, p_B in GeV/c, θ in rad, c9 = 1.
  - π+ (p-Be): c1..c8 = 220.7, 1.080, 1.000, 1.978, 1.32, 5.572, 0.0868, 9.686
  - π- (p-Be): c1..c8 = 213.7, 0.9379, 5.454, 1.210, 1.284, 4.781, 0.07338, 8.329
  Fitted to HARP 8.9 GeV/c and E910 6.4/12.3 GeV/c thin Be data (forward, p > ~0.75 GeV/c).
- Saved to: original-sims/miniboone-sanford-wang-pBe/ (CSV + SOURCE.md).
- [inference] My forward-hemisphere integration (σ_inel(p-Be) ≈ 210 mb assumed): <n_π-> per inelastic interaction ≈
  0.31 (3 GeV), 0.39 (4), 0.47 (5), **0.54 (6 GeV)**, 0.62 (7), 0.69 (8), 0.84 (10 GeV); i.e. **~0.09-0.10 π- per GeV,
  weakly falling with T_p** -> thin-target ~11 GeV per π- at 6 GeV. Low-momentum/large-angle region is extrapolated
  (unreliable) and thick-target cascade multiplication (+20-60 %) is not included. Thick high-Z targets with full
  4π capture (Kelly 2021: 4.7 GeV/π- for d on W; Acceleron: 3.0 GeV) do ~2-3x better than this thin-Be single-interaction
  estimate.

### S23. Gershtein, Petrov & Ponomarev (1990), "Muon catalysis and nuclear breeding" [paper]
- Usp. Fiz. Nauk 160(8), 3-46 (1990); Sov. Phys. Usp. 33(8), 591-615 (1990). DOI 10.1070/PU1990v033n08ABEH002619.
  Full text (English): https://ufn.ru/ufn90/ufn90_8/ufn908a.pdf . Topics 1, 2, 6. Key classic source (Ponomarev school).
- **π- production physics (Sect. 2):** at 1 GeV, an inelastic **nn collision gives a π- with probability 0.83; np/pn
  0.23; pp "virtually none"**. -> use neutron-rich beams and targets. For N≈Z nuclei P(π-) ~ 1/3 per inelastic collision
  -> **~3 GeV per π- in inelastic collisions; ~6 GeV per π- once elastic/ionisation losses are included** (their refs 72-73);
  **tritium beam + tritium target: ~4 GeV per π-**. Fig. 4 (from their ref. 75): energy per π- vs E (GeV/nucleon) for n and p
  on infinite Be target (no π absorption) - neutrons much cheaper than protons; cost falls with energy up to several GeV/u.
- π- -> μ- conversion efficiency theoretical 0.6-0.75 -> **8-10 GeV per μ-, reducible to ~5 GeV/μ- by special choice of
  beam, target material and density**. They adopt **C_μ = 8 GeV/μ-** for hybrid estimates.
- Footnote: proposals (refs 74-75, i.e. Jändel/Rafelski school [inference]) to raise beam energy to **3-4 GeV/nucleon** to
  lower π- cost, but finite-target calculations with absorption/elastic losses were "not yet completed" (1990).
- μCF parameters: X_c measured 150 ± 20 (φ = 1.2, LANL/BYU/INEL), 114 ± 10 (φ=1.2), 124 ± 10 (φ=1.45) (PSI/Vienna...);
  realistic λ_c ≈ 0.8e8 /s -> X_c ≈ 100; ω_s ≈ 0.5 %. Energy per muon at X_c = 100: ~2 GeV (dt fusion only).
- **"Pure muon catalysis may become commercially convenient only when X_c ~ 1e4"** (i.e. pure-fusion engineering
  breakeven with realistic η's needs X_c ~ 1e4; cf. Eliezer 1994).
- Hybrid reactor (deuteron 1 GeV/u on Li/Be/B/C target; ~30 % of beam energy -> π-, ~70 % -> U-238 spallation breeding):
  per GeV-nucleon: electronuclear channel 4.2 GeV(e), μCF channel 4.4 GeV(e) (13 fusion neutrons/GeV-nucleon at
  C_μ = 8 GeV/μ, X_c = 100; each 14 MeV n -> 0.82 fission, 2.4 Pu, 0.7 T in U/6Li blanket). Total 8.6 GeV(e) per GeV.
- **Accelerator efficiency assumed η_a = 0.6** ("completely attainable for high-current accelerators according to
  specialists", their refs 83-84). 1 GWe system -> accelerator ~200 MWe -> **2 GeV deuterons at I_d = 120 mA
  (240 MW beam)**; synthesiser ~50 MW fusion power. Called for development of > 1 GeV/u, ~100 mA deuteron accelerators.
- [inference] Implied hybrid numbers: 240 MW beam / 8 GeV per μ = 1.9e17 μ/s; x100 fusions x 17.6 MeV = 53 MW fusion -
  consistent with their 50 MW.

## Topic 2: μCF physics numbers

### S24. Kamimura, Kino & Yamashita (2023), "Comprehensive study of muon-catalyzed nuclear reaction processes in the dtμ molecule" [abstract only]
- Phys. Rev. C 107, 034607 (2023); arXiv:2112.08399. DOI 10.1103/PhysRevC.107.034607.
- **Initial α-μ sticking ω_s0 = 0.857 %** (≈7 % below previous 0.91-0.93 % literature values; explains 2001 high-density
  data). dtμ fusion rate 1.15e12 /s; emitted muon peak 1.1 keV, mean 9.5 keV.
- Per Ignatov 2025 slide (S10) citing this work: **effective ω_s = 0.557 % (with reactivation R ≈ 0.35 at high density)
  -> Y_max ≈ 180 cycles per muon** (sticking-limited ceiling with infinitely fast cycling).
- Effective sticking formula: ω_s = ω_s0 (1 - R); external-field-assisted reactivation proposals use
  ω_s^eff = ω_s0 (1 - R_col)(1 - R_X) (2026 preprint, "external field assisted muon reactivation ... rate network criterion").

### S25. Consolidated μCF physics benchmarks (from S1, S5, S6, S9, S10, S23, S24 + standard literature) [inference/compilation]
- Energy per dt fusion: 17.6 MeV (3.5 MeV α + 14.1 MeV n). With Li blanket (tritium breeding, exothermic 6Li(n,t)α):
  ~20.4 MeV (Sawan & Abdou, via Parisi 2025), 25 MeV (Acceleron), 26 MeV (Kelly 2021, 1.75 Li reactions/n).
- Muon lifetime τ = 2.197 μs (λ_0 = 4.55e5 /s).
- Cycling rate λ_c (normalised to LHD φ): ~1e8 /s typical at LHD, up to ~(2-3)e8 /s at optimum T, c_t ~ 0.4-0.5.
- Record X_c: **150 ± 20 f/μ** (LANL/BYU/INEL, Jones et al. PRL 56, 588 (1986), φ ≈ 1.2, high T). PSI/Vienna: 114-124.
  Typical 100-200 depending on T, φ, c_t, phase.
- Sticking: ω_s0 theory 0.857-0.93 %; reactivation R ≈ 0.3-0.4 at LHD -> ω_s ≈ 0.55-0.6 % (theory); measured effective
  0.3-0.5 % at 1.2 LHD (EPN 1989), ~0.45-0.47 % commonly used (Kelly; Yin), indications of lower sticking at high density
  (Nagamine 2008 compilation; MuFusE motivation). Sticking-limited ceiling X_max = 1/ω_s ≈ 180-330.
- X_c formula: 1/X_c = λ_0/(φ λ_c) + ω_s  [S3, S4b].
- **Scientific break-even (beam energy only): X_c ≥ E_μ(beam)/17.6 MeV** -> 284 at 5 GeV, 170 at 3 GeV, 114 at 2 GeV.
- **Engineering break-even** (electric out = electric in): X_c · E_f · η_th ≥ E_μ(beam)/η_acc - (recovered heat) ...
  see summary table below; values quoted in literature: ~415 (Parisi, η=0.4, E_μ=5 GeV, η_μ=0.8 beam-heat recovery),
  ~1e3 (Eliezer "advanced"), ~1e4 (Eliezer/GPP "standard technology").

## Topic 3: revival efforts 2020-2026 (cont.)

### S26. Kino (Tohoku), μCF talk at Int. Conf. on μCF and Future Applications, Liverpool, Jul 2026 [report - slides]
- https://indico.ph.liv.ac.uk/event/2421/contributions/10928/attachments/5294/7470/Liverpool2026_Kino.pdf
- Framing: "Energy source: **output 3.5 GeV/muon vs input 5.0 GeV/muon**" (i.e. X_c ≈ 200 x 17.6 MeV vs 5 GeV beam cost).
- New coupled-channel model (Kamimura-Kino-Yamashita): fusion rate 1.15e12 /s, sticking components shown; slides suggest
  "#fusion ~200-220" at their model sticking; in-flight μCF (IFμCF: 1-10 keV tμ atoms colliding with d, skipping
  dtμ formation) explored with gas-circulating Mach-shock targets (Chubu Univ. patent; NIFS/KAKENHI 18H05461);
  Yamashita et al., Sci. Rep. 12, 6393 (2022): resonant muonic molecules in hot compressed D-T gas; J-PARC TES X-ray
  measurements; aspirational ~1000 f/μ (Yamashita, Muons4Future 2025) - projection only.
- Japan's in-flight concept (Iiyoshi et al., AIP Conf. Proc. 2179, 020010 (2019)): 1e16 μ/s x 1000 f/μ -> 28 MW fusion,
  8.5 MW electricity (S10).

### S27. Funding / company status notes (secondary sources) [abstract only / news]
- Acceleron Fusion (Cambridge MA; spun out of NK Labs after 2020 ARPA-E $2.28 M award): **~$24 M raised from investors
  in 2024** (Ignatov 2025 slide; IEEE Spectrum "colder muon fusion energy"); collabfund.com and techcrunch coverage.
  Approach: high-P/high-T DT in diamond anvil cells (MuFusE at PSI), active-target muon source (3.0 GeV/μ- simulated),
  superconducting accelerator + Brayton cycle; "energy breakeven test at Brookhaven in ~5 years" (2025 statement).
- Marathon Fusion (Parisi & Rutkowski 2025): isotope-production first market (S4/S4b).
- China (IMP-CAS / Huizhou CiADS-HIAF): EMuS muon source ≥1e8 μ-/s after 2028; μCF roadmap papers (S2, S3).
- Fermilab: 2021 MTA pion-production-target studies for a μCF experiment at the 400 MeV linac (indico poster, 403 on
  fetch - [abstract only]); 2021 Fermilab accelerator design meeting on μCF (Shiltsev), cited by Ignatov.

### S1b. Kelly, Hart & Rose (2021) - details from full PDF (Oxford ORA copy) [paper]
- ORA copy: https://ora.ox.ac.uk/objects/uuid:1931d933-7f30-41f7-91d9-b20bad97e65a/files/rsn009z223 (IOP page later
  bot-walled). G4beamline simulation, genetic optimisation (512 configs/generation).
- Beams: deuterons or tritons only - **protons not simulated** because "as Jändel [6] showed, beams of neutrons are more
  effective at producing negative pions than beams of protons". Targets: carbon, LiPb (17 % Li, 90 % 6Li), tungsten.
- **Counting assumption: 100 % of π-/μ- exiting the target are assumed to be used for catalysis** (they note real
  utilisation "well below 100 %") -> the 4.70 GeV/μ- is an optimistic upper bound on yield (lower bound on cost).
  Their later Q_elec uses η_μ = 50 % delivery, i.e. effectively ~9.4 GeV beam per useful μ-.
- Relative Q (Fig. 2): t+LiPb best; d beams only marginally behind tritons; carbon targets ~5-20 % worse than W/LiPb;
  W ≈ LiPb for deuterons. Optimal beam energy 2-6 GeV (total) and "volatile" - Q vs E is flat-topped (rises steeply to
  ~2 GeV, flat to ≥5 GeV for d on W).
- The literature "5-6 GeV per muon" figure is **Jändel M., J. Fusion Energy 8, 81-87 (1989)** (their ref. 6).

### S28. Bekmirzaev et al. (2021), "Comparison of some properties of charged pions in p12C and n12C collisions at 4.2 GeV/c" [paper]
- Physics of Complex Systems 2(3), 132-138 (2021). DOI 10.33910/2687-153X-2021-2-3-132-138 (JINR 2 m propane bubble
  chamber data, Dubna Synchrophasotron; via cyberleninka).
- **Measured mean multiplicity per inelastic collision at p = 4.2 GeV/c (T ≈ 3.4 GeV):**
  **p+C: π- 0.36 ± 0.02, π+ 0.63 ± 0.02; n+C: π- 0.64 ± 0.02, π+ 0.37 ± 0.02** (modified FRITIOF overestimates by ~10 %).
- -> **neutrons give 1.8x more π- than protons** at ~3.4 GeV on carbon. Related data sets: 6736 pC, 7071 dC, 11974 αC events
  at 4.2 GeV/c/u (Olimov et al.; Abdrahmanov et al. Z. Phys. C 1980 "Interaction cross sections and negative pion
  multiplicities in nucleus-nucleus collisions at 4.2 GeV/c per nucleon").
- [inference] A 4.2 GeV/c/u deuteron (≈6.7 GeV total) ≈ p + n -> ~0.36 + 0.64 ≈ 1.0 π- per inelastic event vs ~0.5-0.55 for
  a single ~6-7 GeV proton (S22) -> **per unit beam energy, deuterons ≈ 1.6-1.9x better than protons in the first
  interaction**; in thick targets the secondary-neutron cascade narrows the gap (Kelly found d ≈ t, and GPP give
  t-on-t 4 GeV vs ~6 GeV/π- for N≈Z). Consistent with S11/S21: SW thin-target p-Be at 6 GeV ≈ 0.54 π-/inelastic.

## Topic 6: beam power, protons/s and beam-quality tolerances for a μCF muon factory [inference, anchored to S1, S11, S21, S23]

Numbers below come from /tmp script `budget.py` (not saved in repo); e = 1.602e-19 J/eV.

**Per 1 MW of 6 GeV proton beam:** 1.04e15 p/s (167 μA). Muon rate and dt fusion power (17.6 MeV/fusion):

| beam energy per useful μ- (E_b) | μ- per 6 GeV proton | μ-/s per MW | P_fus at X=150 | P_fus at X=300 |
|---|---|---|---|---|
| 3 GeV (Acceleron active-target claim) | 2.0 | 2.1e15 | 0.88 MW | 1.76 MW |
| 5 GeV (classic literature) | 1.2 | 1.25e15 | 0.53 MW | 1.06 MW |
| 8 GeV (GPP 1990 adopted value) | 0.75 | 7.8e14 | 0.33 MW | 0.66 MW |
| 12 GeV (my thin-target-based proton estimate incl. π->μ losses) | 0.5 | 5.2e14 | 0.22 MW | 0.44 MW |

**1 GW of dt fusion power (17.6 MeV only)** needs 2.4e18 μ/s at X=150 (1.2e18 at X=300; 3.6e17 at X=1000) ->
beam 1.9 GW (X=150, 5 GeV/μ) / 0.95 GW (X=300) / 0.28 GW (X=1000); at 6 GeV & 5 GeV/μ that is 2.0e18 / 1.0e18 / 3e17 p/s
= 0.32 / 0.16 / 0.05 A.

**1 GWe-net plant (optimistic Acceleron-like budget, E_b = 3 GeV, X = 300, 25 MeV/fusion, 83 % beam-heat recovery,
η_th = 0.64):** η_acc = 0.5 -> Q_eng = 1.07, 1.6e19 μ/s, **7.6 GW beam (1.27 A at 6 GeV)**; η_acc = 0.8 -> Q_eng = 1.7,
2.4e18 μ/s, **1.1 GW beam (0.19 A)**. Even with X = 1000 and E_b = 5 GeV, η_acc = 0.5 gives 4 GW beam for 1 GWe net.
GPP 1990 hybrid (fission blanket does the work): 2 GeV d, 120 mA, 240 MW beam per GWe.

**Demonstrator scales:** isotope μCF (Parisi): 1e12 μ/s ≈ 1-10 kW beam. "Scientific break-even" demonstration with
X ≈ 150-300: any beam power works; ~1 MW gives ~1e15 μ/s and ~0.5-1.8 MW fusion (Acceleron targets a MW-scale
breakeven test at BNL ~2030).

**Beam-quality tolerances for a pion-production target (inference from target designs in S1, S11, S21):**
- Energy: π- yield per unit beam energy is flat within ~10-15 % from ~2 to ~11 GeV (Strait 2010; MuCol FLUKA 3-10 GeV;
  Kelly: flat-topped above ~2 GeV total for d). -> **a broad energy spread (even ±50 % around 6 GeV) costs ≲10 % in yield,
  provided little beam energy sits below ~1-2 GeV/nucleon** (yield per GeV collapses toward the ~0.3 GeV π threshold;
  energy in a low tail is mostly wasted, partly recovered as heat). So LWFA-typical energy spread is acceptable.
- Transverse: targets are long, thin rods: W Ø5.1 mm x 652 mm (Kelly; ≈ 6.6 λ_I since λ_I(W) ≈ 9.9 cm),
  graphite Ø30 mm x 800 mm with beam σ = 5 mm (MuCol), Hg/Ta Ø10 mm x 2 λ_I (NF). Requirement: beam stays inside rod
  radius over ~0.5-0.8 m -> rms size ≲ 1-2 mm (W) / ≲ 5 mm (graphite) and divergence ≲ 1-3 mrad, pointing jitter ≲ 1 mm.
  Geometric emittance ≲ ~5 mm·mrad -> normalised ε_n ≲ ~30-40 mm·mrad at 6 GeV (βγ ≈ 7.4): **very loose** compared with
  LWFA beams (ε_n ~ 0.1-1 mm·mrad for electrons; laser-ion beams have low emittance but large divergence that must be
  captured/collimated - divergence of tens of mrad would be the actual problem).
- Time structure: pion lifetime 26 ns and muon lifetime 2.2 μs; no bunch-length requirement for yield. Limits come from
  peak power deposition/thermal shock in target (MuCol 2 MW graphite: 5e14 p per 2 ns pulse at 5 Hz is the design
  envelope) and from instantaneous muon density in the fuel. High rep-rate (kHz-MHz) low-charge pulses are benign.
- Pion -> muon conversion: π- that stop in matter are captured by nuclei (no muon); pions must decay in flight inside a
  solenoid / magnetic-mirror decay volume and the μ- must then stop in the D-T. GPP: theoretical π->μ efficiency 0.6-0.75;
  Kelly assumes 50 % delivery. This factor multiplies E_b.

### S29. Plasma-accelerator wall-plug efficiency context [abstract only / search snippets]
- Hooker et al. (2014), "Multi-pulse laser wakefield acceleration: a new route to efficient, high-repetition-rate plasma
  accelerators", arXiv:1401.7874: present LWFA drivers (Ti:sapphire) limit LWFA to **< ~1 Hz and ~0.1 % wall-plug**.
- Hooker review arXiv:1406.5118: laser->wake ~50 % and wake->bunch ~50 % assumed -> laser power ≈ 4x beam power.
- PWFA collider concept (Hogan, LBNL 2016 slides): 50 % x 90 % wall-plug->drive beam, 35 % drive->main -> 15.7 % overall.
- DLA TeV-collider study (arXiv:2203.03811): 10-12 % wall-plug assuming > 30 % efficient solid-state lasers and 40 %
  laser->beam coupling.
- [inference] Even the most optimistic plasma/laser-accelerator efficiency targets (~10-20 % wall-plug, for electrons) are
  at or below today's PSI cyclotron (18 %). For *protons*, laser->proton coupling at multi-GeV is unproven (record laser-ion
  energy ~150 MeV, S16).

---

## μCF energy budget summary (table)

Definitions: E_b = accelerator beam energy spent per μ- that actually stops in the D-T fuel (GeV); X = dt fusions per μ-;
E_f = heat per fusion (17.6 MeV bare; ~20-26 MeV with Li breeding blanket); f_rec = fraction of beam energy recovered as
useful high-temperature heat; η_th = heat->electric; η_acc = wall-plug->beam.
Scientific gain Q_sci = X·E_f/E_b. Engineering gain **Q_eng = η_acc · η_th · (X·E_f + f_rec·E_b) / E_b**.
Required **η_acc(Q_eng=1) = E_b / [η_th (X·E_f + f_rec·E_b)]**; a commercial plant needs Q_eng ≳ 3-5.

### Key literature numbers

| Quantity | Value | Source |
|---|---|---|
| Floor on muon cost | m_μc² = 105.7 MeV (absolute); "theoretical limit < 2 GeV" | S12, S5 |
| π- cost, inelastic only, N≈Z target | ~3 GeV/π- | S23 (GPP 1990) |
| π- cost incl. elastic/ionisation losses | ~6 GeV/π- (p/d on light target); ~4 GeV with t beam on t target | S23 |
| Classic beam cost per μ- | 5 GeV (Jändel 1989; "5-6 GeV"); 5-10 GeV for deuterons; GPP adopt 8 GeV | S1, S5, S6, S23 |
| Best published simulation, d beam | 4.70 GeV per π-/μ- exiting (3.61 GeV d on W rod), 100 % utilisation assumed | S1 |
| Best claimed design (active target, fields in target) | 3.3 GeV (2023) -> 3.0 GeV per μ- exiting (2025), unverified | S12, S8 |
| Collider-style capture (graphite, p<500 MeV/c), 6 GeV p | 0.16 (π- + μ-)/proton -> ~38 GeV per captured negative | S21 |
| Thin-target <n_π-> per inelastic event | p+C 0.36, n+C 0.64 (4.2 GeV/c); p+Be ~0.54 at 6 GeV (SW fit) | S28, S22 |
| Energy dependence per unit beam power | flat (±10-15 %) from ~2 to ~11 GeV; π- slightly favours lower T | S11, S21, S1 |
| π- -> stopped μ- conversion | 0.6-0.75 theoretical; 0.5 assumed by Kelly | S23, S1 |
| X_c record | 150 ± 20 (LANL 1986); typical 100-200 | S23, S25 |
| ω_s0 / ω_s(eff) | 0.857 % (2023 theory) / 0.3-0.6 % -> X_max ≈ 180-330 | S24, S5, S25 |
| X for Q_sci = 1 | 284 (5 GeV), 170 (3 GeV) | S2, S12 |
| X for electric break-even | ~415 (η_th 0.4, E_μ 5 GeV, 80 % beam-heat recovery); 1e3 "advanced", 1e4 "standard" | S4b, S6, S23 |
| Acceleron target ledger | 3 GeV/μ, 300 f/μ x 25 MeV, 64 % Brayton, 47 % recirc (implicitly η_acc ≈ 1) | S8 |
| Kelly 2021 present-tech ledger | Q_elec ≈ 14 % (η_acc 18 %, X=150) | S1 |

### Required accelerator wall-plug efficiency (my calculation)

| Scenario | Q_sci | η_acc for Q_eng=1 | η_acc for Q_eng=3 |
|---|---|---|---|
| Today: E_b 5 GeV, X 150, 17.6 MeV, no recovery, η_th 0.35 | 0.53 | 5.4 (impossible) | 16 |
| E_b 5, X 150, 22 MeV, f_rec 0.8, η_th 0.40 | 0.66 | 1.7 (impossible) | 5.1 |
| Kelly-like: E_b 4.7, X 150, 26 MeV, f_rec 0.8, η_th 0.40 | 0.83 | 1.5 (impossible) | 4.6 |
| E_b 3, X 150, 22 MeV, f_rec 0.6, η_th 0.45 | 1.10 | 1.3 (impossible) | 3.9 |
| E_b 8 (realistic proton beam), X 300, 22 MeV, f_rec 0.6, η_th 0.45 | 0.82 | 1.6 (impossible) | 4.7 |
| E_b 4, X 300, 22 MeV, f_rec 0.6, η_th 0.45 | 1.65 | 0.99 | 3.0 |
| E_b 3, X 300, 22 MeV, f_rec 0.6, η_th 0.45 | 2.20 | 0.79 | 2.4 |
| Acceleron: E_b 3, X 300, 25 MeV, f_rec 0.83, η_th 0.64 | 2.50 | **0.47** | 1.41 |
| E_b 8, X 1000, 22 MeV, f_rec 0.6, η_th 0.45 | 2.75 | 0.66 | 2.0 |
| E_b 5, X 1000, 22 MeV, f_rec 0.6, η_th 0.45 | 4.40 | **0.44** | 1.33 |

Benchmarks for η_acc (wall-plug -> beam): PSI HIPA 18.3 % accelerator-only / 10.4 % site, marginal 73 % (S17, S18);
SNS ~9 % (S19); J-PARC linac+RCS ~3 % (S19); ESS ~10 % site-level est. (S20); HIPA at 3 mA projected 20-24 %; ADS
literature assumes 40-60 % (GPP 1990 assumed 0.6; Rubbia ~0.43, unverified); LWFA today ~0.1 %, plasma-collider targets
10-20 % (S29).

**Bottom line:** with demonstrated physics (X ≈ 150, E_b ≥ 4.7 GeV) no accelerator efficiency gives electrical
break-even (required η_acc > 1). Pure-μCF electricity requires simultaneously X ≳ 300 (at or beyond the sticking limit),
E_b ≲ 3-4 GeV per *stopped* μ-, high-temperature heat recovery of the beam energy, and η_acc ≳ 0.5-1.0 just for
Q_eng = 1 (≳ 1.4 for Q_eng = 3, i.e. impossible). Accelerator efficiency is necessary but not the binding constraint;
X and E_b are. Non-electric uses (isotopes, neutron source, fission-hybrid/breeder) relax the requirement by orders of
magnitude (S4b, S23).

## Requirements this places on a 6 GeV proton LWFA (efficiency, protons/s, beam power)

1. **Beam energy - OK.** 6 GeV protons sit on the flat optimum of π- production per unit beam power (2-11 GeV; S11, S21).
   No benefit from going higher; ~0-15 % benefit from 3-4 GeV for low-Z targets. However **protons are ~1.6-1.9x worse
   than deuterons (neutron-rich beams) per GeV in the first interaction** (S28, S23); a deuteron or triton LWFA beam (same
   rigidity issues) would be preferable if feasible. Expected realistic yield for 6 GeV protons on an optimised thick high-Z
   target with solenoid capture: ~0.8-1.2 π- per proton exiting the target -> ~0.5-0.9 stopped μ- per proton ->
   **E_b ≈ 7-12 GeV per stopped μ-** [inference]; 4-6 GeV/μ- only with Kelly-type 100 %-utilisation accounting; ~3 GeV
   only if Acceleron's active-target concept (fields inside target) is validated - and its applicability to protons is not
   stated.
2. **Energy spread - loose.** ±30-50 % spread around 6 GeV costs ≲10 % in yield; avoid energy in components < 1-2 GeV.
3. **Emittance/divergence - loose but finite.** Hit a 5-30 mm diameter rod over 0.5-0.8 m: rms spot ≲ 1-5 mm, divergence
   ≲ 1-3 mrad (ε_n ≲ ~30 mm·mrad). Large laser-ion divergence (tens of mrad) would need capture optics.
4. **Average power / flux.** Physics demonstrator: ~1 MW = 1.0e15 p/s (167 μA) -> ~0.5-2e15 μ/s, 0.2-1.8 MW fusion.
   Isotope pilot: 1e12 μ/s ≈ 1-10 kW. Power plant (1 GWe net, optimistic physics): **1-8 GW of 6 GeV beam
   (2e18-8e18 p/s, 0.2-1.3 A)**. For reference, today's most powerful proton machines deliver 1.4-2 MW.
   Per-pulse: at 1 kHz, 1 MW needs 1 kJ/pulse = 1.0e12 protons (167 nC) per shot; at 100 kHz, 1.7 nC per shot.
5. **Wall-plug efficiency.** To matter for electricity the LWFA must reach **η_wall->beam ≳ 0.5 in the most optimistic
   (X=300, 3 GeV/μ, 64 % Brayton) budget, ≳ 0.8-1.0 in moderate budgets, and > 1 (impossible) with today's X ≈ 150**. That is
   ≥ 2.5x PSI HIPA (18 %), ≥ 5x SNS, ≥ 500x present LWFA (~0.1 %), and ≥ 2.5-5x the best plasma-collider projections
   (10-20 %). Competing goal for a LWFA in this project should therefore be stated as: **beat conventional drivers on
   cost per beam-watt and footprint at η ≳ 20-30 %, for non-electric μCF applications (isotopes, neutron sources,
   hybrids)**, while electricity production additionally depends on X ≳ 300 and E_b ≲ 3-4 GeV that no one has shown.


---

## Not accessed / to follow up
- Jändel M., J. Fusion Energy 8, 81-87 (1989) - origin of the "5-6 GeV per muon" figure (paywalled; not found open).
- Jändel M., CERN-TH-4810/87 (1987) - try CERN CDS scanned preprint.
- Latysheva et al., "Negative pion production by deuterons", Hyperfine Interact. 102, 669-676 (1996) - INR cascade
  calculations of π- yield vs deuteron energy and C/Be target size (abstract only seen).
- Ponomarev, Contemp. Phys. 31, 219 (1990); Breunlich, Kammel, Cohen, Leon, Annu. Rev. Nucl. Part. Sci. 39, 311 (1989);
  Ponomarev & Petitjean, Fusion Technol. (1991) - classic reviews (paywalled).
- Chapline/Moir LLNL μCF-hybrid reports - not located on OSTI in this session.
- Fermilab MTA "Pion production studies" poster (2021, indico.fnal.gov/event/50386) - HTTP 403.
- Yakovlev et al., IPAC2017 FRXCB1 paper version (talk slides used instead).
- Primary Acceleron/MuFusE μCF results papers (arXiv:2606.05333 DAC; 2606.19304 gas system) - only abstracts read.
- Recommended next step [inference]: run our own Geant4/FLUKA (FTFP_BERT / INCL) for 6 GeV p vs 3 GeV/u d on W/C/LiPb rods
  inside a 5-20 T solenoid, counting π- that decay in flight and μ- stopping in a D-T volume - this is the number that
  decides E_b for the LWFA concept.
