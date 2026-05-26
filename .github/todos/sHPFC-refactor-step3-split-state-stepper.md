# sHPFC Refactor — Step 3: Split `sHPFC` into state container + stepper strategies

Purpose: separate buffer ownership from timestep orchestration so steppers can be swapped or unit-tested independently.

Current slice: `SimulationState` now owns the arrays, kernel views, and shared helper methods. `sHPFC` remains a thin facade over that state plus the split timestep modules.

Checklist
- [x] Add `HPFC/state.py` with `SimulationState` dataclass that owns backend adapter and preallocated arrays (preserve names/shapes).
- [x] Add one stepper file per variant under `HPFC/steppers/` (or an equivalent layout) so each file eventually contains all variant-specific math for that timestep family in one place.
- [x] Name stepper functions to mirror the LaTeX expression names in `HPFC/specs/sHPFC_exp.md` using ASCII identifiers and matching docstrings, e.g. functions corresponding to `\mathcal{J}_1`, `\mathcal{J}_2`, `\mathcal{H}_1`, `\mathcal{H}_2`, `\partial_t \psi`, and `\rho_0 \partial_t \mathbf{v}`.
- [x] Keep `KernelRules` limited to primitive operators and reusable coefficients; compose them into `dpsi_dt`, `dv_dt`, and variant-specific update expressions in the stepper file.
- [x] Update `sHPFC.py` to become a thin construction facade for `SimulationState` and a chosen stepper.
- [x] Add tests that construct a `SimulationState` and call each stepper, verifying outputs against baselines.
- [x] Keep commits small: first add `SimulationState` and wire through without changing step logic; then add stepper classes that call existing methods.
- [x] Write minimal migration notes for the small runner codebase instead of maintaining compatibility shims.

Exit criteria
- All tests still pass and `sHPFC` remains import-compatible.
