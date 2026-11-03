# Electric-field tailoring in inaccessible regions -> an "electric flying focus" for protons?

> **Side note (2026-11-03).** This is the first, broader review. The focused follow-up — the
> electric version of Mach-Batlle's active shell as a moving virtual charge, with simulations
> (S046) — is in `electric-flying-focus.md`. The concepts below (wavelength ladder, proton DLA,
> THz arrays, plasma gratings) are kept as background and are not simulated.


Started 2026-11-03. Literature review + theory proposal. Labels: [paper] = read full text/open version,
[abstract only], [press], [inference/estimate] = my reasoning or rough numbers.

Question: "Tailoring Magnetic Fields in Inaccessible Regions" shapes a field inside a source-free region
using sources placed only outside it. Can an electric analogue make a moving
electric-field/potential structure ("electric flying focus") whose velocity is programmable (sub-luminal and
increasing) to accelerate protons from low energy toward ~6 GeV?

## Source log

### S1. Mach-Batlle et al., "Tailoring magnetic fields in inaccessible regions", PRL 125, 177204 (2020)
- Citation verified [paper]: Rosa Mach-Batlle, Mark G. Bason, Nuria Del-Valle, Jordi Prat-Camps,
  Phys. Rev. Lett. 125, 177204 (Oct 2020), DOI 10.1103/PhysRevLett.125.177204. First author is
  **Rosa** Mach-Batlle (not "G."). Open accepted version: https://ddd.uab.cat/record/321739 (read in full).
  No arXiv version found.
- Idea [paper]: a cylindrical shell with relative permeability mu = -1 acts as a magnetostatic "perfect lens"
  (Pendry-type near-field lens, via transformation optics). A wire at radius d inside the shell
  (inner radius R1, outer R2) appears outside as a **replica wire** at d' = d R2^2/R1^2, which can lie in
  empty space (d' > R2). Passive static mu<0 does not exist, so the shell is emulated by **active surface
  currents**. The simplified device is a centred wire I plus a surface current on rho = R2:
  K(phi) = sum_{n=1}^{nT} (I/(pi R2)) (d'/R2)^n cos(n phi).
- Earnshaw/Laplace [paper]: no local maximum of |B| in free space. The replica does not break this: the
  exact solution **diverges throughout the annulus R2 < rho < d'** (fields between the device and the
  replica are larger than at the replica), and the exact external current diverges when d' > R2. Only a
  truncated series (nT terms) is physical.
- **Cost scaling (the key lesson for us)** [paper]: the current on the outermost wire grows as
  (d'/R2)^nT, and the angular structure needs ~2 nT wires. Focusing quality improves with nT, but the
  power grows exponentially with (distance/aperture) x (sharpness). This is the generic evanescent-harmonic /
  superoscillation cost: a sharp feature at distance from a source-free boundary is built from harmonics that
  decay as (R2/rho)^n, so you pay (d'/R2)^n to put them back.
- Experiment [paper]: R2 = 40 mm, height 400 mm, replica I = -0.5 A at d' = 60 mm (d'/R2 = 1.5), nT = 10,
  discretised into 20 wires + centre wire (21 currents). Measured with fluxgates (errors < 0.025 uT); matches
  calculations. Also showed **remote cancellation** of a real "target" wire placed at the replica position.
  Field gradient dBy/dy beyond the device is sharper than a real wire at the device surface would give.
- Extensions stated [paper]: works for **low-frequency AC** fields while wavelength >> device (quasi-static,
  induced E negligible); their setup to ~100 MHz. 3D version (point dipole) would need a spherical mu=-1
  shell with complicated currents. Superconductors suggested for high current.
- Electric analogue [inference/estimate]: electrostatics obeys the same Laplace equation, so an
  "epsilon = -1 shell" emulated by surface charges/electrode potentials can create a **replica charge or
  line charge at a distance**, with the same exponential cost (d'/R2)^n and the same constraint: |E| is
  highest at the boundary/in the annulus, never a free-space maximum. Negative permittivity is natural at
  optical frequencies (metals/plasmas below omega_p, i.e. surface plasmons) - that is exactly Pendry's
  silver superlens. So the electric analogue is not exotic: in the optical/THz regime it *is* plasmonic /
  near-field optics.
- What this means for a proton accelerator [inference/estimate]: the useful field in a source-free gap is
  always <= the field at the electrodes. Field "at a distance" does not beat the material breakdown limit;
  it only shapes the field. The relevant electric analogue for acceleration is therefore not "a field
  maximum in empty space" but "a travelling potential/field pattern in a gap, driven by surrounding
  sources with programmable timing" - i.e. the phased near-field (slow-wave) accelerator.

### S2. Related "field at a distance" work from the same group (search results; not all read in full)
- Navau, Prat-Camps, Sanchez, "Magnetic energy harvesting and concentration at a distance by transformation
  optics", PRL 109, 263903 (2012), arXiv:1207.7030 [abstract only]: a transformation-optics shell
  (superconductor + ferromagnet implementation) collects magnetic energy and delivers it to a point in free
  space. Experimental ferromagnetic-metamaterial version: Prat-Camps, Navau, Sanchez, APL 105, 234101 (2014),
  arXiv:1308.5878 [abstract only].
- Mach-Batlle et al., "Negative permeability in magnetostatics and its experimental demonstration", PRB 96,
  094422 (2017); "Magnetic illusion", PR Applied 9, 034007 (2018), arXiv:1803.08009 [abstract only, via
  citation]. Active currents emulate mu<0.
- Electrostatic side [abstract only, search snippets]: the equivalent literature is the "complementary media /
  anomalous localized resonance (ALR)" theory (Milton, Nicorovici, McPhedran, Podolskiy, Proc R Soc A 461,
  3999 (2005); Nguyen et al.). An eps ~ -1 + i delta shell gives fields that **blow up in an annulus** as
  loss -> 0 - the same divergent annulus Mach-Batlle find. No paper found that does a Mach-Batlle-style
  "electric replicator" for accelerating particles.
- [inference/estimate] Conclusion of task 1 so far: shaping a quasi-static field at a distance is possible
  but (a) cannot beat the boundary field (maximum principle), (b) costs exponentially in sharpness and
  distance, (c) remains valid only while device << wavelength. For acceleration we need |E| ~ GV/m at
  optical/THz frequencies, where "device << wavelength" means nanostructures - i.e. DLA / plasmonics.

### S3. Torrisi et al., "Feasibility study and perspectives of proton DLA (p-DLA)", arXiv:2106.13701 (2021)
- [abstract only] White paper (INFN-LNS Catania + others). Proposes integrating a nanoscale proton/light-ion
  source with sub-relativistic DLA stages; a **proton dielectric RFQ (p-DRFQ)** bridges the front end to
  drift-tube-like and high-beta sections; Alternating Phase Focusing (APF) suggested for long interaction
  length at ultra-low injection energy. Key difficulty stated: aperture ~ laser wavelength, so only
  low-charge, high-rep/CW, ultralow-emittance beams. Applications: proton beam writing, micro-NRA,
  mini-beam therapy, etc. No experimental proton DLA acceleration exists (as of these sources).

### S4. Marcia, Corte, Wilton, Picciotto (FBK Trento), "SMART - a small particle accelerator on chip",
IPAC'26 preprint TUP3010 (May 2026)  [paper, read full preprint]
- Fused-silica double-grating DLA for **100 keV protons (beta = 0.01459)**, lambda0 = 2 um, CST FDTD.
- Synchronicity lambda_p = n lambda0 beta: n=1 -> 29 nm period, n=3 -> 87 nm (chosen for fabrication).
- Optimised: gap 35 nm, pillars 44 x 44 nm. **Peak local field > 4 GV/m but effective synchronous gradient
  only 34.3 MV/m** [paper]. Gradient falls rapidly with gap width ("evanescent regime") [paper].
- They propose moving to mid-IR to enlarge features; injector: Marcia et al., EPL 154, 54001 (2026),
  on-chip electrostatic injector [abstract only via reference].
- [inference/estimate] The 4 GV/m -> 34 MV/m loss (~1%) is the core physics for slow particles, explained in
  "Physics limits" below: the synchronous harmonic of a field with phase velocity beta*c decays away from the
  wall as exp(-2 pi y/(beta gamma lambda)); at beta=0.0146, lambda=2 um the 1/e length is **4.6 nm**.
  Using harmonic n=3 adds a further penalty.

### KEY THEORETICAL LINK (Mach-Batlle <-> slow-wave accelerators) [inference/estimate, standard physics]
- Any field component synchronous with a particle of velocity beta*c, at angular frequency omega, has
  k_z = omega/(beta c). In vacuum it must satisfy (nabla_perp^2 - k_z^2 + omega^2/c^2) E = 0, i.e. it decays
  transversely with kappa = omega/(beta gamma c): 1/e length L = beta gamma lambda / (2 pi).
- Equivalently: Lorentz-boost to the frame moving at beta*c. There the synchronous field is **static**, so it
  obeys Laplace's equation in the source-free beam channel. So the "electric flying focus" is, in its own
  rest frame, *exactly* the Mach-Batlle problem (an electrostatic pattern inside an inaccessible region,
  produced by sources on the boundary):
  * no local maximum of |E| (or of the potential) inside the channel -> field is largest at the walls;
  * a feature of transverse scale ~ its longitudinal period is exponentially suppressed with distance from
    the sources: Mach-Batlle's (d'/R2)^n cost becomes exp(+2 pi d/(beta gamma lambda)) in required wall field;
  * Earnshaw in the rest frame -> a synchronous particle cannot be simultaneously accelerated and focused
    in all directions by one harmonic (the Panofsky-Wenzel / "no 3D stable synchronous point" result);
    remedy = time/space alternation (APF, alternating-gradient), i.e. the same trick as dynamic Paul/magnetic
    traps that Mach-Batlle mention for high-field seekers.
- Practical rule: the beam aperture a must be <~ beta gamma lambda/(2 pi). For a proton:
  | T_p | beta | 2 um laser | 10 um CO2 | 0.3 mm (1 THz) | 3 mm (100 GHz) | 0.85 m (352 MHz RF) |
  |---|---|---|---|---|---|---|
  | 100 keV | 0.0146 | 4.6 nm | 23 nm | 0.70 um | 7 um | 2.0 mm |
  | 3 MeV | 0.080 | 25 nm | 0.13 um | 3.8 um | 38 um | 11 mm |
  | 50 MeV | 0.31 | 0.10 um | 0.52 um | 15 um | 0.15 mm | 44 mm |
  | 1 GeV | 0.875 | 0.56 um | 2.8 um | 84 um | 0.84 mm | 0.24 m |
  | 6 GeV | 0.99 | 2.3 um | 11.7 um | 0.35 mm | 3.5 mm | 1.0 m |
  (computed: L = beta*gamma*lambda/(2*pi)). This table is why RFQs run at 100-400 MHz for keV-MeV protons,
  and why optical-wavelength near-field ("electric flying focus" on a chip) is only plausible for
  protons above ~100 MeV-1 GeV, or with THz drivers at MeV energies.
- Programmable velocity: for a phased array of independently timed sources with pitch p and inter-element
  delay tau, the pattern phase velocity is p/tau - arbitrary, including sub-luminal and *chirped*
  (accelerating) by varying tau along the array. Nothing in Maxwell forbids it; the price is purely the
  evanescent decay above (the sub-luminal pattern cannot radiate, so it is bound to the array).

### S5. Chlouba, Shiloh, Kraus, Brueckner, Litzel, Hommelhoff, "Coherent nanophotonic electron accelerator",
Nature 622, 476-480 (2023), DOI 10.1038/s41586-023-06602-7  [abstract only + press quotes]
- APF DLA with silicon pillar macrocells, 120 deg phase jumps between macrocells alternate transverse
  focusing/defocusing while keeping acceleration. 28.4 keV electrons (beta ~0.32) -> +12.3 keV (43%) over
  ~500 um in a 225 nm channel [abstract only]. Average ~25 MV/m [inference/estimate: 12.3 keV/500 um].
  Authors project GeV/m with high-damage dielectrics [press].
- Relevance: first demonstration that a **tapered, phase-programmed near-field** can accelerate *and*
  confine a sub-relativistic beam over many periods - i.e. a working "programmable-velocity electric
  structure", but for electrons at beta 0.32-0.38, not protons at beta 0.01-0.1.

### S6. Broaddus et al. (Stanford, Byer/Solgaard/Leedle/Niedermayer), "Subrelativistic alternating phase
focusing dielectric laser accelerators", PRL 132, 085001 (2024), arXiv:2310.02434  [abstract only]
- Two silicon pillar arrays pumped symmetrically by pulse-front-tilted beams (pulse-front tilt = optical
  way of making the drive "arrive" in sync with a slow particle along the structure). Interaction length up
  to 708 um, energy gain up to 23.7 keV (25% increase from ~96 keV), design gradients 35 and 50 MeV/m.
- [inference/estimate] Pulse-front tilt (PFT) is the DLA analogue of a transverse flying focus: the
  laser intensity sweeps along the structure at a programmable speed so a short pulse can drive a long
  structure. The project's "transverse flying focus" idea and DLA-with-PFT are the same optical primitive.

### S7. DLA review, gradients and efficiency theory
- England et al., "Dielectric laser accelerators", Rev. Mod. Phys. 86, 1337 (2014) [abstract only]; covers
  damage thresholds, structures, efficiency.
- Hanuka & Schaechter (Technion), PRAB 2018 operating-regime analysis [abstract only, search snippet]:
  gradients ~1-6 GV/m with **20-80% laser->beam efficiency** feasible *in theory* when the beam is heavily
  loaded (many bunches / recirculated laser); max gradient and max efficiency occur at different points;
  beam loading may allow ~10 GV/m. Damage fluence ~2 J/cm^2 for < 0.4 ps pulses, > 5 J/cm^2 above ~10 ps.
- Experimental relativistic DLA gradients: ~0.3 GV/m (Peralta et al., Nature 503, 91 (2013)) up to ~0.85 GV/m
  (Cesar et al., Commun. Phys. 2018) [inference/estimate: recalled from prior knowledge, not re-fetched];
  "around 1 GV/m, damage-limited" [abstract only, snippet].
- [inference/estimate] Demonstrated laser->electron energy efficiency in DLA experiments is tiny
  (~1e-6 to 1e-4, because a fC-scale or single-electron beam is driven by uJ pulses). High efficiency requires
  the beam to extract a large fraction of the stored near-field energy: N_e e G L ~ U_laser. For a 100 nm
  channel this means very low charge per bunch, so high efficiency needs very many parallel channels and
  MHz-GHz bunch trains with laser recycling.

### S8. THz-driven acceleration
- Nanni et al., "Terahertz-driven linear electron acceleration", Nat. Commun. 6, 8486 (2015), arXiv:1411.4709
  [abstract only]: dielectric-loaded circular waveguide, 60 keV DC-gun electrons gain 7 keV over 3 mm
  (~2.3 MV/m average). Authors argue THz structures could in principle serve electron *or proton*
  accelerators with simple structures, high rep rate and significant charge.
- Sharma, Tibai, Hebling (2016), "Intense tera-hertz laser driven proton acceleration in plasmas"
  [abstract only]: PIC, near-critical H plasma driven by intense THz; a plasma scheme, not a structure.
- Low-beta RF (microwave) hadron structures using the first negative spatial harmonic, target >= 50 MV/m
  [abstract only, snippet] - compact hadron-therapy linacs.
- [inference/estimate, prior knowledge, not re-fetched] Later THz results: segmented THz electron
  accelerator (STEAM, Zhang et al., Nat. Photon. 2018) and relativistic THz acceleration (Hibberd et al.,
  Nat. Photon. 2020) reached ~10-100 MV/m class fields; optical->THz conversion in LiNbO3 tilted-pulse-front
  sources is ~0.1-1% (few % record at cryogenic temperature). So THz drivers inherit a ~1e-2 wall-to-THz
  penalty on top of THz->beam coupling. No THz proton accelerating structure found in the literature.

### S9. Existing "moving potential well" technologies (search: no hit for "electric flying focus")
- No literature found using the phrase "electric flying focus" or "programmable-velocity electric field"
  for accelerators [search result, 2026-11-03].
- **Traveling-wave (TW) ion guides / TW ion mobility** (Waters "T-wave", SLIM devices; patents e.g.
  US 9799503 "Traveling-well ion guides") [abstract only, patents]: DC potential wells move along a stack of
  electrodes by sequencing voltages; RF on alternate electrodes provides radial confinement (Earnshaw
  workaround). Ions "surf" if the wave speed is not too high. Speeds ~1-1000 m/s, fields ~V/mm, energies eV.
- **Traveling-wave Stark decelerators** (Meijer/Fritz-Haber group: Osterwalder et al. 2010; Lewandowski
  group JILA) [abstract only]: ring electrodes driven by sinusoidal voltages with **chirped frequency**
  create true 3D traps that move at a programmable, continuously varying velocity (decelerate polar
  molecules from ~300 m/s to rest). This is literally an "electric flying focus" - a moving trap built by
  surrounding sources with programmed timing. It works in 3D because neutral low-field-seeking molecules
  sit at a *minimum* of |E|, which Laplace allows; a charged particle needs a potential minimum, which
  Laplace forbids in the co-moving frame, hence the RF/APF trick.
- [inference/estimate] Scaling of such electrode-array schemes: wave speed v = f * period. To reach proton
  speeds (beta 0.01-0.5, i.e. 3e6-1.5e8 m/s) with mm-scale electrodes you need GHz drive -> it becomes an RF
  slow-wave structure (Wideroe/IH/DTL). The electrode-array "flying focus" at proton speeds already exists:
  it is the RF linac with its cell-length taper (fixed velocity programme baked into hardware). The only
  genuinely new degree of freedom an optical/electronically phased array offers is **re-programmability**
  of the velocity profile and the ability to use many independent short-pulse sources.

### S10. Near-field plates / superoscillation / inverse-designed sources
- Grbic, Jiang, Merlin, "Near-field plates: subdiffraction focusing with patterned surfaces", Science 320,
  511 (2008), DOI 10.1126/science.1154753 [abstract only + press]: a modulated-reactance surface
  (interdigitated capacitors) focuses 1.027 GHz (30 cm) to ~lambda/20 (1.5 cm) - at a distance *within the
  near field* of the plate (focal distance << lambda). Theory: Merlin, Science 317, 927 (2007).
- [inference/estimate] Near-field plates and superoscillatory lenses obey the same trade-off as the
  Mach-Batlle replicator: sub-wavelength feature size s at distance d costs ~exp(2 pi d/s) in source
  amplitude/energy and makes the result exquisitely sensitive to errors. For acceleration the relevant
  "feature" is the synchronous period beta*lambda, giving the exp(-2 pi d/(beta gamma lambda)) rule above.
  These techniques cannot evade it; they can only choose which harmonic content arrives.
- Inverse design [inference/estimate, prior knowledge not re-fetched]: Sapra et al., "On-chip integrated
  laser-driven particle accelerator", Science 367, 79 (2020) - adjoint-optimised silicon DLA with
  waveguide-integrated drive, ~0.9 keV gain over 30 um (~30 MV/m) for 83 keV electrons; Hughes et al.,
  PR Applied 2018 (adjoint inverse design of DLA power delivery). Inverse design maximises
  G/E_max (synchronous gradient per peak surface field) - exactly the figure of merit for the slow-proton
  problem.

### S11. Dielectric Wall Accelerator (DWA), LLNL (Caporaso et al., ~2007-2010) - the closest existing
"electric flying focus"  [abstract only / talks / Wikipedia; OSTI 923108, 970674; PAC2009 TH3GAI02]
- Stack of fast pulse-forming (Blumlein) lines behind a high-gradient insulator (HGI) bore; each line is
  closed by a laser-triggered SiC photoconductive switch. "**Virtual traveling wave**": the accelerating
  field pulse is not a propagating guided wave but is locally re-excited by each line, and **the switch
  timing sets the propagation speed** - i.e. programmable, sub-luminal, accelerating velocity profile for
  protons [abstract only/talk].
- Numbers: target ~100 MV/m average for compact proton therapy (~150-250 MeV) [talk]; HGI samples held
  100 MV/m for few-ns pulses [talk]; SiC switch that closes and opens demonstrated at 27.5 MV/m [talk];
  2-m strawman with ~60 MV/m average, 120 MeV nominal proton bunch [paper snippet, 2010]. No full-system
  100 MV/m demonstration found; no results after ~2010 found [search].
- [inference/estimate] Physics: ns pulses -> wavelength ~0.3 m >> bore (cm), so this is the **quasi-static,
  Laplace-equation regime - exactly Mach-Batlle's regime**. The wall potential pattern of axial length l
  penetrates the bore as I0(2 pi r/l)^-1, so l must be >~ bore radius; the field in the bore is bounded by
  the HGI surface field (maximum principle). The concept failed to reach target mainly on hardware
  (switch jitter/lifetime, insulator flashover, energy storage), not on field physics [inference from
  status; program believed discontinued ~2011-2013, not verified].
- [inference/estimate] Efficiency: stored energy in each Blumlein is mostly *not* taken by a low-charge
  proton bunch; laser->proton efficiency is dominated by line energy -> beam coupling (beam loading).
  For high-current pulses (induction-linac-like) this can be 10s of %; for therapy-level charge (~nC) it is
  low.
- Induction linacs [inference/estimate, prior knowledge]: ~0.2-1.5 MV/m, efficiency to beam up to ~30-50%
  at kA currents (e.g. DARHT, ATA, heavy-ion fusion driver studies); velocity programme set by cell timing.
  They are the "efficient but low-gradient" end of the same family.

### S12. Plasma gratings / photonic-crystal accelerators (search, background only)
- Plasma Bragg gratings form where two pump pulses cross in underdense plasma (ponderomotive) [abstract
  only]; Lehmann & Spatschek, Phys. Plasmas 2017+ "laser-driven plasma photonic crystals" [abstract only,
  not read]. An "oscillating plasma grating accelerator" thesis (Strathclyde) sets plasma-wave phase speed
  by grating wavenumber and CO2 laser frequency [abstract only]. Dual-grating dielectric / photonic-crystal
  DLAs slow the phase velocity to match the particle [abstract only]. No 2023-2026 plasma-grating *ion*
  accelerator found.
- Cross-reference: this repo's docs/research/new-ideas-surface-plasmon-and-pv.md (Lei et al., PRL 137,
  105002 (2026)) already found that a tube surface plasmon's on-axis field falls as 1/I0(kR/gamma) and
  is usable only for protons >~1 GeV - the same evanescent rule derived here.

---------------------------------------------------------------------------------------------------------

## Physics limits (task 3)

1. **Static (Laplace/Earnshaw)** [paper S1 + standard theory]: in a charge-free region phi is harmonic, so
   phi has no interior extremum and |E| has no interior maximum (|E|^2 is subharmonic). No electrostatic
   3D trap for a charged particle; the strongest field is always on the boundary. Mach-Batlle's
   "source at a distance" respects this through a divergent annulus and exponentially large boundary
   currents.
2. **Synchronous fields are static in the particle frame** [inference/estimate, standard]: a wave with phase
   velocity v_p = beta c is electrostatic in the frame moving at beta c, so (1) applies in that frame:
   decay kappa = omega/(beta gamma c), and no simultaneous longitudinal + transverse stability from a single
   synchronous harmonic (Panofsky-Wenzel/Earnshaw). Escapes: (a) time-alternation in the particle frame -
   APF (alternating phase focusing; demonstrated S5, S6), alternating-gradient quadrupoles, RFQ's
   electric quadrupole focusing, ponderomotive (second-order) focusing from non-synchronous harmonics
   (the "Paul trap" route); (b) space charge/plasma (ion channel, plasma lens). These are all
   time-dependent fields seen by the particle, which is why Earnshaw does not forbid them.
3. **Gradient limits** [mix]:
   - Normal-conducting RF ~ 50-100 MV/m surface/accelerating at GHz (CLIC ~100 MV/m with ~200 ns pulses);
     proton linacs operate far lower: RFQ ~1-3 MV/m average energy gain per length (surface ~30-40 MV/m,
     Kilpatrick-limited), DTL/SC cavities ~3-20 MV/m [inference/estimate, prior knowledge].
   - Pulsed-power insulators (DWA): ~100 MV/m for few-ns pulses on samples (S11 [talk]).
   - Dielectric at optical frequencies: peak surface fields 1-10 GV/m for sub-ps pulses
     (fluence ~2 J/cm^2), experimental DLA gradients ~0.3-0.85 GV/m (S7).
   - Plasma: no damage limit, wakes 10-100 GV/m (repo's main line).
   - But for slow particles the *usable* gradient is G = (G/E_wall) * E_wall with
     G/E_wall <~ 1/cosh(a/L), L = beta gamma lambda/2pi, times a structure factor (~0.1-0.5, worse for
     higher spatial harmonics). Check against S4: a = 17.5 nm, L = 4.65 nm -> 1/cosh = 0.046; with n=3
     harmonic and structure factor ~0.2, G/E ~ 0.009 vs. the paper's 34 MV/m/4 GV/m = 0.0086. Consistent.
4. **Phase velocity of a near field is set by drive timing** [inference/estimate, standard; DWA S11 is the
   experimental precedent; PFT-DLA S6 is the optical precedent]: for N independently driven elements with
   pitch p_i and trigger delays t_i, the local pattern speed is v(z) = dz/dt = p_i/(t_{i+1}-t_i). Any
   v < c (and even v > c) is allowed; chirping the delays gives an accelerating pattern with no hardware
   change. A sub-luminal pattern has k_z > omega/c so it is non-radiating and evanescent: it cannot be
   delivered from far away (no "remote" electric flying focus in vacuum), only from sources within ~L.
5. **Efficiency/coupling** [inference/estimate]: the energy the beam can take per unit length is at most the
   near-field energy per length in its reach. Example: E = 1 GV/m over a 1 um x 10 um vacuum channel stores
   ~9e-5 J/m; a 1 GV/m proton bunch depletes it at q ~ 0.09 pC (~5.5e5 protons) per optical microbunch per
   channel. Laser energy is also stored in the dielectric and in non-synchronous harmonics (typically
   3-30x the synchronous part), so single-pass laser->proton efficiency with realistic charge is
   ~1e-4 - 1e-2 unless (i) the laser is recycled (resonant/ring cavity, Siemann/Na/Byer intracavity
   concept), (ii) many parallel channels share a drive, (iii) charge per channel approaches the beam-loading
   limit. Theory papers (S7) allow 20-80% only in that regime. For slow protons the useful stored energy
   fraction is further reduced by (G/E_wall)^2 ~ (1/cosh(a/L))^2.

### The "wavelength ladder" design rule (main take-away) [inference/estimate]
Requiring an aperture a ~ L = beta gamma lambda/2pi (so G/E_wall ~ 0.65) gives lambda_max ~ 2 pi a/(beta gamma).
For a practical aperture that carries useful charge (a >= ~1 um on chip, >= ~1 mm in a beam pipe):
- 50 keV - 3 MeV: lambda >~ 0.1-1 m -> RF (RFQ, 100-400 MHz). Optical/THz near fields are useless here.
- 3 - 100 MeV: lambda ~ 1-30 mm (10-300 GHz) for mm-scale bores, or ~0.3 mm THz for ~10 um channels;
  quasi-static ns-pulse wall-driven structures (DWA) also fit.
- 100 MeV - 1 GeV: mid-IR (5-10 um) dielectric/plasma near fields with ~1-3 um channels become viable
  (G/E_wall 0.5-0.9).
- > 1 GeV: near-luminal; ordinary DLA (2 um) or plasma wakes; velocity matching is a small correction.
This makes the honest answer to the user's question: an "electric flying focus" exists only as a
wall-bound travelling evanescent pattern with programmable timing; its reach shrinks with beta, so it
must be implemented with a driver wavelength that grows as the proton slows down.

---------------------------------------------------------------------------------------------------------

## Answer to the question (summary) [inference/estimate unless tagged]
- Citation verified: R. Mach-Batlle, M. G. Bason, N. Del-Valle, J. Prat-Camps, PRL 125, 177204 (2020)
  [paper]. It does *not* create a free-space field maximum. It creates a replica source whose field is
  correct outside a divergent annulus, and the required current grows exponentially, as (d'/R2)^nT [paper].
- The electric analogue exists mathematically: same Laplace equation, an eps = -1 shell, and negative eps
  occurs naturally in metals/plasmas at optical frequencies. But a field maximum created at a distance and
  then moved is forbidden. What is allowed, and already exists in several forms, is a **travelling,
  wall-bound, evanescent field pattern whose speed is set by the timing of the surrounding sources**.
  Examples: the RF linac cell taper, the DWA virtual travelling wave (switch timing) [talk], travelling-wave
  Stark decelerator traps (chirped frequency) [abstract only], and pulse-front-tilted APF DLAs [abstract only].
- In the particle's rest frame this pattern is electrostatic, so Mach-Batlle's cost law becomes
  E_wall/G >~ cosh(a/L), with L = beta gamma lambda/2pi. This explains quantitatively why the only proton
  DLA design (100 keV, 2 um) gets 34 MV/m from 4 GV/m peak fields [paper S4]. It also dictates a
  "wavelength ladder": RF below ~3 MeV, mm-wave/THz/ns-pulsed walls for ~3-100 MeV, mid-IR near fields
  above ~100-200 MeV, near-luminal DLA/plasma above ~1 GeV.

## Proposed concepts

Numbers: "lit" = from the sources above; "est" = my estimate.

### C1. Laser-switched virtual-travelling-wave wall accelerator ("electric replicator linac")
- Principle: a modern DWA. A stack of thin pulse-forming lines/cells sits behind a high-gradient-insulator
  bore. Each is closed by a laser-triggered photoconductive switch (SiC/GaN/diamond). The trigger laser's
  delay line programmes the pattern speed v(z) to track the proton (chirped delays). The step beyond the
  classic DWA is Mach-Batlle-style harmonic synthesis: several electrodes per wavelength, with independently
  timed amplitudes, shape E_z(r,z,t) in the bore and add APF/alternating radial focusing.
- Energy range: ~2-200 MeV (quasi-static regime, ns pulses, cm bore; the aperture rule is easily met).
- Gradient: lit target 100 MV/m, 2-m strawman ~60 MV/m average [talk]; est. realistic 20-50 MV/m.
- Efficiency: est. wall-plug -> stored line energy 50-70%; line -> beam 1-30%, depending on current
  (beam loading). The laser only triggers switches (mJ), so it is *not* in the energy path. Est. overall
  1-20%: 10-1e4 x better than laser-driven slow drivers, comparable to or below RF linacs.
- Risks: insulator flashover at 100 MV/m, switch jitter (needs <~50-100 ps est.), switch lifetime at high
  rep rate, recovering unused line energy. History: the programme stalled ~2010 [search].
- Compared with RF: 3-10x the gradient of DTL/RFQ, re-programmable velocity, no klystrons; but no
  demonstrated system. Compared with laser-plasma: far lower gradient, far better efficiency.

### C2. Optically timed THz near-field array for 1-100 MeV protons
- Principle: a dielectric-lined slab channel (10-100 um gap) fed by a line of THz emitters (tilted-pulse-
  front LiNbO3 segments or large-area photoconductive antennas). The same laser fires each emitter with a
  programmable delay ("STEAM-like" segmentation, but for slow particles). The synchronous spatial harmonic
  has v = p/tau.
- Energy range: 1-100 MeV (at 0.3 mm wavelength, L = 4-16 um for 3-50 MeV -> gaps ~10-30 um).
- Gradient: est. 20-100 MV/m (THz structure fields ~0.1-1 GV/m, G/E 0.1-0.5).
- Efficiency: est. 1e-5 - 1e-3 (optical->THz 1e-3-1e-2 [prior knowledge], THz->proton <=0.1 with tiny
  charge). Same order as laser-plasma slow drivers; worse than RF.
- Risks: THz conversion efficiency, tiny charge per channel, emitter synchronisation, dielectric damage.
- Comparison: offers programmability but loses to RFQ/DTL on efficiency. Only interesting if a
  compact, low-charge front end is wanted.

### C3. Pulse-front-tilt-driven, inverse-designed APF proton DLA ("optical electric flying focus on chip")
- Principle: double pillar/grating arrays in Si, diamond or ZnSe, driven at lambda = 2-10 um by a
  pulse-front-tilted (or transverse-flying-focus) laser whose sweep speed matches the proton. The period
  taper plus the PFT programme the velocity. APF macrocells provide 3D confinement, and inverse design
  maximises G/E_max at each beta. Many parallel channels share one drive, and the laser is recycled
  through a ring/cavity.
- Energy range: ~0.2-3 GeV (beta 0.57-0.97). At 1 GeV with lambda = 10 um, L = 2.9 um, so 1-2 um channels
  give G/E_wall ~0.7-0.9 (est.). Not useful below ~100 MeV.
- Gradient: lit electron DLA 0.3-0.85 GV/m measured [prior knowledge], 1-6 GV/m in theory (S7); est. for
  protons 0.2-1 GV/m.
- Efficiency: lit theory gives 20-80% only when heavily beam-loaded (S7). Est. single-pass with realistic
  charge 1e-4-1e-3; with laser recycling and parallel channels 1e-2-1e-1. The beam-loading charge is
  ~0.1 pC per microbunch per channel (est., Physics limits #5).
- Risks:
  * Acceptance: needs nm-rad-class emittance, so a 200 MeV proton beam from a plasma stage or linac must
    be matched into um channels.
  * The proton flux this project needs likely means 1e4-1e6 channels.
  * Damage at high average power, metre-scale alignment, wakefields/beam break-up in um channels.
- Comparison: 10-50x the gradient of SC RF, ~10x below plasma. Velocity matching is passive and exact.
  Potentially much better efficiency than laser-plasma slow drivers in this beta range.

### C4. Laser-imprinted chirped plasma grating in a hollow channel ("plasma slow-wave wall")
- Principle: a hollow plasma channel whose wall density carries an axial grating with chirped period
  Lambda(z) = n lambda0 beta(z), written by interfering ionising beams (or a swept/transverse flying focus).
  A long-wave driver (CO2, 10 um) guided in the channel scatters off the grating into a synchronous
  harmonic with v_p = beta c. The plasma wall tolerates >>10 GV/m (no damage limit).
- Energy range: ~0.3-6 GeV (the repo's tube plasmon/evanescent analysis says >~1 GeV is comfortable).
- Gradient: est. wall fields 10-30 GV/m x G/E 0.3-0.8 -> 3-20 GV/m (unverified).
- Efficiency: est. 1e-3-1e-2 (most of the driver stays in the guided mode; grating coupling is weak).
- Risks: grating lifetime (ion motion smears it in ~ps), wall heating/expansion, hollow-channel beam
  break-up, survival at rep rate, phase stability of the imprint.
- Comparison: competes directly with the repo's guided beat train and flying-focus wakes. Its advantage is
  that the phase velocity is imprinted (programmable) rather than set by a group or beat velocity.

### C5. Hybrid "wavelength-ladder" machine (an architecture, not a device)
- Chain: RFQ (50 keV-3 MeV, 352 MHz, lit standard) -> C1 virtual-TW wall or conventional DTL/SC linac
  (3-200 MeV) -> C3 mid-IR DLA or C4 plasma wall (0.2-1 GeV) -> plasma wake stage to 6 GeV.
- Principle: in every section the driver wavelength satisfies lambda >~ 2 pi a/(beta gamma), so G/E_wall
  stays above ~0.5. Efficiency est.: set by the lowest-efficiency section that carries the most energy
  gain. What matters is putting the bulk of the energy gain (1-6 GeV) in a near-luminal, efficient stage.
- Comparison: makes explicit that no single "electric flying focus" should span 50 keV -> 6 GeV. The slow
  end belongs to RF (efficient, mature); the laser-driven parts belong only where beta > ~0.5.

## Proposed simulations

### Sim 0 (all concepts): "Mach-Batlle for accelerators" - analytic/semi-analytic limit map
- Code: Python/numpy/scipy. A 2D slab and axisymmetric modal solution of (nabla^2 + omega^2/c^2)E = 0 in
  a vacuum channel. Least-squares (Tikhonov) synthesis of the wall field/potential that yields a target
  synchronous E_z on axis, as Mach-Batlle did for the wire (truncated harmonic series).
- Output: minimum E_wall/G vs (beta, lambda, aperture) and the cost of sharpening/focusing harmonics; a
  "wavelength ladder" plot; a check against S4 (34 MV/m from 4 GV/m).
- Proves/disproves: whether any concept can reach its claimed G within damage limits.
- Cost: laptop CPU, minutes.

### Sim C1: quasi-static switched-wall linac
- Code: axisymmetric finite-difference/FEM Laplace solver (Python, or Elmer/FEniCS) with N = 200-2000
  ring electrodes. Their potentials follow programmed switch waveforms (rise ~0.2-1 ns). RK4 proton
  tracking 3 -> 50 MeV, Monte-Carlo switch jitter, and optionally a Meep cylindrical full-wave run to check
  that the quasi-static approximation holds.
- Geometry: bore radius 5-10 mm, cell pitch 2-5 mm, HGI surface field capped at 100 MV/m.
- Proof quantities:
  * the pattern velocity tracks beta(z) (error < 1%);
  * average gain >= 30 MV/m with E_wall <= 100 MV/m;
  * longitudinal capture fraction and transverse stability with APF;
  * energy per pulse in the lines vs beam energy (efficiency vs current);
  * jitter tolerance.
- Cost: laptop CPU, minutes to a few hours.

### Sim C2: THz phased array
- Code: Meep FDTD (2D first, 3D later) with a row of independently timed THz sources (0.3-1 THz) along a
  dielectric-lined slab. Extract the synchronous harmonic amplitude and its phase velocity vs z, then
  track protons (3 -> 10 MeV) in the recorded fields.
- Proof: v_p(z) follows the programmed delays, G/E_max >= 0.1, G >= 20 MV/m at realistic THz pulse energy
  (uJ-mJ), and the THz->proton energy fraction.
- Cost: 2D on a laptop, 1-10 CPU-hours; 3D 50-500 core-hours or 1-5 GPU-hours (Tidy3D/Meep-MPI), ~$5-30.

### Sim C3: inverse-designed APF proton DLA (top priority, see below)
- Code, in three steps:
  1. 2D FDFD/FDTD adjoint inverse design (Meep adjoint or ceviche/SPINS) maximising G/E_max of the
     synchronous harmonic. Cases: beta = 0.6, 0.8, 0.9 at lambda = 2 um (Si) and 10 um (ZnSe/diamond/Ge),
     gap 1-3 um, fabrication constraints (min feature 100 nm).
  2. A 2D FDTD run with a pulse-front-tilted 100 fs-1 ps pulse over 100-1000 periods.
  3. 6D proton tracking (custom Python or DLAtrack6D-style macro-cell transfer maps) through tapered APF
     macrocells over 1 mm-10 cm (e.g. 200 -> 210 MeV), with a beam-loading/energy-balance estimate.
- Proof quantities:
  * G/E_max >= 0.3 at beta 0.6-0.9;
  * G >= 0.3 GV/m at E_max <= 2 GV/m;
  * transmission > 50% with emittance growth < 2x over > 1 cm;
  * laser->proton efficiency vs charge per channel (target > 1e-2 with recycling).
- Cost: 2D inverse design + tracking on a laptop CPU, ~2-24 CPU-hours. 3D verification of the final cell:
  1 cloud GPU for ~2-6 h (~$5-30), or 100-500 CPU core-hours.

### Sim C4: chirped plasma grating in a hollow channel
- Code: FBPIC quasi-3D (already running on Modal GPU in this repo). Setup: a hollow channel with an
  imposed axial wall-density modulation (chirped period), a guided CO2 (10 um) driver, and proton test
  particles at beta 0.6-0.95. Follow up with Smilei/WarpX 2D with mobile ions to get the grating lifetime.
- Proof: synchronous on-axis E_z amplitude, and v_p tracking the target beta(z); proton energy gain per mm;
  driver depletion -> laser->proton efficiency; grating survival time vs ion mass/temperature.
- Cost: 1-4 GPU-hours per run, ~10 runs -> ~$20-100 on Modal A100/H100.

### Sim C5: system model
- Code: a Python spreadsheet plus 1D longitudinal tracking, with stage gradients/efficiencies from
  Sims 0-C4.
- Proof: total wall-plug->6 GeV efficiency and length vs the repo's plasma-only baseline.
- Cost: laptop, minutes.

## Recommendation (which to try first)
1. **Sim 0 first** (laptop, < 1 hour). It is nearly free, decides which concept can work in which energy
   band, and turns the Mach-Batlle analogy into a quantitative design rule for the repo.
2. **Then Sim C3 in 2D** (laptop, ~1 day of CPU; 3D check ~$5-30 GPU): an inverse-designed, PFT-driven APF
   proton DLA at beta 0.6-0.9, lambda 2-10 um. Reason: 0.2-1 GeV is where the repo's plasma options are
   weakest (the driver must be sub-luminal; efficiency 1e-3-1e-5), and where an optical "electric flying
   focus" is physically allowed (G/E_wall 0.5-0.9). A result of G/E_max >= 0.3 with stable APF transport
   would justify C3/C5. G/E_max << 0.1 would rule out optical near-field options for protons below 1 GeV.
3. Sim C1 is the cheapest physics check for the low-beta end (laptop, hours), but its open questions are
   hardware (switches, flashover), so simulation proves less there. Sim C4 reuses the existing FBPIC/Modal
   setup and is the natural next GPU job if C3 looks promising but its channel/charge limits are too tight.
- Bottom line [inference/estimate]: below ~100 MeV, no electric-near-field concept found here beats
  RFQ/DTL on efficiency. The "electric flying focus" idea adds most value as a programmable-velocity
  booster at beta ~0.5-0.95.
