from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
HPFC_DIR = ROOT / "HPFC"
if str(HPFC_DIR) not in sys.path:
    sys.path.insert(0, str(HPFC_DIR))

from PFC2D_geometry import geometry_2D
from PFC2D_model import model_2D
import backend
from sim_pfc_std import build_model as _sim_pfc_std_build_model


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
