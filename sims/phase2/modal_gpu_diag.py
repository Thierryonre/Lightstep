"""Diagnose the GPU stack for FBPIC on Modal (numba.cuda + cupy)."""
import modal
img = (modal.Image.from_registry("nvidia/cuda:12.4.1-devel-ubuntu22.04", add_python="3.11")
       .pip_install("numpy<2.3", "scipy", "numba", "numba-cuda[cu12]", "cuda-python", "cupy-cuda12x", "pyfftw", "fbpic==0.27.1")
       .env({"NUMBA_CUDA_USE_NVIDIA_BINDING": "1"}))
app = modal.App("mcf-gpu-diag", image=img)

@app.function(gpu=["L4", "A10G", "T4", "L40S"], timeout=600)
def diag(force_driver: bool):
    import os, subprocess, textwrap
    env = dict(os.environ)
    if force_driver:
        env["NUMBA_CUDA_DRIVER"] = "/usr/lib/x86_64-linux-gnu/libcuda.so.1"
    code = textwrap.dedent("""
        import glob, numpy as np
        print('libcuda candidates:', glob.glob('/usr/lib/x86_64-linux-gnu/libcuda*')[:3], glob.glob('/usr/local/nvidia/lib64/libcuda*')[:3])
        from numba import cuda
        print('numba cuda available:', cuda.is_available()); cuda.detect()
        @cuda.jit
        def k(a): 
            i = cuda.grid(1)
            if i < a.size: a[i] += 1
        a = cuda.to_device(np.zeros(1000)); k[4, 256](a); print('numba kernel ok:', a.copy_to_host().sum())
        import cupy as cp; print('cupy ok:', float(cp.arange(10).sum()))
    """)
    p = subprocess.run(["python", "-u", "-X", "faulthandler", "-c", code], env=env, capture_output=True, text=True)
    return f"force_driver={force_driver} rc={p.returncode}\n{p.stdout[-3000:]}\n{p.stderr[-2000:]}"

@app.local_entrypoint()
def main():
    for f in (False,):
        print(diag.remote(f)); print("-" * 60)
