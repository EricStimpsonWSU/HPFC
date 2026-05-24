from __future__ import annotations

import pytest


def test_psi_hat_00_preserved(simple_model, simple_geometry, psi0, force_numpy_backend):
    from sHPFC import sHPFC

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    expected = psi0.mean() * psi0.size
    assert sim.psi_hat_00 == pytest.approx(expected)
