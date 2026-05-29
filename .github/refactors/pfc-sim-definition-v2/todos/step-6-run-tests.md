# Step 6 — Run Deterministic Tests

Purpose: Verify that the refactor preserves numerical behavior and determinism.

Status: not-started

Checklist:
- [ ] Run narrow deterministic tests (small grid, few steps) for each variant.
- [ ] Run the import-contract tests and any architecture tests added in Step 2.
- [ ] Run baseline checks for canonical outputs where available.
- [ ] Run the full test suite and ensure all tests pass.

Exit criteria:
- All relevant deterministic and contract tests pass; full test suite passes in CI/local virtualenv.

Notes (constraints):
- Preserve numerical determinism: avoid non-deterministic scheduling or race conditions.
- If numerical differences arise, investigate code placement or subtle ordering changes in steppers.

Progress update:
- Tests will be executed after wiring fixes; failures will be investigated and fixed.