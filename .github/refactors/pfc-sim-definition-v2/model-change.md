Mapping (steppers (mutating), state (non-mutating) → sim files)

- `PFC/Core/steppers.py: StdPFCTimestepper.step` -->
  - `PFC/stdPFC/sim_pfc_std.py` as `step`
  - `PFC/sHPFC/sim_shpfc_std.py` as `std_step`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py` as `std_step`
  - `PFC/sHPFC/sim_shpfc_psigradmu.py` as `std_step`

- `PFC/Core/steppers.py: SHPFCTimestepper._calc_common_hydro_fields` -->
  - `PFC/sHPFC/sim_shpfc_std.py` as `_calc_common_hydro_fields`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py` as `_calc_common_hydro_fields`

- `PFC/Core/steppers.py: SHPFCTimestepper.step` -->
  - `PFC/sHPFC/sim_shpfc_std.py` as `step`

- `PFC/Core/steppers.py: SHPFCTimestepper.step_div_vpsi` -->
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py` as `step`

- `PFC/Core/steppers.py: SHPFCTimestepper.step_psigradmu` -->
  - `PFC/sHPFC/sim_shpfc_psigradmu.py` as `step`

- `PFC/Core/state.py: SimultationState.calc_poly_psi`
  - `PFC/Core/state.py` [doesn't move]

- `PFC/Core/state.py: SimultationState.calc_mu`
  - `PFC/stdPFC/sim_pfc_std.py` as `calc_mu`
  - `PFC/sHPFC/sim_shpfc_std.py` as `calc_mu`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py` as `calc_mu`
  - `PFC/sHPFC/sim_shpfc_psigradmu.py` as `calc_mu`

- `PFC/Core/state.py: SimultationState.calc_f`
  - `PFC/stdPFC/sim_pfc_std.py` as `calc_f`
  - `PFC/sHPFC/sim_shpfc_std.py` as `calc_f`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py` as `calc_f`
  - `PFC/sHPFC/sim_shpfc_psigradmu.py` as `calc_f`
