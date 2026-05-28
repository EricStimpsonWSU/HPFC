from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
HPFC_DIR = ROOT / "HPFC"
if str(HPFC_DIR) not in sys.path:
    sys.path.insert(0, str(HPFC_DIR))

from PFC2D_geometry import geometry_2D
from PFC2D_model import model_2D
import backend
from HPFC.sim_pfc_std import build_model as _sim_pfc_std_build_model


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
    core_package.geometry_2D = core_package.PFC2D_geometry.geometry_2D
    core_package.model_2D = core_package.PFC2D_model.model_2D
    core_package.kernels = importlib.import_module("HPFC.PFC2D_kernels").kernels
    core_package.gaussian_kernel_fft = core_package.kernel_rules.gaussian_kernel_fft
    core_package.resolve_model_parameter = core_package.PFC2D_model.resolve_model_parameter

    std_package = types.ModuleType("PFC.stdPFC")
    std_package.__path__ = []
    std_package.sim_pfc_std = importlib.import_module("HPFC.sim_pfc_std")
    std_package.build_model = std_package.sim_pfc_std.build_model
    std_package.make_sim = std_package.sim_pfc_std.make_sim

    shpfc_package = types.ModuleType("PFC.sHPFC")
    shpfc_package.__path__ = []
    shpfc_package.sim_shpfc_std = importlib.import_module("HPFC.sim_shpfc_std")
    shpfc_package.sim_shpfc_div_vpsi = importlib.import_module("HPFC.sim_shpfc_div_vpsi")
    shpfc_package.sim_shpfc_psigradmu = importlib.import_module("HPFC.sim_shpfc_psigradmu")
    shpfc_package.make_sim = shpfc_package.sim_shpfc_std.make_sim

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


@pytest.fixture
def simple_model() -> model_2D:
    # Use the simulation module's model builder so the model's class
    # is defined in the sim module and KernelRules can locate
    # `build_lin_kernels` without a legacy fallback.
    return _sim_pfc_std_build_model(temp=-0.25, beta=1.5, Gamma=1.0, rho0=1.0, Gamma_s=0.75, dt=0.05)


@pytest.fixture
def simple_geometry() -> geometry_2D:
    return geometry_2D(shape=(4, 4), Lx=8.0, Ly=8.0)


@pytest.fixture
def psi0() -> np.ndarray:
    grid = np.arange(16, dtype=np.float64).reshape(4, 4)
    return 0.1 * grid


@pytest.fixture
def contract_model_kwargs() -> dict[str, float]:
    return {
        "temp": -0.25,
        "beta": 1.5,
        "Gamma": 1.0,
        "rho0": 1.0,
        "Gamma_s": 0.75,
        "dt": 0.05,
    }


@pytest.fixture
def contract_geometry_kwargs() -> dict[str, object]:
    return {
        "shape": (4, 4),
        "Lx": 8.0,
        "Ly": 8.0,
    }


@pytest.fixture
def contract_psi0() -> np.ndarray:
    x = np.linspace(0.0, 2.0 * np.pi, 4, endpoint=False)
    y = np.linspace(0.0, 2.0 * np.pi, 4, endpoint=False)
    xx, yy = np.meshgrid(x, y)
    return 0.05 * (np.sin(xx) + np.cos(yy))


@pytest.fixture
def numpy_backend():
    return backend._resolve_numpy_backend()


@pytest.fixture
def force_numpy_backend(monkeypatch):
    monkeypatch.setattr(backend, "resolve_backend", backend._resolve_numpy_backend)
    return backend._resolve_numpy_backend()


@pytest.fixture
def backend_resolution_mocks(monkeypatch):
    def apply(*, cupy_backend=None, numpy_fftw_backend=None):
        monkeypatch.setattr(backend, "_resolve_cupy_backend", lambda: cupy_backend)
        monkeypatch.setattr(backend, "_resolve_numpy_fftw_backend", lambda: numpy_fftw_backend)

    return apply
