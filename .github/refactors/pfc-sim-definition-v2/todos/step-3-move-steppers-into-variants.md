# Step 3 — Move Steppers Into Variants (Break‑More)

Purpose: Move timestepper implementations (member methods) into their corresponding `sim_<model>_<variant>.py` `_SimImpl` member methods according to `model-change.md`.

Status: completed

Checklist (member-method moves, per-file):

- `PFC/stdPFC/sim_pfc_std.py`
	- [x] Add `def step(self) -> None:` method to the `_SimImpl` class containing the body of `StdPFCTimestepper.step`, adapted to use `self.state`.
	- [x] Add `def calc_mu(self, *, psi_hat_is_current: bool = False) -> None:` method on `_SimImpl` copied/adapted from `SimulationState.calc_mu` and updated to reference `self.state`.
	- [x] Add `def calc_f(self, *, psi_hat_is_current: bool = False) -> None:` method on `_SimImpl` copied/adapted from `SimulationState.calc_f`.

- `PFC/sHPFC/sim_shpfc_std.py`
	- [x] Add `def _calc_common_hydro_fields(self) -> None:` method on `_SimImpl` copied/adapted from `SHPFCTimestepper._calc_common_hydro_fields`.
	- [x] Add `def step(self) -> None:` method on `_SimImpl` containing the body of `SHPFCTimestepper.step`, adapted to `self.state`.
	- [x] Add `def std_step(self) -> None:` method on `_SimImpl` containing the body of `StdPFCTimestepper.step` (std-PFC equivalent), adapted to `self.state`.
	- [x] Add `def calc_mu(self, *, psi_hat_is_current: bool = False) -> None:` and `def calc_f(self, *, psi_hat_is_current: bool = False) -> None:` methods on `_SimImpl` copied/adapted from `SimulationState`.

- `PFC/sHPFC/sim_shpfc_div_vpsi.py`
	- [x] Add `def _calc_common_hydro_fields(self) -> None:` method on `_SimImpl` copied/adapted from `SHPFCTimestepper._calc_common_hydro_fields`.
	- [x] Add `def step(self) -> None:` method on `_SimImpl` containing the body of `SHPFCTimestepper.step_div_vpsi`, adapted to `self.state`.
	- [x] Add `def std_step(self) -> None:` method on `_SimImpl` containing the body of `StdPFCTimestepper.step`, adapted to `self.state`.
	- [x] Add `def calc_mu(self, *, psi_hat_is_current: bool = False) -> None:` and `def calc_f(self, *, psi_hat_is_current: bool = False) -> None:` methods on `_SimImpl`.

- `PFC/sHPFC/sim_shpfc_psigradmu.py`
	- [x] Add `def step(self) -> None:` method on `_SimImpl` containing the body of `SHPFCTimestepper.step_psigradmu`, adapted to `self.state`.
	- [x] Add `def std_step(self) -> None:` method on `_SimImpl` containing the body of `StdPFCTimestepper.step` adapted to `self.state`.
	- [x] Add `def calc_mu(self, *, psi_hat_is_current: bool = False) -> None:` and `def calc_f(self, *, psi_hat_is_current: bool = False) -> None:` methods on `_SimImpl`.

- Cleanup and verification subtasks (kept as part of Step 3):
    - [x] Remove `Timestep_*` facades from `PFC/*/sim_*.py`.
	- [x] Verify each moved method preserves variable references to `self.state` and adapts `state = self.state` patterns as needed.
	- [x] Keep changes limited to the `_SimImpl` classes in the sim modules to keep diffs focused.
	- [x] Run the refactor contract tests after moves to inspect the new failure surface.
	- [x] Run the full test suite and inspect the new failure surface.

Test summary:
- Updated the contract and entrypoint tests to expect sim-owned `step` entrypoints, and `std_step` where the sHPFC variants still expose the std-PFC path.
- Replaced direct `Timestep_*` calls in behavior, hydro, and relaxation-energy tests with `sim.step()` so they exercise the public variant API.
- Switched the baseline regression helper and benchmark runner to dispatch through `step()` instead of the removed facade names.
- Confirmed the touched test subset passes after the API alignment.

Exit criteria:
- Each mapped variant sim file contains the expected sim-owned `step` entrypoint (and `std_step` for sHPFC variants where indicated by `model-change.md`) and the moved helper functions. Production imports may be broken but the expected member methods are verified by tests.  The failure surface of the full test suite is documented.

Notes (constraints):
- Do not yet fix imports or wiring — this step focuses on placing code only.
- Keep changes minimal and local to sim files to simplify subsequent diffs.
- Prefer copy+paste of extracted function bodies over refactoring during placement to minimize accidental logic changes.
- Preserve original function signatures and behavior; only rename entrypoints according to `model-change.md` where needed (e.g., rename `StdPFCTimestepper.step` to `step` or `std_step` as mapped).

Progress update:
- Ready to copy extracted stepper function bodies into the target sim files; imports will be intentionally left broken until Step 5.