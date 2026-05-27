# PFC Simulation Definition Split — Step 0: Capture and Verify Baselines

Purpose: lock in deterministic numerical outputs for the current simulation variants so later refactors can prove behavioral equivalence.

Status: not started.

Checklist
- [ ] Confirm the baseline harness under `tests/baselines/` exercises the standard PFC path plus both hydrodynamic variants on a fixed small geometry.
- [ ] Verify the harness records the reference arrays needed for regression detection, including `psi`, `psi_hat`, `psi_hat_00`, and hydrodynamic outputs such as `v_x`, `v_y`, and `div_vpsi_hat` where applicable.
- [ ] Add or update the regression test that loads the committed `.npz` files and compares current outputs against references with strict tolerances.
- [ ] Ensure the baseline generation path remains deterministic by using the existing fixtures and a small grid / low step-count configuration.
- [ ] Run the narrow baseline check and then the full test suite to confirm the repository is stable before step 1 work begins.

Exit criteria
- Baseline reference files exist and are committed.
- Baseline-check tests pass on the unmodified code.
- The baseline harness is reproducible and suitable for later refactor verification.

Notes
- Treat the current baseline data under `tests/baselines/data/` as the truth set for the step-0 refactor boundary.
- Keep this step strictly behavior-preserving; do not change numerical algorithms while capturing baselines.