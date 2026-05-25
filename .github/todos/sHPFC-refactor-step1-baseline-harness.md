# sHPFC Refactor — Step 1: Baseline run harness and CI integration

Purpose: provide tooling and CI support to (re)generate baseline truth sets and validate them on PRs.

Checklist
- [ ] Add `tools/baselines/generate_baselines.py` which reuses the harness in `tests/baselines`.
- [ ] Add `tools/baselines/README.md` with instructions to re-generate and commit reference files.
- [ ] Add optional GitHub Actions job `ci-baseline-check.yml` that runs `tests/test_baselines_check.py` on PRs.
- [ ] Document the acceptable numeric tolerances and how to re-record baselines if intentional changes are made.

Exit criteria
- Baseline generation is reproducible locally and the CI job validates baseline equivalence for PRs.
