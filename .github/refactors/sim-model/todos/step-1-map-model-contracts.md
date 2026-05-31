# Step 1 - Map Current Model Contracts

Purpose: Inventory which properties each `sim_[model]_[variant].py` module currently expects, including aliases, variant-only extras, and existing contract hooks.

Status: planned

Checklist:
- [ ] List the base properties that appear everywhere: `temp`, `beta`, `Gamma`, and `dt`.
- [ ] List variant-only extras such as `rho0` and `Gamma_s` where they are required.
- [ ] Note any local aliases used by a variant to realize a shared semantic property under a different name.
- [ ] Capture the current consumer entrypoints that build models through each sim module.
- [ ] Capture the current `build_model` signature and whether `build_lin_kernels` already exists.
- [ ] Note any hidden shared fallback behavior that should be removed later.

Exit criteria:
- A concrete parameter inventory exists for each simulation variant.

Notes (constraints):
- This is read-only analysis.
- Do not normalize names yet; just record the current surfaces.

Progress update:
- Mapping work is ready to start. The next step is to pin the desired contract in tests.
