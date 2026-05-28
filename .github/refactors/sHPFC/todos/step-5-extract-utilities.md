# sHPFC Refactor — Step 5: Extract DC, FFT batching, and helper utilities

Purpose: consolidate cross-cutting numeric helpers into a single testable module so assumptions are explicit and reusable.

- Checklist
- [x] Add `HPFC/fft_utils.py` with helpers:
  - `get_dc_mode`, `set_dc_mode`
  - `batched_fftn`, `batched_ifftn_real`
- [x] Replace simple inline FFT/DC operations in steppers with calls to these helpers where appropriate.
- [x] Unit tests for each helper (added `tests/test_fft_utils.py`).

Notes
- I added `HPFC/fft_utils.py` and `tests/test_fft_utils.py` and committed them in "Step 5: add FFT/DC helpers and tests (batched FFT helpers)".

Exit criteria
- Helpers tested and referenced by steppers; numerical behavior preserved.

Exit criteria
- Helpers tested and referenced by steppers; numerical behavior preserved.
