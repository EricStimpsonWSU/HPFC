import pytest


def test_pfc_shpfc_imports():
    from PFC.sHPFC import make_sim

    assert callable(make_sim)
