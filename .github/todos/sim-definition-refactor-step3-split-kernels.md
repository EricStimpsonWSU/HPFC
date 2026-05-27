
# PFC Simulation Definition Split — Step 3: Split shared kernels from simulation-specific kernels

Purpose: keep reusable spectral operators and ETD-building helpers in `HPFC/kernel_rules.py` while moving model-specific linear-kernel definitions into the per-simulation definition modules.

Status: not-started.

Checklist
- [ ] Add narrow tests that assert the public reusable operators produced by `HPFC/kernel_rules` (derivatives, Gaussian smoothing, wavenumber arrays) on a tiny grid (16x16).
- [ ] Add tests that capture the current simulation-specific linear kernels for each variant on tiny deterministic configs (32x32, 1–5 steps) and commit minimal `.npz` references under `tests/baselines/data/`.
- [ ] Create `HPFC/sim_*` module placeholders if missing, to own each variant's linear-kernel definition.
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
- Add the two narrow tests and minimal baseline `.npz` files, then refactor `HPFC/kernel_rules.py` to extract reusable operators only.

Next action
- I'll add `tests/test_kernel_rules_shared_ops.py` and `tests/test_sim_specific_kernels.py` with minimal deterministic cases, and commit the small baseline `.npz` references, then begin the refactor.

Progress update
- Step 3 TODO file created and standardized to match Steps 0–2 conventions.
Files likely touched
