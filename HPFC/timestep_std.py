"""Standard PFC timestep strategy."""

from __future__ import annotations

from state import SimulationState


class StdPFCTimestepper:
    def __init__(self, state: SimulationState) -> None:
        self.state = state

    def step(self) -> None:
        sim = self.state.sim
        sim.psi_hat[...] = sim._payload_mgr.fftn(sim.psi)
        sim.nonlin_hat[...] = sim._payload_mgr.fftn(sim.psi**3)
        sim.psi1_hat[...] = (
            sim.kernel_lin_psi_exp * sim.psi_hat +
            sim.kernel_d2_dlap * sim.kernel_nonlin_psi_exp * sim.nonlin_hat
        )
        sim.psi[...] = sim._payload_mgr.real(sim._payload_mgr.ifftn(sim.psi1_hat))
        sim.t += sim.model.dt