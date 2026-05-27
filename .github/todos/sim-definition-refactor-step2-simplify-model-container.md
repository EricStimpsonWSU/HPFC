# PFC Simulation Definition Split — Step 2: Simplify the Model Container

Purpose: reduce duplication in model assembly by introducing a minimal, shared model container shape that all simulation variants can consume.

Status: in-progress.

Checklist
- [x] Add narrow tests that exercise the minimal model container shape and its consumer call sites (use existing small-grid, low-step fixtures).
- [ ] Create focused fixtures for the simplified model container that mirror the consumer-facing contract validated in Step 1.
- [x] Update the narrowest set of call sites (model construction, sim assembly) to accept the shared container shape; prefer adapters over wholesale rewrites.
- [ ] Run baseline-checks on the small-grid deterministic cases and update only if behavior-preserving changes require baseline refresh.
- [ ] Integrate these narrow tests into the baseline/CI harness so regressions are caught early.

Exit criteria
- The simplified container shape is defined and covered by tests demonstrating correct consumption by all variants.
- Narrow, behavior-preserving changes are implemented and validated by the small-grid baseline suite.
- No design/spec docs were edited as part of this step.

Notes
- Keep changes minimal and behavior-preserving; prefer small adapters and backwards-compatible call-site shims.
- Add/adjust narrow tests before making implementation changes.
- Use the workspace Python environment and deterministic small-grid / low-step configurations for all tests.
- Ignore any sHPFC-refactor* files for this step.
- Do not edit the design/spec documents under `design/` or `/.github/specs/` unless explicitly requested.

Next focus
- Author the narrow tests and fixtures that codify the simplified container shape; then implement the smallest code changes required to make those tests pass.
Next action
- Create focused fixtures for the simplified container shape and extend coverage to the hydrodynamic variants.

Note: Implemented a lightweight adapter in `HPFC/sim_pfc_std.build_model` and added a narrow test exercising the simplified container. Run tests locally with the workspace venv.
