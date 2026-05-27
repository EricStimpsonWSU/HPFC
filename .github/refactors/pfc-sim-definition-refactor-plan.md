# PFC Simulation Definition Split Plan

Goal: split the current PFC simulation family into explicit simulation definition modules so each simulation has a single source of truth for model parameters, stateful and temporary fields, chemical potential and free energy calculations, linear kernels, and timestep orchestration. The refactor should keep the current numerical behavior intact while making `PFC2D_model` more generic and keeping `kernel_rules` focused on reusable spectral operators and universal ETD construction.

Guidelines
- Test-first: every behavior change should be covered by the narrowest relevant regression test before implementation.
- Keep the scope local: prefer the smallest code path that establishes the new simulation-definition boundary.
- Preserve numerical behavior: this is a structural refactor, not a physics change.
- Use importable Python module names: the simulation files should follow the `sim_[model]_[variant].py` style, not hyphenated module names.
- Let the new sim modules be the source of truth: shared modules should expose only reusable infrastructure or primitives.
- Treat `sHPFC` as transitional only if it still has a clear compatibility purpose after the split; otherwise remove it.

Prerequisites
- Keep `HPFC/backend.py`, `HPFC/PFC2D_geometry.py`, and the baseline test infrastructure stable while the simulation split is introduced.
- Use the existing baseline checks as the behavioral truth set for the three current variants.
- Keep documentation and design notes aligned with the code path that is currently intended to be canonical.

Step 0 - Capture and verify baselines [MANDATORY]
Purpose: lock in deterministic numerical outputs for the current variants so later refactors can assert equivalence.
Subtasks:
- Add or keep a small harness under `tests/baselines/` that runs the standard PFC path and the two hydrodynamic variants on a fixed small geometry.
- Save the reference arrays needed to detect regressions, including `psi`, `psi_hat`, `psi_hat_00`, and hydrodynamic outputs such as `v_x`, `v_y`, and `div_vpsi_hat` where applicable.
- Add or update tests that load the reference outputs and compare them to the current implementation with strict tolerances.
Exit conditions:
- Reference baseline files exist and are committed.
- Baseline-check tests pass on the unmodified code.

Step 1 - Define the new simulation contract
Purpose: make the consumer workflow explicit before moving any ownership boundaries.
Subtasks:
- Add tests that describe how a consumer assembles a simulation: import the correct sim module, import supporting model and geometry definitions, build the model, build the geometry, create the initial state, and instantiate the sim.
- Confirm that the simulation definition, not the old facade, is the place where the variant-specific assembly contract is visible.
- Decide the canonical import surface for the new modules and capture it in tests.
Exit conditions:
- The new consumer workflow is expressed in tests.
- The expected import path for each simulation variant is clear and stable.

Step 2 - Simplify the model container
Purpose: make `PFC2D_model` a generic container for shared model settings, with variant-specific extras separated cleanly.
Subtasks:
- Reduce the base model to the shared parameters every simulation needs, including `temp`, `beta`, `Gamma`, and `dt`.
- Move additional parameters that only apply to specific variants into a separate extension object or equivalent namespaced config.
- Update fixtures and call sites so they construct the new model shape without changing the numerical behavior of existing runs.
Exit conditions:
- The shared model container no longer mixes unrelated variant-specific settings.
- Existing tests that construct models still pass after the updated shape is introduced.

Step 3 - Split shared kernels from simulation-specific kernels
Purpose: keep reusable spectral operators in the shared kernel layer while moving model-specific linear-kernel definitions into the sim modules.
Subtasks:
- Keep derivative kernels, Gaussian smoothing, and the universal ETD-building helpers in `kernel_rules`.
- Move the specific linear-kernel definitions used by each simulation into the corresponding sim module.
- Preserve the logic that turns a chosen linear kernel into the linear and nonlinear ETD factors used by timestep updates.
- Update tests to verify that the shared kernel layer still produces the same reusable arrays and that the variant-specific kernels match the prior behavior.
Exit conditions:
- The shared kernel layer only owns reusable operators and universal ETD logic.
- Variant-specific kernel behavior is covered by focused regression tests.

Step 4 - Introduce the per-simulation definition modules
Purpose: make each simulation variant a complete definition file with its own model expectations, field layout, kernels, and timestep wiring.
Subtasks:
- Create one module for the standard PFC algorithm, named `sim_pfc_std`.
- Create separate modules for the two hydrodynamic variants, using clear variant names that reflect their timestep differences.
- Put the simulation-specific definitions in those modules: stateful and temporary field expectations, linear kernel selection, chemical potential and free energy calculations, and timestep orchestration.
- Keep the standard algorithm explicitly non-hydrodynamic.
Exit conditions:
- Each simulation variant has a dedicated definition module.
- The standard variant is named separately from the hydrodynamic family.
- The simulation modules can be imported directly by consumers.

Step 5 - Decide the fate of `sHPFC`
Purpose: eliminate naming ambiguity after the migration.
Subtasks:
- Decide whether `sHPFC` still has a valid post-migration role.
- If it does not, remove it after the new sim modules are adopted.
- If it does, rename it to something meaningfully descriptive and keep it only as a compatibility or factory layer.
- Update tests and call sites so the canonical entry point is the new simulation definition module, not the old facade.
Exit conditions:
- The repository has a clear answer for whether `sHPFC` still exists.
- The canonical API no longer depends on the old name.

Step 6 - Update state and field ownership
Purpose: preserve buffer ownership in `SimulationState` while removing assumptions that belong in the simulation definition.
Subtasks:
- Keep `SimulationState` as the owner of preallocated buffers and shared helpers.
- Move variant-specific field expectations out of `state` and into the sim modules where possible.
- Update field wrappers or buffer aliases only where they simplify the new simulation-definition boundary.
- Add or adjust tests that ensure named views still reference the same underlying arrays.
Exit conditions:
- State management works with the new sim modules.
- Buffer aliasing and array ownership remain stable.

Step 7 - Finalize tests, cleanup, and migration notes
Purpose: make the new path the obvious long-term API and remove temporary scaffolding.
Subtasks:
- Update the narrowest affected tests first, then run the baseline suite and the rest of the variant behavior tests.
- Keep compatibility shims only if they are still justified by consumer migration needs.
- Update README snippets and migration notes to show the new import surface and the new consumer workflow.
- Add a short design note or migration note describing the split and the role of the new sim modules.
Exit conditions:
- Baseline and focused regression tests pass.
- Documentation points to the new simulation definition modules.
- Temporary compatibility code is either gone or clearly marked as transitional.

Appendix: Suggested file layout
- `HPFC/sim_pfc_std.py` - standard PFC simulation definition.
- `HPFC/sim_pfc_hydro_div_vpsi.py` - hydrodynamic variant using `div(v psi)`.
- `HPFC/sim_pfc_hydro_psigradmu.py` - hydrodynamic variant using `psi grad(mu)`.
- `HPFC/PFC2D_model.py` - shared model container.
- `HPFC/kernel_rules.py` - reusable spectral operators and universal ETD construction.
- `HPFC/state.py` - shared buffer ownership and array helpers.

Validation strategy
- Run the narrowest tests for each touched boundary before widening scope.
- Keep the baseline checks green after every meaningful change.
- Only after the new sim modules are stable should broader cleanup or documentation work be considered complete.
