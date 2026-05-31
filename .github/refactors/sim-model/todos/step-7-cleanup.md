# Step 7 - Cleanup

Purpose: Remove dead compatibility code and finalize the migration notes after the explicit sim contracts are stable.

Status: planned

Checklist:
- [ ] Remove stale aliases and helper paths that are no longer needed.
- [ ] Trim unused imports and dead code introduced by the refactor.
- [ ] Update comments or migration notes that still describe the old shared model assumption.
- [ ] Re-run the focused and full regression suite after cleanup.
- [ ] Delete any temporary validation helper if the tests no longer need it.

Exit criteria:
- The model-property refactor is documented, consistent, and free of obvious dead code or generic fallbacks.

Notes (constraints):
- Do not change physics during cleanup.
- Keep the final changes mechanical and local.
- Keep the explicit contract, even if the old broad fallback was shorter.

Progress update:
- Cleanup is the final pass once the contract is stable and verified.
