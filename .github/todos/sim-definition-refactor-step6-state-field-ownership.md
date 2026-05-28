# PFC Simulation Definition Split — Step 6: Update State and Field Ownership

Purpose: keep `SimulationState` responsible for owned buffers and shared helpers while moving any remaining variant-specific field assumptions into the sim modules.

Status: in progress.

Boundary
- `SimulationState` keeps ownership of preallocated buffers, shared batch wrappers, `psi_hat_00`, and the lazy hydrodynamic storage that backs the shared hydro fields.
- The sim modules own the public field contract for each variant, including which names are exposed to consumers and which hydrodynamic aliases are intentionally visible.
- Shared named views such as `psi_batch`, `grad_batch`, `grad_psi_batch`, `grad_mu_batch`, and `force_batch` must continue to reference the same underlying arrays.
- Variant-specific names like `v_x`, `v_y`, `v_x_hat`, `v_y_hat`, `div_v`, `v_dot_grad_psi`, and `div_vpsi_hat` should be treated as sim-module surface decisions, not as assumptions baked into `SimulationState`.

Checklist
- [ ] Add narrow contract tests that prove `SimulationState` still owns the shared buffers and that the batch views alias the same arrays.
- [ ] Add narrow contract tests that verify the standard module hides hydrodynamic names while the hydrodynamic sim modules expose only the names they need.
- [ ] Add a focused test that checks the named hydro views still share backing storage when they are allocated.
- [ ] Move or trim any remaining variant-specific field exposure logic out of `HPFC/state.py` only if the new tests show it is still coupled there.
- [ ] Keep the change local to the state/sim boundary; do not touch design/spec docs or unrelated kernel/model code.

Exit criteria
- `SimulationState` still owns the common buffers, lazy allocation helpers, and identity-preserving named views.
- Variant-specific field exposure is defined by the sim modules rather than assumed by `SimulationState`.
- Named views and hydro aliases remain identity-preserving under the new boundary.
- The narrow Step 6 tests pass without changing the committed baseline behavior.

Next action
- Add the narrow state-ownership and aliasing tests first, then make the smallest state/sim boundary adjustment those tests require.

Notes
- Treat `.github/refactors/pfc-sim-definition-refactor-plan.md` as the source of truth for the split.
- Ignore any files matching `sHPFC-refactor*`.
- Do not edit design/spec documents.
- Use the existing small-grid, low-step fixtures and the workspace test command for validation.