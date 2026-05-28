from __future__ import annotations

import importlib
import sys
import types

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
    ),
    "PFC.stdPFC": ("sim_pfc_std",),
    "PFC.sHPFC": ("sim_shpfc_std", "sim_shpfc_div_vpsi", "sim_shpfc_psigradmu"),
}


def _install_legacy_pfc_namespace() -> None:
    pfc_package = types.ModuleType("PFC")
    pfc_package.__path__ = []

    core_package = types.ModuleType("PFC.Core")
    core_package.__path__ = []
    core_package.backend = importlib.import_module("HPFC.backend")
    core_package.fft_utils = importlib.import_module("HPFC.fft_utils")
    core_package.fields = importlib.import_module("HPFC.fields")
    core_package.payload = importlib.import_module("HPFC.payload")
    core_package.state = importlib.import_module("HPFC.state")
    core_package.kernel_rules = importlib.import_module("HPFC.kernel_rules")
    core_package.PFC2D_geometry = importlib.import_module("HPFC.PFC2D_geometry")
    core_package.PFC2D_model = importlib.import_module("HPFC.PFC2D_model")

    std_package = types.ModuleType("PFC.stdPFC")
    std_package.__path__ = []
    std_package.sim_pfc_std = importlib.import_module("HPFC.sim_pfc_std")

    shpfc_package = types.ModuleType("PFC.sHPFC")
    shpfc_package.__path__ = []
    shpfc_package.sim_shpfc_std = importlib.import_module("HPFC.sim_shpfc_std")
    shpfc_package.sim_shpfc_div_vpsi = importlib.import_module("HPFC.sim_shpfc_div_vpsi")
    shpfc_package.sim_shpfc_psigradmu = importlib.import_module("HPFC.sim_shpfc_psigradmu")

    pfc_package.Core = core_package
    pfc_package.stdPFC = std_package
    pfc_package.sHPFC = shpfc_package

    sys.modules["PFC"] = pfc_package
    sys.modules["PFC.Core"] = core_package
    sys.modules["PFC.stdPFC"] = std_package
    sys.modules["PFC.sHPFC"] = shpfc_package


@pytest.fixture
def pfc_contract_namespace() -> None:
    try:
        importlib.import_module("PFC.Core")
    except ModuleNotFoundError as exc:
        if exc.name != "PFC":
            raise
        _install_legacy_pfc_namespace()


@pytest.mark.usefixtures("pfc_contract_namespace")
@pytest.mark.parametrize("package_name, expected_attributes", PACKAGE_SURFACES.items())
def test_public_pfc_package_contract(package_name: str, expected_attributes: tuple[str, ...]) -> None:
    package = importlib.import_module(package_name)

    assert package.__name__ == package_name
    for attribute_name in expected_attributes:
        assert hasattr(package, attribute_name)


def test_hpfc_compatibility_import_path_remains_available() -> None:
    package = importlib.import_module("HPFC")

    assert package.__name__ == "HPFC"