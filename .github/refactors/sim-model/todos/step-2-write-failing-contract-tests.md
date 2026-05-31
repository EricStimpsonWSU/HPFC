# Step 2 - Write Failing Contract Tests

Purpose: Add narrow tests that define the desired model-property contract and kernel-builder hook before implementation changes begin.

Status: planned

Checklist:
- [ ] Add tests that assert every variant exposes the shared base contract.
- [ ] Add tests that assert variant-specific extras exist only where needed.
- [ ] Add tests that pin the aliasing behavior for variants that use local names for shared semantics.
- [ ] Add tests that exercise model construction through the canonical sim module entrypoint.
- [ ] Add tests that assert `REQUIRED_MODEL_PARAMS`, `OPTIONAL_MODEL_PARAMS`, `build_model`, and `build_lin_kernels` exist where expected.
- [ ] Add tests that fail when a sim module relies on a hidden generic fallback instead of its own declared contract.

Exit criteria:
- The test suite documents the target model-property contract and kernel-builder hook and fails on the current implementation for the right reasons.

Notes (constraints):
- Do not fix the production code yet.
- Prefer the narrowest possible contract assertions.
- Make the tests opinionated: they should describe the final contract, not a compromise shape.

Progress update:
- Contract tests are the next practical checkpoint once the current parameter map is recorded.
