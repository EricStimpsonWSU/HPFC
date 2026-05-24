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