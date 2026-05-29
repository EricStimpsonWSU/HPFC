# Step 2 — Write Failing Tests (Break‑First)

Purpose: Codify the desired architecture using tests that will fail until steppers are moved into sim files.

Status: not-started

Checklist:
- [ ] Add tests that assert each `sim_<model>_<variant>.py` contains a timestepper class definition (simple string checks are acceptable initially).
- [ ] Add tests that assert no production code imports `PFC.Core.steppers` (import-contract style).
- [ ] Add narrow contract tests that pin behavior which must remain stable (small-grid deterministic runs for one or two timesteps).
- [ ] Keep tests minimal and targeted so failures indicate architecture not behavior.

Exit criteria:
- The test suite contains tests that fail for the expected architectural reasons (i.e., tests reference steppers-in-sim and absence of `PFC.Core.steppers`).

Notes (constraints):
- Prefer creating new failing tests over temporarily patching production code.
- Tests should be easy to revert or update in the fix phase.
- Do not modify existing production code to satisfy new tests yet.

Progress update:
- Ready to write the failing tests that document the target architecture.