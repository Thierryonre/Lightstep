# Sanford-Wang parametrisation of pi+/pi- production in p-Be (MiniBooNE fit to HARP/E910 data)

Source: MiniBooNE Collaboration, "The Neutrino Flux prediction at MiniBooNE", Phys. Rev. D 79, 072002 (2009),
arXiv:0806.1449, Section B "Sanford-Wang Fit to the Pion Production Data", Tables V (pi+) and VI (pi-).
Values transcribed by hand from the arXiv PDF on 2026-10-27 (check against the original before relying on them;
covariance matrices are in the paper).

Formula (Eq. 11), p = pion momentum [GeV/c], theta = pion angle [rad], pB = proton beam momentum [GeV/c]:

    d2sigma/dp dOmega = c1 * p^c2 * (1 - p/(pB - c9)) * exp( -c3 * p^c4 / pB^c5  - c6 * theta * (p - c7 * pB * cos(theta)^c8) )

Units: mb / (GeV/c sr) (as used by MiniBooNE/HARP). c9 = 1 fixed for pions.
Fitted data: HARP 8.9 GeV/c thin Be (30-210 mrad, 0.75-6.5 GeV/c), E910 6.4 and 12.3 GeV/c Be.
Validity: forward angles and p > ~0.5 GeV/c; extrapolation to low momentum / large angle (the region that matters
for stopped-muon production) is NOT constrained - use only for rough energy scaling, prefer Geant4/FLUKA for absolute
low-momentum yields.

Rough integration (my own, forward hemisphere only, sigma_inel(p-Be) ~ 210 mb assumed) gives
<n_pi-> per inelastic p-Be ~ 0.31 (3 GeV), 0.47 (5 GeV), 0.54 (6 GeV), 0.69 (8 GeV), 0.84 (10 GeV),
i.e. ~0.09-0.10 pi- per GeV of proton kinetic energy, slowly falling with energy.
