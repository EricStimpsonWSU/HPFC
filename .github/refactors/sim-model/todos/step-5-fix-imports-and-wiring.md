# Step 5 - Fix Imports and Wiring

Purpose: Update builders, fixtures, and consumers so they construct models through the variant contract and respect explicit validation.

Status: planned

Checklist:
- [ ] Update imports that still assume a single shared model shape.
- [ ] Update fixtures and helper builders for the correct per-variant parameters.
- [ ] Prefer the sim module as the canonical entrypoint for model construction.
- [ ] Keep any compatibility shim as small and explicit as possible.
- [ ] Thread any small validation helper through the remaining callers if it helps produce a clear error for missing params.

Exit criteria:
- Consumers resolve model construction through the variant contract without relying on outdated shared assumptions, and missing hooks fail clearly.

Notes (constraints):
- Avoid reintroducing a monolithic model factory.
- Keep the wiring changes local.
- Prefer deleting broad shims over preserving them.

Progress update:
- Once the contract is defined and ownership has moved, this step will reconnect the call sites.
