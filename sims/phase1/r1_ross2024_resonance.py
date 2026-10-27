"""R1: reproduce Ross et al., PRR 6, L022001 (2024): resonant excitation by a ~10-pulse train,
spacing 170 fs, 31 fs FWHM pulses, lambda = 800 nm. Measured resonance at 4.3e17 cm^-3 with FWHM
1.6e17; their fluid model gives ~3 GV/m (0.8 J effective) to ~10 GV/m (2.5 J).
1D nonlinear fluid model (fluid1d) — reports wake amplitude behind the train vs on-axis density.
a0 per pulse from energy: E_pulse = E_train/N, w0 = 45.5 um (1/e^2 intensity radius), 31 fs FWHM.
"""
import sys, os, json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import fluid1d as F
import plasma as PL
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
lam = 0.8e-6; N = 10; spacing = 170e-15; fwhm_t = 31e-15; w0 = 45.5e-6

def a0_from_energy(Ep):
    P = Ep / (fwhm_t * 1.0645)          # Gaussian: E = P * FWHM * sqrt(pi/(4 ln2))
    I = 2 * P / (np.pi * w0**2)          # peak intensity W/m^2
    return PL.a0_from_intensity(I, lam)

def wake_amp(n_cm3, a0, N=N, spacing=spacing):
    n = n_cm3 * 1e6
    wp = PL.omega_p(n)
    gp = PL.gamma_p_of_density(n, lam); bp = np.sqrt(1 - 1 / gp**2)
    sp = spacing * wp * bp; fw = fwhm_t * wp * bp       # in c/wp
    lamp = 2 * np.pi
    xi = np.arange(-(N - 1) * sp - 6 * lamp, 4 * fw, 0.01)
    a2 = sum(F.gaussian_envelope(xi, -k * sp, fw, a0) for k in range(N))
    phi, E, br = F.solve_wake(xi, a2, np.zeros_like(xi), bp)
    m = xi < -(N - 1) * sp - 2 * fw
    return np.abs(E[m]).max() * PL.E0(n) / 1e9, br

dens = np.linspace(1.5e17, 8e17, 66)
res = {}
for label, Etr in [("linear(0.01J)", 0.01), ("0.8J", 0.8), ("2.5J", 2.5)]:
    a0 = a0_from_energy(Etr / N)
    amps = np.array([wake_amp(d, a0)[0] for d in dens])
    i = np.argmax(amps); half = amps >= amps[i] / 2
    idx = np.where(half)[0]
    fwhm_n = dens[idx[-1]] - dens[idx[0]]
    res[label] = dict(a0=float(a0), n_res=float(dens[i]), amp_res_GVm=float(amps[i]), fwhm_n=float(fwhm_n),
                      fwhm_rel=float(fwhm_n / dens[i]), amps=amps.tolist())
    print(f"{label:14s}: a0/pulse={a0:.3f} resonance n={dens[i]:.3g} cm^-3, peak wake={amps[i]:.2f} GV/m, "
          f"amplitude-FWHM={fwhm_n:.3g} cm^-3 (rel {fwhm_n/dens[i]:.3f}; paper theory 8/(3N)={8/(3*N):.3f}; measured 1.6e17/4.3e17={1.6/4.3:.3f})")
fig, ax = plt.subplots(figsize=(7, 4))
for k, v in res.items():
    ax.plot(dens / 1e17, np.array(v["amps"]) / max(v["amps"]), label=f"{k}, a0={v['a0']:.2f}")
ax.axvline(4.3, color="k", ls="--", lw=0.8, label="measured resonance 4.3e17")
ax.axvspan(4.3 - 0.8, 4.3 + 0.8, color="gray", alpha=0.15, label="measured FWHM 1.6e17")
ax.set_xlabel("on-axis density [1e17 cm^-3]"); ax.set_ylabel("normalised wake amplitude"); ax.legend(fontsize=8)
ax.set_title("R1: Ross 2024 resonance, 10 pulses @170 fs (1D fluid)")
plt.tight_layout(); plt.savefig(os.path.join(ROOT, "results", "figures", "R1_ross2024_resonance.png"), dpi=110)
json.dump(dict(dens=dens.tolist(), cases=res), open(os.path.join(ROOT, "results", "data", "R1_ross2024.json"), "w"), indent=1)
