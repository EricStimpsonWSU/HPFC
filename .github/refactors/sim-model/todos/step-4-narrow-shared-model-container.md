# Step 4 - Narrow the Shared Model Container

Purpose: Reduce the shared model container to the true base contract and shared helpers only, and remove any generic fallback that masks missing sim contracts.

Status: planned

Checklist:
- [ ] Keep `temp`, `beta`, `Gamma`, and `dt` explicit as the shared base contract.
- [ ] Remove or isolate variant-only assumptions from the shared container.
- [ ] Move any remaining variant-specific defaulting logic into the sim modules.
- [ ] Leave compatibility helpers only if the transition still needs them.
- [ ] Add or keep only the smallest validation helper needed to fail fast on missing declared parameters.
- [ ] Remove any generic kernel/model fallback that assumes all variants expose the same extra attributes.

Exit criteria:
- The shared model layer is generic and no longer implies one universal property shape or fallback contract.

Notes (constraints):
- Do not change algorithmic behavior.
- Keep the shared layer as small as possible.
- Do not reintroduce a monolithic resolver or builder in the name of convenience.

Progress update:
- The shared container cleanup should happen only after the variant modules are expressing the right contract.
