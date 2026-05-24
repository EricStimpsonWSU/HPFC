from __future__ import annotations

import numpy as np
import pytest

import backend
from sHPFC import sHPFC
from tests.helpers import assert_allclose


def test_shpfc_initialization_builds_backend_arrays(simple_model, simple_geometry, psi0, force_numpy_backend):

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    assert sim.psi.shape == psi0.shape
    assert sim.psi_hat.shape == psi0.shape
    assert sim.mu.shape == psi0.shape
    assert sim.f.shape == psi0.shape
    assert sim.v_x.shape == psi0.shape
    assert sim.v_y.shape == psi0.shape
    assert_allclose(sim.psi_hat_00, psi0.mean() * psi0.size)


def test_std_pfc_timestep_advances_state(simple_model, simple_geometry, psi0, force_numpy_backend):

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)
    initial_t = sim.t
    initial_zero_mode = sim.psi_hat_00

    sim.Timestep_stdPFC()

    assert sim.t == pytest.approx(initial_t + simple_model.dt)
    assert sim.psi.shape == psi0.shape
    assert_allclose(sim.psi_hat[0, 0], initial_zero_mode)


def test_divergence_based_shpfc_timestep_runs(simple_model, simple_geometry, psi0, force_numpy_backend):

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    sim.Timestep_sHPFC_div_vpsi()

    assert sim.t == pytest.approx(simple_model.dt)
    assert sim.psi.shape == psi0.shape
    assert np.isfinite(sim.psi).all()
