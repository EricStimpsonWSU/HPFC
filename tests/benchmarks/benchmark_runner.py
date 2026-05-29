"""Deterministic benchmark runner for sHPFC/stdPFC pre/post refactor comparisons.

Saves JSON results to a specified output path. Designed to be copied into
old worktrees for running against pre-refactor commits.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
import os
import sys

import numpy as np


def configure_backend_env(backend_mode: str) -> None:
    if backend_mode == "cpu":
        os.environ["SHPFC_ARRAY_BACKEND"] = "numpy"
        os.environ["SHPFC_FFT_BACKEND"] = "numpy"
        return
    if backend_mode == "gpu":
        os.environ["SHPFC_ARRAY_BACKEND"] = "cupy"
        os.environ["SHPFC_FFT_BACKEND"] = "cupy"
        return
    raise ValueError(f"Unsupported backend mode: {backend_mode}")


def build_sim(seed: int, nx: int, ny: int, *, backend_mode: str):
    configure_backend_env(backend_mode)

    # insert repo root so imports work when run from repo root
    repo_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(repo_root))

    from PFC.Core.PFC2D_model import model_2D
    from PFC.Core.PFC2D_geometry import geometry_2D
    from PFC.stdPFC.sim_pfc_std import make_sim as sHPFC

    rng = np.random.RandomState(seed)
    psi0 = rng.randn(nx, ny) * 0.1

    model = model_2D(temp=-0.25, beta=1.5, Gamma=1.0, rho0=1.0, Gamma_s=0.75, dt=0.05)
    geometry = geometry_2D(shape=(nx, ny), Lx=32.0, Ly=32.0)

    sim = sHPFC(psi0, model=model, geometry=geometry)
    if backend_mode == "gpu" and getattr(sim, "backend_name", None) != "cupy":
        raise RuntimeError("GPU benchmark requested, but simulation did not resolve to CuPy backend")

    return sim


def run_single_benchmark(seed: int, nx: int, ny: int, warmup: int, steps: int, repeats: int, *, backend_mode: str):
    sim = build_sim(seed, nx, ny, backend_mode=backend_mode)

    # warmup
    for _ in range(warmup):
        sim.step()

    times = []
    for r in range(repeats):
        t0 = time.perf_counter()
        for _ in range(steps):
            sim.step()
        t1 = time.perf_counter()
        times.append((t1 - t0) / steps)

    return {
        "nx": nx,
        "ny": ny,
        "seed": seed,
        "backend_mode": backend_mode,
        "backend_name": getattr(sim, "backend_name", "unknown"),
        "backend_fft_name": getattr(sim, "backend_fft_name", "unknown"),
        "backend_summary": getattr(sim, "backend_summary", "unknown"),
        "warmup": warmup,
        "steps": steps,
        "repeats": repeats,
        "times_s": times,
    }


def run_benchmark(out_path: Path, seed: int, nx: int, ny: int, warmup: int, steps: int, repeats: int, *, backend_mode: str):
    if backend_mode == "both":
        data = {
            "cpu": run_single_benchmark(seed, nx, ny, warmup, steps, repeats, backend_mode="cpu"),
            "gpu": run_single_benchmark(seed, nx, ny, warmup, steps, repeats, backend_mode="gpu"),
        }
    else:
        data = run_single_benchmark(seed, nx, ny, warmup, steps, repeats, backend_mode=backend_mode)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2))
    print(f"Wrote results to {out_path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--nx", type=int, default=64)
    p.add_argument("--ny", type=int, default=64)
    p.add_argument("--warmup", type=int, default=2)
    p.add_argument("--steps", type=int, default=1)
    p.add_argument("--repeats", type=int, default=5)
    p.add_argument("--backend-mode", choices=("cpu", "gpu", "both"), default="both")
    p.add_argument("--force-numpy", action="store_true", help="Deprecated alias for --backend-mode=cpu")

    args = p.parse_args()
    backend_mode = "cpu" if args.force_numpy else args.backend_mode
    run_benchmark(
        Path(args.out),
        args.seed,
        args.nx,
        args.ny,
        args.warmup,
        args.steps,
        args.repeats,
        backend_mode=backend_mode,
    )


if __name__ == "__main__":
    main()
