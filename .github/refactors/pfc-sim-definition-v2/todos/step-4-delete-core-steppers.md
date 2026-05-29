# Step 4 — Delete Core Steppers (Break‑Everything)

Purpose: Remove `PFC.Core.steppers` so that the Core contains no model-specific timestep logic.

Status: not-started

Checklist:
- [ ] Ensure all variant sim files contain local timestepper classes (Step 3 complete).
- [ ] Remove the `PFC/Core/steppers.py` (or package) file from the tree.
- [ ] Run tests to observe the expected breakage.
- [ ] Record failures and map them to missing imports/wiring to guide the fix phase.

Exit criteria:
- `PFC.Core.steppers` no longer exists in the repository and import errors are produced where expected.

Notes (constraints):
- This is the intentional break phase — expect and accept test failures.
- Do not attempt to patch external users or write compatibility shims in this step; the fix phase will address wiring.

Progress update:
- Deletion will be performed once steppers exist inside sim files; tests will be used to guide fixes.