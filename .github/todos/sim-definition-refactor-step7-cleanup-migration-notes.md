---
title: "PFC Simulation Definition Split — Step 7: Finalize cleanup, docs, and migration notes"
---

Purpose
-------
Make the sim-module split the obvious long-term API, remove any remaining temporary scaffolding, and document the canonical consumer workflow.

Status
------
Pending.

Current state
-------------
- Step 6 boundary is stable: `SimulationState` still owns the shared buffers and the sim modules own the variant-specific field contract.
- The canonical consumer surface is `HPFC.sim_*` and the consumer workflow is `build_model` -> `build_geometry` -> `make_initial_state` -> `make_sim` -> timestep method.
- The full test suite currently passes.
- `README.md` still shows the legacy `from sHPFC import sHPFC` example and needs to be updated to the new import surface.

Remaining work
--------------
- Replace the README usage example with the canonical per-simulation module imports and the small consumer workflow.
- Add a short migration note that maps the old `sHPFC`-style entry points to the new `HPFC.sim_*` modules.
- Keep or remove any surviving compatibility shim only if it is still justified by consumer migration needs; otherwise leave the canonical path free of legacy indirection.
- Verify the narrow contract tests still describe the canonical import surface and that legacy imports are not part of the documented consumer workflow.

Checklist
---------
- [ ] Update `README.md` to import from `HPFC.sim_pfc_std`, `HPFC.sim_shpfc_std`, `HPFC.sim_shpfc_div_vpsi`, and `HPFC.sim_shpfc_psigradmu` instead of `sHPFC`.
- [ ] Add a concise migration note that shows the old-to-new import mapping and the expected consumer assembly steps.
- [ ] Update `models.md` with the additional architectural details needed to explain the sim-module split and the canonical import surface.
- [ ] Clarify whether any compatibility shim remains; if it does, mark it as transitional and keep it out of the canonical workflow docs.
- [ ] Rerun `e:\HPC\.venv\Scripts\python.exe -m pytest` after the cleanup so the docs update is verified against the current contract tests.
- [ ] Keep the baseline checks green after the final cleanup.

Exit criteria
-------------
- Documentation points to `HPFC.sim_*` as the canonical import surface.
- Any surviving compatibility code is clearly transitional, or it has been removed.
- The focused contract tests and full suite remain green after the cleanup.
- The migration note is short, explicit, and aligned with the stable sim-module split.

Next action
-----------
- Update the README example first, then add the migration note and rerun the test suite.

Notes
-----
- Treat `.github/refactors/pfc-sim-definition-refactor-plan.md` as the source of truth.
- Do not edit design/spec docs.
- Ignore any files matching `sHPFC-refactor*`.
- Keep the change local and minimal; this step is documentation and cleanup, not another structural refactor.
