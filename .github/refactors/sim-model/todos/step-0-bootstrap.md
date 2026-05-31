# Step 0 - Bootstrap the Refactor

Purpose: Create the refactor workspace for `sim-model` and capture the current model-property inventory, including the contract markers each sim module should own.

Status: planned

Checklist:
- [ ] Create the folder `.github/refactors/sim-model/`.
- [ ] Add `.github/refactors/sim-model/plan.md`.
- [ ] Create `.github/refactors/sim-model/todos/`.
- [ ] Record the current model-property map for each variant module.
- [ ] Record whether each module already exposes `REQUIRED_MODEL_PARAMS`, `OPTIONAL_MODEL_PARAMS`, `build_model`, and `build_lin_kernels`.

Exit criteria:
- The refactor folder exists and the model-property mapping work has a clear starting point, including the current contract hooks.

Notes (constraints):
- Keep this step strictly as setup and inventory.
- Do not modify production code here.
- Capture the current fallback behavior too, because the later steps should remove any hidden assumptions.

Progress update:
- Bootstrap pending. Ready to map the current model-property surfaces.
