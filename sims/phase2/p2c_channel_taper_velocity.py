"""P2c (optics): programming the velocity of the guided resonant train by tapering the channel.
Lasers' frequencies are fixed (designed at T = 1 GeV, see fbpic_train_design.json). Along the
stage the channel spot W(z) and on-axis density n0(z) change; for each (W, n0) we compute the
modal wavenumbers k_q of the fixed frequencies and (i) the peak velocity (best linear fit of
w_q vs k_q), (ii) the comb non-rigidity (residual phase slip per unit length -> coherence
length), (iii) the resonance detuning (mean spacing / local w_p).
Then we solve for the taper W(z) (n0 fixed, and n0 scaled) that keeps the train matched to a
proton accelerating from 1 GeV at a given gradient."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "codes"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
import plasma as PL
from p1e_waveguide_train_optics import kmode
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
d = json.load(open(os.path.join(os.path.dirname(__file__), "fbpic_train_design.json")))
wq = 2*np.pi*PL.c/np.array(d["lambdas"]); pq = np.array(d["p_modes"])
def props(W, n_cm3):
    kp0 = PL.k_p(n_cm3*1e6)
    kq = np.array([kmode(wq[i], kp0, W, pq[i]) for i in range(len(wq))])
    if not np.all(np.isfinite(kq)): return None
    A = np.polyfit(kq, wq, 1); va = A[0]/PL.c
    res = wq - np.polyval(A, kq)                       # frequency residual from rigid line
    dk_res = res/ (va*PL.c)                           # equivalent wavenumber error
    Lcoh = np.pi/np.max(np.abs(dk_res)) if np.max(np.abs(dk_res))>0 else np.inf
    detune = np.mean(-np.diff(wq))/PL.omega_p(n_cm3*1e6)
    return va, Lcoh, detune
W0, n0 = d["W"], d["n_cm3"]
print("W/W0   n/n0   beta_train   L_coh[mm]   spacing/w_p")
table = []
for nf in [1.0, 0.8, 0.6]:
    for Wf in [1.0, 1.1, 1.25, 1.5, 2.0, 3.0]:
        r = props(W0*Wf, n0*nf)
        if r is None: continue
        g = 1/np.sqrt(1-r[0]**2); T = (g-1)*938.272
        table.append(dict(W_rel=Wf, n_rel=nf, beta=r[0], T_matched_MeV=T, Lcoh_mm=r[1]*1e3, spacing_over_wp=r[2]))
        print(f"{Wf:5.2f} {nf:5.2f}   {r[0]:.5f} (T={T:6.0f} MeV)   {r[1]*1e3:8.2f}   {r[2]:.3f}")
json.dump(table, open(os.path.join(ROOT, "results", "data", "P2c_channel_taper.json"), "w"), indent=1)
