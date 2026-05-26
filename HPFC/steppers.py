"""Timestep strategy objects for sHPFC variants."""

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


class SHPFCTimestepper:
    def __init__(self, state: SimulationState) -> None:
        self.state = state

    def _calc_common_hydro_fields(self):
        sim = self.state.sim
        sim.calc_poly_psi()
        sim.calc_mu(psi_hat_is_current=True)
        sim.calc_f(psi_hat_is_current=True)

        sim.f_hat[...] = sim._payload_mgr.fftn(sim.f)
        sim.psi_x_hat[...] = sim.kernel_d_dx * sim.psi_hat
        sim.psi_y_hat[...] = sim.kernel_d_dy * sim.psi_hat
        sim.f_x_hat[...] = sim.kernel_d_dx * sim.f_hat
        sim.f_y_hat[...] = sim.kernel_d_dy * sim.f_hat
        sim._batch_grad[...] = sim._payload_mgr.real(sim._payload_mgr.ifftn(sim._batch_grad_hat, axes=(-2, -1)))
        sim.force_x[...] = sim.mu * sim.psi_x - sim.f_x
        sim.force_y[...] = sim.mu * sim.psi_y - sim.f_y
        sim._batch_force_hat[...] = sim._payload_mgr.fftn(sim._batch_force, axes=(-2, -1))
        sim.v_x_hat[...] = sim.kernel_lin_v_exp * sim.v_x_hat + 1 / sim.model.rho0 * sim.kernel_nonlin_v_exp * sim.kernel_gaussian * sim.force_x_hat
        sim.v_y_hat[...] = sim.kernel_lin_v_exp * sim.v_y_hat + 1 / sim.model.rho0 * sim.kernel_nonlin_v_exp * sim.kernel_gaussian * sim.force_y_hat
        sim._batch_v[...] = sim._payload_mgr.real(sim._payload_mgr.ifftn(sim._batch_v_hat, axes=(-2, -1)))

    def step(self) -> None:
        sim = self.state.sim
        self._calc_common_hydro_fields()
        sim.v_dot_grad_psi[...] = sim.v_x * sim.psi_x + sim.v_y * sim.psi_y
        sim.v_dot_grad_psi_hat[...] = sim._payload_mgr.fftn(sim.v_dot_grad_psi)
        sim.v_dot_grad_psi_hat[0, :] = 0
        sim.v_dot_grad_psi_hat[:, 0] = 0
        sim.psi_hat[...] = sim.kernel_lin_psi_exp * sim.psi_hat + sim.kernel_nonlin_psi_exp * (sim.model.Gamma * sim.kernel_d2_dlap * sim.psi3_hat - sim.v_dot_grad_psi_hat)
        sim.psi_hat[0, 0] = sim.psi_hat_00
        sim.psi[...] = sim._payload_mgr.real(sim._payload_mgr.ifftn(sim.psi_hat))
        sim.t += sim.model.dt

    def step_div_vpsi(self) -> None:
        sim = self.state.sim
        self._calc_common_hydro_fields()
        sim.div_vpsi_hat[...] = (
            sim.kernel_d_dx * sim._payload_mgr.fftn(sim.v_x * sim.psi) +
            sim.kernel_d_dy * sim._payload_mgr.fftn(sim.v_y * sim.psi)
        )
        sim.psi_hat[...] = sim.kernel_lin_psi_exp * sim.psi_hat + sim.kernel_nonlin_psi_exp * (sim.model.Gamma * sim.kernel_d2_dlap * sim.psi3_hat - sim.div_vpsi_hat)
        sim.psi_hat[0, 0] = sim.psi_hat_00
        sim.psi[...] = sim._payload_mgr.real(sim._payload_mgr.ifftn(sim.psi_hat))
        sim.t += sim.model.dt

    def step_psigradmu(self) -> None:
        sim = self.state.sim
        sim.calc_poly_psi()
        sim.calc_mu(psi_hat_is_current=True)
        sim.calc_f(psi_hat_is_current=True)
        sim.psi_x_hat[...] = sim.kernel_d_dx * sim.psi_hat
        sim.psi_y_hat[...] = sim.kernel_d_dy * sim.psi_hat
        sim._batch_grad_psi[...] = sim._payload_mgr.real(sim._payload_mgr.ifftn(sim._batch_grad_psi_hat, axes=(-2, -1)))
        sim.mu_hat[...] = sim._payload_mgr.fftn(sim.mu)
        sim.mu_x_hat[...] = sim.kernel_d_dx * sim.mu_hat
        sim.mu_y_hat[...] = sim.kernel_d_dy * sim.mu_hat
        sim._batch_grad_mu[...] = sim._payload_mgr.real(sim._payload_mgr.ifftn(sim._batch_grad_mu_hat, axes=(-2, -1)))
        sim.force_x[...] = -sim.psi * sim.mu_x
        sim.force_y[...] = -sim.psi * sim.mu_y
        sim._batch_force_hat[...] = sim._payload_mgr.fftn(sim._batch_force, axes=(-2, -1))
        sim.v_x_hat[...] = sim.kernel_lin_v_exp * sim.v_x_hat + 1 / sim.model.rho0 * sim.kernel_nonlin_v_exp * sim.kernel_gaussian * sim.force_x_hat
        sim.v_y_hat[...] = sim.kernel_lin_v_exp * sim.v_y_hat + 1 / sim.model.rho0 * sim.kernel_nonlin_v_exp * sim.kernel_gaussian * sim.force_y_hat
        sim._batch_v[...] = sim._payload_mgr.real(sim._payload_mgr.ifftn(sim._batch_v_hat, axes=(-2, -1)))
        sim.v_dot_grad_psi[...] = sim.v_x * sim.psi_x + sim.v_y * sim.psi_y
        sim.v_dot_grad_psi_hat[...] = sim._payload_mgr.fftn(sim.v_dot_grad_psi)
        sim.v_dot_grad_psi_hat[0, :] = 0
        sim.v_dot_grad_psi_hat[:, 0] = 0
        sim.psi_hat[...] = sim.kernel_lin_psi_exp * sim.psi_hat + sim.kernel_nonlin_psi_exp * (sim.model.Gamma * sim.kernel_d2_dlap * sim.psi3_hat - sim.v_dot_grad_psi_hat)
        sim.psi_hat[0, 0] = sim.psi_hat_00
        sim.psi[...] = sim._payload_mgr.real(sim._payload_mgr.ifftn(sim.psi_hat))
        sim.t += sim.model.dt