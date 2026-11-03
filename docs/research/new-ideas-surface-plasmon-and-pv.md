# Additional ideas (2026-11-03): beat-driven surface plasmons and photovoltaic energy recovery

## 1. Laser-beat-driven surface-plasma (surface-plasmon) acceleration
- **Source:** B. Lei, H. Zhang, A. Bonatto, B. Liu, J. Resta-López, M. Zepf, G. Xia, C. Welsch,
  "Resonant Excitation of Surface Plasmon for Wakefield Acceleration by Beating GW Lasers on
  Smooth Cylindrical Surface", Phys. Rev. Lett. 137, 105002 (4 Sep 2026), DOI 10.1103/2dkn-db5z.
  Press: Cockcroft Institute, 14 Sep 2026. [abstract + press only; full text not accessible]
- **Claims [press/abstract]:** two lasers of different wavelength beat inside a smooth hollow
  (cylindrical) plasma–vacuum channel; the beat resonantly drives a surface plasmon whose field
  extends into the channel; curvature replaces gratings for phase matching and brings the plasmon
  phase velocity closer to c; tens of GV/m with few-GW drivers, sub-TV/m with tens–hundreds of GW;
  up to 10 MeV electron gain over 40 µm in 3D PIC; electrons only; not yet tested experimentally.
- **Our analysis (S040):** surface plasmons are intrinsically sub-luminal, but in a tube the slow
  branch needs R ≳ 3 c/ω_p(wall), and the on-axis field falls as 1/I₀(kR/γ): usable for protons
  ≳ 1 GeV (on-axis/wall 0.75–0.94), not for ≲ 300 MeV. Open questions needing PIC: driving a
  slow plasmon (co-propagating beats are ≈ luminal; mode beating could give Δk > Δω/c), field per
  GW, efficiency, repetition-rate survival of the channel wall, hollow-channel beam break-up
  (known issue from positron hollow-channel studies).

## 2. Monochromatic photovoltaic recovery of leftover laser light
- **Literature:** 68.9 % (GaAs thin film, single-wavelength, ~0.85 µm — record cited by the user);
  at ~1.07 µm the best demonstrated laser power converters reach 55 % (Broadcom 8-junction
  InGaAsP, Photonics 2025; 57.9–59.0 % on small chips at 35–69 W/cm²); ~45 % at 1.55 µm
  (Surrey); GaInAsP/InP at 1064 nm predicted ~40 % (Ioffe 2025). GaAs cannot absorb ≥ 0.9 µm.
  Thermodynamic limits for monochromatic, collimated light approach ~100 % in theory.
- **Our analysis (S039):** light that drove the wake is red- and blue-shifted far outside a cell's
  band (in-band fraction 77 % → 11–15 % at ~50 % absorption for a two-line drive; 96 % → 5 % for a
  short pulse), so PV yields on it drop to ~23 % (beat) or ~2.5 % (short pulse). Recovered
  electricity re-enters through the laser's own efficiency, bounding the gain at
  1/(1 − η_laser η_PV f_rec): ≲ 1.2× at 40 % laser / 55 % cells, ≲ 1.5× with ideal cells.
  Worth including (×1.04–1.18 in our designs), mainly for schemes that waste most light.
