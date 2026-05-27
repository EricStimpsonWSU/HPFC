# PFC Simulation Definition Split — Step 2: Simplify the Model Container

Purpose: reduce duplication in model assembly by introducing a minimal, shared model container shape that all simulation variants can consume.

Status: in-progress — CI integrated and validated locally.

Checklist
- [x] Add narrow tests that exercise the minimal model container shape and its consumer call sites (use existing small-grid, low-step fixtures).
- [x] Update the narrowest set of call sites (model construction, sim assembly) to accept the shared container shape; prefer adapters over wholesale rewrites.
- [x] Run baseline-checks on the small-grid deterministic cases and update only if behavior-preserving changes require baseline refresh.
- [x] Integrate these narrow tests into the baseline/CI harness so regressions are caught early.

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
- Integrate the narrow hydro-container tests into the baseline/CI harness, then decide whether any remaining fixtures are still needed for Step 2.
Next action
- Keep the new hydro-container contract tests aligned with the canonical sim-definition coverage.

Note: Implemented lightweight adapters in the canonical sim definition modules and added narrow tests exercising the simplified container. Validated with `tests/test_simplified_model_container_sim_shpfc_std.py`, `tests/test_simplified_model_container_sim_shpfc_div_vpsi.py`, `tests/test_simplified_model_container_sim_shpfc_psigradmu.py`, and `tests/test_sim_definition_contract.py`.

Progress update

- **CI integration:** Updated `.github/workflows/ci-baseline-check.yml` to run the baseline regression check plus the simplified-model-container contract tests.
- **Local validation:** Executed the CI test slice with the workspace venv (`e:/HPC/.venv/Scripts/python.exe`) — all tests passed (24 passed).
