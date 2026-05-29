import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]


def _read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf8")


def test_stdpfc_has_step_and_calc_helpers():
    src = _read("PFC/stdPFC/sim_pfc_std.py")
    assert "def step(" in src, "expected `step` function in sim_pfc_std.py"
    assert "calc_mu" in src, "expected `calc_mu` helper in sim_pfc_std.py"
    assert "calc_f" in src, "expected `calc_f` helper in sim_pfc_std.py"


def test_shpfc_std_exposes_step_and_std_step():
    src = _read("PFC/sHPFC/sim_shpfc_std.py")
    assert "def step(" in src, "expected `step` in PFC/sHPFC/sim_shpfc_std.py"
    assert "def std_step(" in src, "expected `std_step` in PFC/sHPFC/sim_shpfc_std.py"


def test_shpfc_div_vpsi_exposes_step_and_std_step():
    src = _read("PFC/sHPFC/sim_shpfc_div_vpsi.py")
    assert "def step(" in src, "expected `step` in PFC/sHPFC/sim_shpfc_div_vpsi.py"
    assert "def std_step(" in src, "expected `std_step` in PFC/sHPFC/sim_shpfc_div_vpsi.py"


def test_shpfc_psigradmu_exposes_step_and_std_step():
    src = _read("PFC/sHPFC/sim_shpfc_psigradmu.py")
    assert "def step(" in src, "expected `step` in PFC/sHPFC/sim_shpfc_psigradmu.py"
    assert "def std_step(" in src, "expected `std_step` in PFC/sHPFC/sim_shpfc_psigradmu.py"


def test_shpfc_std_common_hydro_fields_present():
    src = _read("PFC/sHPFC/sim_shpfc_std.py")
    assert "_calc_common_hydro_fields" in src, "expected `_calc_common_hydro_fields` in PFC/sHPFC/sim_shpfc_std.py"


def test_shpfc_div_vpsi_common_hydro_fields_present():
    src = _read("PFC/sHPFC/sim_shpfc_div_vpsi.py")
    assert "_calc_common_hydro_fields" in src, "expected `_calc_common_hydro_fields` in PFC/sHPFC/sim_shpfc_div_vpsi.py"


def test_core_steppers_no_stepper_classes():
    assert not (ROOT / "PFC/Core/steppers.py").exists(), "PFC/Core/steppers.py should be deleted"


def test_core_state_no_calc_mu_calc_f():
    src = _read("PFC/Core/state.py")
    assert "def calc_mu" not in src, "calc_mu should be moved out of Core/state.py"
    assert "def calc_f" not in src, "calc_f should be moved out of Core/state.py"
