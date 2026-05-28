import pytest


def test_pfc_std_imports():
    from PFC.stdPFC import make_sim, build_model

    assert callable(make_sim)
    assert callable(build_model)
