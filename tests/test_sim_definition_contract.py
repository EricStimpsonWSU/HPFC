from __future__ import annotations

import importlib

import pytest


VARIANT_SPECS = (
    ("HPFC.sim_pfc_std", "Timestep_stdPFC", ()),
    ("HPFC.sim_shpfc_std", "Timestep_sHPFC", ("v_x", "v_y")),
    ("HPFC.sim_shpfc_div_vpsi", "Timestep_sHPFC_div_vpsi", ("v_x", "v_y", "div_vpsi_hat")),
    ("HPFC.sim_shpfc_psigradmu", "Timestep_sHPFC_psigradmu", ("v_x", "v_y", "v_dot_grad_psi_hat")),
)


@pytest.mark.parametrize("module_path,step_method,expected_fields", VARIANT_SPECS)
def test_canonical_sim_module_import_paths(
    module_path: str,
    step_method: str,
    expected_fields: tuple[str, ...],
) -> None:
    module = importlib.import_module(module_path)

    assert module.__name__ == module_path
    assert hasattr(module, "build_model")
    assert hasattr(module, "build_geometry")
    assert hasattr(module, "make_initial_state")
    assert hasattr(module, "make_sim")
    assert hasattr(module, "build_lin_kernels")


@pytest.mark.parametrize("module_path,step_method,expected_fields", VARIANT_SPECS)
def test_consumer_assembly_contract_for_canonical_variants(
    module_path: str,
    step_method: str,
    expected_fields: tuple[str, ...],
    contract_model_kwargs,
    contract_geometry_kwargs,
    contract_psi0,
    force_numpy_backend,
) -> None:
    module = importlib.import_module(module_path)

    model = module.build_model(**contract_model_kwargs)
    geometry = module.build_geometry(**contract_geometry_kwargs)
    state = module.make_initial_state(contract_psi0, model=model, geometry=geometry)
    sim = module.make_sim(contract_psi0, model=model, geometry=geometry)

    assert state.model is model
    assert state.geometry is geometry
    assert state.psi.shape == contract_psi0.shape
    assert state.psi_hat.shape == contract_psi0.shape
    assert state.psi_hat_00 == pytest.approx(contract_psi0.mean() * contract_psi0.size)

    assert sim.model is model
    assert sim.geometry is geometry
    assert sim.psi.shape == contract_psi0.shape
    assert hasattr(sim, step_method)
    assert callable(getattr(sim, step_method))

    if module_path == "HPFC.sim_pfc_std":
        assert not hasattr(sim, "Timestep_sHPFC")
        assert not hasattr(sim, "Timestep_sHPFC_div_vpsi")
        assert not hasattr(sim, "Timestep_sHPFC_psigradmu")
        assert not hasattr(sim, "v_x")
        assert not hasattr(sim, "v_y")
        assert not hasattr(sim, "div_vpsi_hat")
        assert not hasattr(sim, "v_dot_grad_psi_hat")

    getattr(sim, step_method)()

    assert sim.t == pytest.approx(contract_model_kwargs["dt"])
    assert sim.psi.shape == contract_psi0.shape
    assert sim.psi_hat.shape == contract_psi0.shape
    assert sim.psi_hat[0, 0] == pytest.approx(sim.psi_hat_00)

    for field_name in expected_fields:
        field_value = getattr(sim, field_name)
        assert field_value.shape == contract_psi0.shape
