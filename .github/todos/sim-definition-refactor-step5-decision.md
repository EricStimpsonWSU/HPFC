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

Checklist (test-first)
----------------------
- [ ] Add narrow tests that assert the canonical import paths exist and construct simulations via the sim modules (examples: `HPFC.sim_pfc_std.make_sim`, `HPFC.sim_shpfc_std.make_sim`, `HPFC.sim_shpfc_div_vpsi.make_sim`, `HPFC.sim_shpfc_psigradmu.make_sim`).
- [ ] Add a focused contract test that ensures consumers can run the canonical assembly workflow without importing `sHPFC`.
- [ ] Add a test that `from HPFC.payload import BackendPayloadManager` is importable and behaves as the backend/FFT allocator interface.
- [ ] Extract `BackendPayloadManager` and any FFT batching helpers from `HPFC/sHPFC.py` into `HPFC/payload.py` (implementation step after tests fail).
- [ ] Update sim modules to import `BackendPayloadManager` from `HPFC.payload` and ensure they do not import `sHPFC`.
- [ ] Remove `HPFC/sHPFC.py` once tests and baselines pass.

Exit criteria
-------------
- Canonical import-path tests are added and pass locally (CI green for the narrow tests).
- `BackendPayloadManager` lives in `HPFC/payload.py` and is importable.
- Sim modules no longer import `sHPFC`; `HPFC/sHPFC.py` is removed.
- README and migration note updated to show `HPFC.sim_*` as canonical surface.

Next action (immediate)
-----------------------
- Create the narrow contract tests listed in Checklist (test-first). Keep grids and step counts minimal and deterministic. Do not change implementation code in this step.
- After tests land and fail expecting `HPFC.payload` to exist, extract `BackendPayloadManager` into `HPFC/payload.py` and update sim modules to import from there. Run narrow tests, baseline checks, and then remove `HPFC/sHPFC.py`.

Notes / Constraints
-------------------
- Do not edit design/spec docs; keep scope minimal and local.
- Ignore any `sHPFC-refactor*` files when implementing tests and decisions.
- This file intentionally records the decision but does not change runtime code in Step 5.
