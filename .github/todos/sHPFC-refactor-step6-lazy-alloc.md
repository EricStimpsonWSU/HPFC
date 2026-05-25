# sHPFC Refactor — Step 6: Introduce lazy allocation for hydrodynamic-only fields

Purpose: reduce memory footprint for standard PFC runs by allocating hydrodynamic buffers only when needed.

Checklist
- [ ] Implement lazy allocation API on `SimulationState`: `ensure_hydro_buffers()` or `get_hydro_buffers()`.
- [ ] Update steppers and tests to call the allocation only for hydrodynamic variants.
- [ ] Verify memory usage reduction in small smoke runs.

Exit criteria
- `stdPFC` runs do not allocate hydrodynamic buffers; hydrodynamic runs produce identical results.
