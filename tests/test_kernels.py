from __future__ import annotations

import numpy as np
import pytest

from PFC.Core.PFC2D_kernels import _normalize_kernel_hat_mean, gaussian_kernel_fft, kernels
from tests.helpers import assert_allclose


def test_gaussian_kernel_fft_validates_width():
    with pytest.raises(ValueError, match="provide width"):
        gaussian_kernel_fft(np.ones((2, 2)))

    with pytest.raises(ValueError, match="width must be positive"):
        gaussian_kernel_fft(np.ones((2, 2)), width=0)


def test_gaussian_kernel_fft_normalizes_dc_mode():
    kernel_hat = gaussian_kernel_fft(np.array([[0.0, 1.0], [2.0, 3.0]]), width=1.0)

    assert kernel_hat.dtype == np.complex128
    assert kernel_hat.flat[0] == pytest.approx(1.0 + 0.0j)


def test_normalize_kernel_hat_mean_sets_dc_mode_to_one():
    kernel_hat = np.array([[2.0 + 0.0j, 0.5 + 0.0j], [0.25 + 0.0j, 0.125 + 0.0j]])

    normalized = _normalize_kernel_hat_mean(kernel_hat)

    assert normalized.flat[0] == pytest.approx(1.0 + 0.0j)
    assert_allclose(normalized, kernel_hat / kernel_hat.flat[0])


def test_kernels_build_expected_fields(simple_model, simple_geometry):
    kernel_set = kernels(model=simple_model, geometry=simple_geometry)

    expected_shape = simple_geometry.k2.shape
    assert_allclose(kernel_set.d_dx, 1j * simple_geometry.KX)
    assert_allclose(kernel_set.d_dy, 1j * simple_geometry.KY)
    assert_allclose(kernel_set.d2_dlap, -simple_geometry.k2)
    assert_allclose(kernel_set.d4_dlap2, simple_geometry.k2**2)
    assert_allclose(kernel_set.d6_dlap3, -(simple_geometry.k2**3))
    assert kernel_set.d_dx.shape == expected_shape
    assert kernel_set.d_dy.shape == expected_shape
    assert kernel_set.d2_dlap.shape == expected_shape
    assert kernel_set.d4_dlap2.shape == expected_shape
    assert kernel_set.d6_dlap3.shape == expected_shape
    assert kernel_set.lin_mu_kernel.shape == expected_shape
    assert kernel_set.lin_f_kernel.shape == expected_shape
    assert kernel_set.lin_v_kernel.shape == expected_shape
    assert kernel_set.lin_psi_exp.shape == expected_shape
    assert kernel_set.nonlin_psi_exp.shape == expected_shape
    assert kernel_set.lin_v_exp.shape == expected_shape
    assert kernel_set.nonlin_v_exp.shape == expected_shape
    assert_allclose(kernel_set.lin_mu_kernel, (simple_model.temp + simple_model.beta) + 2 * simple_model.beta * kernel_set.d2_dlap + simple_model.beta * kernel_set.d4_dlap2)
    assert_allclose(kernel_set.lin_f_kernel, 0.5 * simple_model.beta * (kernel_set.d4_dlap2 + 2 * kernel_set.d2_dlap))
    assert_allclose(kernel_set.lin_v_kernel, (simple_model.Gamma_s / simple_model.rho0) * kernel_set.d2_dlap)
    assert kernel_set.gaussian_kernel.flat[0] == pytest.approx(1.0 + 0.0j)
