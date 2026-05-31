# Step 6 - Run Deterministic Tests

Purpose: Verify that the refactor preserves behavior and that the new model contract, kernel hook, and validation path are stable.

Status: planned

Checklist:
- [ ] Run the narrow contract tests for each variant module.
- [ ] Run small deterministic regression tests for the affected variants.
- [ ] Run any baseline checks already used in the repo for the canonical variants.
- [ ] Confirm the full test suite passes once the wiring is fixed.
- [ ] Confirm that missing required params or missing `build_lin_kernels` fail loudly where the tests expect them to.

Exit criteria:
- Contract tests, validation-path tests, and deterministic behavior checks pass.

Notes (constraints):
- Preserve numerical determinism.
- Investigate any difference before widening the scope.
- Prefer fixing the contract boundary over adding compatibility logic if a test fails.

Progress update:
- Validation comes after the contract and wiring are aligned.
