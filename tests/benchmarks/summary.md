# Benchmark summary — pre vs post refactor (sanity checks)

Repository state
- Pre-refactor commit: `7cf81e1` (baseline truth tests commit).
- Post-refactor branch: `main` (current HEAD).

Environment
- Platform: developer laptop (local dev environment).
- Forced backend: NumPy arrays + NumPy FFTs (`SHPFC_ARRAY_BACKEND=numpy`, `SHPFC_FFT_BACKEND=numpy`).
- Runner: `tests/benchmarks/benchmark_runner.py` (warmup=2, steps=1, repeats=5, seed=0, nx=64, ny=64).

Results (per-step timings in seconds)

Pre (commit 7cf81e1)
- samples: [0.0005171000011614524, 0.00042070000017702114, 0.00033290000101260375, 0.00030810000134806614, 0.00030669999978272244]
- mean = 0.0003771 s
- median = 0.0003329 s
- std  ≈ 0.0000814 s

Post (main)
- samples: [0.0003269000008003786, 0.0003161999993608333, 0.0003130000004603062, 0.00031070000113686547, 0.0003259999994043028]
- mean = 0.0003186 s
- median = 0.0003162 s
- std  ≈ 0.0000067 s

Comparison
- Mean time reduced from ~0.3771 ms to ~0.3186 ms.
- Speedup factor (pre_mean / post_mean) ≈ 1.18×.
- Relative reduction: ~15.5% faster per step (sanity check).

Notes
- These are quick sanity checks on a laptop using a small problem size and short runs. Results are noisy but show no regression; post-refactor is modestly faster here.
- For production-grade benchmarking use fixed server hardware and longer runs (Colab/CI machines are suitable). This belongs in `future-ideas` for the next, performance-focused refactor.

Artifacts
- Runner: `tests/benchmarks/benchmark_runner.py`
- Raw results: `tests/benchmarks/results_pre_7cf81e1_np.json`, `tests/benchmarks/results_post_main_np.json`
