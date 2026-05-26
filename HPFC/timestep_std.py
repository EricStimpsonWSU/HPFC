"""Standard PFC timestep strategy."""

from __future__ import annotations

from state import SimulationState


class StdPFCTimestepper:
    def __init__(self, state: SimulationState) -> None:
        self.state = state

    def step(self) -> None:
        state = self.state
        state.psi_hat[...] = state._payload_mgr.fftn(state.psi)
        state.nonlin_hat[...] = state._payload_mgr.fftn(state.psi**3)
        state.psi1_hat[...] = (
            state.kernel_lin_psi_exp * state.psi_hat +
            state.kernel_d2_dlap * state.kernel_nonlin_psi_exp * state.nonlin_hat
        )
        state.psi[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.psi1_hat))
        state.t += state.model.dt