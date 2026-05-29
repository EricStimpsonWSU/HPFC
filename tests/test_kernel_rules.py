from __future__ import annotations

import pytest

from PFC.Core.kernel_rules import KernelRules
from tests.helpers import assert_allclose


def test_kernel_rules_build_expected_fields(simple_model, simple_geometry):
    kernel_set = KernelRules(model=simple_model, geometry=simple_geometry)

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


def test_kernel_rules_match_legacy_shim(simple_model, simple_geometry):
    kernel_set = KernelRules(model=simple_model, geometry=simple_geometry)
    legacy_kernel_set = KernelRules(model=simple_model, geometry=simple_geometry)

    assert_allclose(kernel_set.lin_mu_kernel, legacy_kernel_set.lin_mu_kernel)
    assert_allclose(kernel_set.lin_f_kernel, legacy_kernel_set.lin_f_kernel)
    assert_allclose(kernel_set.lin_v_kernel, legacy_kernel_set.lin_v_kernel)
    assert_allclose(kernel_set.lin_psi_exp, legacy_kernel_set.lin_psi_exp)
    assert_allclose(kernel_set.nonlin_psi_exp, legacy_kernel_set.nonlin_psi_exp)