# PFC Simulation Definition Split — Step 4: Introduce the per-simulation definition modules

Purpose: make each simulation variant a complete definition file with its own model expectations, field layout, kernels, and timestep wiring.

Status: not-started.

Checklist
- [ ] Add narrow tests that describe the consumer-facing contract for each simulation module on deterministic small-grid, low-step fixtures.
- [ ] Create or update the `HPFC/sim_pfc_std.py`, `HPFC/sim_shpfc_std.py`, `HPFC/sim_shpfc_div_vpsi.py`, and `HPFC/sim_shpfc_psigradmu.py` modules so they are directly importable by consumers.
- [ ] Move the simulation-specific definitions into those modules: field expectations, linear-kernel selection, chemical potential and free-energy calculations, and timestep orchestration.
- [ ] Keep the standard PFC algorithm explicitly non-hydrodynamic.
- [ ] Run the narrow baseline checks and update committed references only if the implementation remains behavior-preserving.

Exit criteria
- Each simulation variant has a dedicated definition module.
- The standard variant is named separately from the hydrodynamic family.
- The simulation modules can be imported directly by consumers.

Notes
- Keep changes minimal and behavior-preserving; add/adjust narrow tests before implementation changes.
- Preserve deterministic small-grid / low-step configurations for regression checks.
- Ignore any files matching `sHPFC-refactor*`.
- Do not edit the design/spec documents under `design/` or `.github/specs/` unless explicitly requested.

Next focus
- Add the narrow consumer-contract tests for Step 4 first, then wire the simulation-specific definitions into the new modules.

Next action
- Define the minimal Step 4 regression slice in tests so the new per-simulation modules can be implemented against a stable contract.