# PFC Simulation Definition Split — Step 0: Capture and Verify Baselines

Purpose: lock in deterministic numerical outputs for the current simulation variants so later refactors can prove behavioral equivalence.

Status: complete.

Checklist
- [x] Confirm the baseline harness under `tests/baselines/` exercises all four current variants on a fixed small geometry: `stdPFC`, `Timestep_sHPFC`, `Timestep_sHPFC_div_vpsi`, and `Timestep_sHPFC_psigradmu`.
- [x] Verify the harness records the reference arrays needed for regression detection, including `psi`, `psi_hat`, `psi_hat_00`, and hydrodynamic outputs such as `v_x`, `v_y`, and `div_vpsi_hat` / `v_dot_grad_psi_hat` where applicable.
- [x] Confirm `tests/test_baselines_check.py` parametrizes every variant and step count so all four baselines are exercised as the refactor progresses.
- [x] Ensure the baseline generation path remains deterministic by using the existing fixtures and a small grid / low step-count configuration.
- [x] Run the narrow baseline check against the committed `.npz` files and verify the baseline tree stays unchanged.
- [x] Run the full test suite before step 1 work begins.

Exit criteria
- Baseline reference files exist and are committed.
- Baseline-check tests pass on the unmodified code.
- The baseline harness is reproducible and suitable for later refactor verification.

Notes
- Treat the current baseline data under `tests/baselines/data/` as the truth set for the step-0 refactor boundary, with one baseline file set for each of the four current variants.
- Keep this step strictly behavior-preserving; do not change numerical algorithms while capturing baselines.

Next focus
- Step 1: baseline harness and CI integration around the existing truth set.

Next action
- Run the full test suite, then move to the step-1 harness/CI follow-up once the repository is green.