# sHPFC Refactor — Step 5: Extract DC, FFT batching, and helper utilities

Purpose: consolidate cross-cutting numeric helpers into a single testable module so assumptions are explicit and reusable.

Checklist
- [ ] Add `HPFC/utils.py` with helpers:
  - `preserve_dc(psi_hat, psi_hat_00)`
  - `batch_ifft(payload_mgr, arr, axes=(-2,-1))`
  - `safe_etd_nonlin(dt, lin_kernel)`
  - `normalize_kernel_hat_mean` (thin wrapper around existing helper)
- [ ] Replace inline code in steppers with calls to these helpers.
- [ ] Unit tests for each helper.

Exit criteria
- Helpers tested and referenced by steppers; numerical behavior preserved.
