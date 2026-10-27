"""R3: reproduce the dephasing-mitigation result of Lahaye et al., PRR 8, 023274 (2026) with
Wake-T (2D quasi-static, laser-envelope evolution), using the paper's FBPIC parameter set:
1 J-class Gaussian pulse, a0 = 1.6, tau(I FWHM) = 25 fs, w0 = 21 um (I FWHM 25 um), 0.8 um,
pre-formed matched parabolic channel n(r) = n0(z) + r^2/(pi r_e w0^4),
n0 = 1e18 cm^-3 flat  vs  n0 (1 + 0.08 z[mm]) linear up-ramp.
Paper (FBPIC): flat dephases after ~19 mm; gradient reaches ~1.4 GeV (+~20 %).
Injection differs: here a long, negligible-charge witness spread over the first bucket is
loaded at z = 0 (external injection) and the best-phase energy is tracked vs z.
"""
import sys, os, json, time, argparse
import numpy as np
import scipy.constants as ct
from wake_t import GaussianPulse, PlasmaStage, ParticleBunch

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
ap = argparse.ArgumentParser()
ap.add_argument("--case", default="flat")
ap.add_argument("--L", type=float, default=0.024)
ap.add_argument("--nout", type=int, default=24)
a = ap.parse_args()

n0 = 1e18 * 1e6
lam = 0.8e-6
w0 = 21e-6
a0 = 1.6
tau = 25e-15
r_e = ct.physical_constants["classical electron radius"][0]
par = 1.0 / (np.pi * r_e * w0 ** 4)
grad = 0.08 if a.case == "gradient" else 0.0


def dens(z):
    zmm = np.asarray(z) * 1e3
    ramp = 0.02 + 0.98 * np.clip(zmm / 0.5, 0, 1)   # 0.5 mm entrance ramp (Wake-T needs n>0)
    return n0 * ramp * (1 + grad * np.clip(zmm, 0, None))


kp = np.sqrt(n0 * ct.e ** 2 / (ct.epsilon_0 * ct.m_e)) / ct.c
lam_p = 2 * np.pi / kp
laser = GaussianPulse(xi_c=0.0, a_0=a0, w_0=w0, tau=tau, z_foc=0.0, l_0=lam)
# witness: uniform in xi over the region behind the laser (negligible charge), 100 MeV
npart = 6000
rng = np.random.default_rng(0)
xi = rng.uniform(-1.4 * lam_p, -0.2 * lam_p, npart)
x = rng.normal(0, 1e-6, npart); y = rng.normal(0, 1e-6, npart)
gam = 100.0 / 0.511
pz = np.full(npart, gam)
px = np.zeros(npart); py = np.zeros(npart)
w = np.full(npart, 1e-3)          # macro-particle weights (~1e-16 C total): test particles
bunch = ParticleBunch(w, x, y, xi, px, py, pz, name="witness")
bunch.xi0 = xi.copy()
stage = PlasmaStage(a.L, dens, wakefield_model="quasistatic_2d", n_out=a.nout,
                    laser=laser, laser_evolution=True, r_max=4 * w0, r_max_plasma=3.8 * w0,
                    xi_min=-1.6 * lam_p, xi_max=2.5 * ct.c * tau, n_r=100, n_xi=300,
                    parabolic_coefficient=par, ppc=2, dz_fields=lam_p / 4)
t0 = time.time()
out = stage.track(bunch, opmd_diag=False, show_progress_bar=False)
rows = []
for b in out:
    g = np.sqrt(1 + b.px ** 2 + b.py ** 2 + b.pz ** 2)
    E = (g - 1) * 0.511
    rows.append(dict(z_mm=float(b.prop_distance * 1e3), E_max_MeV=float(E.max()),
                     E_p99_MeV=float(np.percentile(E, 99.5))))
    print(f"z={b.prop_distance*1e3:6.2f} mm  E_max={E.max():7.1f} MeV", flush=True)
res = dict(case=a.case, n0_cm3=1e18, grad_per_mm=grad, a0=a0, w0=w0, tau=tau, rows=rows,
           runtime_s=time.time() - t0)
json.dump(res, open(os.path.join(ROOT, "results", "data", f"R3_lahaye_{a.case}.json"), "w"), indent=1)
print("runtime", time.time() - t0)
