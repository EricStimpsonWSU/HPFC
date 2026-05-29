from __future__ import annotations

import importlib


def test_stdpfc_entrypoint_exists_and_makes_sim(pfc_contract_namespace, simple_model, simple_geometry, psi0, force_numpy_backend):
    PFC_std = importlib.import_module("PFC.stdPFC")

    assert hasattr(PFC_std, "make_sim")
    assert callable(PFC_std.make_sim)

    sim = PFC_std.make_sim(psi0, model=simple_model, geometry=simple_geometry)
    assert hasattr(sim, "step")
    assert callable(sim.step)
    assert sim.psi.shape == psi0.shape


def test_shpfc_entrypoint_exists_and_makes_sim(pfc_contract_namespace, simple_model, simple_geometry, psi0, force_numpy_backend):
    PFC_sh = importlib.import_module("PFC.sHPFC")

    assert hasattr(PFC_sh, "make_sim")
    assert callable(PFC_sh.make_sim)

    sim = PFC_sh.make_sim(psi0, model=simple_model, geometry=simple_geometry)
    assert hasattr(sim, "step")
    assert callable(sim.step)
    assert hasattr(sim, "std_step")
    assert callable(sim.std_step)
    assert sim.psi.shape == psi0.shape
