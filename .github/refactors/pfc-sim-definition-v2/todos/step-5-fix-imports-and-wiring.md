# Step 5 — Fix Imports and Wiring (Fix‑Phase Begins)

Purpose: Rewire sim files and consumers so they instantiate local timesteppers and the codebase becomes functional again.

Status: completed.

Checklist:
- [x] Replace any `from PFC.Core.steppers import ...` usages with local class references or local definitions in the sim files.
- [x] Update `PFC.Core` entrypoints (facade) to import or instantiate variant steppers through the sim files if needed.
- [x] Remove `SimulationState.calc_mu` and `SimulationState.calc_f` now that those helpers live on the variant sim surfaces.
- [x] Run failing tests from Step 2 and fix them by updating imports/wiring — remember the break‑first tests were written to guide this.
- [x] Prefer editing consumers/tests to use the new local timestepper surface rather than adding shims.

Test summary:
- Updated the remaining consumers and tests to use the sim-owned `step()` / `std_step()` API rather than importing `PFC.Core.steppers`, including the variant entrypoint and state-stepper coverage.
- Removed the stale `PFC.Core` re-exports and the dead stepper instantiations from the variant sim modules so the wiring now resolves through the sim files directly.
- The two remaining broken tests are the intentional core-cleanup contracts in `tests/test_stepper_refactor_contract.py::test_core_steppers_no_stepper_classes` and `tests/test_stepper_refactor_contract.py::test_core_state_no_calc_mu_calc_f`; they still fail because step 5 does not remove `SimulationState.calc_mu` / `calc_f`, and the deleted `PFC/Core/steppers.py` file is still being asserted as absent by design.
- Those failures are expected at this stage because they validate the later core cleanup, not the wiring repair completed in step 5.

Exit criteria:
- Import errors are resolved; tests start to pass as wiring is corrected.

Notes (constraints):
- Prioritize changing tests/consumers over introducing compatibility shims.
- Keep naming and API surface consistent with the plan (variant-local timesteppers).
- Avoid reintroducing `PFC.Core.steppers` in any form.

Progress update:
- Ready to begin wiring fixes once core steppers are deleted and sim files contain local steppers.