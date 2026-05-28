# Step 2 - Model Split

Purpose: move the standard and hydrodynamic model entry points into `PFC/stdPFC` and `PFC/sHPFC`.

Checklist
- [x] Identify all files that are model-specific (std vs sHPFC).
- [x] Confirm shared/core modules that must remain in `PFC/Core`.
- [x] Create a runnable list of source files to move for `PFC/stdPFC`.
- [x] Create a runnable list of source files to move for `PFC/sHPFC`.
- [x] Add narrow import-contract tests: `tests/test_pfc_entrypoints_model_contract.py` (verifies `PFC.stdPFC.make_sim` and `PFC.sHPFC.make_sim`) — ran locally (2 passed).
- [ ] Move the listed source files into `PFC/stdPFC` (perform after confirmation).
- [ ] Move the listed source files into `PFC/sHPFC` (perform after confirmation).
- [ ] Verify no design/spec markdown needs editing for this step.

What to verify first
- Which modules are model-specific rather than shared infrastructure.
- Which consumer tests currently anchor the public simulation import surface.

What to implement next
- Relocate the standard PFC modules into `PFC/stdPFC`.
- Relocate the hydrodynamic modules into `PFC/sHPFC`.
- Keep the variant-specific timestep orchestration with the matching model folder.

Constraints
- Do not alter timestep math or kernel behavior.
- Preserve the deterministic baseline fixtures.

Exit criteria
- Each model family has a clear folder boundary and stable import path.

Next action
- Produce the explicit file-to-folder mapping (stdPFC vs sHPFC) and post it in this todo for review. After approval, implement the moves in a follow-up step.

Confirmed file mapping (for review)

- PFC/stdPFC (move these source files into `PFC/stdPFC`):
	- [HPFC/sim_pfc_std.py](HPFC/sim_pfc_std.py) -> PFC/stdPFC/sim_pfc_std.py
	- [HPFC/timestep_std.py](HPFC/timestep_std.py) -> PFC/stdPFC/timestep_std.py

- PFC/sHPFC (move these source files into `PFC/sHPFC`):
	- [HPFC/sim_shpfc_std.py](HPFC/sim_shpfc_std.py) -> PFC/sHPFC/sim_shpfc_std.py
	- [HPFC/sim_shpfc_div_vpsi.py](HPFC/sim_shpfc_div_vpsi.py) -> PFC/sHPFC/sim_shpfc_div_vpsi.py
	- [HPFC/sim_shpfc_psigradmu.py](HPFC/sim_shpfc_psigradmu.py) -> PFC/sHPFC/sim_shpfc_psigradmu.py
	- [HPFC/timestep_hydro.py](HPFC/timestep_hydro.py) -> PFC/sHPFC/timestep_hydro.py

- Shared (keep in `PFC/Core`):
	- [PFC/Core/backend.py](PFC/Core/backend.py)
	- [PFC/Core/fft_utils.py](PFC/Core/fft_utils.py)
	- [PFC/Core/fields.py](PFC/Core/fields.py)
	- [PFC/Core/PFC2D_geometry.py](PFC/Core/PFC2D_geometry.py)
	- [PFC/Core/PFC2D_model.py](PFC/Core/PFC2D_model.py)
	- [PFC/Core/kernel_rules.py](PFC/Core/kernel_rules.py)
	- [PFC/Core/PFC2D_kernels.py](PFC/Core/PFC2D_kernels.py)
	- [PFC/Core/payload.py](PFC/Core/payload.py)
	- [PFC/Core/state.py](PFC/Core/state.py)
	- [PFC/Core/steppers.py](PFC/Core/steppers.py)
	- [PFC/Core/_simulation_facade.py](PFC/Core/_simulation_facade.py)

Notes
- `steppers.py` is already a Core facade; implementors (`timestep_std.py`, `timestep_hydro.py`) should reside with the model-specific code but the facade lives in `PFC/Core` for compatibility.
- Leave compatibility shims (top-level HPFC facades) in place until import-contract tests are added in Step 1/2.
