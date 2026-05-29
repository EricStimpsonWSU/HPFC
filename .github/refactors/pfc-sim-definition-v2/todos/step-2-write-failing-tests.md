# Step 2 — Write Failing Tests (Break‑First)

Purpose: Codify the desired architecture using tests that will fail until steppers are moved into sim files.

Status: completed

Checklist:
- [x] Add tests that assert each `sim_<model>_<variant>.py` exposes sim-owned `step` entrypoint function(s) with the appropriate timestep and helper functions.
  - [x] For `sHPFC` sims, also assert the presence of a `std_step` entrypoint that implements the std-PFC stepping behavior.
- [x] Add tests that assert `PFC/Core/steppers.py` no longer contains the timestepper classes and stepper-owned helpers that are being moved.
- [x] Add tests that assert `PFC/Core/state.py` no longer contains the stepper-owned helpers that are being moved into sim files.

Per-file test matrix:

| File | Expected failing assertions |
| --- | --- |
| `PFC/stdPFC/sim_pfc_std.py` | Provides a sim-owned `step` entrypoint and local `calc_mu` / `calc_f` helpers. |
| `PFC/sHPFC/sim_shpfc_std.py` | Provides sim-owned `step` and `std_step` entrypoints (primary `step` for sHPFC behavior, `std_step` for std-PFC equivalent) plus `_calc_common_hydro_fields` and local `calc_mu` / `calc_f` helpers. |
| `PFC/sHPFC/sim_shpfc_div_vpsi.py` | Provides sim-owned `step` and `std_step` entrypoints (div-vpsi `step` plus `std_step` equivalent) plus `_calc_common_hydro_fields` and local `calc_mu` / `calc_f` helpers. |
| `PFC/sHPFC/sim_shpfc_psigradmu.py` | Provides sim-owned `step` and `std_step` entrypoints (psigradmu `step` plus `std_step` equivalent) and local `calc_mu` / `calc_f` helpers. |
| `PFC/Core/steppers.py` | Does not define the moved timestepper classes or stepper-owned helper methods anymore. |
| `PFC/Core/state.py` | Does not define the helper methods that are being relocated into the sim files. |

Notes:
- steppers will be member functions in sims rather than separate classes.

Exit criteria:
- The test suite contains tests that fail for the expected architectural reasons (i.e., tests reference steppers-in-sim and absence of moved logic from `PFC.Core.steppers` and `PFC.Core.state`).

Validation:
- I ran the new contract tests in the workspace venv (`python -m pytest -q tests/test_stepper_refactor_contract.py`). All tests failed as expected, showing:
  - Missing `step` / `std_step` functions in the sim files (pre-refactor state).
  - `_calc_common_hydro_fields` absent where expected prior to move.
  - `StdPFCTimestepper` / `SHPFCTimestepper` still present in `PFC/Core/steppers.py` and `calc_mu` / `calc_f` still present in `PFC/Core/state.py` (these failures are the intended break-first signals).

Status note: Exit criteria met — Step 2 is complete (failing tests added and validated).

Constraints:
- Prefer creating new failing tests over temporarily patching production code.
- Tests should be easy to revert or update in the fix phase.
- Do not modify existing production code to satisfy new tests yet.

Progress update:
- Ready to write the failing tests that document the target architecture.