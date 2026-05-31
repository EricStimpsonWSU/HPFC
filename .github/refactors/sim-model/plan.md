# `plan.md` - Refactor: PFC Simulation Model Property Surfaces
### Refactor Name: `sim-model`
### Goal: Make each `sim_[model]_[variant].py` module the source of truth for its model contract, required extras, aliases, and kernel builder while preserving current numerical behavior
### Refactor Philosophy: Break First, Fix Later

---

# 1. Purpose of This Refactor

The current model surface mixes shared parameters and variant-specific parameters too early. Some simulations need only the shared base contract, while others require additional values or expose the same semantic property under a different local name.

This refactor makes the simulation module the canonical place where a model's property contract is defined:

- Every sim module declares `REQUIRED_MODEL_PARAMS`
- Optional extras are declared in `OPTIONAL_MODEL_PARAMS` where they exist
- Every model exposes the shared base contract: `temp`, `beta`, `Gamma`, and `dt`
- Variant modules may require extra parameters, such as `rho0` and `Gamma_s`
- Variant modules may also realize the shared semantics under local names, such as `temp` being represented as `r` or `epsilon`
- Every sim module provides `build_model`
- Every sim module provides `build_lin_kernels`
- The shared Core should only own reusable infrastructure and any truly common helpers
- The consumer contract should remain explicit and testable for each `sim_[model]_[variant].py` module
- If a sim module needs a validator, it should be a small helper local to the shared Core, not a new generic model layer

This is a structural refactor, not a physics change.

Non-negotiables
- No hidden generic fallback that assumes every model has `rho0` and `Gamma_s`
- No shared model constructor that forces unused parameters onto std PFC
- No ambiguous kernel discovery path; if a sim does not define `build_lin_kernels`, that should fail loudly during the break-first phase
- Keep the plan sequential and opinionated; do not defer contract decisions until the end

---

# 2. Scope & Boundaries

### In Scope
- Defining a clear model-property contract for each simulation module
- Separating shared base model properties from variant-specific extras
- Allowing variant modules to expose local aliases for shared semantics
- Requiring each sim module to declare and validate its own required parameter set
- Requiring each sim module to provide its own kernel-builder hook
- Updating tests so they describe the desired contract before implementation
- Updating consumers to use the model contract exported by the sim module they actually instantiate
- Introducing small validation helpers only if they keep the contract explicit

### Out of Scope
- Changing physics
- Changing timestep algorithms
- Changing FFT or backend behavior
- Changing geometry definitions
- Broad package renames
- Editing unrelated design documents
- Keeping generic fallbacks that mask missing sim-module contracts

---

# 3. Refactor Classification

**Type:** Structural cleanup with contract clarification
**Risk Level:** Medium
**Test Strategy:**
- Test-first contract coverage
- Narrow per-variant regression tests
- Deterministic small-grid verification for final validation
- Contract failures should happen early and loudly, before any compatibility shim is added

---

# 4. High-Level Plan

1. Bootstrap the refactor folder and document the current model-property map.
2. Write failing tests that pin the required parameter lists, optional parameter lists, and kernel-builder hook for each sim module.
3. Move variant-specific model expectations, aliases, and model dataclasses into the relevant sim modules.
4. Narrow the shared model container and Core helpers so they no longer assume a universal parameter shape.
5. Fix imports, builders, and call sites so consumers assemble models through the sim modules and validate the declared contract.
6. Run focused deterministic tests to verify behavior and naming remain stable.
7. Clean up compatibility code, dead aliases, and migration notes.

The plan intentionally tolerates temporary breakage while the ownership boundary is being moved.

---

# 5. Exit Criteria

This refactor is complete when:

- Each `sim_[model]_[variant].py` file clearly defines the model properties it owns
- The shared base contract is limited to `temp`, `beta`, `Gamma`, and `dt`
- Variant-specific extras are explicit and documented in the variant module that needs them
- Required and optional parameter lists are explicit in each sim module
- `build_lin_kernels` exists where the sim needs it, and the absence of it is treated as a failure during the break phase
- Local aliases are allowed, but the contract is covered by tests
- Consumers can determine the required model shape by looking at the sim module they import
- Deterministic behavior is unchanged after the refactor
- Any validation helper used during the transition is small, explicit, and easy to delete later

---

# 6. Step Files

You will later split these into:

```
.github/refactors/sim-model/
    plan.md
    todos/
        step-0-bootstrap.md
        step-1-map-model-contracts.md
        step-2-write-failing-contract-tests.md
        step-3-move-variant-model-ownership.md
        step-4-narrow-shared-model-container.md
        step-5-fix-imports-and-wiring.md
        step-6-run-tests.md
        step-7-cleanup.md
```

---

# Step 0 - Bootstrap the Refactor

### Step goal
Create the refactor workspace and record the current model-property boundaries, including the explicit contract markers we expect every sim module to own.

### Why it matters
The rest of the work depends on a shared understanding of which parameters are base properties, which are optional, and which sim module owns the kernel builder.

### What to test or verify first
Nothing - this is setup and inventory.

### What to implement next
- Create:
  ```
  .github/refactors/sim-model/
  ```
- Add this `plan.md`
- Create:
  ```
  .github/refactors/sim-model/todos/
  ```
- Record the current `build_model` signature, `build_lin_kernels` surface, and any alias names used by each variant

### Constraints
Do not modify production code yet.

### Exit criteria
The refactor folder exists and contains the plan plus todo scaffolding, and the current contract surface is inventoried.

---

# Step 1 - Map Current Model Contracts

### Step goal
List the current model properties, aliases, and extra requirements for each simulation module.

### Why it matters
The target contract must be grounded in the current code, not in assumptions about how the models should look.

### What to test or verify first
Nothing - this is discovery.

### What to implement next
- Record which modules require only the base contract.
- Record which modules require extra properties such as `rho0` and `Gamma_s`.
- Record any local aliases used by a variant to realize a shared semantic property under a different name.
- Note whether any builder currently exposes compatibility names that should remain during the transition.
- Note whether the module already exposes `REQUIRED_MODEL_PARAMS`, `OPTIONAL_MODEL_PARAMS`, `build_model`, and `build_lin_kernels` or needs them added.

### Constraints
Do not change production code during mapping.

### Exit criteria
There is a clear inventory of the model-property surfaces and the current contract hooks owned by each sim module.

---

# Step 2 - Write Failing Contract Tests

### Step goal
Codify the desired model-property contract in tests before changing the implementation.

### Why it matters
These tests will fail until the model ownership boundary is moved into the sim modules.

### What to test or verify first
- The shared base contract is always present: `temp`, `beta`, `Gamma`, and `dt`.
- Variant-specific modules require their own extra properties where needed.
- Sim modules may expose local aliases, but the public contract is still clear to consumers.
- The consumer entrypoint for a variant is the variant's `sim_[model]_[variant].py` module, not a shared model factory hidden elsewhere.
- Each sim module advertises `REQUIRED_MODEL_PARAMS` and `OPTIONAL_MODEL_PARAMS`.
- Each sim module exposes `build_model` with a signature that matches its declared contract.
- Each sim module exposes `build_lin_kernels`; missing it should fail during the break-first phase.

### What to implement next
Add or update narrow tests that:
- Build each variant's model from its sim module
- Assert the required base properties exist
- Assert variant-specific extras exist only where needed
- Assert the alias mapping is stable for the variants that use one
- Assert the contract markers are present and aligned with the builder signature

### Constraints
Do not fix the implementation yet.

### Exit criteria
The test suite documents the desired model-property contract, kernel-builder hook, and alias behavior and fails for the right reasons on the current code.

---

# Step 3 - Move Variant Model Ownership

### Step goal
Move variant-specific model expectations and aliases into the relevant sim modules.

### Why it matters
The sim module should own the exact property names that its algorithm needs.

### What to test or verify first
- The failing contract tests still point at the old shared assumptions.

### What to implement next
- Update each sim module so it declares the properties it actually needs.
- Keep base properties available through the sim module contract.
- Add or retain local aliases only where they improve compatibility or clarity for that variant.
- Preserve current numerical behavior while changing only the property surface.
- Add per-sim model dataclasses or typed config objects if they make the contract clearer than a monolithic shared model object.
- Make `build_model` construct the sim-specific model shape directly.
- Make `build_lin_kernels` live next to that same contract.

### Constraints
Do not broaden the shared model surface just to avoid touching call sites.

### Exit criteria
The variant modules own their own model-property requirements, aliases, builder signatures, and kernel-builder hooks.

---

# Step 4 - Narrow the Shared Model Container

### Step goal
Reduce the shared container so it only represents the true base contract and shared helpers.

### Why it matters
The shared container should not imply that all variants share the same property names or extra parameters.

### What to test or verify first
- The variant model tests should still describe the final contract.

### What to implement next
- Keep the shared base fields explicit.
- Remove variant-only assumptions from the shared container.
- Move any remaining variant-specific defaults or helper lookups into the sim modules.
- Preserve whatever compatibility path is needed for existing consumers during the transition.
- Add or keep only the smallest helper needed to validate a declared contract; do not reintroduce a generic model resolver that papers over missing attributes.

### Constraints
Do not change behavior outside the model property boundary.

### Exit criteria
The shared model layer is generic, variant-specific behavior lives in the variant modules, and no generic fallback remains that silently supplies missing parameter assumptions.

---

# Step 5 - Fix Imports and Wiring

### Step goal
Update consumers and builders so they assemble models through the correct variant module contract.

### Why it matters
Once the ownership boundary moves, old imports and call sites should stop assuming a single shared parameter shape.

### What to test or verify first
- The contract tests fail only where the wiring still points at the old shape.

### What to implement next
- Update any import surfaces that still construct models from the wrong layer.
- Update fixtures and helpers to pass the correct parameters for each variant.
- Prefer the variant module as the canonical entrypoint for model construction.
- Keep any compatibility shim as small and explicit as possible.
- If a validator helper exists, use it to fail fast when required params or kernel builders are missing.

### Constraints
Avoid reintroducing a monolithic model factory.

### Exit criteria
The codebase builds models through the variant contract instead of relying on shared assumptions, and failures are explicit when a sim does not declare the hooks it needs.

---

# Step 6 - Run Deterministic Tests

### Step goal
Verify that the refactor preserves behavior and that the new contract is stable.

### Why it matters
The model-property boundary can change without changing physics, but only if the numerical results remain stable.

### What to test or verify first
- Narrow variant tests for each touched module
- The contract tests added in Step 2
- Any deterministic small-grid regression checks already used in the repo
- Tests that prove missing `build_lin_kernels` or missing required params fail loudly before any fallback can hide the problem

### What to implement next
- Run the narrowest tests first.
- Expand to the behavior and baseline checks only after the contract is stable.

### Constraints
Do not skip the focused checks just because the refactor is documentation-driven.

### Exit criteria
The model contract tests and deterministic behavior checks pass.

---

# Step 7 - Cleanup

### Step goal
Remove dead compatibility code and finalize the migration notes.

### Why it matters
The new ownership boundary should be obvious to the next person who reads the code.

### What to test or verify first
- The full contract and deterministic test suite

### What to implement next
- Remove stale aliases or helper paths that are no longer needed
- Trim unused imports and dead code
- Update any migration notes or comments that still describe the old shared model assumption

### Constraints
Do not change physics or rework the contract again during cleanup.

### Exit criteria
The model-property refactor is stable, documented, and free of obvious dead code.
