"""R2: reproduce Hooker et al., J. Phys. B 47, 234003 (2014) multi-pulse LWFA design:
N = 120 pulses, 10 mJ, 100 fs FWHM, lambda = 1 um, a0 = 0.052, spacing = plasma period,
n = 1.75e17 cm^-3. Paper: wake grows linearly with N to 4.7 GV/m (immobile / Xe8+ ions),
~2.5 GV/m with mobile hydrogen ions (published version).
1D envelope PIC (kinetic) with immobile ions and with mobile protons; wake amplitude vs
position in the train (i.e. vs number of pulses that have passed).
"""
import sys, os, json, time
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
import pic1d_env as P
import plasma as PL
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
lam = 1.0e-6; n = 1.75e17 * 1e6; a0 = 0.052; N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
wp = PL.omega_p(n); E0 = PL.E0(n)
gp = PL.gamma_p_of_density(n, lam); bg = np.sqrt(1 - 1 / gp**2)
fw = 100e-15 * wp           # intensity FWHM in c/wp (luminal)
sp = 2 * np.pi * bg         # spacing = one plasma period (in xi, at v_g)
print(f"E0={E0/1e9:.1f} GV/m, gamma_g={gp:.1f}, pulse FWHM={fw:.2f} c/wp, spacing={sp:.3f} c/wp")
pulses = [P.Pulse(a0, fw, -k * sp, "gauss") for k in range(N)]
out = {}
fig, ax = plt.subplots(figsize=(9, 4))
for mobile in [False, True]:
    drv = P.Driver(pulses, x_start=0.0, velocity=bg)
    Ltrain = (N - 1) * sp
    Lx = Ltrain + 40.0
    Lr = 60.0
    dens = lambda x: np.sin(0.5 * np.pi * np.clip((x - 10.0) / Lr, 0, 1))**2
    sim = P.Sim1D(Lx, 0.05, dens, drv, ppc=8, dt=0.025, mobile_ions=mobile, x_window0=-(Ltrain + 30.0))
    t0 = time.time()
    sim.run(10.0 + Lr + Ltrain + 40.0)
    xi = sim.grid - drv.xd
    # amplitude of wake vs number of pulses passed: max |E| in each period after pulse k
    ks = np.arange(1, N + 1)
    amp = []
    for k in ks:
        m = (xi < -(k - 1) * sp - 0.5 * sp) & (xi > -k * sp - 0.5 * sp)
        amp.append(np.abs(sim.E[m]).max() if m.any() else np.nan)
    amp = np.array(amp) * E0 / 1e9
    behind = np.abs(sim.E[xi < -Ltrain - 2 * fw]).max() * E0 / 1e9
    lab = "mobile H+" if mobile else "immobile ions"
    out[lab] = dict(amp_vs_N=amp.tolist(), amp_behind_train_GVm=float(behind), runtime_s=time.time() - t0,
                    laser_work=float(sim.pond_work))
    print(f"{lab}: wake behind train = {behind:.2f} GV/m; after 30 pulses {amp[29]:.2f}, 60: {amp[min(59,N-1)]:.2f} GV/m ({time.time()-t0:.0f}s)")
    ax.plot(ks, amp, label=lab)
ax.plot(ks, ks * amp[0] if False else ks * out["immobile ions"]["amp_vs_N"][0], "k:", lw=0.8, label="linear growth (N x first pulse)")
ax.axhline(4.7, color="C0", ls="--", lw=0.8, label="paper: 4.7 GV/m (immobile/Xe8+)")
ax.axhline(2.5, color="C1", ls="--", lw=0.8, label="paper: ~2.5 GV/m (mobile H)")
ax.set_xlabel("number of pulses passed"); ax.set_ylabel("wake amplitude [GV/m]"); ax.legend(fontsize=8)
ax.set_title("R2: Hooker 2014 multi-pulse LWFA, 1D envelope PIC")
plt.tight_layout(); plt.savefig(os.path.join(ROOT, "results", "figures", "R2_hooker2014_multipulse.png"), dpi=110)
json.dump(out, open(os.path.join(ROOT, "results", "data", "R2_hooker2014.json"), "w"), indent=1)
