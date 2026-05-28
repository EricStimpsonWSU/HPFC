# Step 1 - Core Split

Purpose
- Move the shared implementation into PFC/Core while keeping runtime behavior and numerical outputs unchanged. This step only defines the shared/core boundary and a minimal, file-level migration plan — no code moves or implementation are performed here.

Checklist (file-level classification)
- [ ] Core (should be moved to `PFC/Core`):
	- HPFC/backend.py
	- HPFC/fft_utils.py
	- HPFC/fields.py
	- HPFC/payload.py
	- HPFC/state.py
	- HPFC/kernel_rules.py
	- HPFC/PFC2D_geometry.py
	- HPFC/PFC2D_kernels.py
	- HPFC/PFC2D_model.py
	- HPFC/_simulation_facade.py (shared entrypoints)
	- HPFC/steppers.py

- [ ] Model-specific (must remain under model folders):
	- HPFC/sim_pfc_std.py  -> PFC/stdPFC
	- HPFC/sim_shpfc_std.py -> PFC/sHPFC
	- HPFC/sim_shpfc_div_vpsi.py -> PFC/sHPFC
	- HPFC/sim_shpfc_psigradmu.py -> PFC/sHPFC
	- HPFC/timestep_std.py -> PFC/stdPFC
	- HPFC/timestep_hydro.py -> PFC/sHPFC

Notes / rationale
- The items listed as Core are infrastructure, numerical primitives, and shared kernels/geometry used by both models. The sim_*/timestep_* modules contain variant-specific orchestration and numerical choices and must remain model-specific.
- Treat files under `HPFC/specs/` and design markdown as read-only for this step; model documentation migration is Step 5.
- Ignore any `sHPFC-refactor*` drafts for this classification.

Constraints
- Preserve deterministic numerical outputs and existing baselines.
- Keep changes minimal and local; plan-only at this stage.

Exit criteria (explicit)
- The shared-core boundary is recorded in this todo with a concrete per-file classification.
- A follow-up Step 2 plan is ready: a narrow import-contract test suite that references the files above and verifies importability from both `PFC/Core` and the model packages.
- A clear list of files to move during implementation is present and unambiguous.

Next action
- Prepare the Step 2 artifacts: a small set of import-contract tests and a mapping file that records old -> new import paths. After you approve this classification I will generate the import-contract tests (using e:\\HPC\\.venv\\Scripts\\python.exe -m pytest) and then implement the first guarded moves in small commits.

Exit note
- This file is intentionally conservative: if you want an alternative split (for example moving `PFC2D_model.py` into model folders), tell me which files to reconsider and I will update the classification before implementation.
