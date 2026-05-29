# Step 3 — Move Steppers Into Variants (Break‑More)

Purpose: Place each timestepper class directly into its corresponding `sim_<model>_<variant>.py` file.

Status: not-started

Checklist:
- [ ] For each variant, paste the extracted timestepper implementation into the matching sim file under `PFC/<model>/`.
- [ ] Rename classes only if needed to avoid name collisions and to make intent explicit.
- [ ] Ensure timestepper helper methods used by the stepper are available (either moved or imported from Core utilities that remain).
- [ ] Leave imports broken intentionally for the next step.

Exit criteria:
- Each variant sim file contains a timestepper class; production imports may be broken but the AST and presence of classes is verified by tests.

Notes (constraints):
- Do not yet fix imports or wiring — this step focuses on placing code only.
- Keep changes minimal and local to sim files to simplify subsequent diffs.
- Prefer copy+paste over refactoring during placement to minimize accidental logic changes.

Progress update:
- Prepared to move extracted stepper code into variant files; imports will be addressed in the fix phase.