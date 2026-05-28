# Step 1 - Core Split

Purpose: move the shared implementation into `PFC/Core` while keeping the current runtime behavior intact.

What to verify first
- Shared modules that do not belong to a specific model variant.
- Import sites that currently depend on `HPFC` package placement.

What to implement next
- Move shared backend, FFT, field, payload, state, kernel-rule, geometry, and model primitives into the core boundary.
- Keep variant-specific logic out of the shared core.

Constraints
- Preserve existing numerical outputs.
- Keep changes local and minimal.

Exit criteria
- Shared infrastructure imports from `PFC/Core` and tests still pass.
