import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]


def _read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf8")


def test_stdpfc_has_step_and_calc_helpers():
    src = _read("PFC/stdPFC/sim_pfc_std.py")
    assert "def step(" in src, "expected `step` function in sim_pfc_std.py"
    assert "calc_mu" in src, "expected `calc_mu` helper in sim_pfc_std.py"
    assert "calc_f" in src, "expected `calc_f` helper in sim_pfc_std.py"


def test_shpfc_variants_expose_step_and_std_step():
    paths = [
        "PFC/sHPFC/sim_shpfc_std.py",
        "PFC/sHPFC/sim_shpfc_div_vpsi.py",
        "PFC/sHPFC/sim_shpfc_psigradmu.py",
    ]
    for p in paths:
        src = _read(p)
        assert "def step(" in src, f"expected `step` in {p}"
        assert "def std_step(" in src, f"expected `std_step` in {p}"


def test_shpfc_common_hydro_fields_present():
    for p in ["PFC/sHPFC/sim_shpfc_std.py", "PFC/sHPFC/sim_shpfc_div_vpsi.py"]:
        src = _read(p)
        assert "_calc_common_hydro_fields" in src, f"expected `_calc_common_hydro_fields` in {p}"


def test_core_steppers_no_stepper_classes():
    src = _read("PFC/Core/steppers.py")
    assert "class StdPFCTimestepper" not in src, "StdPFCTimestepper should be moved out of Core/steppers.py"
    assert "class SHPFCTimestepper" not in src, "SHPFCTimestepper should be moved out of Core/steppers.py"


def test_core_state_no_calc_mu_calc_f():
    src = _read("PFC/Core/state.py")
    assert "def calc_mu" not in src, "calc_mu should be moved out of Core/state.py"
    assert "def calc_f" not in src, "calc_f should be moved out of Core/state.py"
