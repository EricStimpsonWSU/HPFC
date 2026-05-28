from __future__ import annotations

import pytest


def test_psi_hat_00_preserved(simple_model, simple_geometry, psi0, force_numpy_backend):
    from HPFC.sim_shpfc_std import make_sim as make_shpfc_sim

    sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)

    expected = psi0.mean() * psi0.size
    assert sim.psi_hat_00 == pytest.approx(expected)
