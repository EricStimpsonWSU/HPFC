"""Canonical simulation definition surface for standard (non-hydro) PFC."""

from __future__ import annotations

import numpy as np

from PFC2D_geometry import geometry_2D
from PFC2D_model import model_2D
from kernel_rules import KernelRules
from sHPFC import BackendPayloadManager, sHPFC
from state import SimulationState
from PFC2D_model import resolve_model_parameter
import numpy as _np


def build_lin_kernels(model: model_2D, geometry: geometry_2D):
    # Model-specific linear kernels for the canonical non-hydro PFC variant.
    temp = model.temp
    beta = model.beta
    gamma = model.Gamma
    rho0 = resolve_model_parameter(model, "rho0")
    gamma_s = resolve_model_parameter(model, "Gamma_s")

    k2 = geometry.k2
    d2 = -k2
    d4 = k2 ** 2
    d6 = k2 ** 3

    lin_dpsi = gamma * ((temp + beta) * d2 + 2 * beta * d4 + beta * (-d6))
    lin_mu_kernel = (temp + beta) + 2 * beta * d2 + beta * d4
    lin_f_kernel = 0.5 * beta * (d4 + 2 * d2)
    lin_v_kernel = (gamma_s / rho0) * d2

    return lin_dpsi, lin_mu_kernel, lin_f_kernel, lin_v_kernel


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
