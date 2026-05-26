# sHPFC Refactor — Step 6: Introduce lazy allocation for hydrodynamic-only fields

Purpose: reduce memory footprint for standard PFC runs by allocating hydrodynamic buffers only when needed.

Checklist

Checklist
- [x] Add lazy allocation to `HPFC/state.py` for hydrodynamic-only fields
- [x] Keep steppers backward-compatible; use a `VelBatch` proxy to preserve `state.vel_batch` usage
- [x] Unit tests for lazy allocation (`tests/test_lazy_alloc.py`)

Notes
- Implemented `_VelBatchProxy` in `HPFC/state.py` and properties that allocate on first access.
- Fixed proxy to expose `vel`, `vel_hat`, `v_x`, `v_y`, `v_x_hat`, `v_y_hat` so existing steppers remain unchanged.

Exit criteria
- All tests pass and hydrodynamic buffers are only allocated when first accessed.

Exit criteria
- `stdPFC` runs do not allocate hydrodynamic buffers; hydrodynamic runs produce identical results.
