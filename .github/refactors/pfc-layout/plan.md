# PFC Layout Split Plan

Goal: rename the top-level `HPFC` package to `PFC`, split shared code into `PFC/Core`, split model-specific code into `PFC/stdPFC` and `PFC/sHPFC`, and move model documentation next to the model implementation it describes. This is a structural refactor only: numerical behavior, deterministic fixtures, and backend selection must remain unchanged.

Scope
- In scope: package rename, folder split, import-path migration, model-doc relocation, and temporary compatibility shims if needed during the transition.
- Out of scope: physics changes, kernel algorithm changes, timestep behavior changes, and edits to design/spec markdown unless the user explicitly asks later.
- Preserve existing baseline data and small deterministic fixtures unless a step explicitly requires a path update.

Step order
1. Lock the import contract and transition strategy.
2. Add narrow import-contract coverage before moving code.
3. Split shared infrastructure into `PFC/Core`.
4. Split model-specific implementation into `PFC/stdPFC` and `PFC/sHPFC`.
5. Move model documentation into the matching model folders.
6. Clean up compatibility and update consumers.

Exit criteria
- The new `PFC` layout is the canonical import surface.
- The standard and hydrodynamic model modules live under their model folders.
- Documentation follows the model-specific implementation.
- Focused tests and baseline checks pass after each meaningful move.

Needed step files
- `todos/step-0-import-contract.md`
- `todos/step-1-core-split.md`
- `todos/step-2-model-split.md`
- `todos/step-3-docs-migration.md`
- `todos/step-4-compat-and-cleanup.md`
