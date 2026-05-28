# Step 4 - Compatibility Cleanup

Purpose: remove temporary migration scaffolding and make the new layout the stable long-term surface.

Status: In progress — inventory completed; targeted cleanup pending focused tests.

What to verify first
- Any compatibility shims still needed for consumer migration.
- The smallest set of tests that prove the new layout is stable.

Checklist
- [x] Inventory remaining compatibility shims and compatibility-facing code.
	- Noted shims/places to review: `PFC/Core/PFC2D_kernels.py` (legacy re-export of `KernelRules`), the internal `hydro` view alias in `PFC.stdPFC.build_model`, and residual `HPFC` references in documentation/examples.
- [x] Pin the narrowest import-contract tests that express the canonical `PFC` surface and any accepted compatibility paths.
	- Note: focused import-contract test executed locally and passed.
- [ ] Update internal consumers and tests to use the canonical `PFC` imports rather than legacy views.
- [ ] Remove the `PFC/Core/PFC2D_kernels.py` shim once consumers/tests are migrated.
- [ ] Remove internal parameter-view aliases (e.g., the `hydro` mirror in `build_model`) if no external consumer relies on them.
- [ ] Update migration notes and README examples to deprecate `HPFC` references and point to canonical `PFC` imports.
- [ ] Run focused tests and baseline checks after each minimal change.

Next action
- Run the focused import-contract tests and baseline checks using the project virtualenv to confirm the minimal compatibility surface. Example command to run now:

	`e:\HPC\.venv\Scripts\python.exe -m pytest -q tests/test_pfc_import_contract.py tests/test_pfc_import_compat_hpfc.py`

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
