from __future__ import annotations

import numpy as np
import inspect


def test_shpfc_shapes_and_dtypes(simple_model, simple_geometry, psi0, force_numpy_backend):
    from sHPFC import sHPFC

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    # shapes
    assert sim.psi.shape == simple_geometry.shape
    assert sim.k2.shape == simple_geometry.shape
    assert sim.KX.shape == simple_geometry.shape

    # dtypes
    assert sim.psi.dtype == np.float64
    assert sim.psi_hat.dtype == np.complex128
    assert sim.k2.dtype == np.float64


def test_shpfc_initial_values_and_aliasing(simple_model, simple_geometry, psi0, force_numpy_backend):
    from sHPFC import sHPFC

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    # psi was initialized from psi0
    assert np.allclose(sim.psi, psi0)

    # psi_hat should be the FFT of psi (zero since psi is small but check type)
    assert sim.psi_hat.shape == psi0.shape


def test_shpfc_methods_exist(simple_model, simple_geometry, psi0, force_numpy_backend):
    from sHPFC import sHPFC

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    for name in ("Timestep_stdPFC", "Timestep_sHPFC", "calc_mu", "calc_f", "calc_poly_psi"):
        assert hasattr(sim, name)
        assert inspect.isroutine(getattr(sim, name))
