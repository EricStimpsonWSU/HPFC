# sHPFC Refactor — Step 2: Extract kernel/provider (model rules)

Purpose: centralize the kernel and ETD formula logic into a `KernelRules` dataclass so model-specific expressions are isolated and auditable.

Checklist
- [ ] Add `HPFC/kernel_rules.py` implementing `KernelRules(model, geometry)`.
- [ ] Move ETD and linear/nonlinear kernel-building code from `PFC2D_kernels.py` into `KernelRules`.
- [ ] Keep `PFC2D_kernels.py` as a thin compatibility shim that imports and forwards to `KernelRules` during transition.
- [ ] Add unit tests mirroring `tests/test_kernels.py` that verify numeric equivalence to the pre-refactor outputs.
- [ ] Ensure `sHPFC` can be pointed to `KernelRules` without behavioral change.

Exit criteria
- Kernel/ETD logic lives in `KernelRules` and tests confirm equivalence.
