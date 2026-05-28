import pytest


@pytest.mark.usefixtures("pfc_contract_namespace")
def test_pfc_core_imports():
    from PFC.Core import (
        geometry_2D,
        model_2D,
        kernels,
        gaussian_kernel_fft,
        resolve_model_parameter,
    )

    assert geometry_2D is not None
    assert model_2D is not None
    assert kernels is not None
    assert gaussian_kernel_fft is not None
    assert resolve_model_parameter is not None
