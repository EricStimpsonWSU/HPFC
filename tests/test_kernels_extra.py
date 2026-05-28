from __future__ import annotations

import numpy as np
import pytest

from PFC.Core.PFC2D_kernels import (
    _to_spacing_tuple,
    _cell_volume,
    _normalize_kernel_hat_mean,
    gaussian_kernel_fft,
)


def test_to_spacing_tuple_accepts_scalar_and_sequence():
    assert _to_spacing_tuple(1.0, 2) == (1.0, 1.0)
    assert _to_spacing_tuple([1, 2], 2) == (1.0, 2.0)


def test_to_spacing_tuple_rejects_wrong_length():
    with pytest.raises(ValueError, match="Expected 2 spacing values"):
        _to_spacing_tuple([1, 2, 3], 2)


def test_cell_volume_computes_product():
    assert _cell_volume([2.0, 3.0]) == pytest.approx(6.0)


def test_normalize_kernel_hat_mean_raises_on_zero_dc():
    kernel_hat = np.array([[0.0 + 0.0j, 1.0 + 0.0j]])
    with pytest.raises(ValueError, match="zero DC mode"):
        _normalize_kernel_hat_mean(kernel_hat)


def test_gaussian_kernel_fft_requires_non_scalar_k2():
    with pytest.raises(ValueError, match="k2 must have at least one dimension"):
        gaussian_kernel_fft(np.asarray(0.0), width=1.0)


def test_build_nonlinear_etd_behavior_from_kernels(simple_model, simple_geometry):
    from PFC.Core.PFC2D_kernels import kernels

    ks = kernels(model=simple_model, geometry=simple_geometry)

    lin = np.array([[0.0, 2.0], [3.0, 0.0]])
    dt = 0.1
    out = ks.buildNonlinearETD(dt, lin)

    # entries where lin==0 should equal dt
    assert out[0, 0] == pytest.approx(dt)
    assert out[1, 1] == pytest.approx(dt)

    # entries where lin!=0 should match (exp(lin*dt)-1)/lin
    expected = (np.exp(2.0 * dt) - 1.0) / 2.0
    assert out[0, 1] == pytest.approx(expected)
