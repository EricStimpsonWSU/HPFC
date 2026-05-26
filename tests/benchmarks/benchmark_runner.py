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


def build_sim(seed: int, nx: int, ny: int):
    # insert HPFC package dir so imports work when run from repo root
    repo_root = Path(__file__).resolve().parents[2]
    hpfc_dir = repo_root / "HPFC"
    sys.path.insert(0, str(hpfc_dir))

    from PFC2D_model import model_2D
    from PFC2D_geometry import geometry_2D
    from sHPFC import sHPFC

    rng = np.random.RandomState(seed)
    psi0 = rng.randn(nx, ny) * 0.1

    model = model_2D(temp=-0.25, beta=1.5, Gamma=1.0, rho0=1.0, Gamma_s=0.75, dt=0.05)
    geometry = geometry_2D(shape=(nx, ny), Lx=32.0, Ly=32.0)

    sim = sHPFC(psi0, model=model, geometry=geometry)
    return sim


def run_benchmark(out_path: Path, seed: int, nx: int, ny: int, warmup: int, steps: int, repeats: int):
    sim = build_sim(seed, nx, ny)

    # force numpy backend environment for determinism
    os.environ.setdefault("SHPFC_ARRAY_BACKEND", "numpy")
    os.environ.setdefault("SHPFC_FFT_BACKEND", "numpy")

    # warmup
    for _ in range(warmup):
        sim.Timestep_stdPFC()

    times = []
    for r in range(repeats):
        t0 = time.perf_counter()
        for _ in range(steps):
            sim.Timestep_stdPFC()
        t1 = time.perf_counter()
        times.append((t1 - t0) / steps)

    data = {
        "nx": nx,
        "ny": ny,
        "seed": seed,
        "warmup": warmup,
        "steps": steps,
        "repeats": repeats,
        "times_s": times,
    }

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
    p.add_argument("--force-numpy", action="store_true", help="Force NumPy arrays/FFTs via env vars before import")

    args = p.parse_args()
    if args.force_numpy:
        os.environ["SHPFC_ARRAY_BACKEND"] = "numpy"
        os.environ["SHPFC_FFT_BACKEND"] = "numpy"
    run_benchmark(Path(args.out), args.seed, args.nx, args.ny, args.warmup, args.steps, args.repeats)


if __name__ == "__main__":
    main()
