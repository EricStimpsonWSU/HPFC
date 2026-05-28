---
title: "Sim-definition refactor — Step 5 decision: remove `sHPFC` and extract payload helpers"
---

Decision summary
----------------
- Remove `HPFC/sHPFC.py` as part of Step 5 and extract its backend/FFT/payload responsibilities into a dedicated helper module (suggested: `HPFC/payload.py`).
- Treat the per-simulation modules (`HPFC/sim_*.py`) as the canonical consumer-facing API after Step 5.
- Keep `SimulationState` and the steppers as the owners of arrays and timestep logic; sim modules should import the extracted payload helpers to avoid boilerplate.

Rationale
---------
- Long-term clarity: a single canonical consumer API (`HPFC.sim_*`) reduces confusion and maintenance overhead.
- Separation of concerns: backend/FFT/payload management is a generic PFC concern and belongs in its own module, not in a hydrodynamics-focused `sHPFC` file.
- Minimal pollution: extracting the payload manager avoids duplicating boilerplate across sim modules while letting `SimulationState` keep buffer ownership.

Current status
--------------
- Narrow Step 5 contract tests are in place in `tests/test_sim_definition_contract.py`.
- `HPFC/payload.py` now exists and `BackendPayloadManager` is importable.
- Canonical sim modules have been updated to use `HPFC.payload` and no longer depend on `sHPFC` for construction; removal of `HPFC/sHPFC.py` remains pending.

Checklist (test-first)
----------------------
- [x] Add narrow tests that assert the canonical import paths exist and construct simulations via the sim modules (examples: `HPFC.sim_pfc_std.make_sim`, `HPFC.sim_shpfc_std.make_sim`, `HPFC.sim_shpfc_div_vpsi.make_sim`, `HPFC.sim_shpfc_psigradmu.make_sim`).
- [x] Add a focused contract test that ensures consumers can run the canonical assembly workflow without importing `sHPFC`.
- [x] Add a test that `from HPFC.payload import BackendPayloadManager` is importable and behaves as the backend/FFT allocator interface.
- [x] Extract `BackendPayloadManager` and any FFT batching helpers from `HPFC/sHPFC.py` into `HPFC/payload.py` (implementation step after tests fail).
- [x] Update sim modules to import `BackendPayloadManager` from `HPFC.payload` and ensure they do not import `sHPFC`.
- [x] Remove `HPFC/sHPFC.py` once tests and baselines pass.

Exit criteria
-------------
- Canonical import-path tests are added and pass locally (CI green for the narrow tests).
- `BackendPayloadManager` lives in `HPFC/payload.py` and is importable.
- Sim modules no longer import `sHPFC`; `HPFC/sHPFC.py` has been removed.
- README and migration note updated to show `HPFC.sim_*` as canonical surface.

Next action (immediate)
-----------------------
- All Step 5 implementation and test activities are complete. No further immediate actions required.

Step 5 completion
-----------------
- Step 5 completed: `HPFC/payload.py` added, sim modules updated, tests and baselines passed, legacy `HPFC/sHPFC.py` removed.

Notes / Constraints
-------------------
- Do not edit design/spec docs; keep scope minimal and local.
- Ignore any `sHPFC-refactor*` files when implementing tests and decisions.
- This file intentionally records the decision but does not change runtime code in Step 5.
