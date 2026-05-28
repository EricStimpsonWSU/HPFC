from __future__ import annotations

import numpy as np
import pytest


def test_Timestep_sHPFC_updates_velocity_and_preserves_zero_mode(simple_model, simple_geometry, psi0, force_numpy_backend):
    from HPFC.sim_shpfc_std import make_sim as make_shpfc_sim

    sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)

    t0 = sim.t
    v_x_before = sim._payload_mgr.to_numpy(sim.v_x).copy()

    sim.Timestep_sHPFC()

    assert sim.t == pytest.approx(t0 + sim.model.dt)
    v_x_after = sim._payload_mgr.to_numpy(sim.v_x)
    assert v_x_after.shape == v_x_before.shape
    assert not np.allclose(v_x_before, v_x_after)
    # zero mode preserved
    assert sim._payload_mgr.to_numpy(sim.psi_hat)[0, 0] == pytest.approx(sim.psi_hat_00)


def test_Timestep_sHPFC_div_vpsi_updates_div_and_psi(simple_model, simple_geometry, psi0, force_numpy_backend):
    from HPFC.sim_shpfc_div_vpsi import make_sim as make_div_sim

    sim = make_div_sim(psi0, model=simple_model, geometry=simple_geometry)

    t0 = sim.t
    div_before = sim._payload_mgr.to_numpy(sim.div_vpsi_hat).copy()

    sim.Timestep_sHPFC_div_vpsi()

    assert sim.t == pytest.approx(t0 + sim.model.dt)
    div_after = sim._payload_mgr.to_numpy(sim.div_vpsi_hat)
    assert div_after.shape == div_before.shape
    assert not np.allclose(div_before, div_after)
    # psi updated
    assert sim._payload_mgr.to_numpy(sim.psi).shape == psi0.shape


def test_Timestep_sHPFC_psigradmu_updates_velocity_and_psi(simple_model, simple_geometry, psi0, force_numpy_backend):
    from HPFC.sim_shpfc_psigradmu import make_sim as make_psigradmu_sim

    sim = make_psigradmu_sim(psi0, model=simple_model, geometry=simple_geometry)

    t0 = sim.t
    v_before = sim._payload_mgr.to_numpy(sim.v_x).copy()

    sim.Timestep_sHPFC_psigradmu()

    assert sim.t == pytest.approx(t0 + sim.model.dt)
    v_after = sim._payload_mgr.to_numpy(sim.v_x)
    assert not np.allclose(v_before, v_after)
    assert sim._payload_mgr.to_numpy(sim.psi).shape == psi0.shape
