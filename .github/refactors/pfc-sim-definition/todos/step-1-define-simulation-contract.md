# PFC Simulation Definition Split — Step 1: Define the New Simulation Contract

Purpose: make the consumer-facing assembly workflow explicit before moving ownership boundaries.

Status: complete.

Checklist
- [x] Add tests that demonstrate how a consumer assembles a simulation: import a sim module, import model and geometry helpers, build a `PFC2D_model`, build a geometry, create an initial `SimulationState`, and instantiate the sim object.
- [x] Create focused fixtures that construct minimal `model`, `geometry`, and `state` objects suitable for consumer tests and baseline runs.
- [x] Add tests that assert the canonical import paths for each variant (e.g., `HPFC.sim_pfc_std`, `HPFC.sim_shpfc_std`, `HPFC.sim_shpfc_div_vpsi`, `HPFC.sim_shpfc_psigradmu`) and validate the assembly contract (expected factory functions / names). Prefer the `sHPFC` acronym in spec and tests rather than generic "hydro" naming.
- [x] Ensure consumer tests are deterministic and compatible with the existing baseline harness (reuse small-grid configs / low step-counts).
- [x] Integrate these tests into the baseline-check harness or CI so Step 1 regressions are caught early.
- [x] Add a short design note (or update the refactor plan) capturing the chosen canonical import surface.

Exit criteria
- The consumer workflow is expressed in tests and the expected import path for each simulation variant is clear and stable.
- Focused fixtures exist so tests are reproducible and deterministic.
- The new tests are wired into baseline/CI checks.

Notes
- Follow Step 0 conventions: keep grid sizes small and rely on existing baseline data under `tests/baselines/data/` as the truth set.
- Do not refactor implementation code in this step; only add tests and fixtures that describe the desired consumer contract.

Next focus
- Move to Step 2 (simplify the model container) now that the consumer contract is validated by tests.

Next action
- Start Step 2 by defining the minimal shared model container shape and adjusting fixtures/call sites in the narrowest affected tests.
