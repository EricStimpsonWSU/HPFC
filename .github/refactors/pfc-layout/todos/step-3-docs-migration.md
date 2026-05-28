# Step 3 - Docs Migration

Purpose: move model documentation next to the implementation it describes.

What to verify first
- The current model docs that live under `HPFC/specs/`.
- The intended target folder for each model document.

What to implement next
- Move `HPFC_exps.md` into the `HPFC`-equivalent model folder.
- Move `sHPFC_exp.md` into the hydrodynamic model folder.
- Update any local links or references that must follow the moved files.

Constraints
- Do not edit design/spec markdown beyond the necessary relocation or path updates.
- Keep the docs aligned with the existing code path, not a redesigned API.

Exit criteria
- Model docs sit beside the model-specific implementation they describe.
