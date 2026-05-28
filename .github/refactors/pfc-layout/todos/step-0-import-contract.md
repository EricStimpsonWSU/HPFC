# Step 0 - Import Contract

Purpose: decide whether `HPFC` remains as a temporary compatibility shim or becomes a hard cutover to `PFC`, and lock the accepted public import paths.

What to verify first
- Current `HPFC` imports used by tests and internal consumers.
- The intended `PFC/Core`, `PFC/stdPFC`, and `PFC/sHPFC` entry points.

What to implement next
- Add the narrowest import-contract tests for the new package paths.
- Record the compatibility decision in the refactor plan.

Constraints
- Do not move implementation files yet.
- Do not change numerical behavior.

Exit criteria
- The canonical import surface is explicit and test-backed.
