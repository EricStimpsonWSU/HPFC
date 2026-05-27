
# PFC Simulation Definition Split — Step 3: Split shared kernels from simulation-specific kernels

Purpose: keep reusable spectral operators and ETD-building helpers in `HPFC/kernel_rules.py` while moving model-specific linear-kernel definitions into the per-simulation definition modules.

Status: in-progress.

Checklist
- [x] Add narrow tests that assert the public reusable operators produced by `HPFC/kernel_rules` (derivatives, Gaussian smoothing, wavenumber arrays) on a tiny grid (16x16).
- [x] Add tests that capture the current simulation-specific linear kernels for each variant on tiny deterministic configs (32x32, 1–5 steps) and commit minimal `.npz` references under `tests/baselines/data/`.
- [x] Create `HPFC/sim_*` module placeholders if missing, to own each variant's linear-kernel definition.
- [ ] Refactor implementation: remove variant-specific kernel constructions from shared modules and import them from the new sim modules, preserving the timestep ETD builder interface.
- [ ] Run narrow baseline checks and iterate until outputs match prior references within existing tolerances.

Exit criteria
- The shared kernel layer (`HPFC/kernel_rules.py`) only contains reusable spectral operators and universal ETD construction helpers.
- Variant-specific kernel behavior is owned by the corresponding `HPFC/sim_*` module and covered by narrow regression tests that compare to committed baseline arrays.
- Narrow baseline tests pass on the unmodified CI worker using the workspace Python environment.

Notes
- Use the workspace Python environment; do not modify or install packages without explicit permission.
- Keep changes minimal and behavior-preserving; add/adjust narrow tests before implementation changes.
- Preserve deterministic small-grid, low-step configurations for regression checks.
- Ignore any files matching `sHPFC-refactor*`.
- Do not edit design/spec documents under `design/` or `.github/specs/` unless explicitly requested.

Next focus
- Add/verify minimal sim-specific baseline `.npz` files for each variant (32x32, steps 1–5) under `tests/baselines/data/`, update narrow regression tests to reference them, and continue splitting variant-specific kernel ownership into per-simulation modules (move kernel definitions from shared modules to `HPFC/sim_*`).

Next action
- Completed: added `tests/test_kernel_rules_shared_ops.py` and `tests/test_sim_specific_kernels.py`, ran them in the workspace Python venv (7 passed), committed the new tests, created `HPFC/sim_kernels.py`, and refactored `HPFC/kernel_rules.py` to delegate model-specific kernel construction. `KernelRules` now prefers a `build_lin_kernels` exported by the per-simulation module (e.g. `HPFC.sim_pfc_std` / `HPFC.sim_shpfc_*`) and falls back to `HPFC.sim_kernels.build_lin_kernels` for compatibility.
- Completed: generated the minimal sim-specific baselines in `tests/baselines/data/` and validated them with `tests/test_baselines_check.py` (12 passed).
- Next: continue moving variant-specific kernel code into per-simulation modules (`HPFC/sim_std.py`, `HPFC/sim_shpfc_*.py`) until the shared `HPFC/kernel_rules.py` contains only reusable operators and ETD helpers.
 - Update: added `build_lin_kernels` implementations to each `HPFC/sim_*` module so each simulation now owns its kernel formulas; `HPFC/sim_kernels.py` is retained as a fallback for compatibility.

Progress update
- Added narrow shared-kernel and sim-specific kernel tests, ran them (7 passed), committed the tests, created `HPFC/sim_kernels.py`, refactored `HPFC/kernel_rules.py` to dynamically resolve `build_lin_kernels` from the simulation module (fallback to `sim_kernels`), generated the minimal baselines, and validated them (12 passed). Per-simulation kernel module split remains; next move detailed kernel formulas into each `HPFC/sim_*` file.
Files likely touched
