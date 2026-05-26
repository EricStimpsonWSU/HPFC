---
description: "HPFC test conventions"
applyTo: "tests/**"
---

Treat this repository as pytest-first for test work.

Test conventions:
- Prefer `pytest` for all new tests.
- Keep tests small, deterministic, and behavior-focused.
- Reuse shared fixtures from `tests/conftest.py` instead of building setup inline.
- Use `tests/helpers.py` for floating-point comparison helpers.
- Prefer CPU/NumPy coverage by default so the suite runs in the shared environment.
- Use the `force_numpy_backend` fixture when a test needs to exercise sHPFC without GPU-backed backend selection.
- Mark GPU-specific tests with `@pytest.mark.gpu` and keep them optional.
- Keep one behavior change per test whenever practical.
- Add or update the narrowest relevant test before changing implementation behavior.

Import and path conventions:
- Test modules should import project code through the `HPFC/` directory added in `tests/conftest.py`.
- Keep new helpers in `tests/helpers.py` if they are reused across more than one test module.

Validation conventions:
- Run the narrowest relevant `pytest` slice after adding or changing behavior.
- Update the roadmap todo file when an infrastructure or behavior test item is completed.

Baseline conventions:
- Treat files under `tests/baselines/` as truth fixtures for deterministic regression coverage.
- When creating a new baseline, run the smallest deterministic case that exercises the behavior, capture the post-step snapshot, and commit the generated `.npz` alongside the test that reads it.
- When updating an existing baseline, first confirm the implementation change is intentional, then regenerate only the affected variant/step-count files, and update the corresponding assertion test in the same change.
- Prefer explicit baseline file names that encode the variant and step count, such as `stdPFC_steps_1.npz`.
- Keep baseline generation code under `tests/baselines/` and make it runnable as a direct script from the repo root.
- Baseline truth tests should compare arrays with strict tolerances and should fail loudly when a snapshot key is missing or renamed.
- If a baseline update changes the saved fields or their semantics, document the reason in the related step todo file before committing.

Internal baseline tolerances (maintainers-only):
- Purpose: record the tolerances used by the baseline truth tests so maintainers can decide whether to re-record or relax tolerances when numerical drift occurs.
- Comparison method: tests use `numpy.testing.assert_allclose` (via `tests/helpers.py`) to compare baseline arrays.
- Default tolerances: relative tolerance `rtol=1e-7`, absolute tolerance `atol=1e-9`.
- When to relax: only relax tolerances after confirming the change is not due to a numerical bug (e.g., algorithm change, different boundary handling, or deliberate model parameter updates).
- Re-record policy: re-record baselines only with a PR that documents the change in the step todo and includes a reviewer acknowledgement; keep regenerated files minimal (only affected variant/step files).

Note: this section is intended for internal maintainers and is not user-facing documentation.