import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
import fluid1d as F, track1d as TR
from p1c_pic_check_matched import setup
T_inj, tau, f_field, load = 1000.0, 2.355, 0.7, float(sys.argv[1]) if len(sys.argv)>1 else 0.4
b0, a0, xi_lock, Epk = setup(T_inj, tau, f_field, load, 0.04, 0.75)
lam = 2*np.pi*b0
print(f"b0={b0:.4f} a0={a0:.3f} xi_lock={xi_lock:.3f} E_peak0={Epk:.3f}")
st = dict(beta=b0)
drv = lambda xi, t, xd: F.gaussian_envelope(xi, 0.0, b0*tau, a0)
def bp(t, xd, tr):
    bc = np.mean(TR.proton_beta(tr.pu)); xc = np.mean(tr.pxi)
    return min(max(bc + 0.02*(xc - xi_lock), 0.01), 0.99999)
tr = TR.Tracker(-3*lam - 4*b0*tau, 4*b0*tau, min(lam/300, b0*tau/30), drv, bp)
rng = np.random.default_rng(1)
tr.set_beam(xi_lock + 0.04*lam*rng.standard_normal(2000), T_inj*(1+0.01*rng.standard_normal(2000)), load*Epk/2000)
dt = 0.05*lam
for i in range(int(2000/(b0*dt))+1):
    E = tr.step(dt, energy_every=10, istep=i)
    if i % 2000 == 0:
        Ek, _ = TR.gather_cic(tr.pxi, tr.xi[0], tr.dxi, E)
        phi0, E0u, _ = F.solve_wake(tr.xi, drv(tr.xi,0,0), np.zeros_like(tr.xi), tr.beta_d)
        Eu, _ = TR.gather_cic(np.array([np.mean(tr.pxi)]), tr.xi[0], tr.dxi, E0u)
        print(f"xd={tr.xd:7.1f} beta_d={tr.beta_d:.5f} beta_c={np.mean(TR.proton_beta(tr.pu)):.5f} xc={np.mean(tr.pxi):.3f} (lock {xi_lock:.3f}) "
              f"std_xi={np.std(tr.pxi):.3f} E_at_beam(mean)={Ek.mean():.3f} unloadedE(xc)={Eu[0]:.3f} T={tr.kinetic().mean()*0.511:.1f}")
