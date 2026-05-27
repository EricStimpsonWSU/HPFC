"""Canonical simulation definition surface for standard (non-hydro) PFC."""

from __future__ import annotations

import numpy as np

from PFC2D_geometry import geometry_2D
from PFC2D_model import model_2D
from kernel_rules import KernelRules
from sHPFC import BackendPayloadManager, sHPFC
from state import SimulationState


def build_model(*, temp: float, beta: float, Gamma: float, rho0: float, Gamma_s: float, dt: float) -> model_2D:
    base = model_2D(temp=temp, beta=beta, Gamma=Gamma, rho0=rho0, Gamma_s=Gamma_s, dt=dt)

    class _HydroView:
        def __init__(self, base_obj: model_2D) -> None:
            # Mirror the same parameter names to the hydro view for compatibility
            for _name in ("temp", "beta", "Gamma", "rho0", "Gamma_s", "dt"):
                setattr(self, _name, getattr(base_obj, _name))

    class _ModelContainer:
        def __init__(self, base_obj: model_2D) -> None:
            self._base = base_obj
            self.hydro = _HydroView(base_obj)

        def __getattr__(self, name: str):
            return getattr(self._base, name)

    return _ModelContainer(base)


def build_geometry(*, shape: tuple[int, int], Lx: float, Ly: float) -> geometry_2D:
    return geometry_2D(shape=shape, Lx=Lx, Ly=Ly)


def make_initial_state(
    psi0: np.ndarray,
    *,
    model: model_2D,
    geometry: geometry_2D,
    payload_mgr: BackendPayloadManager | None = None,
) -> SimulationState:
    payload_mgr = payload_mgr or BackendPayloadManager()
    kernels = KernelRules(model=model, geometry=geometry)
    return SimulationState(payload_mgr, model, geometry, kernels, psi0)


def make_sim(psi0: np.ndarray, *, model: model_2D, geometry: geometry_2D) -> sHPFC:
    return sHPFC(psi0, model=model, geometry=geometry)
