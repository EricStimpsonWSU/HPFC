---
title: Baselines and team workflows — future ideas
---

This file collects low-priority ideas related to baselines, CI, and team workflows. It's a light-weight inbox for future infrastructure work; nothing here is prescriptive.

Ideas
- Add a dedicated GitHub Actions job `ci-baseline-check.yml` that runs only `tests/test_baselines_check.py` on PRs touching `HPFC/` or `tests/baselines/`.
- Provide an optional, containerized baseline generation job that runs on a stable reference image to avoid host-dependent numerical differences.
- Add an approval checklist for baseline re-record PRs (e.g., require two maintainers' ACKs for baseline changes).
- Implement a small `tools/baselines/regenerate.py` that accepts variant/step args and writes `.npz` files into `tests/baselines/data/` (idempotent and deterministic).
- Keep a `golden-hardware` note listing recommended hardware/os for reproducing baselines locally (for contributors who want exact reproduction).
- Add a slow/nightly benchmark job that compares current performance to recorded baselines and alerts on large regressions.

Quick next steps (when ready)
- If the team wants automation: add `ci-baseline-check.yml` gated behind a feature flag and iterate after a few PRs that exercise re-recording.
- If reproducibility issues arise: add a containerized generator and provide a `docker/` example image for maintainers.

This note is intentionally short — expand into individual proposal PRs when you want to act on any idea.
