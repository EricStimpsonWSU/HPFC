# sHPFC Refactor — Step 4: Introduce field-layout dataclass wrappers

Purpose: replace magic indexing into `_batch_*` arrays with semantic wrappers to reduce risk of indexing bugs and improve readability.

Checklist
- [x] Add `HPFC/fields.py` with small dataclasses like `PsiBatch`, `GradBatch`, `VelBatch`, `ForceBatch` exposing named attributes that view into the backing arrays.
- [x] Ensure wrappers are zero-cost (attribute access returns a view into the existing array, not a copy).
- [x] Replace direct `_batch_*` indexing in `steppers` and `state` with the wrappers.
- [x] Add tests that assert wrapper attribute assignments update underlying arrays.

Status: complete.

Exit criteria
- No numerical change in outputs; code readability improved.
