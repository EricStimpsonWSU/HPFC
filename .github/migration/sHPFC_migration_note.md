# sHPFC migration note — canonical sim-module workflow

The refactor split internal responsibilities into `KernelRules`, `SimulationState`, and `steppers`, and the long-term consumer surface is now the per-simulation modules under `HPFC.sim_*`.

Old entry points map to the new module surface like this:

- `sHPFC.sHPFC(...)` -> `HPFC.sim_shpfc_std.make_sim(...)`
- `sHPFC.Timestep_stdPFC()` -> `HPFC.sim_pfc_std.make_sim(...).Timestep_stdPFC()`
- `sHPFC.Timestep_sHPFC()` -> `HPFC.sim_shpfc_std.make_sim(...).Timestep_sHPFC()`
- `sHPFC.Timestep_sHPFC_div_vpsi()` -> `HPFC.sim_shpfc_div_vpsi.make_sim(...).Timestep_sHPFC_div_vpsi()`
- `sHPFC.Timestep_sHPFC_psigradmu()` -> `HPFC.sim_shpfc_psigradmu.make_sim(...).Timestep_sHPFC_psigradmu()`

The consumer workflow is:
`build_model` -> `build_geometry` -> `make_initial_state` -> `make_sim` -> timestep method.

If a consumer still relies on compatibility views inside the sim modules, treat them as transitional and prefer the explicit `HPFC.sim_*` imports above.

