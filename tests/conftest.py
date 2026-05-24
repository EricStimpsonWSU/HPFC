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


@pytest.fixture
def simple_model() -> model_2D:
    return model_2D(temp=-0.25, beta=1.5, Gamma=1.0, rho0=1.0, Gamma_s=0.75, dt=0.05)


@pytest.fixture
def simple_geometry() -> geometry_2D:
    return geometry_2D(shape=(4, 4), Lx=8.0, Ly=8.0)


@pytest.fixture
def psi0() -> np.ndarray:
    grid = np.arange(16, dtype=np.float64).reshape(4, 4)
    return 0.1 * grid


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
