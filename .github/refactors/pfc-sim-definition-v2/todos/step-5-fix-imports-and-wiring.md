# Step 5 — Fix Imports and Wiring (Fix‑Phase Begins)

Purpose: Rewire sim files and consumers so they instantiate local timesteppers and the codebase becomes functional again.

Status: not-started

Checklist:
- [ ] Replace any `from PFC.Core.steppers import ...` usages with local class references or local definitions in the sim files.
- [ ] Update `PFC.Core` entrypoints (facade) to import or instantiate variant steppers through the sim files if needed.
- [ ] Run failing tests from Step 2 and fix them by updating imports/wiring — remember the break‑first tests were written to guide this.
- [ ] Prefer editing consumers/tests to use the new local timestepper surface rather than adding shims.

Exit criteria:
- Import errors are resolved; tests start to pass as wiring is corrected.

Notes (constraints):
- Prioritize changing tests/consumers over introducing compatibility shims.
- Keep naming and API surface consistent with the plan (variant-local timesteppers).
- Avoid reintroducing `PFC.Core.steppers` in any form.

Progress update:
- Ready to begin wiring fixes once core steppers are deleted and sim files contain local steppers.