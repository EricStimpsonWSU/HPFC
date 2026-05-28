# Step 2 - Model Split

Purpose: move the standard and hydrodynamic model entry points into `PFC/stdPFC` and `PFC/sHPFC`.

What to verify first
- Which modules are model-specific rather than shared infrastructure.
- Which consumer tests currently anchor the public simulation import surface.

What to implement next
- Relocate the standard PFC modules into `PFC/stdPFC`.
- Relocate the hydrodynamic modules into `PFC/sHPFC`.
- Keep the variant-specific timestep orchestration with the matching model folder.

Constraints
- Do not alter timestep math or kernel behavior.
- Preserve the deterministic baseline fixtures.

Exit criteria
- Each model family has a clear folder boundary and stable import path.
