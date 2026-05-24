from __future__ import annotations

import numpy as np
import pytest

from PFC2D_kernels import gaussian_kernel_fft, kernels


def test_gaussian_kernel_fft_validates_width():
    with pytest.raises(ValueError, match="provide width"):
        gaussian_kernel_fft(np.ones((2, 2)))

    with pytest.raises(ValueError, match="width must be positive"):
        gaussian_kernel_fft(np.ones((2, 2)), width=0)


def test_gaussian_kernel_fft_normalizes_dc_mode():
    kernel_hat = gaussian_kernel_fft(np.array([[0.0, 1.0], [2.0, 3.0]]), width=1.0)

    assert kernel_hat.dtype == np.complex128
    assert kernel_hat.flat[0] == pytest.approx(1.0 + 0.0j)


def test_kernels_build_expected_fields(simple_model, simple_geometry):
    kernel_set = kernels(model=simple_model, geometry=simple_geometry)

    expected_shape = simple_geometry.k2.shape
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
    assert kernel_set.gaussian_kernel.flat[0] == pytest.approx(1.0 + 0.0j)
