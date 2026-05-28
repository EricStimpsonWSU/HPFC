from __future__ import annotations

import importlib


def test_simplified_model_container_consumption_for_sim_shpfc_psigradmu(
    contract_model_kwargs, contract_geometry_kwargs, contract_psi0, force_numpy_backend
) -> None:
    module = importlib.import_module("PFC.sHPFC.sim_shpfc_psigradmu")

    model = module.build_model(**contract_model_kwargs)
    geometry = module.build_geometry(**contract_geometry_kwargs)
    state = module.make_initial_state(contract_psi0, model=model, geometry=geometry)
    sim = module.make_sim(contract_psi0, model=model, geometry=geometry)

    assert hasattr(model, "hydro")
    assert state.model is model
    assert sim.model is model
