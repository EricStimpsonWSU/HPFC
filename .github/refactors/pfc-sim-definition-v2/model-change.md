Mapping (steppers (mutating), state (non-mutating) → sim files)

- `PFC/Core/steppers.py: StdPFCTimestepper.step` -->
  - `PFC/stdPFC/sim_pfc_std.py`
  - `PFC/sHPFC/sim_shpfc_std.py`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py`
  - `PFC/sHPFC/sim_shpfc_psigradmu.py`
  - `PFC/HPFC/sim_hpfc_std.py`

- `PFC/Core/steppers.py: SHPFCTimestepper._calc_common_hydro_fields` -->
  - `PFC/sHPFC/sim_shpfc_std.py`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py`

- `PFC/Core/steppers.py: SHPFCTimestepper.step` -->
  - `PFC/sHPFC/sim_shpfc_std.py`

- `PFC/Core/steppers.py: SHPFCTimestepper.step_div_vpsi` -->
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py`

- `PFC/Core/steppers.py: SHPFCTimestepper.step_psigradmu` -->
  - `PFC/sHPFC/sim_shpfc_psigradmu.py`

- `PFC/Core/state.py: SimultationState.calc_poly_psi`
  - `PFC/Core/state.py`

- `PFC/Core/state.py: SimultationState.calc_mu`
  - `PFC/stdPFC/sim_pfc_std.py`
  - `PFC/sHPFC/sim_shpfc_std.py`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py`
  - `PFC/sHPFC/sim_shpfc_psigradmu.py`
  - `PFC/HPFC/sim_hpfc_std.py`

- `PFC/Core/state.py: SimultationState.calc_f`
  - `PFC/stdPFC/sim_pfc_std.py`
  - `PFC/sHPFC/sim_shpfc_std.py`
  - `PFC/sHPFC/sim_shpfc_div_vpsi.py`
  - `PFC/sHPFC/sim_shpfc_psigradmu.py`
  - `PFC/HPFC/sim_hpfc_std.py`