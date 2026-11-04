"""Quasi-3D (FBPIC) test of the guided resonant flying-focus train (Phase-1 FF + RE combination).

Three Laguerre-Gauss components LG_{p,0}, p = 0, 3, 6, at the rigid-comb frequencies designed in
P1e (lambda = 1.000, 1.052, 1.118 um; peak velocity 0.875 c; spacing ~ w_p), equal power
(equal on-axis a0), focused at the entrance of a matched parabolic channel
n(r) = n0 + dn (r/W)^2, dn = 1/(pi r_e W^2), n0 = 3.09e18 cm^-3, W = 6.83 um (k_p W = 2.26).
Measured: on-axis laser intensity pattern (velocity of the peaks, shape) and the on-axis wake
E_z, to compare with the 1D model driven by the same on-axis intensity.
Run in WSL: python3 fbpic_waveguide_train.py --steps N
"""
import sys, os, json, time, argparse
import numpy as np
from scipy.constants import c, e, m_e, m_p, epsilon_0
from scipy.signal import hilbert
from fbpic.main import Simulation
from fbpic.lpa_utils.laser import add_laser_pulse, LaguerreGaussLaser
from fbpic.lpa_utils.bunch import add_particle_bunch_gaussian
import resource

here = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--steps", type=int, default=4000)
ap.add_argument("--a0", type=float, default=0.3)
ap.add_argument("--fwhm_periods", type=float, default=2.5)
ap.add_argument("--dz_per_lambda", type=float, default=16)
ap.add_argument("--diag_every", type=int, default=500)
ap.add_argument("--out", default="fbpic_train_out")
ap.add_argument("--protons", action="store_true", help="add a 1 GeV, ~16 fC proton test bunch")
ap.add_argument("--zb_um", type=float, default=-175.0)
ap.add_argument("--p_sigr", type=float, default=1.5e-6)
ap.add_argument("--p_sigz", type=float, default=8e-6)
ap.add_argument("--p_emit", type=float, default=1e-7, help="normalised emittance of the proton test bunch [m rad]")
ap.add_argument("--fine_after", type=int, default=1500, help="diagnose every 250 steps after this step")
ap.add_argument("--cuda", action="store_true", help="run on an NVIDIA GPU (FBPIC CUDA backend)")
a = ap.parse_args()
d = json.load(open(os.path.join(here, "fbpic_train_design.json")))
n0 = d["n_cm3"] * 1e6
W = d["W"]
wp = d["wp"]
Tp = 2 * np.pi / wp
lam_p = c * Tp
r_e = e ** 2 / (4 * np.pi * epsilon_0 * m_e * c ** 2)
dn = 1.0 / (np.pi * r_e * W ** 2)
tau = a.fwhm_periods * Tp / np.sqrt(2 * np.log(2))       # FBPIC: E ~ exp(-t^2/tau^2)

lam_min = min(d["lambdas"])
dz = lam_min / a.dz_per_lambda
Lz = 2.5 * c * tau * 2 + 2.5 * lam_p
Nz = int(Lz / dz)
rmax = 4.0 * W
dr = 0.2e-6
Nr = int(rmax / dr)
zmax = 0.0
zmin = -Lz
z0 = -2.6 * c * tau                  # train centre at t = 0
z_ent = z0 + 2.6 * c * tau           # channel entrance (= focus of all components)
ramp = 10e-6


def dens(z, r):
    prof = np.clip((z - z_ent) / ramp, 0.0, 1.0)
    return prof * (1.0 + dn / n0 * (r / W) ** 2)


sim = Simulation(Nz, zmax, Nr, rmax, 2, dz / c, zmin=zmin, n_order=-1, use_cuda=a.cuda,
                 boundaries={"z": "open", "r": "reflective"})
sim.add_new_species(q=-e, m=m_e, n=n0, dens_func=dens, p_nz=1, p_nr=2, p_nt=4,
                    p_zmin=z_ent, p_rmax=0.95 * rmax)
sim.add_new_species(q=e, m=m_p, n=n0, dens_func=dens, p_nz=1, p_nr=2, p_nt=4,
                    p_zmin=z_ent, p_rmax=0.95 * rmax)
for lam, p in zip(d["lambdas"], d["p_modes"]):
    las = LaguerreGaussLaser(p=p, m=0, a0=a.a0, waist=W, tau=tau, z0=z0, zf=z_ent, lambda0=lam)
    add_laser_pulse(sim, las)
bunch = None
if a.protons:
    g0 = 1 + 1000.0 / 938.272
    bunch = add_particle_bunch_gaussian(sim, q=e, m=m_p, sig_r=a.p_sigr, sig_z=a.p_sigz, n_emit=a.p_emit,
                                        gamma0=g0, sig_gamma=1e-3 * g0, n_physical_particles=1e5,
                                        n_macroparticles=20000, tf=0.0, zf=a.zb_um * 1e-6)
    if bunch is None:
        bunch = sim.ptcl[-1]
sim.set_moving_window(v=c)
print(f"n0={n0/1e6:.3e}, W={W*1e6:.2f} um, dn/n0={dn/n0:.2f}, lam_p={lam_p*1e6:.1f} um, "
      f"tau={tau*1e15:.0f} fs, grid {Nz}x{Nr}x2, steps {a.steps}", flush=True)

out = dict(design=d, a0=a.a0, fwhm_periods=a.fwhm_periods, snaps=[])
os.makedirs(os.path.join(here, a.out), exist_ok=True)
print(json.dumps(dict(z0_envelope_centre_um=z0 * 1e6, c_tau_um=c * tau * 1e6, lam_p_um=lam_p * 1e6)), flush=True)
t0 = time.time()
done = 0
while done < a.steps:
    every = a.diag_every if done < a.fine_after else max(a.diag_every // 2, 1)
    n = min(every, a.steps - done)
    sim.step(n, show_progress=False)
    done += n
    # (FBPIC's step() returns with all data back on the CPU, also in GPU mode)
    z = sim.fld.interp[0].z
    Ez0 = sim.fld.interp[0].Ez[:, 0].real                    # on-axis wake (mode 0)
    Er1 = sim.fld.interp[1].Er[:, 0]                         # laser field on axis (mode 1)
    env = np.abs(hilbert(Er1.real))
    E0las = m_e * c ** 2 * (2 * np.pi / 1e-6) / e
    extra = {}
    if bunch is not None:
        extra = dict(pz=bunch.z.copy(), px=bunch.x.copy(), py=bunch.y.copy(), pux=bunch.ux.copy(),
                     puy=bunch.uy.copy(), puz=bunch.uz.copy(), pw=bunch.w.copy())
    np.savez_compressed(os.path.join(here, a.out, f"snap_{done:06d}.npz"), z=z, Ez0=Ez0,
                        env_a=2 * env / E0las, r=sim.fld.interp[0].r,
                        Ez_map=sim.fld.interp[0].Ez.real[::2, ::2], Er_map=sim.fld.interp[0].Er.real[::2, ::2],
                        Bt_map=sim.fld.interp[0].Bt.real[::2, ::2],
                        rho_map=sim.fld.interp[0].rho.real[::2, ::2], t=sim.time, **extra)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    out["snaps"].append(dict(step=done, t=sim.time, Ez_max=float(np.abs(Ez0).max()),
                             a_env_max=float((2 * env / E0las).max()), max_rss_MB=rss))
    msg = f"step {done}: t={sim.time*1e15:.0f} fs, max|Ez| on axis = {np.abs(Ez0).max()/1e9:.2f} GV/m, max a(axis) = {(2*env/E0las).max():.3f}, maxRSS={rss:.0f} MB"
    if bunch is not None:
        gam = np.sqrt(1 + bunch.ux**2 + bunch.uy**2 + bunch.uz**2)
        msg += f", <T_p>={((gam.mean()-1)*938.272):.2f} MeV, r_rms={np.sqrt(np.mean(bunch.x**2+bunch.y**2))*1e6:.2f} um"
    print(msg + f" ({time.time()-t0:.0f}s)", flush=True)
    json.dump(out, open(os.path.join(here, a.out, "summary.json"), "w"), indent=1)
