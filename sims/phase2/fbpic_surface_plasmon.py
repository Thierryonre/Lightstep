"""Quasi-3D (FBPIC) test of laser-beat-driven surface-plasmon acceleration of protons in a hollow
plasma channel (concept of Lei et al., PRL 137, 105002 (2026), adapted to protons at 3 GeV).

Design (from the dispersion study S040): vacuum core radius R = 3 c/w_pw, surface mode at
w_sp = 0.662 w_pw with phase velocity 0.971c (3 GeV protons). Two co-propagating laser colours
(1.00 um and ~1.25 um, beat frequency = w_sp) are guided by the hollow core (core index 1 >
wall index); the beat moves at the guided mode's group velocity, which for w_laser ~ 3.3 w_pw is
close to 0.97c. Wall density n_w = n_c(1 um)/10.9 ~ 1.0e20 cm^-3.
Measured: on-axis E_z, surface-wave amplitude near the wall, beat/wave phase velocity, wave
persistence behind the laser envelope, laser energy absorbed, proton test bunch (3 GeV, small
emittance) energy change and radial focusing.
"""
import os, json, time, argparse
import numpy as np
from scipy.constants import c, e, m_e, m_p, epsilon_0
from scipy.signal import hilbert
from fbpic.main import Simulation
from fbpic.lpa_utils.laser import add_laser_pulse, GaussianLaser
from fbpic.lpa_utils.bunch import add_particle_bunch_gaussian

here = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--steps", type=int, default=6000)
ap.add_argument("--diag_every", type=int, default=500)
ap.add_argument("--a0", type=float, default=0.4)
ap.add_argument("--w_ratio", type=float, default=3.3, help="w_laser / w_pw(wall)")
ap.add_argument("--R_cwp", type=float, default=3.0)
ap.add_argument("--wsp", type=float, default=0.662, help="surface-mode frequency / w_pw")
ap.add_argument("--tau_fs", type=float, default=100.0, help="intensity FWHM of each colour")
ap.add_argument("--w0_R", type=float, default=0.65, help="laser waist / R (LP01 match ~ 0.65+1.619V^-1.5)")
ap.add_argument("--bunch", default="behind", choices=["behind", "centre"], help="proton bunch behind the envelope (S044) or at its centre, inside the beat (S045)")
ap.add_argument("--rmax_R", type=float, default=None, help="radial box size / R (default 3.5 R + 6 c/w_pw)")
ap.add_argument("--cuda", action="store_true")
ap.add_argument("--out", default="fbpic_sp_out")
a = ap.parse_args()

lam1 = 1.0e-6
w1 = 2 * np.pi * c / lam1
wpw = w1 / a.w_ratio
n_w = epsilon_0 * m_e * wpw ** 2 / e ** 2
cwp = c / wpw
R = a.R_cwp * cwp
w2 = w1 - a.wsp * wpw
lam2 = 2 * np.pi * c / w2
w0 = a.w0_R * R                                 # S044: 0.65 R; S045: LP01 mode-field radius
tau = a.tau_fs * 1e-15 / np.sqrt(2 * np.log(2))

dz = lam1 / 30
dr = R / 40
rmax = 3.5 * R + 6 * cwp if a.rmax_R is None else a.rmax_R * R
Nr = int(rmax / dr)
lam_sp = 2 * np.pi * cwp / (a.wsp / 0.9712)
Lz = 2.6 * c * tau * 2 + 8 * lam_sp
Nz = int(Lz / dz)
zmax, zmin = 0.0, -Lz
z0 = -2.6 * c * tau
z_ent = zmin   # hollow channel fills the whole box at t=0: the 1-um-waist laser (Z_R ~ 3 um)
               # starts focused inside the guiding core instead of diverging in vacuum
wall_edge = 0.05 * R


def dens(z, r):
    zp = 1.0
    rp = 0.5 * (1 + np.tanh((r - R) / wall_edge))
    return zp * rp


sim = Simulation(Nz, zmax, Nr, rmax, 2, dz / c, zmin=zmin, n_order=-1, use_cuda=a.cuda,
                 boundaries={"z": "open", "r": "reflective"})
sim.add_new_species(q=-e, m=m_e, n=n_w, dens_func=dens, p_nz=2, p_nr=2, p_nt=4,
                    p_zmin=z_ent, p_rmin=0.8 * R, p_rmax=0.95 * rmax)
sim.add_new_species(q=e, m=m_p, n=n_w, dens_func=dens, p_nz=2, p_nr=2, p_nt=4,
                    p_zmin=z_ent, p_rmin=0.8 * R, p_rmax=0.95 * rmax)
for lam in (lam1, lam2):
    add_laser_pulse(sim, GaussianLaser(a0=a.a0, waist=w0, tau=tau, z0=z0, zf=z0, lambda0=lam))
g0 = 1 + 3000.0 / 938.272
zb = z0 - 2.6 * c * tau - 2 * lam_sp if a.bunch == "behind" else z0
bunch = add_particle_bunch_gaussian(sim, q=e, m=m_p, sig_r=0.15 * R, sig_z=0.5 * lam_sp, n_emit=2e-10,
                                    gamma0=g0, sig_gamma=1e-4 * g0, n_physical_particles=1e4,
                                    n_macroparticles=20000, tf=0.0, zf=zb)
if bunch is None:
    bunch = sim.ptcl[-1]
sim.set_moving_window(v=c)
E0w = m_e * c * wpw / e
info = dict(n_wall_cm3=n_w / 1e6, R_um=R * 1e6, lam2_um=lam2 * 1e6, w0_um=w0 * 1e6, E0_wall_GVm=E0w / 1e9,
            lam_sp_um=lam_sp * 1e6, grid=[Nz, Nr], dz_um=dz * 1e6, dr_um=dr * 1e6)
print(json.dumps(info), flush=True)

os.makedirs(os.path.join(here, a.out), exist_ok=True)
out = dict(design=info, args=vars(a), snaps=[])
t0 = time.time()
done = 0
E0las = m_e * c ** 2 * w1 / c / e
while done < a.steps:
    n = min(a.diag_every, a.steps - done)
    sim.step(n, show_progress=False)
    done += n
    f0 = sim.fld.interp[0]
    z, r = f0.z, f0.r
    Ez_axis = f0.Ez[:, 0].real
    iw = np.argmin(np.abs(r - 0.9 * R))
    Ez_wall = f0.Ez[:, iw].real
    env = 2 * np.abs(hilbert(sim.fld.interp[1].Er[:, 0].real)) / E0las
    g = np.sqrt(1 + bunch.ux ** 2 + bunch.uy ** 2 + bunch.uz ** 2)
    T = (g - 1) * 938.272
    rr = np.sqrt(bunch.x ** 2 + bunch.y ** 2)
    np.savez_compressed(os.path.join(here, a.out, f"snap_{done:06d}.npz"), z=z, r=r, Ez_axis=Ez_axis,
                        Ez_wall=Ez_wall, env_a=env, Ez_map=f0.Ez.real[::2, ::2], Er_map=f0.Er.real[::2, ::2],
                        Bt_map=f0.Bt.real[::2, ::2], t=sim.time, pz=bunch.z.copy(), pr=rr, pT=T,
                        pw=bunch.w.copy())
    rec = dict(step=done, t_fs=sim.time * 1e15, Ez_axis_max_GVm=float(np.abs(Ez_axis).max() / 1e9),
               Ez_wall_max_GVm=float(np.abs(Ez_wall).max() / 1e9), a_max=float(env.max()),
               T_mean=float(T.mean()), T_max=float(T.max()), T_min=float(T.min()),
               r_rms_um=float(np.sqrt(np.mean(rr ** 2)) * 1e6), frac_inside_R=float(np.mean(rr < R)))
    out["snaps"].append(rec)
    print(f"step {done}: t={rec['t_fs']:.0f} fs |Ez|axis={rec['Ez_axis_max_GVm']:.1f} GV/m |Ez|wall={rec['Ez_wall_max_GVm']:.1f} "
          f"a={rec['a_max']:.2f} T={rec['T_min']:.1f}/{rec['T_mean']:.1f}/{rec['T_max']:.1f} MeV "
          f"r_rms={rec['r_rms_um']:.2f}um inside={rec['frac_inside_R']:.2f} ({time.time()-t0:.0f}s)", flush=True)
    json.dump(out, open(os.path.join(here, a.out, "summary.json"), "w"), indent=1)
