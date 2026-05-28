# sHPFC Refactor — Step 2: Extract kernel/provider (model rules)

Purpose: centralize the kernel and ETD formula logic into a `KernelRules` dataclass so model-specific expressions are isolated and auditable.

Checklist
- [x] Add `HPFC/kernel_rules.py` implementing `KernelRules(model, geometry)`.
- [x] Move ETD and linear/nonlinear kernel-building code from `PFC2D_kernels.py` into `KernelRules`.
- [x] Keep `PFC2D_kernels.py` as a thin compatibility shim that imports and forwards to `KernelRules` during transition.
- [x] Add unit tests mirroring `tests/test_kernels.py` that verify numeric equivalence to the pre-refactor outputs.
- [x] Ensure `sHPFC` can be pointed to `KernelRules` without behavioral change.

Notes
- Removed the dead `kernels_2D_CPU` compatibility class; the shim now only re-exports the working provider and helper functions needed for existing tests and staged migration.

Exit criteria
- Kernel/ETD logic lives in `KernelRules` and tests confirm equivalence.
