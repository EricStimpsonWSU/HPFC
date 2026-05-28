from __future__ import annotations

import numpy as np
import pytest

from PFC.Core.kernel_rules import (
    KernelRules,
    _to_spacing_tuple,
    _cell_volume,
    _normalize_kernel_hat_mean,
    gaussian_kernel_fft,
)
from tests.helpers import assert_allclose


def test_to_spacing_and_cell_volume():
    assert _to_spacing_tuple(1.5, 2) == (1.5, 1.5)
    assert _to_spacing_tuple((2.0, 3.0), 2) == (2.0, 3.0)
    assert _cell_volume(1.5) == pytest.approx(1.5 * 1.5)


def test_gaussian_kernel_fft_errors_and_shape(simple_geometry):
    k2 = simple_geometry.k2
    with pytest.raises(ValueError):
        gaussian_kernel_fft(k2, width=None)
    with pytest.raises(ValueError):
        gaussian_kernel_fft(k2, width=0.0)


def test_gaussian_kernel_fft_values(simple_geometry):
    k2 = simple_geometry.k2
    w = simple_geometry.w
    kernel_hat = gaussian_kernel_fft(k2, width=w)
    expected = np.exp(-0.5 * (w * w) * k2).astype(np.complex128)
    expected.flat[0] = 1.0 + 0.0j
    assert kernel_hat.dtype == np.complex128
    assert_allclose(kernel_hat, expected)
    assert kernel_hat.flat[0] == pytest.approx(1.0 + 0.0j)


def test_normalize_kernel_hat_mean():
    arr = np.array([[2.0, 4.0], [6.0, 8.0]], dtype=np.complex128)
    normalized = _normalize_kernel_hat_mean(arr.copy())
    # DC becomes 1 and other entries scaled accordingly
    assert normalized.flat[0] == pytest.approx(1.0 + 0.0j)
    assert_allclose(normalized, arr / 2.0)


def test_kernelrules_build_etd_matches_manual(simple_model, simple_geometry):
    kr = KernelRules(model=simple_model, geometry=simple_geometry)
    dt = simple_model.dt
    # lin_dpsi_exp_kernel should equal exp(Gamma * dt * lin_dpsi)
    expected_lin = np.exp(simple_model.Gamma * dt * kr.lin_dpsi)
    assert_allclose(kr.lin_dpsi_exp_kernel, expected_lin)
    # nonlin_dpsi_kernel matches manual handling of zeros
    manual = np.ones_like(kr.k2) * simple_model.Gamma * dt
    nonzero = kr.lin_dpsi != 0
    manual[nonzero] = (expected_lin[nonzero] - 1.0) / kr.lin_dpsi[nonzero]
    assert_allclose(kr.nonlin_dpsi_kernel, manual)
