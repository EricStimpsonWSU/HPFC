from __future__ import annotations

import importlib

import pytest


PACKAGE_SURFACES = {
    "PFC.Core": (
        "backend",
        "fft_utils",
        "fields",
        "payload",
        "state",
        "kernel_rules",
        "PFC2D_geometry",
        "PFC2D_model",
        "geometry_2D",
        "model_2D",
        "kernels",
        "gaussian_kernel_fft",
        "resolve_model_parameter",
    ),
    "PFC.stdPFC": ("sim_pfc_std", "build_model", "make_sim"),
    "PFC.sHPFC": ("sim_shpfc_std", "sim_shpfc_div_vpsi", "sim_shpfc_psigradmu", "make_sim"),
}


@pytest.mark.usefixtures("pfc_contract_namespace")
@pytest.mark.parametrize("package_name, expected_attributes", PACKAGE_SURFACES.items())
def test_public_pfc_package_contract(package_name: str, expected_attributes: tuple[str, ...]) -> None:
    package = importlib.import_module(package_name)

    assert package.__name__ == package_name
    for attribute_name in expected_attributes:
        assert hasattr(package, attribute_name)