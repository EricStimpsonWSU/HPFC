# Step 4 - Compatibility Cleanup

Purpose: remove temporary migration scaffolding and make the new layout the stable long-term surface.

What to verify first
- Any compatibility shims still needed for consumer migration.
- The smallest set of tests that prove the new layout is stable.

What to implement next
- Trim or remove shims that are no longer justified.
- Update internal consumers and tests to use the new import paths.
- Run focused tests and baseline checks after the cleanup.

Constraints
- Do not widen scope into unrelated refactors.
- Keep the final behavior identical to the pre-refactor behavior.

Exit criteria
- The new package layout is stable, validated, and the cleanup is complete.
