
# PFC Simulation Definition Split — Step 3: Split shared kernels from simulation-specific kernels

Purpose: keep reusable spectral operators and ETD-building helpers in `HPFC/kernel_rules.py` while moving model-specific linear-kernel definitions into the per-simulation definition modules.

Status: complete.

Checklist
- [x] Add narrow tests that assert the public reusable operators produced by `HPFC/kernel_rules` (derivatives, Gaussian smoothing, wavenumber arrays) on a tiny grid (16x16).
- [x] Add tests that capture the current simulation-specific linear kernels for each variant on tiny deterministic configs (32x32, 1–5 steps) and commit minimal `.npz` references under `tests/baselines/data/`.
- [x] Create `HPFC/sim_*` module placeholders if missing, to own each variant's linear-kernel definition.
- [x] Refactor implementation: remove variant-specific kernel constructions from shared modules and import them from the new sim modules, preserving the timestep ETD builder interface.
- [x] Run narrow baseline checks and iterate until outputs match prior references within existing tolerances.

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
- Move to Step 4: introduce the per-simulation definition modules and keep the simulation-specific ownership boundary local to each `HPFC/sim_*` file.

Next action
- Start Step 4 by adding narrow tests that describe the consumer-facing contract for each per-simulation definition module, using the existing deterministic small-grid / low-step configs.

Progress update
- Step 3 kernel ownership has been split into the per-simulation modules, and the narrow baseline checks already cover the behavior-preserving kernel changes.
- The next refactor slice is Step 4, which will make each simulation variant a complete definition module.
