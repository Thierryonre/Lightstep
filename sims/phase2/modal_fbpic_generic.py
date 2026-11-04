"""Run any of the FBPIC scripts here on a Modal GPU, detached, writing output to the Modal Volume
`mcf-fbpic` as it goes (committed every 5 min).

    python ~/.local/bin/modal_avast.py run --detach sims/phase2/modal_fbpic_generic.py \
        --script fbpic_surface_plasmon.py --args "--steps 12000 ..." --out NAME [--bunch local.npz]
    python ~/.local/bin/modal_avast.py volume get mcf-fbpic NAME sims/phase2/
"""
import os
import modal

HERE = os.path.dirname(os.path.abspath(__file__))
image = (
    modal.Image.from_registry("nvidia/cuda:12.4.1-devel-ubuntu22.04", add_python="3.11")
    .pip_install("numpy<2.3", "scipy", "numba", "numba-cuda[cu12]", "cuda-python", "cupy-cuda12x", "h5py", "pyfftw", "fbpic==0.27.1")
    .env({"NUMBA_CUDA_USE_NVIDIA_BINDING": "1"})
    .add_local_file(os.path.join(HERE, "fbpic_surface_plasmon.py"), "/work/fbpic_surface_plasmon.py")
    .add_local_file(os.path.join(HERE, "fbpic_waveguide_train.py"), "/work/fbpic_waveguide_train.py")
    .add_local_file(os.path.join(HERE, "fbpic_train_design.json"), "/work/fbpic_train_design.json")
)
app = modal.App("mcf-fbpic-generic", image=image)
vol = modal.Volume.from_name("mcf-fbpic", create_if_missing=True)


@app.function(gpu=["L40S", "A100", "A10G", "L4"], timeout=12 * 3600, cpu=4, memory=16384, volumes={"/vol": vol})
def run(script: str, args: str, out: str, bunch: bytes = b""):
    import subprocess, time
    t0 = time.time()
    os.makedirs(f"/vol/{out}", exist_ok=True)
    extra = []
    if bunch:
        open("/work/bunch_in.npz", "wb").write(bunch); extra = ["--bunch_file", "/work/bunch_in.npz"]
    log = open(f"/vol/{out}/run.log", "w")
    cmd = ["python", f"/work/{script}", "--cuda", "--out", f"/vol/{out}"] + args.split() + extra
    p = subprocess.Popen(cmd, cwd="/work", stdout=log, stderr=subprocess.STDOUT, text=True)
    while p.poll() is None:
        time.sleep(300); vol.commit()
    vol.commit()
    return dict(returncode=p.returncode, runtime_s=time.time() - t0)


@app.local_entrypoint()
def main(script: str, args: str, out: str, bunch: str = ""):
    data = open(bunch, "rb").read() if bunch else b""
    print(run.remote(script, args, out, data))
