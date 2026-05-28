# Step 3 - Docs Migration

Purpose:
move model documentation next to the implementation it describes.

Status:
completed

Checklist:
- [x] Confirm `plan.md` is source-of-truth for model folder names and layout.
- [x] Map existing model document filenames to their target model folders:
	- `HPFC_specs.md` -> `PFC/HPFC/HPFC_specs.md`
	- `PFC_sHPFC_specs.md` -> `PFC/sHPFC/PFC_sHPFC_specs.md`
- [x] Recover the original `HPFC/specs/` documents from the parent commit that still contained them.
- [x] Move `PFC_specs.md` to `PFC/stdPFC/`.
- [x] Move `PFC_sHPFC_specs.md` to `PFC/sHPFC/`.
- [x] Confirm no local links or references needed path updates.
- [x] Add/update `.gitignore` entries to ignore generated PDFs of model docs.

Next action:
none; Step 3 is complete.

Notes on tests:
- Use the repository Python from the workspace virtualenv for test runs:

	e:\HPC\.venv\Scripts\python.exe -m pytest -q

Exit criteria:
- Model docs sit beside the model-specific implementation they describe.
- PDFs of model docs should be ignored
