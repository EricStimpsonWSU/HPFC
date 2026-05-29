# Step 4 — Delete Core Steppers (Break‑Everything)

Purpose: Remove `PFC.Core.steppers` so that the Core contains no model-specific timestep logic.

Status: not-started

Checklist:
- [x] Ensure all variant sim files contain local timestepper classes (Step 3 complete).
- [x] Remove the `PFC/Core/steppers.py` (or package) file from the tree.
- [x] Run tests to observe the expected breakage.
- [x] Record failures and map them to missing imports/wiring to guide the fix phase.

Broken tests:
- The full suite now fails during collection before any test bodies run. The first visible failure is `ImportError while loading conftest 'tests/conftest.py'`, caused by `tests/conftest.py` importing `PFC.Core.backend`, which imports `PFC.Core` and still pulls in `PFC.Core.steppers` from `PFC/Core/__init__.py`.
- `PFC/Core/__init__.py` still re-exports the deleted `steppers` module and the removed `SHPFCTimestepper` / `StdPFCTimestepper` symbols. Once `PFC/Core/steppers.py` is deleted, that package-level import chain becomes invalid and blocks every test that imports `PFC.Core` directly or indirectly.
- The variant sim modules still contain direct imports of `PFC.Core.steppers` (`PFC/stdPFC/sim_pfc_std.py`, `PFC/sHPFC/sim_shpfc_std.py`, `PFC/sHPFC/sim_shpfc_div_vpsi.py`, and `PFC/sHPFC/sim_shpfc_psigradmu.py`). Those imports are now dead wiring and must be removed or replaced with the local sim-owned implementations introduced in Step 3.
- Net effect: this step is currently broken at the import/wiring layer, not at an assertion layer. The fix phase needs to remove the stale Core package exports and update the sim modules so they no longer depend on the deleted Core steppers module.

Exit criteria:
- `PFC.Core.steppers` no longer exists in the repository and import errors are produced where expected.

Notes (constraints):
- This is the intentional break phase — expect and accept test failures.
- Do not attempt to patch external users or write compatibility shims in this step; the fix phase will address wiring.

Progress update:
- Deletion will be performed once steppers exist inside sim files; tests will be used to guide fixes.