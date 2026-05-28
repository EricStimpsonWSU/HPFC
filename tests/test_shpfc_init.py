from __future__ import annotations

import numpy as np
import pytest

from PFC.Core import backend
from PFC.sHPFC.sim_shpfc_std import make_sim as make_shpfc_sim


def test_shpfc_converts_geometry_and_kernels_to_backend_arrays(simple_model, simple_geometry, psi0, force_numpy_backend):
    sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)
    backend_array_type = force_numpy_backend.xp.ndarray

    # K-space geometry arrays converted
    assert isinstance(sim.KX, backend_array_type)
    assert isinstance(sim.KY, backend_array_type)
    assert isinstance(sim.k2, backend_array_type)

    # kernel fields converted to backend arrays
    assert isinstance(sim.kernel_d_dx, backend_array_type)
    assert isinstance(sim.kernel_d_dy, backend_array_type)
    assert isinstance(sim.kernel_gaussian, backend_array_type)

    # kernels stored in sim.kernels should also be numpy arrays after conversion attempt
    assert isinstance(sim.kernels.lin_mu_kernel, np.ndarray)


def test_shpfc_aliases_are_views_of_internal_batches(simple_model, simple_geometry, psi0, force_numpy_backend):
    sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)

    # psi should share memory with the first slice of internal _psi_poly
    assert np.shares_memory(sim.psi, sim._psi_poly[0])

    # v_x/v_y should share memory with slices of _batch_v
    assert np.shares_memory(sim.v_x, sim._batch_v[0])
    assert np.shares_memory(sim.v_y, sim._batch_v[1])


def test_shpfc_rejects_incompatible_model_types(simple_geometry, psi0, force_numpy_backend):
    class BadModel:
        pass

    with pytest.raises(AttributeError):
        make_shpfc_sim(psi0, model=BadModel(), geometry=simple_geometry)
