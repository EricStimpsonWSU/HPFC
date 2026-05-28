# sHPFC Refactor Plan

Goal: reorganize `sHPFC` and related kernel code so cross-cutting concerns (backend, geometry, coefficients, field layout, ETD kernels, and timestep orchestration) are cleanly separated while preserving the existing high-performance stepping behavior and keeping the test suite green.

Principles
- Test-first: every behavioral change must be covered by a test that asserts numeric equivalence to the pre-refactor baseline.
- Small, reversible steps: each step must leave the repository in a working (tests pass) state.
- Preserve performance: keep preallocated buffers, batched FFTs, and backend-native arrays on the hot path.
- Composition over inheritance: use small strategy/provider bundles for model-specific expressions.
- Minimal migration notes: the codebase is small and can be updated directly, so do not preserve explicit backward-compatibility code; document only the import and call-site changes needed by the simulation runners.

Prerequisites
- Keep `HPFC/backend.py`, `HPFC/PFC2D_geometry.py`, and `HPFC/PFC2D_model.py` stable (inputs to the refactor).
- The working test suite is the baseline validation mechanism. Use `pytest -q` to run the suite.

Step 0 — Capture baselines (truth sets) [MANDATORY]
- Purpose: generate and commit deterministic numerical reference outputs for each timestep variant so later refactors can assert exact (or numerically-close) equivalence.
- Subtasks:
  - Add a small harness under `tests/baselines/` that runs each timestep variant (`Timestep_stdPFC`, `Timestep_sHPFC`, `Timestep_sHPFC_div_vpsi`, `Timestep_sHPFC_psigradmu`) for a small, deterministic model + geometry (use `simple_model` and `simple_geometry`).
  - Produce and commit reference `.npz` files with a tiny number of timesteps (e.g., 1, 2, and 5 steps). For each run save: `psi`, `psi_hat`, `psi_hat_00`, and, for hydrodynamic variants, `v_x`, `v_y`, and `div_vpsi_hat`.
  - Add tests that load these `.npz` files and assert the current implementation reproduces the reference arrays to a strict tolerance (`rtol=1e-12, atol=1e-15` or adjusted after exploring numerical drift). Use `pytest` fixtures that force the NumPy backend to guarantee reproducible results.
  - Keep the harness small and deterministic (fixed RNG seeds if any random initializations are used).
- Exit conditions:
  - The new baseline files are committed under `tests/baselines/`.
  - Baseline-check tests pass on the unmodified code.

Step 1 — Add a minimal baseline-run harness and CI job
- Purpose: make it straightforward to re-generate baselines and run baseline comparisons in CI.
- Subtasks:
  - Add a small CLI or pytest-marked function to produce baseline `.npz` files.
  - Add a GitHub Actions job (optional) that runs baseline checks on PRs.
- Exit conditions: harness exists and baseline-check tests run in CI or locally.

Step 2 — Extract kernel/provider (model rules)
- Purpose: centralize model-specific expressions (linear kernels, ETD build rules, Gaussian smoothing, and nonlinear term definitions) into a single `KernelRules` dataclass or small module.
- Subtasks:
  - Introduce `HPFC/kernel_rules.py` that accepts `model` and `geometry` and returns a `KernelRules` object containing: derivative kernels, `lin_mu_kernel`, `lin_f_kernel`, `lin_v_kernel`, `lin_dpsi`, `lin_psi_exp`, `nonlin_psi_exp`, `lin_v_exp`, `nonlin_v_exp`, and `gaussian_kernel`.
  - Keep `PFC2D_kernels.py` as a compatibility shim that delegates to the new `kernel_rules` for now.
  - Add tests that verify `KernelRules` produces the same arrays as the pre-existing API (use baseline tests and `tests/test_kernels.py`).
- Exit conditions: `KernelRules` is the authoritive source for kernel expressions, and tests confirm numeric equivalence.

Step 3 — Split `sHPFC` into state container + stepper strategies
- Purpose: separate buffer ownership from timestep orchestration, while keeping each timestep variant's full math in its own stepper file.
- Subtasks:
  - Add `HPFC/state.py` with `SimulationState` (thin dataclass) that owns preallocated backend arrays, aliases, and DC preservation helpers. Do not change the internal buffer shapes or names used by existing tests; only change import surface.
  - Add one stepper file per variant under `HPFC/steppers/` or an equivalent single-dispatch module layout, and ensure each file eventually contains all variant-specific math for that timestep family in one place. The file should expose ASCII function names that mirror the LaTeX expressions in `HPFC/specs/sHPFC_exp.md` (for example, functions corresponding to `\mathcal{J}_1`, `\mathcal{J}_2`, `\mathcal{H}_1`, `\mathcal{H}_2`, `\partial_t \psi`, and `\rho_0 \partial_t \mathbf{v}`), with docstrings that point back to the matching expression.
  - Keep `KernelRules` limited to primitive operators and reusable coefficients. Composition of those operators into `dpsi_dt`, `dv_dt`, and other variant-specific update expressions must live in the stepper file, not in `KernelRules`.
  - Keep `sHPFC.py` small: it can become a thin convenience facade that constructs `SimulationState` + chosen stepper.
  - Add tests that construct a `SimulationState` and call each stepper; compare to baseline outputs.
- Exit conditions: refactor is transparent to external imports and tests still pass.

Step 4 — Introduce field-layout dataclass wrappers
- Purpose: give semantic names to batched buffer indices and remove magic indexing.
- Subtasks:
  - Create small wrapper classes in `HPFC/fields.py` that map the existing `_batch_*` arrays to attributes like `.psi`, `.psi2`, `.psi3`, `.psi4`, `.v_x`, `.v_y`, `.psi_x`, `.psi_y`, `.f_x`, `.f_y`, etc.
  - Update `state.py` and stepper implementations to use these wrappers.
  - Add unit tests that exercise the wrappers to ensure attribute views map to the same underlying arrays (no copies).
- Exit conditions: code uses named attributes rather than numeric indexes; tests unchanged.

Step 5 — Extract DC, FFT batching, and helper utilities
- Purpose: centralize cross-cutting numeric utilities so their behavior is explicit and testable.
- Subtasks:
  - Add `HPFC/utils.py` implementing: `preserve_dc(psi_hat, psi_hat_00)`, `batch_ifft(payload_mgr, arr)`, `safe_etd_nonlin(dt, lin_kernel)` (handles zero entries), and `normalize_kernel_hat_mean` wrapper.
  - Replace inline code in steppers/state with calls to these utilities.
  - Add unit tests for each utility function.
- Exit conditions: no numerical change in stepping; utility tests pass.

Step 6 — Introduce lazy allocation for hydrodynamic-only fields
- Purpose: avoid allocating velocity/force buffers for `stdPFC` workflows.
- Subtasks:
  - Make hydrodynamic buffers lazily created by `SimulationState.get_hydro_buffers()` and cached for reuse.
  - Ensure tests that use hydrodynamic steppers still see identical numeric results.
- Exit conditions: stdPFC runs allocate less memory; tests unchanged.

Step 7 — Update tests in lockstep and run benchmarks
- Purpose: ensure extracted code remains numerically equivalent and identify any performance regressions.
- Subtasks:
  - Update tests to reference the new modules. Prefer to expand tests that verify numeric equivalence rather than rewriting them.
  - Run the baseline-check tests and known failing edge-case tests.
  - Add a small benchmark script under `tools/benchmarks/` that runs a small grid for N steps and reports wall-clock time for `stdPFC` vs `sHPFC` variants.
- Exit conditions: baseline tests pass; any measurable performance regressions are within acceptable bounds.

Step 8 — Cleanup, docs, and prepare for extension
- Purpose: finalize the refactor, add documentation and examples.
- Subtasks:
  - Update README snippets to show new import paths (if any) and how to use `SimulationState` + a stepper.
  - Add short migration notes that list the old runner entry points and the new imports/calls they should switch to.
  - Add a `design/patterns/strategy_adapter_dataclass.md` explaining the key patterns with a small Python example (included in this refactor package).
- Exit conditions: all tests pass and docs updated.


Appendix: Running baselines locally

- Generate baselines (recommended):

```bash
python -m pytest tests/baselines --maxfail=1 -q
# or run the harness directly, e.g.:
python tools/baselines/generate_baselines.py
```

- Run baseline checks:

```bash
pytest tests/test_baselines_check.py -q
```


Rollback guidance
- Each step must be a small commit. If tests fail after a step, revert that commit and open a draft PR to continue the split in smaller increments.
