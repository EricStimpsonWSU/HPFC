# Step 3 - Move Variant Model Ownership

Purpose: Move model-property expectations, alias handling, and kernel-builder declarations into the variant sim modules.

Status: planned

Checklist:
- [ ] Update each sim module so it declares the parameters it actually owns.
- [ ] Keep the shared base contract available through the variant module.
- [ ] Move variant-only extras such as hydrodynamic parameters into the relevant sim module contract.
- [ ] Preserve behavior while changing only the property surface.
- [ ] Add per-sim `REQUIRED_MODEL_PARAMS` and `OPTIONAL_MODEL_PARAMS` declarations.
- [ ] Convert `build_model` to the sim-specific signature, or validate `**kwargs` against the declared contract.
- [ ] Add per-sim `build_lin_kernels` implementations next to the model contract.
- [ ] Introduce per-sim dataclasses or small typed config objects if they clarify the contract.

Exit criteria:
- The variant modules own their property names, any local aliases they need, and the kernel builder the Core will call.

Notes (constraints):
- Keep the changes local to the sim modules.
- Do not widen the shared container just to reduce diff size.
- Prefer explicit builders over implicit compatibility shims.

Progress update:
- Ready to move the property ownership boundary into the sim files themselves.
