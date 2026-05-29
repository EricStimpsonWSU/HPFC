# Step 7 — Cleanup

Purpose: Remove dead code, unused imports, and finalize documentation for the new architecture.

Status: completed

Checklist:
- [x] Remove any leftover helper functions that were migrated but no longer used.
- [x] Remove unused imports from Core and sim files.
- [x] Update docstrings and developer docs to reflect steppers now live in sim files.
- [x] Run linters/formatters and fix any style issues introduced by the refactor.
- [x] Update refactor notes and mark the refactor as complete in `.github/refactors/pfc-sim-definition-v2/plan.md`.

Exit criteria:
- No unused code remains; documentation and code style are consistent; the refactor plan is marked complete.

Notes (constraints):
- Do not change physics or algorithmic behavior during cleanup.
- Keep modifications limited to style and dead-code removal.

Progress update:
- Cleanup is complete and the refactor is validated.