# Benchmarking — future-ideas

This note collects pragmatic steps and recommendations for running reproducible performance comparisons of HPFC pre/post refactor on reliable hardware (Colab, cloud VMs, or institutional HPC).

Goals
- Reproducible wall-clock timings for representative workloads (larger sizes than unit tests).
- Compare NumPy/CPU runs and GPU-accelerated runs (CuPy) when available.
- Capture environment metadata (Python, NumPy/CuPy, FFT backend, OS, CPU/GPU model, CUDA version).

Colab (quick, reproducible, GPU available)
- Use a Colab Pro/Free notebook with a GPU runtime if testing GPU backends. For CPU-only sanity checks, default runtime is fine.
- Typical steps (copy to a notebook cell):

```bash
# create and activate venv (optional) and install deps
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt

# (optional) install a CuPy wheel that matches the Colab CUDA version
# e.g., for CUDA 12.x (Colab may differ) - check `nvidia-smi` for CUDA version
# python -m pip install cupy-cuda12x

# Run the deterministic benchmark runner (example)
python tests/benchmarks/benchmark_runner.py --force-numpy --repeats 10 --warmup 5
python tests/benchmarks/benchmark_runner.py --force-cupy --repeats 10 --warmup 5
```

Notes for Colab
- Colab CUDA/runtime versions change; confirm CUDA and match CuPy wheel accordingly. If no matching wheel, run NumPy-only benchmarks.
- Use longer runs (higher `repeats` and `warmup`) to smooth noise from preemption and VM activity.

HPC / Cloud VMs (recommended for formal comparisons)
- Provision a fixed instance type (document CPU model, cores, memory, OS, and GPU model if used).
- Install system packages and proper CuPy wheel matching the machine's CUDA driver.
- Use `taskset`/`numactl` to pin CPU cores and reduce jitter when comparing CPU runs.
- Run multiple independent trials (e.g., 5–10) and collect mean/median/std; store results as JSON alongside git commit hashes.

Reproducibility checklist
- Record: git commit, branch, Python version, package versions, FFT backend, machine name, CPU/GPU details, and exact runner command.
- Use `--seed` / fixed RNG seeds where applicable.

Automation
- Consider adding a CI job that runs an extended benchmark on a fixed runner (if you have a dedicated machine), or a nightly job that uploads results to a simple artifact store.

Presentation
- Keep `tests/benchmarks/summary.md` for quick sanity checks; for publication include fuller tables/plots and raw JSON artifacts.
