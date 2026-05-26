# sHPFC migration note — running simulations after refactor


Summary of changes in this refactor

- The refactor split internal responsibilities into `KernelRules`, `SimulationState`, and `steppers` to improve testability and enable future performance work.
- High-level simulation construction and usage are unchanged: existing notebooks and scripts that construct `sHPFC.sHPFC(psi0=..., model=..., geometry=...)` and call `sim.Timestep_*()` should continue to work without modification.

