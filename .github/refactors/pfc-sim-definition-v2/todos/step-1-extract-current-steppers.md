# Step 1 — Extract Current Steppers

Purpose: Identify and extract all timestepper logic currently living in `PFC/Core/steppers.py: steppers` for later relocation into variant sim files.

Status: completed

Checklist:
- [x] Open `PFC/Core/steppers.py` (or `PFC/Core/steppers/__init__.py`) and list all timestepper classes and functions.
- [x] Create a mapping document: which timestepper method supports which sim file.
- [x] Copy the code into `.github/refactors/pfc-sim-definition-v2/todos/extracted/` for review (do not change production code).
- [x] Note any helper utilities used by steppers that must be moved or kept in Core.

Exit criteria:
- A clear extraction artifact exists that maps steppers → sim files and includes copied code for reference.

Notes (constraints):
- Do not modify production code during extraction — this is read-only analysis.
- Preserve original formatting to make diffs easy later.
- Focus on behavior-preserving extraction: only identify, do not refactor yet.

Progress update:
- Saved reference copies of `PFC/Core/steppers.py` and the target sim files under `.github/refactors/pfc-sim-definition-v2/todos/extracted/`.
- Rewrote the mapping so each stepper method maps explicitly to the sim file(s) that should own it.

Mapping (steppers (mutating), state (non-mutating) → sim files)

- `PFC/Core/steppers.py: StdPFCTimestepper.step` -->
  - `PFC/stdPFC/sim_pfc_std.py`
  - `PFC/sHPFC/sim_shpfc_std.py`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py`
  - `PFC/sHPFC/sim_shpfc_psigradmu.py`

- `PFC/Core/steppers.py: SHPFCTimestepper._calc_common_hydro_fields` -->
  - `PFC/sHPFC/sim_shpfc_std.py`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py`

- `PFC/Core/steppers.py: SHPFCTimestepper.step` -->
  - `PFC/sHPFC/sim_shpfc_std.py`

- `PFC/Core/steppers.py: SHPFCTimestepper.step_div_vpsi` -->
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py`

- `PFC/Core/steppers.py: SHPFCTimestepper.step_psigradmu` -->
  - `PFC/sHPFC/sim_shpfc_psigradmu.py`

- `PFC/Core/state.py: SimultationState.calc_poly_psi`
  - `PFC/Core/state.py`

- `PFC/Core/state.py: SimultationState.calc_mu`
  - `PFC/stdPFC/sim_pfc_std.py`
  - `PFC/sHPFC/sim_shpfc_std.py`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py`
  - `PFC/sHPFC/sim_shpfc_psigradmu.py`

- `PFC/Core/state.py: SimultationState.calc_f`
  - `PFC/stdPFC/sim_pfc_std.py`
  - `PFC/sHPFC/sim_shpfc_std.py`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py`
  - `PFC/sHPFC/sim_shpfc_psigradmu.py`

Notes:
- `calc_poly_psi` stays Core-owned for now because it is cross-cutting and may remain shared.
- `calc_mu` and `calc_f` are currently routed through `SimulationState`, but the target refactor should move each one into the local `sim_[model]_[variant].py` file that owns the behavior.
- `calc_poly_psi` is owned by Core; `calc_mu` and `calc_f` are owned by the sim files.
- Duplication is intentional: these sim files are meant to be self-contained and independently verifiable.

Exit criteria (for Step 1): mapping is ready for review, extracted reference copies exist, and the checklist reflects the extraction inventory.