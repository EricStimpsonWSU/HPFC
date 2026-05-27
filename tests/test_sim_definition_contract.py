from __future__ import annotations

import importlib

import pytest


VARIANT_SPECS = (
    ("HPFC.sim_pfc_std", "Timestep_stdPFC"),
    ("HPFC.sim_shpfc_std", "Timestep_sHPFC"),
    ("HPFC.sim_shpfc_div_vpsi", "Timestep_sHPFC_div_vpsi"),
    ("HPFC.sim_shpfc_psigradmu", "Timestep_sHPFC_psigradmu"),
)


@pytest.mark.parametrize("module_path,_", VARIANT_SPECS)
def test_canonical_sim_module_import_paths(module_path: str, _: str) -> None:
    module = importlib.import_module(module_path)

    assert module.__name__ == module_path
    assert hasattr(module, "build_model")
    assert hasattr(module, "build_geometry")
    assert hasattr(module, "make_initial_state")
    assert hasattr(module, "make_sim")


@pytest.mark.parametrize("module_path,step_method", VARIANT_SPECS)
def test_consumer_assembly_contract_for_canonical_variants(
    module_path: str,
    step_method: str,
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

    assert sim.model is model
    assert sim.geometry is geometry
    assert sim.psi.shape == contract_psi0.shape
    assert hasattr(sim, step_method)
    assert callable(getattr(sim, step_method))
