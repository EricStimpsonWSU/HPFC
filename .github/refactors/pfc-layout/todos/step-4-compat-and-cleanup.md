# Step 4 - Compatibility Cleanup

Purpose: remove temporary migration scaffolding and make the new layout the stable long-term surface.

Status: Completed — imports migrated, shim removed, focused tests, baselines, and full test suite passed.

What to verify first
- Any compatibility shims still needed for consumer migration.
- The smallest set of tests that prove the new layout is stable.

Checklist
- [x] Inventory remaining compatibility shims and compatibility-facing code.
	- Noted shims/places to review: `PFC/Core/PFC2D_kernels.py` (legacy re-export of `KernelRules`), the internal `hydro` view alias in `PFC.stdPFC.build_model`, and residual `HPFC` references in documentation/examples.
- [x] Pin the narrowest import-contract tests that express the canonical `PFC` surface and any accepted compatibility paths.
	- Note: focused import-contract test executed locally and passed.
- [x] Update internal consumers and tests to use the canonical `PFC` imports rather than legacy views.
- [x] Remove the `PFC/Core/PFC2D_kernels.py` shim once consumers/tests are migrated.
- [x] Remove internal parameter-view aliases (e.g., the `hydro` mirror in `build_model`) if no external consumer relies on them.
	- Action: aggressive removal completed; callers and tests updated to use top-level hydrodynamic attributes (`rho0`, `Gamma_s`, or hPFC-specific names).
- [x] Update migration notes and README examples to deprecate `HPFC` references and point to canonical `PFC` imports.
	- Note: you handled README/migration notes outside this chat; not modified here.
- [x] Run focused tests and baseline checks after each minimal change.
	- Note: focused kernel tests, import-contract, and baseline checks passed; full test suite executed below.

Validation notes:

- Updated tests and package surface to use `PFC.Core.kernel_rules` (replacing `kernels` shim).
- Deleted `PFC/Core/PFC2D_kernels.py` compatibility shim.
- Aggressively removed `model.hydro` parameter-view aliases and updated callers/tests to use top-level model attributes.
- Executed focused kernel tests, import-contract test, baseline checks, and the full pytest suite in the project virtualenv; all tests passed (165 passed).

Exit criteria: met — the new package layout is stable, validated by the full test suite, and the cleanup is complete.

Step 4: COMPLETED

Constraints
- Do not widen scope into unrelated refactors.
- Keep the final behavior identical to the pre-refactor behavior.

Removal order (recommended)
- When removing compatibility shims follow this sequence:
	1. Remove the shim (small, local change).
	2. Run the focused tests and baselines (verify failures).
	3. Fix broken tests by switching them to canonical `PFC` imports or remove tests that only asserted shim behavior.

- Note: `tests/test_pfc_import_compat_hpfc.py` currently exercises the shim-backed import surface; treat it as a migration-protection test and update or remove it in step 3 above.

Exit criteria
- The new package layout is stable, validated, and the cleanup is complete.
