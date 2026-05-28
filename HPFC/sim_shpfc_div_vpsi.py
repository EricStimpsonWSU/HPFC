"""Canonical simulation definition surface for sHPFC div(v psi) variant."""

from __future__ import annotations

import numpy as np

from PFC.Core.PFC2D_geometry import geometry_2D
from PFC.Core.PFC2D_model import model_2D, resolve_model_parameter
from PFC.Core.kernel_rules import KernelRules
from PFC.Core._simulation_facade import VariantSimulationFacade
from PFC.Core.payload import BackendPayloadManager
from PFC.Core.state import SimulationState
from PFC.Core.steppers import SHPFCTimestepper, StdPFCTimestepper
BLOCKED_NAMES = {
    "Timestep_stdPFC",
    "Timestep_sHPFC",
    "Timestep_sHPFC_psigradmu",
}


def build_lin_kernels(model: model_2D, geometry: geometry_2D):
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


def make_sim(psi0: np.ndarray, *, model: model_2D, geometry: geometry_2D) -> VariantSimulationFacade:
    state = make_initial_state(psi0, model=model, geometry=geometry)

    class _SimImpl:
        def __init__(self, state: SimulationState):
            self.state = state
            self.model = state.model
            self.geometry = state.geometry
            self.std_stepper = StdPFCTimestepper(self.state)
            self.shpfc_stepper = SHPFCTimestepper(self.state)

        def __getattr__(self, name: str):
            return getattr(self.state, name)

        def Timestep_stdPFC(self) -> None:
            self.std_stepper.step()

        def Timestep_sHPFC(self) -> None:
            self.shpfc_stepper.step()

        def Timestep_sHPFC_div_vpsi(self) -> None:
            self.shpfc_stepper.step_div_vpsi()

        def Timestep_sHPFC_psigradmu(self) -> None:
            self.shpfc_stepper.step_psigradmu()

    return VariantSimulationFacade(_SimImpl(state), blocked_names=BLOCKED_NAMES)
