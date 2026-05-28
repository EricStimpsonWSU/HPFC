import pytest


def test_hpfc_backwards_compat_imports():
    from PFC.sHPFC.sim_shpfc_std import make_sim as make_shpfc_sim
    from PFC.stdPFC.sim_pfc_std import build_model as build_std_model

    assert callable(make_shpfc_sim)
    assert callable(build_std_model)
