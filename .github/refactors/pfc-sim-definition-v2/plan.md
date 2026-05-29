# `plan.md` — Refactor: PFC Simulation Definition Surfaces  
### Refactor Name: `pfc-sim-definition`  
### Goal: Move all std PFC and sHPFC timestepper logic into the relevant `sim_<model>_<variant>.py` files and remove `PFC.Core.steppers`  
### Refactor Philosophy: **Break First, Fix Later**  
### Shared Base Classes: **None** (no StepperBase)

---

# 1. Purpose of This Refactor

The current architecture incorrectly places timesteppers inside `PFC.Core.steppers`, even though timesteppers are **model‑specific** and **variant‑specific**. This refactor restructures the code so that the std PFC and sHPFC surfaces own their own timestepper logic:

- Each variant sim file contains **its own timestepper**
- The Core becomes **fully model‑agnostic**
- Simulation surfaces become **self‑contained**
- No shared steppers exist
- Variant boundaries become **explicit and safe**

This is a **behavior‑preserving cleanup**, but tests will break during the transition.  
This is intentional.

---

# 2. Scope & Boundaries

### In Scope
- Removing `PFC.Core.steppers`
- Moving timestepper logic for std PFC and sHPFC into each variant’s sim file
- Updating std PFC and sHPFC sim files to use their local timesteppers
- Allowing tests to break until the refactor is complete
- Writing new tests that fail until the architecture is correct

### Out of Scope
- Changing physics
- Changing ETD structure
- Changing `SimulationState`
- Changing `KernelRules`
- Changing model parameters
- Changing geometry
- Changing backend behavior
- Changing variant APIs
- Changing naming conventions

---

# 3. Refactor Classification

**Type:** Behavior‑preserving cleanup  
**Risk Level:** Medium  
**Test Strategy:**  
- **Break‑first**: expect failures  
- **Fix‑later**: resolve failures only after structural changes  
- **Narrow contract tests** for any behavior that must remain stable  
- **Deterministic small‑grid tests** for final verification

---

# 4. High‑Level Plan (Break‑First)

1. Create the refactor folder and plan.
2. Extract all timestepper logic from `PFC.Core.steppers`.
3. Write failing tests that assert timesteppers live inside the std PFC and sHPFC sim files.
4. Move timesteppers into each std PFC and sHPFC variant sim file.
5. Update sim files to instantiate local timesteppers.
6. Delete `PFC.Core.steppers` (this will break everything).
7. Fix imports and wiring until tests pass.
8. Run deterministic small‑grid tests for std PFC and sHPFC to confirm behavior is unchanged.
9. Clean up dead code and unused imports.

This plan intentionally breaks the codebase mid‑refactor.  
The system is restored only after all steps are complete.

---

# 5. Exit Criteria

This refactor is complete when:

- No code imports `PFC.Core.steppers`
- Each variant sim file contains its own timestepper class
- All tests pass after the final fix‑phase
- The Core contains **no model‑specific logic**
- The std PFC and sHPFC variant sim files are fully self‑contained
- The facade still blocks/exposes the correct names
- Deterministic small‑grid behavior matches pre‑refactor results

---

# 6. Step Files

You will later split these into:

```
.github/refactors/pfc-sim-definition/todos/
    step-0-bootstrap.md
    step-1-extract-current-steppers.md
    step-2-write-failing-tests.md
    step-3-move-steppers-into-variants.md
    step-4-delete-core-steppers.md
    step-5-fix-imports-and-wiring.md
    step-6-run-tests.md
    step-7-cleanup.md
```

Each section below is written in the required format.

---

# Step 0 — Bootstrap the Refactor

### Step goal
Create the folder structure and initialize the refactor.

### Why it matters
This establishes the workspace for all subsequent steps.

### What to test or verify first
Nothing — this is setup.

### What to implement next
- Create:
  ```
  .github/refactors/pfc-sim-definition/
  ```
- Add this `plan.md`
- Create:
  ```
  .github/refactors/pfc-sim-definition/todos/
  ```

### Constraints
None.

### Exit criteria
Folder exists and contains `plan.md` and an empty `todos/`.

---

# Step 1 — Extract Current Steppers

### Step goal
Identify all timestepper logic in `PFC.Core.steppers`.

### Why it matters
We need to know exactly what logic must be moved into variant sim files.

### What to test or verify first
Nothing — this is analysis.

### What to implement next
- Copy the relevant code into scratch files under `todos/` for reference.

### Constraints
Do not modify production code yet.

### Exit criteria
A clear mapping of:
- which variant uses which stepper
- which methods belong to which variant

---

# Step 2 — Write Failing Tests (Break‑First)

### Step goal
Write tests that assert the **desired architecture**, not the current one.

### Why it matters
These tests will fail immediately — this is intentional.

### What to test or verify first
- Each sim file must contain its own timestepper class.
- No code should import `PFC.Core.steppers`.
- The sim file must expose the correct timestep method.

### What to implement next
Write tests like:

```python
assert "class StdPFCTimestepper" in open("PFC/stdPFC/sim_pfc_std.py").read()
```

### Constraints
Do not fix failing tests yet.

### Exit criteria
Tests fail for the correct reasons.

---

# Step 3 — Move Steppers Into Variants (Break‑More)

### Step goal
Place each timestepper directly inside its corresponding sim file.

### Why it matters
This is the core of the refactor.

### What to test or verify first
- Tests should still fail (expected).

### What to implement next
- Copy stepper logic into each sim file.
- Rename classes as needed.
- Remove unused methods.

### Constraints
Do not fix imports yet.

### Exit criteria
Sim files contain timesteppers but imports are broken.

---

# Step 4 — Delete Core Steppers (Break‑Everything)

### Step goal
Remove `PFC.Core.steppers`.

### Why it matters
The Core must be model‑agnostic.

### What to test or verify first
- Tests should fail loudly.

### What to implement next
- Delete the file.
- Remove any leftover imports.

### Constraints
None — this is the break phase.

### Exit criteria
The codebase is broken in the expected way.

---

# Step 5 — Fix Imports and Wiring (Fix‑Phase Begins)

### Step goal
Update sim files to instantiate local timesteppers.

### Why it matters
This is where the codebase becomes functional again.

### What to test or verify first
- Tests should begin to pass as wiring is corrected.

### What to implement next
Replace:

```python
from PFC.Core.steppers import StdPFCTimestepper
```

with:

```python
class StdPFCTimestepper:
    ...
```

### Constraints
Keep naming consistent.

### Exit criteria
Tests begin passing again.

---

# Step 6 — Run Deterministic Tests

### Step goal
Verify behavior is unchanged.

### Why it matters
This confirms the refactor is behavior‑preserving.

### What to test or verify first
- Small grid (e.g., 16×16)
- Few timesteps (e.g., 3–5)
- Deterministic initial conditions

### What to implement next
Run tests for all variants.

### Constraints
Preserve numerical determinism.

### Exit criteria
All tests pass.

---

# Step 7 — Cleanup

### Step goal
Remove dead imports and unused helpers.

### Why it matters
Ensures the codebase is clean and consistent.

### What to test or verify first
- Ensure no variant imports unused Core utilities.

### What to implement next
- Remove unused imports
- Remove unused helper functions
- Ensure docstrings reflect new structure

### Constraints
Do not modify physics.

### Exit criteria
Codebase is clean, consistent, and self‑contained.
