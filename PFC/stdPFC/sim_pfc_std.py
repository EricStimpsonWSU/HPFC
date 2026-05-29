"""Canonical simulation definition surface for standard (non-hydro) PFC."""

from __future__ import annotations

import logging
import numpy as np

from PFC.Core.PFC2D_geometry import geometry_2D
from PFC.Core.PFC2D_model import model_2D, resolve_model_parameter
from PFC.Core.kernel_rules import KernelRules
from PFC.Core._simulation_facade import VariantSimulationFacade
from PFC.Core.payload import BackendPayloadManager
from PFC.Core.state import SimulationState
BLOCKED_NAMES = {
    "Timestep_sHPFC",
    "Timestep_sHPFC_div_vpsi",
    "Timestep_sHPFC_psigradmu",
    "v_x",
    "v_y",
    "v_x_hat",
    "v_y_hat",
    "div_v",
    "v_dot_grad_psi",
    "v_dot_grad_psi_hat",
    "div_vpsi_hat",
    "vel_batch",
    "force_batch",
    "force_x",
    "force_y",
    "force_x_hat",
    "force_y_hat",
    "mu_x",
    "mu_y",
    "mu_x_hat",
    "mu_y_hat",
    "grad_mu_batch",
}
import numpy as _np


LOGGER = logging.getLogger(__name__)


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
    return base


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
            backend_info = self.state._payload_mgr.backend
            self.backend_name = backend_info.name
            self.backend_fft_name = backend_info.fft_name
            self.backend_summary = backend_info.summary()
            self.backend_is_gpu = backend_info.is_gpu
            LOGGER.info("Created simulation with backend %s", self.backend_summary)

        def __getattr__(self, name: str):
            return getattr(self.state, name)

        def step(self) -> None:
            state = self.state
            state.psi_batch.psi_hat[...] = state._payload_mgr.fftn(state.psi_batch.psi)
            state.nonlin_hat[...] = state._payload_mgr.fftn(state.psi_batch.psi**3)
            state.psi1_hat[...] = (
                state.kernel_lin_psi_exp * state.psi_batch.psi_hat
                + state.kernel_d2_dlap * state.kernel_nonlin_psi_exp * state.nonlin_hat
            )
            state.psi[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.psi1_hat))
            state.t += state.model.dt

        def calc_mu(self, *, psi_hat_is_current: bool = False) -> None:
            state = self.state
            if not psi_hat_is_current:
                state.calc_poly_psi()
            state.lin_mu_hat[...] = state.kernel_lin_mu * state.psi_batch.psi_hat
            state.lin_mu[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.lin_mu_hat))
            state.mu[...] = state.lin_mu + state.psi3

        def calc_f(self, *, psi_hat_is_current: bool = False) -> None:
            state = self.state
            if not psi_hat_is_current:
                state.calc_poly_psi()
            state.lin_f_hat[...] = state.kernel_lin_f * state.psi_batch.psi_hat
            state.lin_f[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.lin_f_hat))
            state.f[...] = state.lin_f * state.psi + 0.5 * (state.model.beta + state.model.temp) * state.psi2 + 0.25 * state.psi4

    return VariantSimulationFacade(_SimImpl(state), blocked_names=BLOCKED_NAMES)
