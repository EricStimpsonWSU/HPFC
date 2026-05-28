# sHPFC Refactor — Step 0: Capture baselines and add regression truth tests

Purpose: create deterministic reference outputs for each timestep variant so later refactors can assert numerical equivalence.

Status: complete.

Checklist
- [x] Add `tests/baselines/generate_baselines.py` harness that runs each variant for small deterministic inputs.
- [x] Run harness locally to produce `tests/baselines/data/stdPFC_steps_1.npz`, `tests/baselines/data/stdPFC_steps_2.npz`, `tests/baselines/data/stdPFC_steps_5.npz`, `tests/baselines/data/sHPFC_steps_1.npz`, `tests/baselines/data/sHPFC_steps_2.npz`, `tests/baselines/data/sHPFC_steps_5.npz`, `tests/baselines/data/sHPFC_div_vpsi_steps_1.npz`, `tests/baselines/data/sHPFC_div_vpsi_steps_2.npz`, `tests/baselines/data/sHPFC_div_vpsi_steps_5.npz`, `tests/baselines/data/sHPFC_psigradmu_steps_1.npz`, `tests/baselines/data/sHPFC_psigradmu_steps_2.npz`, and `tests/baselines/data/sHPFC_psigradmu_steps_5.npz`.
- [x] Add `tests/test_baselines_check.py` that loads `.npz` files and asserts current outputs match references.
- [x] Commit baseline `.npz` files and tests.
- [x] Ensure `pytest -q` passes before continuing to step 1.

Notes
- Use fixtures `simple_model`, `simple_geometry`, and `psi0` from `tests/conftest.py` to ensure determinism.
- Force NumPy backend in harness using the existing `force_numpy_backend` fixture or backend override helper.
- Choose small grid size `(4,4)` and low step counts so files remain tiny.