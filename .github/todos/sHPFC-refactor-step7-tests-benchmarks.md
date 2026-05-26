# sHPFC Refactor — Step 7: Update tests and run benchmarks

Purpose: ensure refactor slices preserve correctness and meet performance expectations.

Checklist (updated)
- [x] Update tests to reference refactored modules (`state.py`, `timestep_std.py`, `kernel_rules.py`, `fields.py`, etc.).
- [x] Run full test-suite during the refactor slices (no regressions observed in our runs).
- [x] Add `tests/benchmarks/benchmark_runner.py` to capture deterministic runtimes (warmup, repeats, seed).
- [x] Capture baseline and post-refactor results: `tests/benchmarks/results_pre_7cf81e1_np.json`, `tests/benchmarks/results_post_main_np.json`.
- [x] Produce a brief summary `tests/benchmarks/summary.md` documenting mean/median/std and a sanity-check conclusion.
- [ ] Optional: add an automated regression check (pytest) to fail on slowdowns > threshold.

Exit criteria
- Tests pass and benchmark artifacts are committed.
- Any observed regressions are documented and tracked; small/noisy differences on laptop runs are acceptable for sanity checks.
- For formal performance verification, run longer benchmarks on fixed hardware (see future-ideas/benchmarking.md).
