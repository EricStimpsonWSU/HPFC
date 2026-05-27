# PFC Simulation Variants — Canonical Model Summary

Purpose: a stable, concise reference describing the four canonical simulation-definition modules, their timestep algorithms, and their intended consumer-facing import paths. Designed to be consulted by tests, refactors, and automation.

Variants

- `sim_pfc_std` (standard PFC — non-hydrodynamic)
  - Canonical import: `HPFC.sim_pfc_std`
  - Timestep: standard PFC timestep (no hydrodynamics)
  - Description: pure PFC algorithm without momentum or velocity fields. Use for baseline `stdPFC` behavior checks.
  - Expected outputs used by baseline checks: `psi`, `psi_hat`, `psi_hat_00`.

- `sim_shpfc_std` (standard sHPFC — hydrodynamic standard)
  - Canonical import: `HPFC.sim_shpfc_std`
  - Timestep: `Timestep_sHPFC` (the repository's standard hydro timestep implementation)
  - Description: the primary hydrodynamic PFC variant. Provides velocity fields and the shared hydro ETD/timestep wiring.
  - Expected outputs used by baseline checks: `psi`, `psi_hat`, `psi_hat_00`, `v_x`, `v_y`, and `div_vpsi_hat` (or other hydro diagnostics the harness expects).

- `sim_shpfc_div_vpsi` (hydro variant: div(v * psi))
  - Canonical import: `HPFC.sim_shpfc_div_vpsi`
  - Timestep: variant of sHPFC with the `div(v psi)` coupling implemented in a modified timestep class (e.g., `Timestep_sHPFC_div_vpsi`).
  - Description: hydrodynamic variant that couples momentum via the divergence of `v * psi` in the update rule.
  - Expected outputs used by baseline checks: all hydro outputs plus variant-specific diagnostics such as `div_vpsi_hat`.

- `sim_shpfc_psigradmu` (hydro variant: psi * grad(mu))
  - Canonical import: `HPFC.sim_shpfc_psigradmu`
  - Timestep: variant of sHPFC with the `psi * grad(mu)` coupling implemented in a modified timestep class (e.g., `Timestep_sHPFC_psigradmu`).
  - Description: hydrodynamic variant that couples momentum via `psi * grad(mu)` terms.
  - Expected outputs used by baseline checks: all hydro outputs plus variant-specific diagnostics such as `v_dot_grad_psi_hat` or equivalent.

Key guidance (for future tasks and tests)

- Always treat `sim_pfc_std` as the non-hydro baseline; do not conflate it with the `sHPFC` family.
- The `sim_shpfc_*` modules share the same conceptual API surface: a model factory/shape, a geometry factory, an initial-state creator, and a simulation/timestep factory. Tests should assert those consumer-facing factory names rather than internal helper names.
- Recommended filenames: `HPFC/sim_pfc_std.py`, `HPFC/sim_shpfc_std.py`, `HPFC/sim_shpfc_div_vpsi.py`, `HPFC/sim_shpfc_psigradmu.py`.
- Baseline harness expectations: tests under `tests/baselines/` should parametrize these four import paths and use small-grid, low-step fixtures to validate numerical equivalence during refactors.

Suggested minimal consumer contract (for tests)

- Import the sim module, call `build_model(**kwargs)` or construct `PFC2D_model` as the sim expects.
- Call `build_geometry(model, **kwargs)` to get a geometry object (grid, k-space arrays).
- Call `make_initial_state(model, geometry, rng_seed=...)` to get a reproducible `SimulationState` with named fields.
- Call `make_sim(model, geometry, state)` or instantiate the sim class to obtain an object exposing a `step()` method and final-state access.

Notes

- This file is intended as a short, machine- and human-readable spec to be consulted by refactors, tests, and CI. Keep it small and stable; update if canonical import paths or timestep class names change.
