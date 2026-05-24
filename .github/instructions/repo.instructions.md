---
description: "Repo-wide PFC workflow rules"
applyTo: "**"
---

Treat this repository as a refactor-in-progress for the 26140 PFC codebase.

Rules:
- Consider any design document, spec, experiment note, or planning markdown as source-of-truth unless the user explicitly asks to revise it.
- Do not edit design documents on your own initiative. If they appear to need updates, ask first or wait for explicit direction.
- Use test-first behavior by default: when changing behavior, add or update the narrowest relevant test before implementation, then validate the change.
- Keep edits local and minimal. Prefer the smallest code path that satisfies the request.
- Prefer frequent, small git commits once a coherent change is complete.

When working in this repo, favor concrete, behavior-scoped changes over broad refactors unless the user explicitly asks for a larger redesign.