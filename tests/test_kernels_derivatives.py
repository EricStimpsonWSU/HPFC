from __future__ import annotations

from math import comb, pi

import numpy as np
from numpy.polynomial.hermite_e import hermeval
import pytest

from PFC.Core.PFC2D_geometry import geometry_2D
from PFC.Core.PFC2D_model import model_2D
from PFC.Core.kernel_rules import KernelRules as kernels
from tests.helpers import assert_allclose


def _spectral_apply(field: np.ndarray, multiplier: np.ndarray) -> np.ndarray:
    return np.fft.ifftn(np.fft.fftn(field) * multiplier).real


def _trig_geometry() -> geometry_2D:
    return geometry_2D(shape=(32, 32), Lx=2 * pi, Ly=2 * pi)


def _gaussian_geometry() -> geometry_2D:
    return geometry_2D(shape=(128, 128), Lx=24.0, Ly=24.0)


def _gaussian_1d_derivative(x: np.ndarray, center: float, sigma: float, order: int) -> np.ndarray:
    u = (x - center) / sigma
    coeffs = [0.0] * order + [1.0]
    return ((-1.0) ** order) * hermeval(u, coeffs) * np.exp(-0.5 * u**2) / (sigma**order)


def _separable_gaussian_derivative(
    geometry: geometry_2D,
    *,
    dx_order: int,
    dy_order: int,
    sigma: float,
) -> np.ndarray:
    gx = _gaussian_1d_derivative(geometry.x, geometry.Lx / 2.0, sigma, dx_order)
    gy = _gaussian_1d_derivative(geometry.y, geometry.Ly / 2.0, sigma, dy_order)
    return np.outer(gy, gx)


def _gaussian_laplacian_power(geometry: geometry_2D, power: int, sigma: float) -> np.ndarray:
    result = np.zeros(geometry.shape, dtype=np.float64)
    for k in range(power + 1):
        coeff = float(comb(power, k))
        gx = _gaussian_1d_derivative(geometry.x, geometry.Lx / 2.0, sigma, 2 * k)
        gy = _gaussian_1d_derivative(geometry.y, geometry.Ly / 2.0, sigma, 2 * (power - k))
        result += coeff * np.outer(gy, gx)
    return result


@pytest.mark.parametrize(
    ("operator_name", "field_builder", "expected_builder", "rtol"),
    [
        (
            "d_dx",
            lambda geom: np.sin(2.0 * geom.X) * np.cos(3.0 * geom.Y),
            lambda geom: 2.0 * np.cos(2.0 * geom.X) * np.cos(3.0 * geom.Y),
            1e-10,
        ),
        (
            "d_dy",
            lambda geom: np.sin(2.0 * geom.X) * np.cos(3.0 * geom.Y),
            lambda geom: -3.0 * np.sin(2.0 * geom.X) * np.sin(3.0 * geom.Y),
            1e-10,
        ),
        (
            "d2_dlap",
            lambda geom: np.sin(2.0 * geom.X) * np.cos(3.0 * geom.Y),
            lambda geom: -(2.0**2 + 3.0**2) * np.sin(2.0 * geom.X) * np.cos(3.0 * geom.Y),
            1e-10,
        ),
        (
            "d4_dlap2",
            lambda geom: np.sin(2.0 * geom.X) * np.cos(3.0 * geom.Y),
            lambda geom: (2.0**2 + 3.0**2) ** 2 * np.sin(2.0 * geom.X) * np.cos(3.0 * geom.Y),
            1e-10,
        ),
        (
            "d6_dlap3",
            lambda geom: np.sin(2.0 * geom.X) * np.cos(3.0 * geom.Y),
            lambda geom: -(2.0**2 + 3.0**2) ** 3 * np.sin(2.0 * geom.X) * np.cos(3.0 * geom.Y),
            1e-10,
        ),
    ],
)
def test_derivative_kernels_match_trigonometric_oracles(operator_name, field_builder, expected_builder, rtol):
    geometry = _trig_geometry()
    kernel_set = kernels(model=model_2D(temp=-0.25, beta=1.5, Gamma=1.0, rho0=1.0, Gamma_s=0.75, dt=0.05), geometry=geometry)
    field = field_builder(geometry)
    expected = expected_builder(geometry)
    operator = getattr(kernel_set, operator_name)

    actual = _spectral_apply(field, operator)

    assert_allclose(actual, expected, rtol=rtol, atol=1e-8)


@pytest.mark.parametrize(
    ("operator_name", "expected_builder", "rtol"),
    [
        (
            "d_dx",
            lambda geom: _separable_gaussian_derivative(geom, dx_order=1, dy_order=0, sigma=1.5),
            1e-4,
        ),
        (
            "d_dy",
            lambda geom: _separable_gaussian_derivative(geom, dx_order=0, dy_order=1, sigma=1.5),
            1e-4,
        ),
        (
            "d2_dlap",
            lambda geom: _gaussian_laplacian_power(geom, 1, sigma=1.5),
            5e-4,
        ),
        (
            "d4_dlap2",
            lambda geom: _gaussian_laplacian_power(geom, 2, sigma=1.5),
            1e-3,
        ),
        (
            "d6_dlap3",
            lambda geom: _gaussian_laplacian_power(geom, 3, sigma=1.5),
            2e-3,
        ),
    ],
)
def test_derivative_kernels_match_gaussian_oracles(operator_name, expected_builder, rtol):
    geometry = _gaussian_geometry()
    kernel_set = kernels(model=model_2D(temp=-0.25, beta=1.5, Gamma=1.0, rho0=1.0, Gamma_s=0.75, dt=0.05), geometry=geometry)
    sigma = 1.5
    field = np.exp(-0.5 * ((geometry.X - geometry.Lx / 2.0) ** 2 + (geometry.Y - geometry.Ly / 2.0) ** 2) / sigma**2)
    expected = expected_builder(geometry)
    operator = getattr(kernel_set, operator_name)

    actual = _spectral_apply(field, operator)

    assert_allclose(actual, expected, rtol=rtol, atol=5e-8)
