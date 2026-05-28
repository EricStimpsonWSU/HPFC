# Step 0 - Import Contract

Purpose: lock the public import boundary before any file moves. `PFC` is the canonical package surface, and `HPFC` remains only as a temporary compatibility shim during the transition.

Checklist
- [x] Confirm the accepted entry points are `PFC/Core`, `PFC/stdPFC`, and `PFC/sHPFC`.
- [x] Keep existing `HPFC` imports working only as a transition path, not as the long-term target.
- [x] Identify the narrowest contract tests needed to pin the import surface before implementation changes.
- [x] Do not move implementation files or change numerical behavior in this step.

Exit criteria
- The canonical `PFC` import surface is explicit.
- The `HPFC` compatibility strategy is documented as temporary and transitional.
- The next-step contract tests are clear enough to add without broadening scope.

Next action
- Add narrow import-contract tests for the accepted `PFC/Core`, `PFC/stdPFC`, and `PFC/sHPFC` paths, plus only the compatibility import path that must remain during the transition.

Verification notes
- I inspected the repository: `HPFC` remains the project package and no `PFC` package or `PFC/Core`, `PFC/stdPFC`, or `PFC/sHPFC` folders exist yet.
- I added narrow import-contract pytest files to pin the desired surface (tests added):
	- `tests/test_pfc_entrypoints_core.py`
	- `tests/test_pfc_entrypoints_std.py`
	- `tests/test_pfc_entrypoints_shpfc.py`
	- `tests/test_pfc_import_compat_hpfc.py`
- The added tests express the expected `PFC` entrypoints and a compatibility test that imports existing `HPFC` simulation helpers.
- With the tests in place the import contract is explicit (the `PFC/*` surface is defined by the tests). Note: the `PFC` package itself is not yet implemented; these tests will fail until thin shim modules are added to expose the specified symbols.

Exit criteria verification
- The canonical `PFC` import surface is explicit: satisfied (the import-contract tests define the surface).
- The `HPFC` compatibility strategy is documented as temporary and transitional: satisfied (compat test added and notes updated).
- The next-step contract tests are clear enough to add without broadening scope: satisfied (tests added; next step is to scaffold `PFC` shims that re-export existing symbols).

Next recommended step
- Scaffold minimal `PFC` package shims (e.g., `PFC/Core.py`, `PFC/stdPFC.py`, `PFC/sHPFC.py`) that re-export the listed symbols from existing modules so the tests pass, then run the new tests and iterate.
