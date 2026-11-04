"""Long FBPIC surface-plasmon run (S048) on a Modal GPU, detached, writing snapshots to a Modal
Volume as it goes (partial results survive a crash/timeout).

    python ~/.local/bin/modal_avast.py run --detach sims/phase2/modal_fbpic_sp_long.py --steps 60000 --diag-every 2000         --extra "..." --out fbpic_sp3_out
    python ~/.local/bin/modal_avast.py volume get mcf-fbpic fbpic_sp3_out sims/phase2/
"""
import os
import modal

HERE = os.path.dirname(os.path.abspath(__file__))
image = (
    modal.Image.from_registry("nvidia/cuda:12.4.1-devel-ubuntu22.04", add_python="3.11")
    .pip_install("numpy<2.3", "scipy", "numba", "numba-cuda[cu12]", "cuda-python", "cupy-cuda12x", "h5py", "pyfftw", "fbpic==0.27.1")
    .env({"NUMBA_CUDA_USE_NVIDIA_BINDING": "1"})
    .add_local_file(os.path.join(HERE, "fbpic_surface_plasmon.py"), "/work/fbpic_surface_plasmon.py")
)
app = modal.App("mcf-fbpic-sp-long", image=image)
vol = modal.Volume.from_name("mcf-fbpic", create_if_missing=True)


@app.function(gpu=["L40S", "A100", "A10G", "L4"], timeout=20 * 3600, cpu=4, memory=16384, volumes={"/vol": vol})
def run(steps: int, diag_every: int, extra: str, out: str):
    import subprocess, time
    t0 = time.time()
    os.makedirs(f"/vol/{out}", exist_ok=True)
    log = open(f"/vol/{out}/run.log", "w")
    cmd = ["python", "/work/fbpic_surface_plasmon.py", "--steps", str(steps), "--diag_every", str(diag_every),
           "--cuda", "--out", f"/vol/{out}"] + extra.split()
    p = subprocess.Popen(cmd, cwd="/work", stdout=log, stderr=subprocess.STDOUT, text=True)
    while p.poll() is None:
        time.sleep(600)
        log.flush(); vol.commit()
    log.flush(); vol.commit()
    return dict(returncode=p.returncode, runtime_s=time.time() - t0)


@app.local_entrypoint()
def main(steps: int = 60000, diag_every: int = 2000, extra: str = "", out: str = "fbpic_sp3_out"):
    print(run.remote(steps, diag_every, extra, out))
