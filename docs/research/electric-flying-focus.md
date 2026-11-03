# Electric flying focus — the electric version of "Tailoring magnetic fields in inaccessible regions"

Focused redo (2026-11-03). Question: Mach-Batlle et al. used active currents on a surface to make
the field of a *virtual* source appear where no source can be placed. Can ring electrodes around a
proton beam do the same with electric fields — a virtual charge that travels with the protons at a
programmable, accelerating speed ("electric flying focus") — and would that make a good
accelerator for this project? Labels: [paper] full text read, [abstract]/[report] partial,
[sim] our simulation (S046), [est] estimate built on simulated numbers, [inference] our reasoning.

The earlier, broader review (wavelength ladder, dielectric laser accelerators, THz, plasma
gratings) is kept as a side note in `electric-field-tailoring.md`.

## 1. Literature (focused)

**Mach-Batlle, Bason, Del-Valle, Prat-Camps, PRL 125, 177204 (2020)** (arXiv:1912.12477) [paper, ar5iv text]
- A long cylindrical shell with μ = −1 acts as a magnetostatic perfect lens: a wire at distance d
  from the centre appears at d′ = d·R₂²/R₁². If d′ > R₂ the replica sits in empty space.
- μ = −1 cannot be passive in statics, so the shell is replaced by surface currents. The simplified
  device is a central wire plus one surface current K(φ) = Σₙ (I/πR₂)(d′/R₂)ⁿ cos nφ, truncated at
  n_T terms. In the experiment: R₂ = 40 mm, replica at 60 mm, n_T = 10, 20 wires, fluxgate
  measurements matching calculation.
- The replica's field is exact only beyond the replica. Between the device and the replica the
  ideal field diverges, so no free-space maximum forms (Earnshaw's theorem is respected). The
  current needed grows as (d′/R₂)^n_T: more fidelity, or a source further away, costs exponentially
  more current.
- Static/low-frequency (≲100 MHz claimed). The authors note no electric analogue.

**Active control of Laplace fields** [abstract/intro]: Guevara Vasquez, Milton, Onofrei — active
exterior cloaking (PRL 103, 2009; arXiv:1105.1221, 1109.3526, 1109.4182); Norris et al. 2012
(multipole arrays). Same mathematics as Mach-Batlle: approximating a harmonic function with sources
outside the region. The achievable region is limited by the convergence of the expansion. The
minimum-energy source density can be found with layer potentials.

**Negative permittivity in electrostatics** [abstract]: image theory for ε < −1 spheres diverges
and needs regularised images (Majić, arXiv:1901.05957). Quasi-static Veselago lens analysis
(arXiv:1405.3885). As with μ, static ε = −1 must be emulated with active charges, i.e. electrodes.

**Dielectric Wall Accelerator (DWA), LLNL** (Caporaso, Chen, Sampayan et al., 2007–2011) [report]
— the closest existing electric flying focus. Fast switches fire transmission lines in sequence
along an insulating wall, making a "virtual travelling wave" whose speed is set by the firing
times, so it can follow a proton as it speeds up. Insulator flashover strength rises for shorter
pulses. The on-axis field falls below the wall field if the pulse is too short. Focusing used
alternating phase. Design ~60 MV/m average over 2 m, 120 MeV ±2 %; not completed as a product.

## 2. Theory — what an electric "virtual charge" can and cannot do

T1. **Proton-frame electrostatics** [standard physics]. A field pattern moving rigidly at v obeys
∇⊥²φ + γ⁻²∂ξ²φ = 0, which is Laplace's equation in the proton's frame. Each axial Fourier
component k of the wall field reaches the axis multiplied by 1/I₀(ka/γ).

T2. **No amplification into the inaccessible region** [standard physics; S046 Part A/B]. The bore
holds no charge, so the field there is harmonic: by the maximum principle the axial field on axis
can never exceed the largest wall field. A Mach-Batlle-style replica of a charge *inside* the bore
reproduces its field only on the axis side of the virtual charge. Driving it needs wall amplitudes
∝ I₀(ka)K₀(kr_v), growing like e^{k(a − r_v)}. That is the analogue of the paper's (d′/R₂)^n_T
cost, and it diverges as the virtual charge approaches the axis. The trick reshapes fields; it
cannot concentrate them. The best gradient per unit wall field (→ 1) comes from the *opposite* of
a point charge: a long, flat moving field region (length ≳ 4γa).

T3. **Programmable velocity is free** [S046 Part C]. The pattern's speed is just the firing
schedule, so any velocity history works, including from ~1 MeV upwards where lasers and plasma
waves cannot follow (this project's hardest problem). Longitudinal phase stability puts the
protons on the falling front edge. There the field also defocuses transversely
(Earnshaw/Panofsky), so external focusing is mandatory.

T4. **Efficiency = beam loading × energy recovery** [S046 Part D]. A pulsed electric pattern must
create its field energy (bore + electrode/insulator region) once per bunch along the whole machine.
The beam can take only Q·E per metre. At low energy the bunch charge is capped by space charge
(∝ γ², ∝ focusing strength), so the beam takes a tiny fraction unless the unused field energy is
recovered. A resonant store that keeps energy between bunches is, in effect, an RF cavity.

## 3. Simulation results (S046, `sims/phase1/e1_electric_flying_focus.py`)

Data: `results/data/E1_electric_flying_focus.json` · figure `results/figures/E1_electric_flying_focus.png`.

- **A. Replicator cost [sim, exact Laplace].** Reproducing a virtual ring charge at r_v inside a
  bore of radius a, to ≤3 % on-axis error, needs a peak wall field of 12× (r_v = 0.75a), 28×
  (0.5a), 2×10⁴× (0.25a) and ~10⁹–10¹¹× (0.1a, still 5–10 % error) the on-axis field. Axis/wall is
  always < 1.
- **B. Best moving pattern [sim].** A flat-top field region moving with the protons transmits
  0.30 / 0.55 / 0.84 / 0.99 / 1.00 of the wall field to the axis for lengths 0.5 / 1 / 2 / 4 / 8 γa.
- **C. Tracking [sim, 6D, paraxial quasi-static fields].** 2 mm-radius bore, 2 mm-pitch ring
  electrodes, 50 MV/m peak wall field, 20 mm flat-top with 10 mm edges (axis 38.5 MV/m;
  synchronous field 32.6 MV/m at 85 % on the front edge). Result: 1 → 100 MeV in 3.04 m,
  **100 % captured**, relative energy spread 0.1 %. Random firing-time jitter of 0 / 2 / 10 / 30 ps
  changes nothing measurable: the edge is mm-long and each proton averages over many electrodes.
  Without external focusing all protons hit the wall. With focusing set to 3× the edge defocusing,
  the requirement at 1 MeV is equivalent to a 10.6 T solenoid or ~200 T/m smooth quadrupole
  gradient. That is demanding but within small-bore permanent-magnet quadrupoles [est], and it
  eases as protons speed up.
- **D. Energy [est on sim fields].** Field energy per energised metre at 50 MV/m: bore 0.14 J/m;
  vacuum-gap ring electrodes ~0.56 J/m total; DWA-style insulator wall ~8 J/m. A space-charge-limited
  bunch (100 T/m-equivalent focusing, 0.5 mm × 3 mm bunch) carries 29 pC at 1 MeV, 0.33 nC at
  100 MeV and 2.3 nC at 1 GeV. Wall-plug→beam with 70 % pulsed power, for a section whose bunch
  charge is set at its start:

  | section starts at | vacuum-gap rings | + 80 % field-energy recovery | DWA insulator wall |
  |---|---|---|---|
  | 1 MeV | 0.12 % | 0.6 % | 0.008 % |
  | 100 MeV | 1.4 % | 6 % | 0.09 % |
  | 1 GeV | 10 % | 31 % | 0.7 % |

## 4. What it means for the 6 GeV proton design [est]

- **As the slow front end** (1 MeV electrostatic injector → electric flying focus → guided laser
  train at 0.5 GeV; no RF, no laser slow section): system efficiency **0.9 %** without recovery and
  **1.9 %** with 80 % recovery, using the projected-fibre train (2.5 %). Compare the all-optical
  design's 1.0 % and RF injector + train 2.9 %. On a per-section basis the electric front end is
  comparable to the laser slow section without recovery (0.12 % vs 0.14 %, S041 inputs) and ~4×
  better with recovery (0.6 %). It also removes the
  least-proven step, self-injection from rest by a slow laser driver, and replaces it with
  well-understood pulsed-power hardware.
- **As the whole machine** it becomes a DWA-type linac at ~30–40 MV/m (≈150–200 m to 6 GeV). Its
  efficiency is set by beam loading and energy recovery, not by the velocity trick.
- **Answer to the question:** yes, an electric flying focus works as an accelerator, and the
  programmable velocity is its real asset. But the Mach-Batlle "field in an inaccessible region"
  feature gives no gain for acceleration: on-axis field ≤ wall field, and emulating a concentrated
  virtual charge only raises the wall field needed (and so the breakdown risk and stored energy).

## 5. Next simulations that would test this further (proposed)

1. Full-EM (FDTD/PIC) model of a ring-electrode cell with realistic switch waveforms and
   transmission-line feeds. Checks the quasi-static assumption (pulse durations 0.2–3 ns), the
   driver energy per pulse, and how much can be recovered.
2. Space-charge PIC of the 1–20 MeV section with a real permanent-magnet-quadrupole or
   alternating-phase-focusing lattice: the true charge limit and emittance growth.
3. Breakdown data review/experiment for ns-pulsed vacuum gaps at 50–100 MV/m (sets the gradient).
