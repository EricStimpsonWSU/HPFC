from __future__ import annotations

import importlib


def test_simplified_model_container_consumption(
    contract_model_kwargs, contract_geometry_kwargs, contract_psi0, force_numpy_backend
) -> None:
    module = importlib.import_module("HPFC.sim_pfc_std")

    model = module.build_model(**contract_model_kwargs)
    geometry = module.build_geometry(**contract_geometry_kwargs)
    state = module.make_initial_state(contract_psi0, model=model, geometry=geometry)
    sim = module.make_sim(contract_psi0, model=model, geometry=geometry)

    # The simplified model container must expose a `hydro` attribute
    assert hasattr(model, "hydro")

    # Consumer assembly should use the exact same model object
    assert state.model is model
    assert sim.model is model
