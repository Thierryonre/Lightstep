# Proton acceleration in laser wakes, and nanoparticle-assisted proton acceleration

Literature notes for the MCF project: an energy-efficient laser wakefield accelerator (LWFA) for **protons to ~6 GeV**.
Compiled 2026-10-27. Notes are added one source at a time.

Labels:
- **[paper]**: read from the full text (arXiv or open access).
- **[abstract only]**: only the abstract or a summary page was available.
- **[inference]**: my own derivation or reading between the lines, not a claim made by the source.

Background problem (from the task brief): in a conventional LWFA the wake phase velocity is about the laser group velocity (γ_p ≈ ω0/ωp ≈ 10–50). A proton near rest cannot be trapped unless it is pre-injected with γ ≈ γ_p (for γ_p = 20, that means a proton kinetic energy of about 18 GeV, more than the target). In the blowout regime the ion cavity defocuses positive particles.

---

## Sources

### S1. Shen, Li, Yu, Cary — "Bubble regime for ion acceleration in a laser-driven plasma" (2007) [abstract only]

- **Citation:** B. Shen, Y. Li, M. Y. Yu, J. Cary, *Phys. Rev. E* **76**, 055402(R) (2007). DOI: [10.1103/PhysRevE.76.055402](https://doi.org/10.1103/PhysRevE.76.055402). I found no arXiv version, and the APS page is paywalled. A companion proceeding, "Electron and ion acceleration in the bubble regime" (Shen, Li, Cary, PAC 2007, p. 127), also exists.
- **Abstract:** 3D PIC simulations show protons being trapped, bunched and accelerated by an "electron bubble-channel structure" when an intense laser propagates in a *high-density* plasma. Acceleration works better when the plasma is mostly heavier ions (**tritium**), because the slow, massive background ions keep a stable bubble with a large space-charge field. The authors interpret the results with a 1D analytical wake model of a three-component plasma (electrons, heavy ions, protons).
- **Key number, as quoted by Guo et al. 2024 (S2):** self-injection of *background protons* into a wake driven by a **Gaussian** pulse needs **I ≈ 10^23 W/cm², i.e. about 100 PW**, because a large focal spot is required. The code was very likely VORPAL (Cary is the VORPAL author; Nieter and Cary 2004 is cited) [inference].
- **Relevance:** This is the founding "self-injected proton in a bubble" result. It sets the brute-force threshold, about 100 PW, that later schemes try to lower with vortex or light-spring pulses, an RPA pre-stage, or external injection.

### S2. Guo, Zhang, Shen, Tajima — "10 GeV proton generation driven by 5 PW light spring pulses" (2024) [paper]

- **Citation:** Y. Guo, X. Zhang, B. Shen, T. Tajima, *High Power Laser Sci. Eng.* **12**, e72 (2024). DOI: [10.1017/hpl.2024.72](https://doi.org/10.1017/hpl.2024.72). Open access (CC-BY 4.0); I read the full PDF.
- **Scheme:** a "light spring" (LS) pulse: a coherent sum of N = 7 Laguerre-Gaussian (LG) modes with l = 1…7 and frequencies ω_n = 0.85…1.15 ω0 (Δω = 0.05 ω0). The intensity profile is helical: one bright spot that rotates around the axis. **Two LS pulses are placed symmetrically**, which is equivalent to Δl = 2, so that a straight on-axis electron column forms. At equal power, the LS peak intensity is **N times** an LG pulse's: I_LS = C N² a0², P_LS = N·C∫a0² dS.
- **Laser:** λ = 0.8 µm. Sub-beam a_LG = 15, giving synthesized a_LS ≈ 100–105 and a peak intensity of **2.15×10^22 W/cm²**. Total power **4.81 PW**. Pulse duration T = 16 µm (equal to the LS pitch λ/δ). Waists w0n = 16, 11.3, 9.24, 8, 7.16, 6.53, 6.05 µm, with w0n√l_n held constant. Effective spot is about 4 µm.
- **Plasma:** near-critical **tritium** plasma doped with hydrogen (T:H = 70:1), n_e = **1.23×10^27 m⁻³ (about 0.71 n_c at 0.8 µm)**. Plasma length 10–800 µm, transverse ±27 µm.
- **Code:** **EPOCH**, 3D. The moving-window box is 80×60×60 µm with 1000×800×800 cells (dx = 0.08 µm, dy = dz = 0.075 µm) and **1 particle per cell**.
- **Results, self-injection:** background protons are trapped and confined by the on-axis electron column (the column gives the positive-charge focusing). Cutoff is **8.7 GeV after about 1 ps** (about 0.3 mm), so the average gradient is roughly 8.7 GeV / 0.3 mm ≈ **29 TeV/m** [inference from t ≈ 1 ps]. Energy conversion efficiency is **11% into protons above 0.5 GeV**. The spectrum is broad (continuous trapping), and the mean divergence is about 1.85°. Measured bubble velocity is v_p = 0.971c (γ_p = 4.18). The predicted P_x = 10.96 m_p c agrees with the simulated 10.31 m_p c.
- **Results, external (witness) injection:** n0 = 6.9×10^26 m⁻³ tritium. A 4×2×2 µm witness proton beam starts at **0.11 GeV** and reaches **>10 GeV (10.6 GeV)** by t = 1.17 ps (P_max = 12.36 m_p c), with energy spread about 0.67 (relative).
- **Comparisons:** at the same 4.81 PW, Gaussian (a ≈ 47) and LG (a ≈ 43) pulses give **<1 GeV** and no self-injection; peak Ex_LG = 6.1 and Ex_GS = 6.7 (in m_e ω0 c/e units). An imperfect LS (random phases between beamlets) needs **12.3 PW** (a_LG = 24) to reach 8.73 GeV, and works in only **25%** of 12 runs. LG at 12.3 PW reaches 1.32 GeV.
- **Implementable formulas** (normalized: momenta in m_p c, φ in m_e c²/e, ε_p = −1/1836, ξ = x − ct):
  - Hamiltonian: h0 = √(1 + p_x² + p⊥² + ε_p²a²) − ε_p φ(ξ) − v_p P_x, with h0 = 1 for a proton initially at rest.
  - Trapping condition: h0 + ε_p φ_trap = 1/γ_p. In physical units: **e Δφ_trap = (1 − 1/γ_p) m_p c²** [rewritten]. The paper quotes φ_trap ≈ 1260 against φ_max ≈ 1305 for LS, while LG only reaches φ_max ≈ 335. Note: for γ_p = 4.18 the formula gives 1836 × (1 − 1/4.18) ≈ 1397, not 1260. The paper's value appears inconsistent (S3 and S9 use the formula exactly) [my check].
  - Momentum after acceleration (their Eq. 3): P_x = [v_p(ε_pφ + h0) + √((ε_pφ + h0)² − (1 − v_p²))] / (1 − v_p²) (sign and charge convention as in the paper). The maximum is bounded by roughly 2γ_p² m_p c for a full potential swing.
- **6 GeV relevance:** this is the closest published "few-PW → ~10 GeV proton" design. The key ingredients are (i) near-critical density, which gives low γ_p ≈ 4 so φ_trap is reachable; (ii) a vortex/OAM structure that supplies an on-axis electron column for proton focusing; and (iii) heavy-ion background (tritium) for a stable bubble. The weakness is that it is ideal 3D PIC at 1 ppc, with high intensity (2×10^22 W/cm²), a broad spectrum, and a coherent 7-beam synthesis requirement.
- **Leads from its reference list:** Shen et al. PRST-AB 12, 121301 (2009); L.-L. Yu et al. NJP 12, 045021 (2010) (external injection, about 10^22 W/cm²); X. Zhang et al. PoP 17, 123102 (2010); X. Zhang et al. PoP 18, 073101 (2011); X. Zhang et al. NJP 16, 123051 (2014) (LG pulse proton acceleration); Bake et al. PoP 19, 083103 (2012); Rau, Tajima, Hojo PRL 78, 3310 (1997); Tajima, Yan, Ebisuzaki, Rev. Mod. Plasma Phys. 4, 7 (2020); Wang et al. PoP 22, 043106 (2015); Vieira and Mendonça PRL 112, 215001 (2014).

### S3. Shen, Zhang, Sheng, Yu, Cary — "High-quality monoenergetic proton generation by sequential radiation pressure and bubble acceleration" (2009) [paper]

- **Citation:** B. Shen, X. Zhang, Z. Sheng, M. Y. Yu, J. Cary, *Phys. Rev. ST Accel. Beams* **12**, 121301 (2009). DOI: [10.1103/PhysRevSTAB.12.121301](https://doi.org/10.1103/PhysRevSTAB.12.121301). Open access (CC-BY 3.0); I read the full PDF.
- **Scheme (hybrid RPA → bubble):** a small, dense **hydrogen micro-target** (10 n_c, 2λ × 2λ) is embedded in an underdense **tritium** background (0.3 n_c). A circularly polarized pulse first radiation-pressure-accelerates the micro-target protons ("light-sail" pre-acceleration). Those pre-accelerated protons are then trapped in front of the wake bubble and accelerated over a long distance. Trapping is much easier than for protons at rest. Because the protons come from the micro-target, a lower background density can be used, which gives a faster bubble (higher γ_p) and hence a higher energy cap.
- **Laser:** λ = 0.8 µm, **CP**, I0 = **2.14×10^23 W/cm²** (a = 316/√2 per component), duration 12.5 T (laser periods), FWHM spot 20λ = 16 µm, **energy 18.26 kJ**. From I and spot I estimate a peak power of roughly 0.6 EW and a duration of about 30 fs [inference]. This is far beyond any existing facility.
- **Plasma:** tritium, n0 = 0.3 n_c = **5.2×10^20 cm⁻³**, 10λ < x < 800λ (about 0.64 mm).
- **Code:** **VORPAL**, **2D**. Box 50λ × 200λ moving window, 2000×400 cells (dx = λ/40, dy = λ/2), 10 ppc per species. The authors checked convergence at 2× resolution.
- **Results:** quasi-monoenergetic peak at **38 GeV**, maximum about **42 GeV**, **12.6% energy spread**, divergence about 2×10⁻² rad, **6.24×10^9 protons above 35 GeV** (about 1 nC; roughly 35–38 J in the bunch, i.e. about 0.2% of 18 kJ [inference]). The acceleration time is about 800 T ≈ 2.1 ps (about 0.64 mm), giving an average gradient of **about 60 TeV/m** [inference]. A lower-intensity variant (a = 100/√2, 3λ × 3λ micro-target, 0.35 n_c) gives a **maximum of about 8 GeV** with a broader spread.
- **Trapping physics (implementable):**
  - Proton Hamiltonian: √(1 + p_x² + p⊥² + ε_p²a²) − ε_p φ − v_p p_x = h0, with ε_p = −1/1836 and φ in m_e c²/e.
  - Trapping when **h0 + ε_p φ = 1/γ_p**. Measured v_p = 0.972c (γ_p = 4.26) gives **φ_trap = 1836 (1 − 1/γ_p) = 1405** for a proton at rest; the simulated φ_max ≈ 1800. This confirms the physical-unit form e Δφ_trap = (1 − 1/γ_p) m_p c². Pre-accelerated protons need less potential.
  - Energy cap: **W_max ≈ 2 γ_p² m_p c²** (about 34 GeV for γ_p = 4.26). This is the key scaling for choosing the plasma density in a 6 GeV design: The more exact form for a proton from rest is W_max = 2γ_p²β_p² m_p c². 6 GeV then needs γ_pβ_p ≈ 1.79 (γ_p ≈ 2.05, v_p ≈ 0.87c) if the full dephasing gain is used [inference].
  - Transverse confinement comes from the field of the compressed fast electron layer at the bubble front (focusing near the front, defocusing elsewhere): E_y = (eσ/4πε0)[ln(x² + (d−y)²) − ln(x² + y²)], with σ = n_p δl. In the lab frame E_y' = γ_p E_y ≈ 0.85×10^14 V/m. Protons sit at the **front** of the bubble, not at the back as electrons do.
  - Linear polarization performs worse (instabilities). The authors caution that 3D effects (shorter Rayleigh length, weaker space-charge field) may change the results.

### S4. Liu, Weng, Wang, Chen, Zhao, Sheng, He, Li, Zhang — "Efficient injection of radiation-pressure-accelerated sub-relativistic protons into laser wakefield acceleration based on 10 PW lasers" (2018) [paper]

- **Citation:** M. Liu et al., *Phys. Plasmas* **25**, 063103 (2018). DOI: [10.1063/1.5033991](https://doi.org/10.1063/1.5033991). arXiv: [1806.10839](https://arxiv.org/abs/1806.10839). I read the full text (arXiv v1).
- **Scheme (RPA + density-tailored near-critical LWFA):** a thin CH₂ foil (n_e = 20 n_c, L = 0.4λ, |y| ≤ 2.5λ) sits in front of a near-critical carbon background with a **decreasing** density, n_e(x) = n0 exp(−x/L_s). RPA (light-sail) gives **sub-relativistic** protons (about 100 MeV, 0.43c). The near-critical plasma makes the laser front slow (v_laser < c), so the wake phase velocity is low enough to trap these protons. As the density falls, the laser front and wake accelerate along with the protons, which **delays dephasing** and also reduces pump depletion. In my view this is the most directly useful mechanism for a 6 GeV design.
- **Laser (baseline):** λ = 1 µm, CP, **a0 = 50 (6.85×10^21 W/cm²)**, sin² envelope, τ = 10T = **33 fs**, waist σ = 8λ. The authors present this as within reach of kJ-class 10 PW facilities (ELI, Apollon, OMEGA EP). The power is about 10 PW-class [their framing].
- **Code:** **OSIRIS 2D**. 70×70 µm moving window, 5600×4200 cells (λ/80 × λ/60), 400 ppc in the foil and 100 ppc in the background.
- **Results, a0 = 50:**
  - Foil only: about 100 MeV peak, 1.5% laser→proton efficiency.
  - Foil + uniform 4 n_c: quasi-monoenergetic **about 1 GeV peak**, 4% efficiency; dephasing ends acceleration at about 30T.
  - Foil + **4 n_c exp(−x/20λ)**: **about 2 GeV peak, 6% efficiency**.
  - Trapezoidal pulse (10T rise + t_f flat + 10T fall): the peak rises to **about 4.7 GeV** as t_f increases, then saturates because of dephasing.
  - A semi-Gaussian profile, 3 n_c exp(−x²/(30λ)²), gives a similar spectrum (about 1–2 GeV).
- **Results, a0 = 120 (4×10^22 W/cm²), foil L = 1λ:** uniform 1.2 n_c gives about 5 GeV mean. **1.2 n_c exp(−x/60λ) gives >10 GeV mean, with efficiency rising from 6.0% to 11.4%** (acceleration over about 300T ≈ 0.3 mm).
- **Implementable formulas:**
  - Light-sail mean ion energy (Eq. 1): E_ion = m_i c² · 2E²/(2E + 1), with E = 2π m_e n_c a0² cτ / (Σ m_i n_i L).
  - Proton energy gain (Eqs. 2–3): dγ_p/dx ≈ (m_e/m_p) · a0 · k0/2, assuming E_x ≈ E_max/2 and E_max ≈ a0 m_e ω0 c/e in the relativistic-transparency regime. In physical units this is about 0.5 · a0 · 3.2 TV/m (for λ = 1 µm) ≈ 80 TV/m at a0 = 50 [inference].
  - Laser-front velocity in near-critical plasma (Eq. 4; Weng et al. PoP 19, 022705, 2012): v_laser ≈ exp(−4 n_e/n_cr) · (1 − n_e/n_cr)^{1/2} · c, with n_cr ≈ (1 + 0.48 a0²)^{1/2} n_c for CP, and v_wake ≈ v_laser. **Density tailoring rule [inference]:** choose n_e(x) so that v_laser(n_e(x)) tracks v_p(x) from integrating dγ_p/dx.
  - Ion Hamiltonian in the wake frame: h(ζ, p_i) = γ_w[(1 + p_i²)^{1/2} − p_i v_wake/c] − (m_e n_c a0²/(2 m_i n_e)) · Φ(ζ) (the potential term is schematic in the extracted text). The ion is trapped if h < 1. At 0.1 n_c only p_i ≳ m_i c protons are trapped; at 4 n_c, **p_i ≈ 0.4 m_i c suffices** (a0 = 50).
- **Experimental routes the authors suggest:** pre-explode the foil with a ns pre-pulse to create the density ramp, or use modulated low-density foam.

### S5. Yu, Xu, Wang, Sheng, Shen, Yu, Zhang — "Generation of tens of GeV quasi-monoenergetic proton beams from a moving double layer formed by ultraintense lasers at intensity 10^21–10^23 W cm^-2" (2010) [abstract only]

- **Citation:** L.-L. Yu et al., *New J. Phys.* **12**, 045021 (2010). DOI: [10.1088/1367-2630/12/4/045021](https://doi.org/10.1088/1367-2630/12/4/045021). Open access, but I read only the abstract page.
- **Scheme:** a thin, overdense, proton-rich foil followed by **underdense gas** (effective Z/A ≈ 1/3), driven by a CP laser. The foil protons are pushed by radiation pressure (pre-acceleration). In the gas the laser drives high-amplitude, fast-moving electrostatic fields: a "moving double layer" that traps and accelerates the pre-accelerated protons. 1D and 2D PIC.
- **Results:** "tens of GeV" quasi-monoenergetic protons for I = 10^21–10^23 W/cm². Zheng et al. (S6) quote "**60 GeV**" for this work. HPLSE 2024 (S2) cites it as the external-injection route that needs about 10^22 W/cm² (tens of PW).
- This is the prototype of the **foil + gas (RPA → wake) "combination target"**, the class S3, S4 and S6 all belong to.

### S6. Zheng, Wang, Yan, Chen, Lu, Guo, Tajima, He — "Generating sub-TeV quasi-monoenergetic proton beam by an ultra-relativistically intense laser in the snowplow regime" (2011/2012) [paper]

- **Citation:** F. L. Zheng et al., arXiv: [1101.2350](https://arxiv.org/abs/1101.2350) (v2, Jan 2011). Published as F. L. Zheng, H. Y. Wang, X. Q. Yan, T. Tajima, M. Y. Yu, X. T. He, "Sub-TeV proton beam generation by ultra-intense laser irradiation of foil-and-gas target", *Phys. Plasmas* **19**, 023111 (2012), DOI [10.1063/1.3684658](https://doi.org/10.1063/1.3684658) (verified via Crossref). I read the full arXiv text.
- **Scheme ("snowplow" RPA → wake):** a hydrogen foil (n0 = 20 n_c, D = 0.5λ) followed by tenuous heavy-ion gas (Z/A = 1/3, n_e = 0.01 n_c, 12000λ = 1.2 cm long). The foil must be thin enough that l_s(skin) < D < (1/2)(n_c/n_e) a0 λ (Eq. 1), so electrons are pushed off, form a "snowplow" electron layer in the gas, and drag the GeV RPA protons into a long wake.
- **Laser:** λ = 1 µm, CP, **a0 = 250 (I0 = 1.71×10^23 W/cm²)**, trapezoidal envelope (20λ sin² rise + 15λ flat top); the abstract quotes 116 fs. The 2D run uses super-Gaussian r0 = 10 µm, τ = 55 fs.
- **Code:** **KLAP** (PKU). 1D: 20 cells/λ, 10 ppc in the gas and 20000 ppc in the foil. 2D: a small box with n_e = 0.2 n_c, 20×5 cells/λ.
- **Results, 1D:** **maximum 540 GeV, mean 437 GeV, FWHM spread <20%**; 1.72% of all protons fall in the peak; acceleration over about **1.1 cm** at E_x ≈ 14.9 m_e ω c/e ≈ **48 TV/m** [inference: 14.9 × 3.21 TV/m]. **2D (0.2 n_c): about 50 GeV**, consistent with 1D scaling.
- **Implementable scalings** (λ = 1 µm, normalized). The numerical factors were reconstructed by matching the quoted numbers, because π factors were lost in text extraction [inference]:
  - Snowplow (laser-front) field: E_B ≈ 3π (a0 n_e/n_c)^{1/2} · (m_e ω c/e); this gives 14.9 for a0 = 250, n_e = 0.01 n_c.
  - Snowplow length l_s ≈ (a0 n_c/n_e)^{1/2} λ. Etching velocity v_etch ≈ 9π² (n_e/n_c)/a0 · c (0.0036c).
  - Pump depletion length L_pd ≈ (L_laser/v_etch) c.
  - Dephasing length **L_dp ≈ (a0 n_c/n_e)^{3/2} λ / (36π²)** (11.1 mm).
  - **W_max ≈ (1/6) a0² (n_c/n_e) m_e c²** (532 GeV), valid when the pulse is long enough that L_pd > L_dp (L_laser > (1/4)(a0 n_c/n_e)^{1/2} λ). W_max = E_B · L_dp.
  - Optimal injection position: about l_s/4 behind the laser front.
- **6 GeV implication [inference]:** with W_max ∝ a0²/n_e, 6 GeV needs only a0²(n_c/n_e) ≈ 7×10^4, e.g. **a0 = 30 with n_e ≈ 0.013 n_c**, *provided* the protons are already relativistic (GeV-class) at injection. Injection from RPA at a0 = 30 is the bottleneck, which is why S4 uses near-critical, ramped density instead.

### S7. Gong, Cao, Palastro, Edwards — "Laser wakefield acceleration of ions with a transverse flying focus" (2024) [paper]

- **Citation:** Z. Gong, S. Cao, J. P. Palastro, M. R. Edwards, *Phys. Rev. Lett.* **133**, 265002 (2024). arXiv: [2405.02690](https://arxiv.org/abs/2405.02690) (v2, Dec 2024). Also presented as APS DPP 2024 JP12.113. I read the full arXiv text; the Supplemental Material was not read.
- **Idea:** instead of slowing the wake with density, **program the focal-spot trajectory**. Chromatic optics (axicon lens + spherical lens + axicon mirror; echelons and time-varying-index optics are alternatives) make each color focus at a different point on the x-axis, with the ring foci collapsing onto the axis. The focal spot moves along x with a *prescribed constant proper acceleration*, so the ponderomotively generated charge-separation field E_x co-moves with an ion that starts **from rest** in **underdense** plasma. The transverse E_y is **ion-focusing**. A purely longitudinal subluminal flying focus fails because the longitudinal intensity gradient is too weak at sub-relativistic focus speeds (finite Rayleigh length).
- **Laser/plasma, demo run:** I ≈ 1.1×10^20 W/cm², hydrogen n_e = 0.05 n_c, focus acceleration α0 = 2×10⁻⁴ c/T0 (T0 = 3.3 fs, λ = 1 µm). Result: **230 MeV** quasi-monoenergetic, 3.9% spread, 0.89° divergence, after **1 mm**.
- **GeV run (3D EPOCH):** laser energy **0.8 kJ, 21 ps, 37.5 TW**, peak at focus **3×10^20 W/cm²**, hydrogen n_e ≈ **5.5×10^19 cm⁻³**. After 4.4 mm (6400 T0): **1.64 GeV peak, 3.7% energy spread, 0.61° divergence, 23.1 pC**. The field is TeV/m-class; the average gradient is about 1.6 GeV/4.4 mm ≈ **0.37 TeV/m (3.7 GeV/cm)**, and 2D shows 4.0 GeV/cm. **Efficiency is only about 0.13%** (laser → all protons).
- **Code:** EPOCH, 2D and 3D (grid details are in the SM, not read).
- **Implementable formulas:**
  - Focal trajectory, a hyperbolic (constant-force) path: **x_f(t) = (c²/α0)[√((α0 t/c)² + 1) − 1]**, with matching α0 = e Z_i E_x / m_i.
  - Co-moving Hamiltonian (ζ = x − x_f): H(ζ, ζ̇) = ½ m_i ζ̇² + [e Z_i Φ(ζ) + m_i α0 ζ]/γ̃³, with γ̃ = √((α0 t/c)² + 1). Trapping exists when the total potential e Z_i Φ + m_i α0 ζ has a local minimum.
  - **Trapping threshold (Eq. 3): α0 < α* ≈ Z_i m_e c² a0 (n_e/n_c)^{1/6} / (m_i σ0)**, from E_x ≈ a0 (n_e/n_c)^{1/6} m_e c²/(e σ0) (fitted γ_e ≈ a0 (n_e/n_c)^{−1/6}; σ0 = focal spot size). Accelerations just below α* give the highest energies.
  - Energy gain ≈ m_i α0 per unit length (4.1 GeV/cm for α0 = 4×10⁻⁴ c/T0).
- **6 GeV relevance [inference]:** this is the only scheme here that starts from protons **at rest**, in **underdense** gas, at **10^20 W/cm²** and tens of TW (high repetition rate is possible). At about 4 GeV/cm, 6 GeV needs about 1.5 cm of focal travel and a correspondingly longer pulse (tens of ps, multi-kJ, since energy scales with the duration needed to cover the path). Efficiency (about 0.1%) is the weak point for an "energy-efficient" machine. It is the most promising *low-intensity* route, and could be combined with the density-ramp idea (S4).
- The paper says the "relativistic ions within the pulse" route (ref. 62 there) needs **>300 PW**.

### S8. Pierce, Miller, Li, Palastro, Mori — "Laser wakefield acceleration driven by a discrete flying focus" (2025) [paper, electron-focused]

- **Citation:** J. R. Pierce et al., *Phys. Rev. Accel. Beams* **28**, 101303 (2025). DOI: [10.1103/qts4-8kgf](https://doi.org/10.1103/qts4-8kgf). arXiv: [2506.19824](https://arxiv.org/abs/2506.19824). Open access (CC-BY 4.0).
- **Content:** a train of collinear pulses with staggered focal points f_j and delays. Each pulse comes into focus where the previous one dephased, so the accelerating phase moves at a *designable* velocity. **150 J total → 40 GeV per electron, 50 pC, in a 30 cm stage** (50 dephasing lengths), using QPAD quasi-static PIC.
- **Formula usable for protons [inference]:** delay choice ψ_j = (v_g/c) ψ0 + (1 − v_g/c) f_j gives a focus velocity v_f = c. Replacing the target velocity with a *ramped* v_f(z) = v_proton(z) would give a programmable subluminal driver for the proton wake. Caveat from Gong et al.: for slow foci in the longitudinal geometry, the longitudinal gradient is weak, so the delivered wake amplitude must be checked.

---

## Topic 2: nanoparticle-assisted injection and nanoparticle-assisted proton acceleration

### N1. Cho, Pathak, Kim, Nam — "Controlled electron injection facilitated by nanoparticles for laser wakefield acceleration" (2018) [paper, via PMC summary]

- **Citation:** M. H. Cho, V. B. Pathak, H. T. Kim, C. H. Nam, *Sci. Rep.* **8**, 16924 (2018). DOI: [10.1038/s41598-018-34998-0](https://doi.org/10.1038/s41598-018-34998-0). Open access (PMC6240057).
- **Mechanism (electrons):** a solid nanoparticle (NP) in the wake path is ionized and its electrons are expelled, leaving a positive Coulomb field. Background electrons passing near it get a longitudinal momentum kick (Δp_z ≈ 0.8 m_e c), via straight or "slingshot" orbits, that lowers the trapping threshold. **Modified trapping condition: Δφ_wake + ΔH < −1**, which becomes Δp_z,NP > 1 + Δφ_wake once the NP field is fully developed. **Injected charge ∝ n_NP r_NP³** up to saturation at n_NP ≈ 10^23 cm⁻³.
- **3D PIC:** **JoPIC**. 8 TW, 16 fs, a0 = 1, W0 = 17.6 µm, n0 = 7×10^18 cm⁻³. NP: 100 nm diameter, n_e = 2×10^23 cm⁻³. Grid λ/40 × λ/5 × λ/5. Result: **130 MeV, 5.7 pC, about 11% spread, and no injection without the NP**. Three NPs give 11 pC.
- **2D (500 TW, a0 = 3.5, 27 cm channel, 10^17 cm⁻³):** 5.1 GeV, 0.8% spread.
- **Ions:** NP ions are included in the simulation but not analysed. The authors note that high laser contrast is needed so the NP ionizes before it explodes.

### N2. Aniculaesei et al. — "Proof-of-principle experiment for nanoparticle-assisted laser wakefield electron acceleration" (2019) [abstract only]

- **Citation:** C. Aniculaesei, V. B. Pathak, K. H. Oh, C. I. Hojbota, P. K. Singh, B. R. Lee, H. T. Kim, E. Brunetti, B. J. Yoo, J. H. Sung, S. K. Lee, C. H. Nam, *Phys. Rev. Applied* **12**, 044041 (2019). DOI: [10.1103/PhysRevApplied.12.044041](https://doi.org/10.1103/PhysRevApplied.12.044041). arXiv: [1902.00921](https://arxiv.org/abs/1902.00921). Done at CoReLS/IBS (Korea). Simulations use OSIRIS with a fully ionized NP in pre-ionized plasma.
- **Content:** aluminium NPs made by laser ablation are introduced into the plasma and trigger electron injection. Compared with self-injection, energy, energy spread and divergence all improve, with the best bunches at **338 MeV peak, 4.7% relative energy spread, 5.9 mrad vertical divergence**.
- **Relevance:** NP-triggered injection works for **electrons** (the NP supplies a localized potential kick). Nothing on protons.

### N3. Aniculaesei, Ha, Yoffe, …, Hegelich — "Acceleration of a high-charge electron bunch to 10 GeV in a 10-cm nanoparticle-assisted wakefield accelerator" (2022/2024) [paper]

- **Citation:** C. Aniculaesei et al., *Matter Radiat. Extremes* **9**, 014001 (2024). arXiv: [2207.11492](https://arxiv.org/abs/2207.11492). Open access. I read the arXiv text (key sections).
- **Setup:** Texas Petawatt, **130 J, 135 fs, 1057 nm**, f/50, FWHM spot 55 µm, **1.2×10^19 W/cm²**, contrast about 10⁻⁸. 10 cm He gas cell at n_e = 6×10^17 cm⁻³. **Al NPs** are made in situ: a 532 nm, 10 ns, 130 mJ ablation pulse (5 J/cm²) hits an Al plate 500 µs before the main pulse. About 19 µg is ablated, roughly 10 nm NPs, an upper bound of about 10^6–10^7 NPs in the laser path.
- **Results:** **340 pC, 10 ± 1.86 GeV, 3.4 GeV rms spread, 0.9 mrad divergence** (2 of 23 NP shots). Baseline without NPs: about 2 GeV. The authors invoke a hybrid LWFA plus direct-laser-acceleration mechanism. Patent application 17/845,223 (Tau Systems).
- **Relevance:** this is the "nanoparticle-assisted" result most often cited. It concerns electrons only.

### N4. Ostermayr, Haffa, Hilz, …, Schreiber — "Proton acceleration by irradiation of isolated spheres with an intense laser pulse" (2016) [abstract only]

- **Citation:** T. M. Ostermayr et al., *Phys. Rev. E* **94**, 033208 (2016). DOI: [10.1103/PhysRevE.94.033208](https://doi.org/10.1103/PhysRevE.94.033208). No arXiv version found. A UT repository copy exists (repositories.lib.utexas.edu/handle/2152/61064).
- **Setup:** Texas Petawatt, about 2–3×10^20 W/cm², 10 µm focal spot. **Isolated, Paul-trap-levitated plastic spheres** of 520 nm to 19.3 µm diameter. Press coverage called them "nanobeads/nanoparticles".
- **Results:** maximum about **25 MeV** for spheres equal to or slightly smaller than the focus. Smaller spheres give non-monotonic spectra, a transition from ambipolar expansion to **Coulomb-explosion-dominated** acceleration. **Conversion efficiency reaches the percent level when sphere diameter ≈ focal spot.** Agrees with 3D PIC.

### N5. Hilz, Ostermayr, Huebl, …, Schreiber — "Isolated proton bunch acceleration by a petawatt laser pulse" (2018) [paper, via PMC summary]

- **Citation:** P. Hilz et al., *Nat. Commun.* **9**, 423 (2018). DOI: [10.1038/s41467-017-02663-1](https://doi.org/10.1038/s41467-017-02663-1). Open access (PMC5788983).
- **Laser:** PHELIX (GSI), **150 J, 500 fs, 1.054 µm**, 3.7 µm FWHM focus. The target sat 1–1.5 z_R out of focus, giving **up to 7×10^20 W/cm²**.
- **Target:** levitated **1 µm PMMA sphere** (solid, or hollow with 100 nm wall) in a Paul trap, ±1 µm positioning. The rising edge pre-expands it to about a critical-density plasma of 5.5–7 µm FWHM.
- **Results:** **quasi-monoenergetic 20–40 MeV** protons, reproducible, about 25% spread (simulations down to 3.5%), almost no low-energy background, about 20° divergence. **30–100× more protons per solid angle than an isotropic Coulomb explosion**. Simulation gives about 10^10 protons (14% of the target's protons). Efficiency is **0.3% into protons** (1.3% into all ions), or about 3% counting only the effective part of the pulse.
- **Code:** **PIConGPU** 3D3V. Box 104×139×104 µm, 30 nm cells (3456×4624×3456), Δt = 57.5 as. Pre-expanded Gaussian PMMA plasma, peak 0.8 n_c, σ = 3.06 µm. a0 = 17, 13.5 µm spot, 500 fs, linear polarization. Ran on 8000 K20x GPUs (Titan), about 1 PB of output. Inputs: PIConGPU is open source (github.com/ComputationalRadiationPhysics/picongpu); I did not find a per-paper input deck in this pass.
- **Mechanism:** the laser self-focuses around the mass-limited plasma, electrons are pulled forward, and a charge-separation field of about 2.5 MV/µm develops. Scaling is about **2.4 MeV per J of laser energy transmitted through the plasma**; a Coulomb-repulsion phase follows.
- **Relevance:** a "nanoparticle/microparticle-as-target" route to **monoenergetic** protons with high per-steradian yield. In my view this is a candidate *injector* (tens of MeV, narrow spread, compact bunch), but only at MeV-class energies [inference].

### N6. Jinno, Kanasaki, …, Kiriyama, Fukuda — "Laser-driven multi-MeV high-purity proton acceleration via anisotropic ambipolar expansion of micron-scale hydrogen clusters" (2022) [paper]

- **Citation:** S. Jinno et al., *Sci. Rep.* **12**, 16753 (2022). DOI: [10.1038/s41598-022-18710-x](https://doi.org/10.1038/s41598-022-18710-x). Open access (PMC9556756). I read the full text via the Europe PMC XML.
- **Laser:** **J-KAREN-P** (QST-KPSI), **9 J, 37 fs, 0.1 Hz**, contrast 10⁻¹¹ (out to 200 ps), F/10, 20 µm (1/e²) spot, **1.6×10^20 W/cm²** in vacuum (a0 ≈ 7.8 effective in the PIC).
- **Target:** **micron-scale H₂ clusters** made by spallation of supercooled liquid or supercritical H₂ (25–50 K, 6 MPa, 250 µm conical nozzle). Most clusters are about 0.3 µm, with a tail of >1 µm clusters. The background gas is about 0.024 n_c.
- **Results:** max **12.4 ± 0.6 MeV** protons along the laser axis (1.3×10^6 /MeV/sr/shot). **1.6×10^9 /MeV/sr/shot at 2.8 MeV**. High purity: protons only. Anisotropic, forward-peaked.
- **Code:** **EPIC3D**. A single cluster at n_e = 4.6×10^22 cm⁻³ (26.8 n_c) in a 10.24×20.48×10.24 µm box, λ = 810 nm.
- **Mechanism:** for clusters larger than the skin depth (about 1–2 µm), **anisotropic ambipolar expansion**: only the peripheral skin layer Coulomb-explodes, forward electrons drag the front protons, and E_max is insensitive to size (12.8 and 13.5 MeV for 1.2 and 2.0 µm). For small clusters (0.33 µm) the whole cluster charges up and gives a **pure Coulomb explosion** (5.8 MeV PIC, 7.5 MeV model, 5.7 MeV measured).
- **Implementable formula (Coulomb explosion of a fully stripped uniform sphere):** **E_max = n_i e² R²/(3ε0)** (energy of a surface ion). Check: n = 4.6×10^22 cm⁻³, R = 0.6 µm gives about 100 MeV, matching the paper's "100 MeV". The mean energy is 3/5 of E_max. This only holds if a0 is large enough to strip the whole cluster (a0 ≳ n_e R/(n_c λ)-ish) [inference].
- **Forward-looking claims:** 3D PIC predicts **117 MeV** directed protons from 1.2 µm clusters at 10^22 W/cm² (Jinno et al. PPCF 60, 044021, 2018). See also N7.

### N7. Matsui, Fukuda, Kishimoto — "Quasimonoenergetic proton bunch acceleration driven by hemispherically converging collisionless shock in a hydrogen cluster coupled with relativistically induced transparency" (2019) [abstract only]

- **Citation:** R. Matsui, Y. Fukuda, Y. Kishimoto, *Phys. Rev. Lett.* **122**, 014804 (2019). DOI: [10.1103/PhysRevLett.122.014804](https://doi.org/10.1103/PhysRevLett.122.014804). Abstract via Europe PMC.
- **Content:** 3D PIC (EPIC3D presumably [inference]). A PW-class laser is focused onto a **micron-size spherical H cluster**. A crescent collisionless shock launched at the irradiated hemisphere **converges at the center at the same moment relativistic induced transparency (RIT) sets in**, and the proton bunch is pushed forward. Result: **quasi-monoenergetic peak at about 300 MeV, about 10% spread, about 5° half-divergence**. Works only within threshold windows of laser intensity and cluster radius (>1.6 µm per Jinno 2022; about 10^22 W/cm²-class).
- **Relevance:** the strongest "cluster/nanoparticle-enhanced proton" simulation result: 300 MeV, monoenergetic, impurity-free, rep-rate compatible. In my view it is a plausible **injector** for a proton wake stage (γ ≈ 1.32, β ≈ 0.65, close to the about 0.43–0.8c injection velocity used in S4) [inference].

### N8. Margarone, Klimo, Kim, Prokůpek, Limpouch, Jeong, Mocek, Pšikal, Kim, Proška, Nam, Štolcová, Choi, Lee, Sung, Yu, Korn — "Laser-driven proton acceleration enhancement by nanostructured foils" (2012) [abstract only]

- **Citation:** D. Margarone et al., *Phys. Rev. Lett.* **109**, 234801 (2012). DOI: [10.1103/PhysRevLett.109.234801](https://doi.org/10.1103/PhysRevLett.109.234801). Author list verified via Crossref.
- **Content:** a **monolayer of polystyrene nanospheres** (535 nm optimum) on the front of a thin plastic foil, shot with a 100 TW laser (GIST/APRI Korea). Absorption rises drastically. **Cutoff energy rises about 60% and the number of protons above 1 MeV about 5×** compared with a flat foil. Interpreted with 2.5D PIC. A follow-up, "Enhanced TNSA acceleration with 0.1–1 PW lasers" (Margarone et al.), extends this to PW.
- **Relevance:** the classic "**nanoparticle-structured target → enhanced proton (TNSA) acceleration**" experiment. It works by absorption enhancement, not wake injection. Similar: Au nanoparticles in polymer films (Torrisi et al. 2015, about 10^15 W/cm², resonant absorption) and nanowire targets (Vallières et al., Sci. Rep. 11, 2226, 2021: about 2× cutoff, 3× temperature).

### N9. Xu, Bae, Ezzat, Kim, Yang, Lee, Yoon, Sung, Lee, Ji, Shen, Nam — "Nanoparticle-insertion scheme to decouple electron injection from laser evolution in laser wakefield acceleration" (2022) [paper, via PMC summary]

- **Citation:** J. Xu et al., *Sci. Rep.* **12**, 11128 (2022). DOI: [10.1038/s41598-022-15125-6](https://doi.org/10.1038/s41598-022-15125-6). Open access (PMC9249746). This is the "Xu et al." in the task brief. Note the co-author **Baifei Shen**, which links it to the proton-wake group of S1–S3.
- **Experiment:** CoReLS 5 Hz Ti:Sa, **1.5 J, 25 fs, 15 µm FWHM, 10^19 W/cm²**, 3 mm He jet at about 1.5×10^18 cm⁻³. **Cu NPs** come from ablating a Cu blade (532 nm, 3 ns, 80–210 J/cm²), giving 10–40 nm NPs (up to 90 nm). The plume expands at 10–30 km/s, the optimal delay is 0.15–0.35 µs, and injection is localized to about 100 µm.
- **Results:** at 84 J/cm²: 23% injection probability, about 55 pC, 143 MeV peak, about 30% spread. At 145 J/cm²: **>90% injection probability, >300 pC**, about 12 mrad divergence. Divergence stays at 8–12 mrad as charge rises from 50 to 500 pC.
- **Simulation:** **VORPAL 3D**. 200×160×160 µm window, 2000×800×800 cells, 1 ppc background and 10^4 ppc in the NP. NP is 100 nm, 100 n_c, at x = 100 µm; about 16 pC trapped.
- **Formula:** NP charge Q = (4π/3) n q r³ (n = atomic density, q = ion charge state). This sets the strength of the local injection field.

### N10. Vallières, Barberio, Scisciò, d'Humières, Antici — "Enhanced laser-driven proton acceleration using ultrasmall nanoparticles" (2019) [paper] **(best title match to "Enhanced proton acceleration using … nanoparticles")**

- **Citation:** S. Vallières, M. Barberio, M. Scisciò, E. d'Humières, P. Antici, *Phys. Rev. Accel. Beams* **22**, 091303 (2019). DOI: [10.1103/PhysRevAccelBeams.22.091303](https://doi.org/10.1103/PhysRevAccelBeams.22.091303). Open access (CC-BY 4.0); I read the full PDF. No arXiv version found.
- **Targets:** **10 nm Au or Ag nanoparticles**, made by laser ablation in solution and **spray-dried** onto 15 µm Al foils. Cheap, rep-rate friendly, and alignment-insensitive. This is front-surface nanostructuring, **not** injection into a wake.
- **Lasers:** **TITAN** (JLF/LLNL): 220 J, 700 fs, 1.054 µm. **ELFIE** (LULI): 12 J, 350 fs, 1.057 µm. Both f/3 to 8–10 µm FWHM, **3×10^19 – 5×10^20 W/cm²**, ASE contrast <10⁻⁶.
- **Experimental results (5-shot averages, TNSA):**
  - TITAN: yield (>1 MeV) **+79% (Ag) / +51% (Au)**; max energy +19% / +23%. The spectra axis extends to about 50 MeV; flat-Al cutoff is a few tens of MeV.
  - ELFIE: yield +67% / **+190%**; max energy +13% / **+97%** (Au best; cutoffs about 5–7 MeV).
  - In the authors' words, a "nearly twofold maximum proton energy and proton number enhancement".
- **Simulations:** **PICLS 2D3V**. p-polarized, 5×10^20 W/cm² (a0 ≈ 15), τ = 25–300 fs, dx = dy = 2 nm (1 nm for the size scans), dt = 6.6 as. Box 24200×420 cells. At 2 nm that is about 48×0.84 µm; the paper's own "(300 × 10)" label has unclear units. Periodic transverse boundaries (plane-wave approximation), 20 ppc, 600 fs run. Target: 20 nm Au spheres on 500 nm Au (2500 n_c), with a 20 nm proton contaminant layer (15 n_c) at the rear.
- **Simulation results:** max-energy enhancement about 50% at 100s of fs and **>250% at 25 fs**. Absorption saturates for d_NP ≳ 20 nm. Hot-electron cutoff doubles for 10–60 nm NPs. Cutoff rises **4×** when varying the diameter (gap g = 0), and **7× with a 100 nm gap** between 10 nm NPs. **The gap matters more than the diameter**: electrons are heated in the vacuum gaps (relativistic trajectories, as in Blanco et al.). Flat-target reference cutoff is 4.5 MeV.
- **Mechanism:** a better pre-plasma and absorption give more and hotter electrons, hence a stronger rear sheath. It does not depend on NP survival at peak intensity.
- **Inputs/code:** PICLS is not public. No input decks were published.
- **Relevance to the 6 GeV project [inference]:** this is an MeV-class **TNSA source enhancement**, about 2× in energy and yield at the same laser energy. It is useful only as a cheap, efficient **low-energy proton source/injector** front end. It does nothing for wake trapping.

### N11. Nishihara, Watari, Matsukado, Sekine, Takeuchi, Takagi, Satoh, Kawashima, Kan — "Laser ion acceleration and neutron source in short-pulse solid-nanoparticle interaction" (2016) [abstract only]

- **Citation:** K. Nishihara et al., *J. Phys.: Conf. Ser.* **688**, 012076 (2016) (IFSA 2015). DOI: [10.1088/1742-6596/688/1/012076](https://doi.org/10.1088/1742-6596/688/1/012076). Open access, but the IOP PDF was blocked by a JS wall; abstract via OpenAlex.
- **Content (3D PIC):** solid **CH and CD nanoparticles** irradiated by an intense short pulse.
  - At a ≈ 2, a 250 nm CD particle is optimal for D–D neutrons (⟨σv⟩ ≈ 2×10⁻¹⁶ cm³/s, effective T_D ≈ 0.5–1 MeV).
  - **At a ≈ 100, radiation pressure around the particle pushes electrons forward and protons follow: 450 MeV in 130 fs from a CH particle of 700 nm radius**, with >10% of all particle protons accelerated forward. Energy keeps rising with time and particle size, and collimation improves with time.
- **Relevance:** a "nanoparticle → directed sub-GeV proton" result at a0 ≈ 100 (about 2×10^22 W/cm² at 0.8 µm). Together with N7 (300 MeV from H clusters), it shows that **isolated nanoparticle/cluster targets can supply 0.3–0.45 GeV protons**: β ≈ 0.65–0.73, γ ≈ 1.3–1.5. That is the kind of pre-acceleration a near-critical, density-ramped proton wake (S4) needs [inference].

### N12. Mehrangiz — "Enhanced quasi-monoenergetic ions generation: based on gold nanoparticles application in gas-filled nanosphere targets" (2021) [abstract only]

- **Citation:** M. Mehrangiz, *Phys. Plasmas* **28**, 123103 (2021) (verified via Crossref). DOI: [10.1063/5.0072087](https://doi.org/10.1063/5.0072087).
- **Content:** builds on Vallières 2019 (N10). An argon-gas-filled nanosphere with V inner layer, p–C outer layer and a spaced Au-NP shell (optimal gap 80 nm). **EPOCH 2D**, 4.61×10^19 W/cm². Quasi-monoenergetic H⁺, C⁶⁺, V²⁰⁺, Au⁴⁹⁺, Ar¹⁵⁺ via spherical Coulomb explosion. **+19% H⁺ cutoff** versus a hollow Au-NP nanosphere (Ar¹⁵⁺ cutoff about 0.49 MeV/u). MeV-class only.

### N13. Klimešová, Kulyk, Dittrich, Andreasson, Krikunova — "Nanoparticle-assisted acceleration of laser-irradiated low-density He ions" (2021) [abstract only]

- **Citation:** E. Klimešová et al., *Phys. Rev. A* **104**, L061101 (2021). DOI: [10.1103/PhysRevA.104.L061101](https://doi.org/10.1103/PhysRevA.104.L061101). Follow-up: Klimešová et al., *New J. Phys.* (2025), DOI [10.1088/1367-2630/ada575](https://doi.org/10.1088/1367-2630/ada575) (FLASH XUV, 92 eV).
- **Content:** a single CsCl nanoparticle in about 10^15 cm⁻³ He gas, irradiated at 2×10^15 W/cm² (NIR). **Ambient He⁺ ions gain higher energy than the NP's own Cs⁺/Cl⁺ ions**, accelerated by the positive surface charge of the NP. This is the closest literal analogue of "ions from the surrounding gas being *injected and accelerated* by a nanoparticle field", but at eV–keV scale.

### Other nanoparticle/cluster items noted (not read in depth)

- **Prencipe et al.**, *New J. Phys.* **23**, 093015 (2021), DOI [10.1088/1367-2630/ac1fcd](https://doi.org/10.1088/1367-2630/ac1fcd). **Cluster-assembled (nanostructured) foam** on 1.5 µm Al, 30 fs, up to 5×10^20 W/cm² (DRACO). Cutoff **18.5 MeV versus 9.5 MeV** for bare foil; 4×10^9 protons above 4.7 MeV versus 1×10^9. [abstract only]
- **Shou et al.**, *Nat. Commun.* **16** (2025), DOI [10.1038/s41467-025-56667-3](https://doi.org/10.1038/s41467-025-56667-3). CoReLS multi-PW on **conduction-restricted, finite-lateral-size nm polymer foils** (mass-limited): **>110 MeV** protons via RPA plus carbon-ion Coulomb repulsion. [abstract only]
- **Sun et al.**, *Nat. Commun.* **15**, 5150 (2024), DOI [10.1038/s41467-024-49569-3](https://doi.org/10.1038/s41467-024-49569-3). Steering of surface-proton emission from **Au nanoparticle nanoplasmas** by laser strength (low-energy physics). [abstract only]
- **Kim, Botton, Zigler**, *Front. Phys.* **12**, 1424755 (2024), DOI [10.3389/fphy.2024.1424755](https://doi.org/10.3389/fphy.2024.1424755). **CH₂ clusters inside a plasma channel**: Coulomb-explosion MeV protons for p-¹¹B, with Bayesian-optimised 2D PIC. [abstract only]
- **Fukuda et al.**, *Phys. Rev. Lett.* **103**, 165002 (2009), DOI [10.1103/PhysRevLett.103.165002](https://doi.org/10.1103/PhysRevLett.103.165002). **Cluster-gas target** (CO₂ clusters in He) raises ion energy to about 10–20 MeV/u at only about 10^17–10^18-class intensities. (Fukuda, Faenov, Tampo, Pikuz, Nakamura, Kando, et al.; citation verified via Crossref, numbers from memory)
- **Karsch et al.**, *Phys. Rev. Lett.* **91**, 015001 (2003). "High-intensity laser induced ion acceleration from heavy-water droplets" (Karsch, Düsterer, Schwoerer, Ewald, Habs, Hegelich, et al.; D₂O microdroplets). [title only, verified via Crossref]
- **Cho/Pathak** and **Aniculaesei 2025** (arXiv [2508.10685](https://arxiv.org/abs/2508.10685), "Towards controlling electron charge with nanoparticle assisted LWFA"): electrons only.

---

## Topic 1 (continued)

### S9. Zhang, Shen, Zhang, Xu, Wang, Wang, Yi, Shi — "Proton acceleration in underdense plasma by ultraintense Laguerre-Gaussian laser pulse" (2014) [paper]

- **Citation:** X. Zhang et al., *New J. Phys.* **16**, 123051 (2014). DOI: [10.1088/1367-2630/16/12/123051](https://doi.org/10.1088/1367-2630/16/12/123051). arXiv: [1407.6467](https://arxiv.org/abs/1407.6467). I read the full arXiv text.
- **Scheme:** a CP **LG10** (donut) pulse makes a bubble with an **on-axis electron pillar/thread**. The pillar gives a **transverse focusing field for protons** (F_t = e(E_y − cB_z) ∼ e n r0) while E_x ≈ 6 m_e ω c/e accelerates. External (witness) injection.
- **Laser:** λ = 0.8 µm, CP LG10, a = a0 (2r/r0) exp(−r⁴/r0⁴) e^{ilφ} sin²(πt/2t0), r0 = 7 µm, t0 = 12.5T. Power is equal to a super-Gaussian pulse of 2.14×10^22 W/cm² (a0 = 70.7).
- **Plasma:** **tritium**, n0 = **2.4×10^20 cm⁻³** (about 0.14 n_c), 12–1000 µm.
- **Code:** **VORPAL 3D**. 60×100×100 µm window, 600×300×300 cells, 1 ppc.
- **Witness:** 3×1×1 µm, **160 pC**, injected at 1 GeV.
- **Result:** **1 GeV → 7 GeV** (peak) by t = 2.13 ps (dephasing at the bubble front), i.e. about 0.64 mm. Average gain is about **9 TeV/m** [inference]. A super-Gaussian driver gives only 2.2 GeV, because the protons scatter. The scheme also works at a0 ≈ 20 if injection energy is higher.
- **Implementable formulas:**
  - Bubble radius from ponderomotive vs. space-charge balance (Eq. 1, garbled in extraction): R ∝ √a0 · √(n_c/n) λ. Use the standard k_p R ≈ 2√a0 [standard, Lu et al. 2007]. **Spot-matching for the pillar: r0 ≈ R/2.**
  - **Bubble (hole-boring-like) velocity in dense plasma (Eq. 3): v_p/c = a√(n_c/n_e′) / (1 + a√(n_c/n_e′))**, with n_e′ = n0 R/d_skin the compressed front-layer density. This gave 0.96 versus 0.967 simulated (γ_p = 3.9). This is the key formula for designing a **slow** proton wake via density and intensity [the formula is the paper's; its use for design is my inference].
  - Trapping condition (Eq. 4): **h0 + ε_p φ_trap = 1/γ_p**, with **h0 = γ0(1 − v_p v0)** for an injected proton (v0, γ0). At rest, φ_trap = 1368 (in m_e c²/e) at γ_p = 3.9, but φ_max ≈ 380, so **γ0,min ≈ 1.4 (≈ 375 MeV)** is needed. At γ0 = 2, φ_trap ≈ 128.
  - Field model: E_x rises linearly over 0 < ξ < R and falls over R < ξ < R + d_skin, with E_max ≈ κ a0 (κ ≈ 2/3 from the simulations); d_skin ≈ 1/√n_e.

### S10. Wan, Andriyash, Pai, Hua, Zhang, Li, Wu, Nie, Mori, Lu, Malka, Joshi — "Ion acceleration with an ultra-intense two-frequency laser tweezer" (2017/2020) [paper]

- **Citation:** Y. Wan, I. A. Andriyash, C. H. Pai, J. F. Hua, C. J. Zhang, F. Li, Y. P. Wu, Z. Nie, W. B. Mori, W. Lu, V. Malka, C. Joshi, *New J. Phys.* **22**, 052002 (2020). DOI [10.1088/1367-2630/ab8678](https://doi.org/10.1088/1367-2630/ab8678) (verified via Crossref). arXiv: [1707.07290](https://arxiv.org/abs/1707.07290). I read the arXiv v2 text.
- **Idea (programmable subluminal driver):** two **counter-propagating CP pulses of different frequencies** (λ1 = 0.8 µm, λ2 = 2λ1) collide on a 20 nm CH foil. Their beat pattern moves at **v_tw = (ω1 − ω2)/(k1 + k2)** (= c/3 here), "grabs" the electron sheet, and drags it at an optically set velocity. This creates a micro-capacitor field **E_z ≈ 60 TV/m** that accelerates the protons.
- **3D OSIRIS:** a0 = 16 each, ten-cycle flat-top, 8 µm spots. Foil n_e = 100 n_c (p 10 n_c, C⁶⁺ 15 n_c). dz = 3 nm, dx = dy = 10 nm, 32 ppc. Result: **220 MeV in about 40 fs** (theory 230 MeV, 36 fs); a quasi-monoenergetic group of about 10^10 p with about 20% FWHM, θ < 10 mrad.
- **2D scaling:** **20 MeV → 830 MeV for 1 → 80 J total laser energy**, 4–20% spread, and 2–5× the energy of light-sail at equal laser energy. Jitter tolerance is about 10 fs, with |a2/a1 − 1| < 0.2. The sheet erodes at t_eff ≈ 1.3 w0/c.
- **6 GeV relevance [inference]:** this demonstrates *optical* control of the accelerating-structure velocity (v_tw set by the frequency ratio). In principle a **chirped** pair could ramp v_tw(t) to follow the proton. Acceleration lengths are µm-scale, so it is an **injector** concept (0.2–0.8 GeV at 10–80 J), not a 6 GeV stage.

### S11. Positive-charge focusing: linear/quasi-linear wakes, hollow channels, electron columns [standard theory + papers]

- **Linear (a0 ≲ 1) wake** [standard; Esarey, Schroeder, Leemans, *Rev. Mod. Phys.* **81**, 1229 (2009)]. For a Gaussian driver, E_z ∝ cos(k_p ξ) and the radial force ∝ sin(k_p ξ) · ∂_r(e^{−2r²/w0²}). Each of "accelerating" and "focusing" for a given charge sign covers half a plasma period, so **for any charge sign there is a quarter-period (λ_p/4) window that both accelerates and focuses**. For positive particles this window is shifted by λ_p/2 from the electron window. A proton (or positron) can therefore be focused and accelerated in a *linear* wake, but at a field of only about 0.1–0.5 E0. Here E0 = m_e c ω_p/e ≈ 96 √(n_e[cm⁻³]) V/m, e.g. 96 GV/m at 10^18 cm⁻³. In the **blowout** regime the ion cavity defocuses protons everywhere except in the electron sheath and at the bubble front (the compressed electron layer; see S3).
- **Bubble front / compressed electron layer (S3):** focusing for protons near the dense front layer: E_y = (eσ/4πε0)[ln(x² + (d−y)²) − ln(x² + y²)]. This is why protons ride at the **front** of the bubble in the Shen-type schemes.
- **On-axis electron column (S2, S9; Vieira and Mendonça PRL 112, 215001, 2014):** OAM/LG or light-spring drivers leave an electron filament on axis, so **radial focusing for protons inside the cavity** with F_t ≈ e n r0. This is the most robust published fix for transverse proton loss in high-intensity wakes.
- **Hollow plasma channel:** Yi, Shen, Lotov, et al., *Phys. Rev. ST Accel. Beams* **16**, 071301 (2013), DOI [10.1103/PhysRevSTAB.16.071301](https://doi.org/10.1103/PhysRevSTAB.16.071301), arXiv [1306.1613](https://arxiv.org/abs/1306.1613) [abstract only]. A proton-*driven* wake in a hollow channel with driver radius about the channel width gives charge separation at the wall that **focuses positive witnesses on axis**. Buckets are much larger than in uniform-plasma blowout, and witness phasing is tunable by the channel radius. 2D sims give **1.3 GeV/m average over 1 km**. (Laser-driven hollow channels have little transverse focusing on axis for any species; the wall field is what matters [inference].)
- **Design rule [inference]:** for a 6 GeV proton LWFA, either (a) operate quasi-linearly (a0 ≈ 1–2) and place protons in the positive-focusing quarter-period, accepting lower gradient but good efficiency and beam quality; or (b) use high-intensity near-critical bubbles with an electron-column (OAM) driver or the front-layer focusing. Option (a) also needs γ_p small enough to trap, which in the linear regime means **n_e near critical (γ_p ≈ ω0/ω_p ≈ 1–3)**, where linear theory breaks down. So the realistic options are density-ramped near-critical (S4) or programmable-focus (S7, S8) drivers.

### S12. Badiali, Almeida, Malaca, Fonseca, Silva, Vieira — "Tailored laser wakefield acceleration for decaying particles" (2026) [paper] **(key design model)**

- **Citation:** C. Badiali et al., *Phys. Rev. Research* **8**, 023077 (2026), published 27 Apr 2026. DOI: [10.1103/1pp8-qx35](https://doi.org/10.1103/1pp8-qx35). Open access (CC-BY 4.0); I read the full PDF. The data are not public ("available on request").
- **Scheme:** a **subluminal space-time / flying-focus driver** (intensity peak at fixed v_f < c inside an envelope moving at c) plus a **tailored plasma density n(z)**, chosen so the phase velocity of the n_w-th bucket equals the instantaneous beam velocity. The profile starts with a down-ramp, which slows the bucket's back so the slow beam is captured, then an up-ramp that shortens λ_p and keeps phase-lock as v → v_f. The model works for **any particle mass, including protons**. In the linear regime it extends to positive particles.
- **Implementable model** (Eqs. 1a, 1b; Appendix A):
  - **d[γ(z) v(z)]/dz = ε0 (q/e)(m_e/m_p)(ω_p0 c / v_f) √(n(z)/n0)**, with E_z = ε0 (m_e ω_p0 c/e) √(n/n0).
  - **v_w = v_f − 2π n_w (v_f²/ω_p0) · d/dz √(n0/n(z))**, and impose v_w = v(z).
  - The bucket centre sits at ζ_w = v_f t − n_w λ_p(z), with λ_p = 2π v_f/ω_p(z). Later buckets (n_w > 1) react more strongly to density changes, so a gentler taper suffices.
  - Laser energy (Eq. 2): **𝓔[J] ≈ 0.1 a0² w0²[µm] λ⁻²[µm] L[mm]** (L = envelope length).
  - The peak slips out of the envelope after t ≈ L/(c − v_f), so the useful focal travel is l = L v_f/(c − v_f).
  - Energy gain: Δγ m_p c² = q E_acc L v_f/(c − v_f).
  - Combined (Eq. 3): the required laser energy is ∝ a0² (Δγ m_p/(q m_e)) (c/v_f − 1) E_acc⁻¹ w0²/λ².
- **PIC:** **OSIRIS**, quasi-3D (modes m = 0, 1, benchmarked to m ≤ 3). n0 = 4×10^18 cm⁻³ (ω0/ω_p = 20). Window 344×51 µm, 27000×400 cells (dξ = 0.005 k_p⁻¹, dr = 0.05 k_p⁻¹), dt = 0.03 fs. Driver: λ = 0.8 µm, a0 = 3 (nonlinear) or 0.8 (linear), w0 = 3.56 µm, envelope 275 µm (L_env = 108 k_p⁻¹), injected by a plane-wave method. Witness: 0.2 mm × 0.5 µm, n_b = 10⁻³ n0. Masses tested up to m_π (264 m_e).
- **Results:**
  - Fixed v_f = 0.96c, beams starting at 0.94c: E_z ≈ **20 GV/m (0.2 GV/cm)**, stable for >9 ps. Maximum γ versus mass agrees with theory.
  - m_μ/4 beams from 0.5c, 0.7c and 0.9c with v_f = 0.8c, 0.9c and 0.97c are tracked well.
  - Beam loading: η_load = 0.13 gives **100% trapping of an 80 pC witness**, with 50% above 0.99c.
  - **Protons (theory only, Fig. 4): 0.5c → about 0.9c in tens of mm**, with a0 = 0.8, ω0/ω_p = 20, v_f = 0.7c.
  - Eq. 3 example (a0 = 0.8, w0 = 3.6 µm, v_f = 0.97c, E_acc = 20 GV/m): **Δγ = 5 needs about 9.2 J for protons** (about 4.7 GeV nominal gain, for a proton already near v_f) [rechecked: L ≈ 7.3 mm, 𝓔 ≈ 9.4 J].
- **Caveats [inference]:** Δγ = 5 for a proton at v ≈ 0.97c means γ ≈ 4 → 9, so the proton overtakes a fixed v_f = 0.97c focus. Reaching 6 GeV in one stage needs a **programmable (accelerating) focal velocity v_f(z)** rather than a fixed one, or staging. Sub-relativistic protons (0.5c) need low v_f, where the weak longitudinal gradient caveat of S7 applies. Still, this is the cleanest **quasi-linear, Joule-class, density-and-driver-co-designed** model in the literature for slow heavy particles. It fits an "energy-efficient" brief, since linear wakes allow beam loading at high efficiency.

### S13. Isayama, Nakahara, Morita, Hoshino, Abe, Taguchi, Nikaido, Kuramoto, et al. — "Bow-wake acceleration of ions toward a relativistic regime" (2026) [paper] **(first experiment claiming proton injection into a laser-driven wake)**

- **Citation:** S. Isayama et al., *Commun. Phys.* **9** (2026). DOI: [10.1038/s42005-026-02749-7](https://doi.org/10.1038/s42005-026-02749-7). Open access (CC-BY 4.0); I read the full PDF. **Code and data:** Zenodo [10.5281/zenodo.20821422](https://doi.org/10.5281/zenodo.20821422), with EPOCH input deck and filament-generation Python scripts (see `original-sims/bow-wake-isayama2026/`).
- **Concept, "bow-wake acceleration" (BWA):** in near- or over-critical, relativistically transparent plasma the laser front moves slowly. The compressed electron layer *ahead* of the laser (the "bow wake") forms a charge-separation potential that co-moves almost synchronously with ions, so **protons at rest can be trapped**. This is the same physics as the front-layer trapping in S1–S3, in experimentally accessible parameters.
- **Experiment:** **J-KAREN-P**, 800 nm, **4.3 J (case A) / 7.6 J (case B) on target, 45 fs, F/1.3, 1.6 µm FWHM spot**, giving **3.07 / 5.48 ×10^21 W/cm²**. Linear polarization, plasma mirror (10⁻⁸ at 1 ps). Targets: **100 µm resorcinol-formaldehyde foam**, 30 and 100 mg/cm³ (n_e,ave ≈ **5 n_c and 17 n_c**; H:C:O = 5:4:2). Detection: 3-layer scintillator TOF at 5.45 m.
- **Results:** 29 shots. Most are TNSA-like; **2 shots reach about 46 MeV (A) and about 60 MeV (B)**, both near the relativistic-transparency threshold. Rear TNSA in simulation gives only 17 MeV, and the isothermal TNSA estimate is 28–37 MeV. Interaction length about 5 µm.
- **3D EPOCH:** box 200×20×20 µm, **dx = dy = dz = 80 nm**, 10 ppc per species, T_e = T_i = 10 keV initial (100 eV tests give little change). Pre-ionized H⁺:C⁶⁺:O⁶⁺ foam with a **stochastic 3D filament model** of the foam structure. Case B gives BWA protons **42–167 MeV (mean 113 MeV) over 5 random-filament runs**. Slab-model theory: **E_inj ≈ 0 (rest protons trapped), E_p,max ≈ 162 MeV**. Case A: E_inj ≈ 36 MeV, so protons are not fully trapped.
- **Model (slab, Ref. 28 = Brantov et al. PRL 116, 085004, 2016, "Synchronized ion acceleration by ultraintense slow light"):** the bow-wake potential amplitude balances the ponderomotive potential, and the propagation velocity comes from hole-boring with relativistic transparency (Weng et al. PoP 19, 022705; NJP 14, 063026). The trapping condition has the same form as S3/S9 with v_p = front velocity.
- **Outlook in the paper:** density gradients to extend the interaction (cf. S4), and dual-pulse two-stage (solid-density seed, then low-density BWA; Isayama et al. PoP 28, 073101, 2021).
- **6 GeV relevance [inference]:** this is the experimental proof that slow, near-critical laser fronts trap rest protons. It is the realistic **injector physics** for a density-ramped proton wake. Energies are 60 MeV measured and about 160 MeV simulated.

### S14. Additional slow-wake, hybrid and confined-field proton schemes (shorter notes)

- **Brantov, Govras, Kovalev, Bychenkov**, "Synchronized ion acceleration by ultraintense slow light", *Phys. Rev. Lett.* **116**, 085004 (2016), DOI [10.1103/PhysRevLett.116.085004](https://doi.org/10.1103/PhysRevLett.116.085004) [abstract only]. A relativistic pulse enters **near-critical** plasma, **slows strongly, then speeds up** as it propagates (self-focusing/transparency), so ions stay synchronized. 3D PIC, fs PW-class, gives a significant gain over optimized ultrathin foils. This is the theoretical basis of BWA (S13) and the same physics as the S4 density ramp.
- **Isayama, Chen, Liu, Chen, Kuramitsu**, "Efficient hybrid acceleration scheme for generating 100 MeV protons with tabletop dual-laser pulses", *Phys. Plasmas* **28**, 073101 (2021), DOI [10.1063/5.0049725](https://doi.org/10.1063/5.0049725) [abstract only]. Tens-of-TW, few-J **dual pulses** on tandem solid plus near-critical targets. RPA → LWFA → TNSA gives about **220 MeV** (2D PIC), about 3× single-pulse.
- **Murakami et al.**, "Generation of giga-electron-volt proton beams by micronozzle acceleration", *Sci. Rep.* **15**, 19112 (2025), DOI [10.1038/s41598-025-03385-x](https://doi.org/10.1038/s41598-025-03385-x) [abstract only]. A micron H₂ rod inside a hollow micronozzle makes a long-lived axial field at the nozzle tail, giving **≳GeV protons** (2D PIC; the required intensity was lost in the abstract formula, likely about 10^22–10^23 W/cm²).
- **Pan and Murakami**, "Dual-pulse micronozzle acceleration of sub-GeV-class protons", *Phys. Rev. Accel. Beams* **29** (2026), DOI [10.1103/kjnr-rfy9](https://doi.org/10.1103/kjnr-rfy9) [abstract only]. A prepulse makes a compact proton front that is **phase-locked** with the main-pulse axial field. At 10^21 W/cm², sub-GeV cutoffs with **about 20% total laser→proton efficiency and >13% into E_p > 100 MeV**. 3D slit geometry gives about 60% higher cutoff than an unconfined rod. **This is the highest efficiency figure found** and is relevant to an "energy-efficient" injector.
- **Chen, Lu, Wang, Xiong, Chen, Zhou, Lan, Huang**, "High-energy proton beam generation via combined radiation pressure acceleration and laser wakefield acceleration in modulated plasma channels", *Eur. Phys. J. D* **79** (2025), DOI [10.1140/epjd/s10053-025-00977-0](https://doi.org/10.1140/epjd/s10053-025-00977-0) [title only; no abstract retrieved]. This is the latest RPA+LWFA hybrid, using a modulated channel.
- **Willim, Vieira, Malka, Silva**, "Proton acceleration with intense twisted laser light", *Phys. Rev. Research* **5**, 023083 (2023), DOI [10.1103/PhysRevResearch.5.023083](https://doi.org/10.1103/PhysRevResearch.5.023083) [abstract only]. A few-J twisted (OAM) laser on a double-layer H target in near-critical plasma gives about **40 MeV, with 6.5× lower divergence** than Gaussian. 3D PIC (OSIRIS presumably).
- **Arrowsmith, Miller, …, Palastro, et al.**, "Dephasingless laser wakefield acceleration of electrons using a flying focus", *Nat. Phys.* **22**, 1513 (2026), DOI [10.1038/s41567-026-03352-x](https://doi.org/10.1038/s41567-026-03352-x) [abstract only]. The **first experimental demonstration** that a flying focus beats the dephasing limit (by 2×) for electrons. It validates the spatiotemporal-driver tools of S7, S8 and S12.
- **Debus, Pausch, Huebl, Steiniger, Widera, Cowan, Schramm, Bussmann**, "Circumventing the dephasing and depletion limits of laser-wakefield acceleration" (TWEAC), *Phys. Rev. X* **9**, 031044 (2019), DOI [10.1103/PhysRevX.9.031044](https://doi.org/10.1103/PhysRevX.9.031044) [abstract only]. Two obliquely incident, pulse-front-tilted pulses whose overlap moves at c. Electrons only, and **no ion/proton TWEAC study found** (2026-10). [inference] The overlap velocity is a geometric parameter (tilt and crossing angle), so a subluminal TWEAC variant for protons is conceivable but unpublished.
- **Barraza-Valdez, Tajima, Strickland, Roa**, "Laser beat-wave acceleration near critical density", *Photonics* **9**, 476 (2022), DOI [10.3390/photonics9070476](https://doi.org/10.3390/photonics9070476) [abstract only]. Two co-propagating lasers beat near n_c, giving a low-phase-velocity wake at 10^14 W/cm² (1D PIC, keV electrons). [inference] It is a possible low-intensity route to slow wakes, not shown for ions.

---

## Which paper is "Enhanced proton acceleration using (self-)injected nanoparticles"? [inference]

No paper with that exact title was found. I checked arXiv API full-text fields, OpenAlex, Europe PMC, Crossref, Zenodo and web search; no arXiv abstract combines "nanoparticle" with "proton acceleration". Ranked candidates:

1. **Vallières et al., PRAB 22, 091303 (2019), "Enhanced laser-driven proton acceleration using ultrasmall nanoparticles" (N10).** This is the closest title match ("Enhanced … proton acceleration using … nanoparticles").
   - Setup: 10 nm Au/Ag NPs spray-dried onto 15 µm Al. TITAN (220 J, 700 fs) and ELFIE (12 J, 350 fs) lasers at 3×10^19 – 5×10^20 W/cm².
   - Measured: about **2× in maximum energy and yield** (best: +97% E_max, +190% yield with Au on ELFIE).
   - Simulated: PICLS 2D gives up to 4× (diameter scan) and **7× (100 nm gaps)** in cutoff.
   - The NPs are deposited, not injected, and the mechanism is TNSA absorption enhancement.
2. **NP-assisted *injection* (electrons):** Aniculaesei et al. PR Applied 2019 (338 MeV, 4.7%); Aniculaesei et al. MRE 2024 (10 GeV, 340 pC, Texas PW); Cho et al. Sci. Rep. 2018 (theory, JoPIC); Xu et al. Sci. Rep. 2022 (>90% injection, >300 pC). These match "injected nanoparticles" in the sense of NPs *introduced into the gas* to *trigger injection*, but for **electrons**. The ablation-in-cell method makes the NPs inside the target itself, which may be the origin of "self-injected".
3. **Cluster/nanoparticle targets for high-energy protons (simulation):** Matsui, Fukuda, Kishimoto PRL 2019 (**about 300 MeV**, 10% spread, from a micron H cluster with converging shock and RIT). Nishihara et al. 2016 (**450 MeV** from a 700 nm CH particle at a ≈ 100). Jinno et al. 2022 (experiment: 12.4 MeV, 1.6×10^9 /MeV/sr at 2.8 MeV, J-KAREN-P 0.1 Hz).
4. **Mass-limited spheres:** Hilz et al. Nat. Commun. 2018 (20–40 MeV quasi-monoenergetic, PHELIX 150 J).
5. **Ambient-ion acceleration by an NP's field:** Klimešová et al. PRA 2021 (He⁺ from the surrounding gas gains more energy than the NP's own ions). This is the literal "ions injected by an NP field", at eV–keV scale.

If the phrase came from a talk or slide about **proton** wakes, the most plausible intended meaning is either (1) as a citation for "enhanced proton acceleration", or (2)+(3) as the idea "use NPs/clusters inside the gas as a local proton source plus injector for the wake". Item (3) has the right energy scale (0.3–0.45 GeV, β ≈ 0.65–0.73) to feed a near-critical density-ramped proton wake. That is my inference; no published paper does this.

---

## Summary table of proton-wake (and proton-injector) schemes

Gradient = average energy gain / acceleration length, my estimate unless the paper states it. Efficiency = laser → protons as reported. "n/r" = not reported.

| Scheme (ref) | Laser parameters | Plasma / target | Proton energy reached | Avg. gradient | Efficiency | Injection | Code |
|---|---|---|---|---|---|---|---|
| Bubble self-injection, Gaussian (S1, Shen 2007) | about 10^23 W/cm², about 100 PW (quoted by S2) | dense tritium + H | multi-GeV (abstract) | n/r | n/r | self (background p) | VORPAL 3D (likely) |
| Sequential RPA → bubble (S3, Shen 2009) | CP, 2.14×10^23 W/cm², 18.3 kJ, 12.5T, 16 µm | H micro-target 10 n_c in 0.3 n_c T | **38 GeV peak** (42 max), 12.6%, 6×10^9 p >35 GeV; a = 71: about 8 GeV | about 60 TV/m | about 0.2% [inf.] | RPA pre-accel. | VORPAL 2D |
| Moving double layer (S5, Yu 2010) | CP, 10^21–10^23 W/cm² | thin foil + underdense gas | "tens of GeV" (60 GeV quoted) | n/r | n/r | RPA pre-accel. | 1D/2D PIC |
| Snowplow RPA → wake (S6, Zheng 2011) | CP, a0 = 250 (1.7×10^23), about 116 fs | H foil 0.5λ + 0.01 n_c gas, 1.2 cm | **540 GeV** (1D), 50 GeV (2D, 0.2 n_c) | about 48 TV/m | n/r | RPA pre-accel. | KLAP 1D/2D |
| RPA + **density-ramped near-critical** LWFA (S4, Liu 2018) | CP, a0 = 50 (6.9×10^21), 33 fs, about 10 PW; a0 = 120 (4×10^22) | CH foil + C plasma 4 n_c e^{−x/20λ} (1.2 n_c e^{−x/60λ}) | **2 GeV** (a0 = 50), 4.7 GeV (flat-top pulse); **>10 GeV** (a0 = 120) | about 20–35 TV/m | **6%** (a0 = 50); **11.4%** (a0 = 120) | RPA → slow near-critical wake | OSIRIS 2D |
| LG10 donut, electron pillar (S9, Zhang 2014) | CP LG10, P equal to 2.14×10^22 W/cm² SG (a0 = 70.7) | tritium 2.4×10^20 cm⁻³ | **1 → 7 GeV** (witness, 160 pC) | about 9 TV/m | n/r | external (1 GeV) | VORPAL 3D |
| **Light-spring** OAM (S2, Guo 2024) | 2×LS, 4.81 PW, a ≈ 100, 2.15×10^22 W/cm² | T:H = 70:1, 1.23×10^27 m⁻³ (0.71 n_c) | **8.7 GeV** self-inj.; **0.11 → 10.6 GeV** witness | about 29 TV/m | **11%** (>0.5 GeV) | self + external | EPOCH 3D |
| **Transverse flying focus** (S7, Gong 2024) | 0.8 kJ, 21 ps, 37.5 TW, 3×10^20 W/cm² | H, 5.5×10^19 cm⁻³ (underdense) | **1.64 GeV**, 3.7%, 23 pC | about 0.37 TV/m | **0.13%** | **from rest** | EPOCH 3D |
| Subluminal driver + tailored density (S12, Badiali 2026) | a0 = 0.8–3, few-J, v_f = 0.7–0.97c | n0 = 4×10^18 cm⁻³, tailored n(z) | protons: theory 0.5c → 0.9c; Δγ = 5 for about 9 J (Eq. 3) | about 0.02 TV/m (20 GV/m) | n/r (80 pC trapped 100%, μ/4 test) | external, velocity-matched | OSIRIS q-3D |
| **Bow-wake** (S13, Isayama 2026), **experiment** | J-KAREN-P 7.6 J, 45 fs, 5.5×10^21 W/cm² | RF foam 17 n_c, 100 µm | **60 MeV** measured; 42–167 MeV sim | about 12 TV/m (60 MeV / 5 µm) | n/r | **from rest** (slow front) | EPOCH 3D (**deck public**) |
| Two-frequency tweezer (S10, Wan 2020) | 2×CP a0 = 16, λ and 2λ, 10 cycles; 1–80 J scan | 20–50 nm CH foil | 220 MeV (3D); **20–830 MeV** (2D, 1–80 J) | about 60 TV/m field | n/r (2–5× LS) | optical beat velocity | OSIRIS 3D/2D |
| Dual-pulse micronozzle (S14, Pan and Murakami 2026) | about 10^21 W/cm², two pulses | H rod in micronozzle | sub-GeV cutoffs | n/r | **about 20%** (>13% for >100 MeV) | phase-locked prepulse front | PIC 2D/3D |
| H-cluster shock + RIT (N7, Matsui 2019) | PW-class, about 10^22 W/cm² | micron H cluster | **about 300 MeV**, 10%, 5° | n/r | n/r | n/a (injector) | 3D PIC |
| CH nanoparticle (N11, Nishihara 2016) | a ≈ 100 | 700 nm-radius CH particle | **450 MeV** in 130 fs | n/r | >10% of particle protons forward | n/a (injector) | 3D PIC |
| Levitated microsphere (N5, Hilz 2018), **experiment** | PHELIX 150 J, 500 fs, ≤7×10^20 W/cm² | 1 µm PMMA sphere | 20–40 MeV, about 25% spread | about 2.5 TV/m field | 0.3% (sim.) | n/a (injector) | PIConGPU 3D |
| Ultrasmall NPs on foil (N10, Vallières 2019), **experiment** | TITAN 220 J/700 fs; ELFIE 12 J/350 fs; ≤5×10^20 | 10 nm Au/Ag NP on 15 µm Al | about 2× E_max and yield vs flat (MeV–tens of MeV) | TNSA | n/r (absorption ↑) | n/a (TNSA source) | PICLS 2D |

---

## Implications for a 6 GeV proton LWFA [inference unless cited]

1. **The trapping requirement sets the wake velocity.** For a proton starting at rest, the wake potential must satisfy **e Δφ ≥ (1 − 1/γ_p) m_p c²** (S3, S9, S2). With the full potential swing, the dephasing-limited gain is **W_max = 2 γ_p² β_p² m_p c²**.
   - 6 GeV therefore needs only **γ_p β_p ≈ 1.8 (v_p ≈ 0.87c, γ_p ≈ 2.05)** with a trapping potential of (1 − 1/2.05) × 938 MeV/e ≈ **0.48 GV**.
   - This is far below the γ_p ≈ 10–50 of gas-density LWFA, which would demand 0.85–0.92 GV of potential to trap a rest proton and would then overshoot. A *fixed-velocity* 6 GeV stage is therefore a **near-critical** device.
   - With the hole-boring front-velocity law v_p/c = Ξ/(1 + Ξ), Ξ = a√(n_c/n_e′) (S9, Eq. 3), v_p = 0.873c means **a√(n_c/n_e′) ≈ 6.9**. Use the Weng formula (S4, Eq. 4) as a cross-check.
   - Shen 2009's lower-intensity variant (a = 100/√2, 0.35 n_c → about 8 GeV) is consistent with this.
2. **Positive-charge focusing must be designed in.** Options:
   - (a) OAM/LG or light-spring drivers that leave an on-axis electron column (S2, S9). This is the most robust in 3D PIC, at about 5 PW.
   - (b) Riding the compressed front layer of the bubble (S3, S13).
   - (c) Quasi-linear wakes, using the λ_p/4 window where E_z accelerates and E_r focuses positive charges (S11, S12).
   - Plain Gaussian blowout loses protons transversely (S2, S9: <1–2 GeV).
3. **Use a ramp, not a uniform plasma.** A down-ramped near-critical density (S4) or a velocity-programmed driver (S7, S12) lets the wake accelerate with the proton. S4 roughly doubles the energy (1 → 2 GeV at a0 = 50; 5 → >10 GeV at a0 = 120) and the efficiency (4 → 6%; 6 → 11.4%) compared with uniform density. The Badiali coupled equations (S12, Eqs. 1a, 1b) are the most general way to compute the taper. Couple them with the near-critical front-velocity law for the high-density part.
4. **Recommended architecture (3 stages, each from published physics):**
   - **(i) Injector, 0.1–0.45 GeV (β ≈ 0.43–0.73).** Options: bow-wake/near-critical foam (S13, demonstrated 60 MeV); dual-pulse micronozzle (S14, about 20% efficiency); H-cluster or CH-nanoparticle targets (N7 300 MeV, N11 450 MeV); or an RPA foil (S4).
   - **(ii) Near-critical, density-down-ramped wake to about 2–5 GeV.** S4 parameters scaled: a0 ≈ 50–120, n_e from about 4 n_c down to ≪ n_c over 50–300 µm. Add an OAM driver for focusing (S2).
   - **(iii) Optional quasi-linear, velocity-matched booster** (flying-focus or space-time driver plus tailored n(z), S12) to finish at 6 GeV with better beam quality and beam-loading efficiency.
   - The single-stage alternative is the S2 light-spring scheme, 8.7 GeV at 4.8 PW.
5. **Gradients and length.** Near-critical stages give **20–60 TV/m** average, so 6 GeV is reached in about **0.1–0.3 mm** (S2–S4). The underdense TFF (S7) gives about 0.4 TV/m (about 1.5 cm for 6 GeV). The quasi-linear tailored stage gives about 20 GV/m (about 0.3 m for 6 GeV).
6. **Energy budget.** E_laser ≈ N_p W / η.
   - With the best simulated efficiencies (S2: 11%; S4: 11.4%), 10^10 protons at 6 GeV (9.6 J in the beam) need about **90–100 J** of laser on target. That is single-shot PW-class (5–10 PW, 20–50 fs). TFF-type efficiencies (0.1%) would need about 10 kJ.
   - S12's Eq. 3 suggests a quasi-linear booster needs only tens of J per few-GeV for small charge, but its efficiency is unquantified.
   - **Efficiency, not peak energy, should be the main optimisation target for the project.** The literature reports ≤11% (high-intensity) and ≤20% (sub-GeV micronozzle).
7. **Key risks:**
   - All multi-GeV results are **simulations** (2D or 1-ppc 3D). The only experimental proton-wake evidence is BWA at 60 MeV (S13).
   - Near-critical laser propagation is sensitive to filamentation, hosing and foam inhomogeneity. S13 sees large shot-to-shot spread (42–167 MeV across random-filament runs).
   - Many schemes use **heavy-ion (tritium/carbon) backgrounds** for bubble stability (S1–S3, S9, S2). That is impractical (tritium) or changes the physics (carbon).
   - The S2 light-spring needs coherent 7-beam OAM synthesis; an imperfect LS needs 12.3 PW and works in 25% of runs.
8. **Simulation plan for MCF.**
   - Start from the public EPOCH bow-wake deck (`original-sims/bow-wake-isayama2026/`) for the injector physics.
   - Rebuild S4 (OSIRIS 2D parameters in `original-sims/rpa-lwfa-hybrid/SOURCE.md`) in EPOCH or WarpX with an exponential down-ramp.
   - Validate trapping against e Δφ = (1 − 1/γ_p) m_p c² and v_p(Ξ).
   - Then add an LG/OAM driver (parameters in `original-sims/proton-bubble-vortex/SOURCE.md`) and measure laser→proton efficiency above 1 GeV as the primary metric.
