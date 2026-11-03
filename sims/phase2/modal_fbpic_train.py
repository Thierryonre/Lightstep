"""Run the FBPIC guided-train simulation (S042) on a Modal GPU and copy the results back.

Usage (from the repo root, via the Avast-compatible launcher):
    python ~/.local/bin/modal_avast.py run sims/phase2/modal_fbpic_train.py --steps 4500
Outputs land in sims/phase2/fbpic_train_out/ (snapshots are git-ignored; summary.json is kept).
"""
import os
import modal

HERE = os.path.dirname(os.path.abspath(__file__))

image = (
    modal.Image.from_registry("nvidia/cuda:12.4.1-devel-ubuntu22.04", add_python="3.11")
    .pip_install("numpy<2.3", "scipy", "numba", "numba-cuda[cu12]", "cuda-python", "cupy-cuda12x", "h5py", "pyfftw", "fbpic==0.27.1")
    .env({"NUMBA_CUDA_USE_NVIDIA_BINDING": "1"})
    .add_local_file(os.path.join(HERE, "fbpic_waveguide_train.py"), "/work/fbpic_waveguide_train.py")
    .add_local_file(os.path.join(HERE, "fbpic_train_design.json"), "/work/fbpic_train_design.json")
)
app = modal.App("mcf-fbpic-guided-train", image=image)


@app.function(gpu=["L4", "A10G", "T4", "L40S"], timeout=3 * 3600, cpu=4, memory=16384)
def run(steps: int = 4500, diag_every: int = 500):
    import subprocess, glob, time
    t0 = time.time()
    cmd = ["python", "/work/fbpic_waveguide_train.py", "--steps", str(steps), "--diag_every", str(diag_every),
           "--protons", "--cuda", "--out", "fbpic_train_out"]
    p = subprocess.run(cmd, cwd="/work", capture_output=True, text=True)
    files = {}
    for f in glob.glob("/work/fbpic_train_out/*"):
        files[os.path.basename(f)] = open(f, "rb").read()
    return dict(returncode=p.returncode, stdout=p.stdout[-20000:], stderr=p.stderr[-8000:],
                files=files, runtime_s=time.time() - t0)


@app.local_entrypoint()
def main(steps: int = 4500, diag_every: int = 500):
    res = run.remote(steps, diag_every)
    out = os.path.join(HERE, "fbpic_train_out")
    os.makedirs(out, exist_ok=True)
    for name, data in res["files"].items():
        open(os.path.join(out, name), "wb").write(data)
    open(os.path.join(HERE, "fbpic_train_run_modal.log"), "w").write(res["stdout"] + "\n--- stderr ---\n" + res["stderr"])
    print(f"returncode={res['returncode']} runtime={res['runtime_s']:.0f}s files={len(res['files'])}")
    print("\n".join(l for l in res["stdout"].splitlines() if l.startswith("step") or "Error" in l)[-3000:])
