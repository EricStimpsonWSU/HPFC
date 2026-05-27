from __future__ import annotations

import numpy as np

from HPFC.kernel_rules import KernelRules
from tests.helpers import assert_allclose


def test_buildLinear_and_buildNonlinear_ETD_manual():
    dt = 0.1
    lin = np.array([0.0, -1.0, 2.0], dtype=np.float64)
    # linear ETD
    lin_exp = KernelRules.buildLinearETD(dt, lin)
    assert_allclose(lin_exp, np.exp(lin * dt))
    # nonlinear ETD
    nonlin = KernelRules.buildNonlinearETD(dt, lin)
    expected = np.ones_like(lin) * dt
    nz = lin != 0
    expected[nz] = (np.exp(lin[nz] * dt) - 1.0) / lin[nz]
    assert_allclose(nonlin, expected)


def test_lin_nonlin_v_exp_consistency(simple_model, simple_geometry):
    kr = KernelRules(model=simple_model, geometry=simple_geometry)
    # lin_v_exp should be exp(lin_v_kernel * dt)
    expected_lin_v = np.exp(kr.lin_v_kernel * simple_model.dt)
    assert_allclose(kr.lin_v_exp, expected_lin_v)
    # nonlin_v_exp follows the same pattern as buildNonlinearETD
    expected_nonlin_v = KernelRules.buildNonlinearETD(simple_model.dt, kr.lin_v_kernel)
    assert_allclose(kr.nonlin_v_exp, expected_nonlin_v)
