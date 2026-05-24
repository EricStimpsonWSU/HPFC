from __future__ import annotations

import numpy as np
import pytest


def test_calc_poly_psi_updates_powers_and_fft(simple_model, simple_geometry, psi0, force_numpy_backend):
    from sHPFC import sHPFC

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    sim.calc_poly_psi()

    # check powers
    assert np.allclose(sim._payload_mgr.to_numpy(sim.psi2), psi0**2)
    assert np.allclose(sim._payload_mgr.to_numpy(sim.psi3), psi0**3)
    assert np.allclose(sim._payload_mgr.to_numpy(sim.psi4), psi0**4)

    # check FFT of psi stored in _psi_hat_poly[0]
    psi_hat_np = np.fft.fftn(psi0)
    assert np.allclose(sim._payload_mgr.to_numpy(sim._psi_hat_poly[0]), psi_hat_np)


def test_calc_mu_and_calc_f_small_field(simple_model, simple_geometry, psi0, force_numpy_backend):
    from sHPFC import sHPFC

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    # ensure psi_hat is current
    sim.psi_hat[...] = sim._payload_mgr.fftn(sim.psi)
    sim.calc_poly_psi()

    sim.calc_mu(psi_hat_is_current=True)
    lin_mu_hat = sim.kernels.lin_mu_kernel * sim.psi_hat
    lin_mu = sim._payload_mgr.real(sim._payload_mgr.ifftn(lin_mu_hat))
    expected_mu = sim._payload_mgr.to_numpy(lin_mu) + sim._payload_mgr.to_numpy(sim.psi3)
    assert np.allclose(sim._payload_mgr.to_numpy(sim.mu), expected_mu)

    sim.calc_f(psi_hat_is_current=True)
    lin_f_hat = sim.kernels.lin_f_kernel * sim.psi_hat
    lin_f = sim._payload_mgr.real(sim._payload_mgr.ifftn(lin_f_hat))
    expected_f = sim._payload_mgr.to_numpy(lin_f) * sim._payload_mgr.to_numpy(sim.psi) + 0.5 * (sim.model.beta + sim.model.temp) * sim._payload_mgr.to_numpy(sim.psi2) + 0.25 * sim._payload_mgr.to_numpy(sim.psi4)
    assert np.allclose(sim._payload_mgr.to_numpy(sim.f), expected_f)


def test_calc_StructureTensor_returns_smoothed_components(simple_model, simple_geometry, psi0, force_numpy_backend):
    from sHPFC import sHPFC

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    # prepare psi_hat
    sim.psi_hat[...] = sim._payload_mgr.fftn(sim.psi)
    sim.calc_poly_psi()
    sim.calc_StructureTensor(psi_xy_is_current=True)

    assert sim.S_xx.shape == simple_geometry.shape
    assert sim.S_yy.shape == simple_geometry.shape
    assert sim.S_xy.shape == simple_geometry.shape


def test_Timestep_stdPFC_advances_time_and_updates_psi(simple_model, simple_geometry, psi0, force_numpy_backend):
    from sHPFC import sHPFC

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    t0 = sim.t
    psi_before = sim._payload_mgr.to_numpy(sim.psi).copy()
    sim.Timestep_stdPFC()
    assert sim.t == pytest.approx(t0 + sim.model.dt)
    psi_after = sim._payload_mgr.to_numpy(sim.psi)
    assert psi_after.shape == psi_before.shape
    assert not np.allclose(psi_before, psi_after)
