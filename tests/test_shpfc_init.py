from __future__ import annotations

import numpy as np
import pytest

import backend
from sHPFC import sHPFC


def test_shpfc_converts_geometry_and_kernels_to_backend_arrays(simple_model, simple_geometry, psi0, force_numpy_backend):
    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    # K-space geometry arrays converted
    assert isinstance(sim.KX, np.ndarray)
    assert isinstance(sim.KY, np.ndarray)
    assert isinstance(sim.k2, np.ndarray)

    # kernel fields converted to backend arrays
    assert isinstance(sim.kernel_d_dx, np.ndarray)
    assert isinstance(sim.kernel_d_dy, np.ndarray)
    assert isinstance(sim.kernel_gaussian, np.ndarray)

    # kernels stored in sim.kernels should also be numpy arrays after conversion attempt
    assert isinstance(sim.kernels.lin_mu_kernel, np.ndarray)


def test_shpfc_aliases_are_views_of_internal_batches(simple_model, simple_geometry, psi0, force_numpy_backend):
    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    # psi should share memory with the first slice of internal _psi_poly
    assert np.shares_memory(sim.psi, sim._psi_poly[0])

    # v_x/v_y should share memory with slices of _batch_v
    assert np.shares_memory(sim.v_x, sim._batch_v[0])
    assert np.shares_memory(sim.v_y, sim._batch_v[1])


def test_shpfc_rejects_incompatible_model_types(simple_geometry, psi0, force_numpy_backend):
    class BadModel:
        pass

    with pytest.raises(AttributeError):
        sHPFC(psi0, model=BadModel(), geometry=simple_geometry)
