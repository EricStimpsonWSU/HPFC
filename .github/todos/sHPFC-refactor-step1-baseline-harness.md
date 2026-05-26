# sHPFC Refactor — Step 1: Baseline run harness and CI integration

Purpose: provide tooling and CI support to (re)generate baseline truth sets and validate them on PRs.

Status: complete (harness and baseline files committed; instructions updated).

Checklist
- [x] Add baseline creation/update notes to `.github/instructions/test.instructions.md` so future baseline edits stay consistent.
- [x] Add a direct baseline generator under `tests/baselines/generate_baselines.py` that reuses the step 0 harness.
- [x] Document the acceptable numeric tolerances and how to re-record baselines if intentional changes are made (internal notes in `test.instructions.md`).
- [x] Commit generated baseline `.npz` files under `tests/baselines/data/`.
- [x] Add a small, maintainers-only ideas note under `.github/future-ideas/` for later CI/infrastructure work.

Notes
- CI job deferred: GitHub Actions baseline job is intentionally not added yet; see `.github/future-ideas/` for ideas and next steps.

Exit criteria
- Baseline generation is reproducible locally and the repository contains the baseline data plus a regression test (`tests/test_baselines_check.py`) that validates them.