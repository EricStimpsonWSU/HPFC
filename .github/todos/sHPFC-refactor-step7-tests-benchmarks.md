# sHPFC Refactor — Step 7: Update tests and run benchmarks

Purpose: ensure refactor slices preserve correctness and meet performance expectations.

Checklist
- [ ] Update tests to reference new modules (`state.py`, `steppers.py`, `kernel_rules.py`, etc).
- [ ] Run `pytest -q` to verify no regressions.
- [ ] Add `tools/benchmarks/run_benchmarks.py` to compare runtime for `stdPFC` and `sHPFC` on a small grid for N steps.
- [ ] Evaluate any performance regression; if >5% slow-down, investigate and revert the offending change.

Exit criteria
- Tests pass and any performance regressions are tracked and addressed.
