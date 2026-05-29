from __future__ import annotations

import numpy as np
import inspect


def test_shpfc_shapes_and_dtypes(simple_model, simple_geometry, psi0, force_numpy_backend):
    from PFC.sHPFC.sim_shpfc_std import make_sim as make_shpfc_sim

    sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)

    # shapes
    assert sim.psi.shape == simple_geometry.shape
    assert sim.k2.shape == simple_geometry.shape
    assert sim.KX.shape == simple_geometry.shape

    # dtypes
    assert sim.psi.dtype == np.float64
    assert sim.psi_hat.dtype == np.complex128
    assert sim.k2.dtype == np.float64


def test_shpfc_initial_values_and_aliasing(simple_model, simple_geometry, psi0, force_numpy_backend):
    from PFC.sHPFC.sim_shpfc_std import make_sim as make_shpfc_sim

    sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)

    # psi was initialized from psi0
    assert np.allclose(sim.psi, psi0)

    # psi_hat should be the FFT of psi (zero since psi is small but check type)
    assert sim.psi_hat.shape == psi0.shape


def test_shpfc_methods_exist(simple_model, simple_geometry, psi0, force_numpy_backend):
    from PFC.stdPFC.sim_pfc_std import make_sim as make_std_sim
    from PFC.sHPFC.sim_shpfc_std import make_sim as make_shpfc_sim

    std_sim = make_std_sim(psi0, model=simple_model, geometry=simple_geometry)
    shpfc_sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)

    assert hasattr(std_sim, "step")
    assert inspect.isroutine(getattr(std_sim, "step"))

    assert hasattr(shpfc_sim, "step")
    assert inspect.isroutine(getattr(shpfc_sim, "step"))
    assert hasattr(shpfc_sim, "std_step")
    assert inspect.isroutine(getattr(shpfc_sim, "std_step"))

    # core calculation routines live on the state and should be available
    assert hasattr(std_sim, "calc_mu")
    assert inspect.isroutine(getattr(std_sim, "calc_mu"))
    assert hasattr(std_sim, "calc_f")
    assert inspect.isroutine(getattr(std_sim, "calc_f"))
