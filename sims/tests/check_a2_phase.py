import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
from test_pic1d_vs_fluid import run_case
for dx, ppc in [(0.02, 16), (0.01, 32)]:
    sim, xi_p, Ef = run_case(2.0, 1.0, 2.3548, dx=dx, ppc=ppc)
    m = (xi_p < -2) & (xi_p > -25)
    def zc(E):
        s = np.where(np.diff(np.sign(E[m])) != 0)[0]
        return xi_p[m][s]
    print("PIC zero crossings  :", np.round(zc(sim.E)[-6:], 3))
    print("fluid zero crossings:", np.round(zc(Ef)[-6:], 3))
    en = sim.energies()
    print("energy: laser_work=%.4f field+kin_e=%.4f" % (en["laser_work"], en["field"] + en["kin_e"]))
