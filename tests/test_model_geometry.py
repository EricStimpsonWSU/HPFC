from __future__ import annotations

import numpy as np
import pytest

from PFC2D_geometry import geometry_2D, geometry_2D_CPU, geometry_1D, geometry_3D
from PFC2D_model import model_2D, model_2D_CPU, model_1D, model_3D
from tests.helpers import assert_allclose


def test_model_2d_stores_parameters_as_floats():
    model = model_2D(temp=-0.3, beta=1.2, Gamma=2, rho0=3, Gamma_s=4, dt=0.01)

    assert model.temp == pytest.approx(-0.3)
    assert model.beta == pytest.approx(1.2)
    assert model.Gamma == pytest.approx(2.0)
    assert model.rho0 == pytest.approx(3.0)
    assert model.Gamma_s == pytest.approx(4.0)
    assert model.dt == pytest.approx(0.01)


def test_model_2d_cpu_emits_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="model_2D_CPU is deprecated"):
        model = model_2D_CPU(temp=1, beta=2, Gamma=3, rho0=4, Gamma_s=5, dt=6)

    assert model.temp == pytest.approx(1.0)
    assert model.dt == pytest.approx(6.0)


@pytest.mark.parametrize(
    "model_cls, message",
    [
        (model_1D, "1D PFC models are not yet supported"),
        (model_3D, "3D PFC models are not yet supported"),
    ],
)
def test_unsupported_model_dims_raise_clear_errors(model_cls, message):
    with pytest.raises(NotImplementedError, match=message):
        model_cls()


def test_geometry_2d_constructs_expected_grid_and_frequency_space():
    geometry = geometry_2D(shape=(4, 3), Lx=8.0, Ly=6.0)

    assert geometry.dx == pytest.approx(2.0)
    assert geometry.dy == pytest.approx(2.0)
    assert_allclose(geometry.x, [0.0, 2.0, 4.0, 6.0])
    assert_allclose(geometry.y, [0.0, 2.0, 4.0])
    assert geometry.X.shape == (3, 4)
    assert geometry.Y.shape == (3, 4)
    assert geometry.KX.shape == (3, 4)
    assert geometry.KY.shape == (3, 4)
    assert geometry.k2.shape == (3, 4)
    assert_allclose(geometry.KX[0], 2 * np.pi * np.fft.fftfreq(4, d=geometry.dx))
    assert_allclose(geometry.KY[:, 0], 2 * np.pi * np.fft.fftfreq(3, d=geometry.dy))
    assert_allclose(geometry.k2, geometry.KX**2 + geometry.KY**2)


def test_geometry_2d_cpu_emits_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="geometry_2D_CPU is deprecated"):
        geometry = geometry_2D_CPU(shape=(2, 2), Lx=2.0, Ly=2.0)

    assert geometry.X.shape == (2, 2)


@pytest.mark.parametrize(
    "geometry_cls, message",
    [
        (geometry_1D, "1D geometry is not yet supported"),
        (geometry_3D, "3D geometry is not yet supported"),
    ],
)
def test_unsupported_geometry_dims_raise_clear_errors(geometry_cls, message):
    with pytest.raises(NotImplementedError, match=message):
        geometry_cls()
