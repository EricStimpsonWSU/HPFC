from __future__ import annotations

import importlib
from pathlib import Path

import numpy as np
import pytest

from PFC.Core import backend
from PFC.Core.PFC2D_geometry import geometry_2D
from PFC.Core.PFC2D_model import model_2D
from PFC.stdPFC.sim_pfc_std import build_model as _sim_pfc_std_build_model


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--backend-mode",
        action="store",
        default="both",
        choices=("cpu", "gpu", "both"),
        help="Select backend coverage mode for backend-sensitive tests.",
    )


def _resolve_required_gpu_backend() -> backend.ArrayBackend:
    gpu_backend = backend._resolve_cupy_backend()
    if gpu_backend is None:
        pytest.fail("--backend-mode requires a working CuPy backend, but CuPy is unavailable")
    try:
        sample = gpu_backend.array([0.0], dtype=np.float64)
        gpu_backend.to_numpy(sample)
    except Exception as exc:  # pragma: no cover - hardware dependent
        pytest.fail(f"--backend-mode requires a working CuPy backend, but allocation failed: {exc}")
    return gpu_backend


@pytest.fixture
def pfc_contract_namespace() -> None:
    importlib.import_module("PFC.Core")


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
def backend_mode(pytestconfig) -> str:
    return pytestconfig.getoption("--backend-mode")


@pytest.fixture(params=("cpu", "gpu"))
def backend_target(request, backend_mode: str) -> str:
    target = request.param
    if backend_mode != "both" and target != backend_mode:
        pytest.skip(f"skipped by --backend-mode={backend_mode}")
    if target == "gpu":
        _resolve_required_gpu_backend()
    return target


@pytest.fixture
def force_cpu_backend(monkeypatch):
    selected = backend._resolve_numpy_backend()
    monkeypatch.setattr(backend, "resolve_backend", lambda *args, **kwargs: selected)
    return selected


@pytest.fixture
def force_gpu_backend(monkeypatch):
    selected = _resolve_required_gpu_backend()
    monkeypatch.setattr(backend, "resolve_backend", lambda *args, **kwargs: selected)
    return selected


@pytest.fixture
def force_numpy_backend(monkeypatch, backend_target: str):
    if backend_target == "gpu":
        selected = _resolve_required_gpu_backend()
    else:
        selected = backend._resolve_numpy_backend()
    monkeypatch.setattr(backend, "resolve_backend", lambda *args, **kwargs: selected)
    return selected


@pytest.fixture
def backend_resolution_mocks(monkeypatch):
    def apply(*, cupy_backend=None, numpy_fftw_backend=None):
        monkeypatch.setattr(backend, "_resolve_cupy_backend", lambda: cupy_backend)
        monkeypatch.setattr(backend, "_resolve_numpy_fftw_backend", lambda: numpy_fftw_backend)

    return apply
