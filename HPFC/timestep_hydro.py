"""Hydrodynamic PFC timestep strategies."""

from __future__ import annotations

from state import SimulationState


class SHPFCTimestepper:
    def __init__(self, state: SimulationState) -> None:
        self.state = state

    def _calc_common_hydro_fields(self) -> None:
        state = self.state
        state.calc_poly_psi()
        state.calc_mu(psi_hat_is_current=True)
        state.calc_f(psi_hat_is_current=True)

        state.f_hat[...] = state._payload_mgr.fftn(state.f)
        state.grad_batch.psi_x_hat[...] = state.kernel_d_dx * state.psi_batch.psi_hat
        state.grad_batch.psi_y_hat[...] = state.kernel_d_dy * state.psi_batch.psi_hat
        state.grad_batch.f_x_hat[...] = state.kernel_d_dx * state.f_hat
        state.grad_batch.f_y_hat[...] = state.kernel_d_dy * state.f_hat
        state.grad_batch.grad[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.grad_batch.grad_hat, axes=(-2, -1)))
        state.force_batch.force_x[...] = state.mu * state.grad_batch.psi_x - state.grad_batch.f_x
        state.force_batch.force_y[...] = state.mu * state.grad_batch.psi_y - state.grad_batch.f_y
        state.force_batch.force_hat[...] = state._payload_mgr.fftn(state.force_batch.force, axes=(-2, -1))
        state.vel_batch.v_x_hat[...] = state.kernel_lin_v_exp * state.vel_batch.v_x_hat + 1 / state.model.rho0 * state.kernel_nonlin_v_exp * state.kernel_gaussian * state.force_batch.force_x_hat
        state.vel_batch.v_y_hat[...] = state.kernel_lin_v_exp * state.vel_batch.v_y_hat + 1 / state.model.rho0 * state.kernel_nonlin_v_exp * state.kernel_gaussian * state.force_batch.force_y_hat
        state.vel_batch.vel[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.vel_batch.vel_hat, axes=(-2, -1)))

    def step(self) -> None:
        state = self.state
        self._calc_common_hydro_fields()
        state.v_dot_grad_psi[...] = state.vel_batch.v_x * state.grad_batch.psi_x + state.vel_batch.v_y * state.grad_batch.psi_y
        state.v_dot_grad_psi_hat[...] = state._payload_mgr.fftn(state.v_dot_grad_psi)
        state.v_dot_grad_psi_hat[0, :] = 0
        state.v_dot_grad_psi_hat[:, 0] = 0
        state.psi_batch.psi_hat[...] = state.kernel_lin_psi_exp * state.psi_batch.psi_hat + state.kernel_nonlin_psi_exp * (state.model.Gamma * state.kernel_d2_dlap * state.psi_batch.psi3_hat - state.v_dot_grad_psi_hat)
        state.psi_batch.psi_hat[0, 0] = state.psi_hat_00
        state.psi[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.psi_batch.psi_hat))
        state.t += state.model.dt

    def step_div_vpsi(self) -> None:
        state = self.state
        self._calc_common_hydro_fields()
        state.div_vpsi_hat[...] = (
            state.kernel_d_dx * state._payload_mgr.fftn(state.vel_batch.v_x * state.psi_batch.psi) +
            state.kernel_d_dy * state._payload_mgr.fftn(state.vel_batch.v_y * state.psi_batch.psi)
        )
        state.psi_batch.psi_hat[...] = state.kernel_lin_psi_exp * state.psi_batch.psi_hat + state.kernel_nonlin_psi_exp * (state.model.Gamma * state.kernel_d2_dlap * state.psi_batch.psi3_hat - state.div_vpsi_hat)
        state.psi_batch.psi_hat[0, 0] = state.psi_hat_00
        state.psi[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.psi_batch.psi_hat))
        state.t += state.model.dt

    def step_psigradmu(self) -> None:
        state = self.state
        state.calc_poly_psi()
        state.calc_mu(psi_hat_is_current=True)
        state.calc_f(psi_hat_is_current=True)
        state.grad_psi_batch.psi_x_hat[...] = state.kernel_d_dx * state.psi_batch.psi_hat
        state.grad_psi_batch.psi_y_hat[...] = state.kernel_d_dy * state.psi_batch.psi_hat
        state.grad_psi_batch.grad[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.grad_psi_batch.grad_hat, axes=(-2, -1)))
        state.mu_hat[...] = state._payload_mgr.fftn(state.mu)
        state.grad_mu_batch.mu_x_hat[...] = state.kernel_d_dx * state.mu_hat
        state.grad_mu_batch.mu_y_hat[...] = state.kernel_d_dy * state.mu_hat
        state.grad_mu_batch.grad_mu[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.grad_mu_batch.grad_mu_hat, axes=(-2, -1)))
        state.force_batch.force_x[...] = -state.psi_batch.psi * state.grad_mu_batch.mu_x
        state.force_batch.force_y[...] = -state.psi_batch.psi * state.grad_mu_batch.mu_y
        state.force_batch.force_hat[...] = state._payload_mgr.fftn(state.force_batch.force, axes=(-2, -1))
        state.vel_batch.v_x_hat[...] = state.kernel_lin_v_exp * state.vel_batch.v_x_hat + 1 / state.model.rho0 * state.kernel_nonlin_v_exp * state.kernel_gaussian * state.force_batch.force_x_hat
        state.vel_batch.v_y_hat[...] = state.kernel_lin_v_exp * state.vel_batch.v_y_hat + 1 / state.model.rho0 * state.kernel_nonlin_v_exp * state.kernel_gaussian * state.force_batch.force_y_hat
        state.vel_batch.vel[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.vel_batch.vel_hat, axes=(-2, -1)))
        state.v_dot_grad_psi[...] = state.vel_batch.v_x * state.grad_psi_batch.psi_x + state.vel_batch.v_y * state.grad_psi_batch.psi_y
        state.v_dot_grad_psi_hat[...] = state._payload_mgr.fftn(state.v_dot_grad_psi)
        state.v_dot_grad_psi_hat[0, :] = 0
        state.v_dot_grad_psi_hat[:, 0] = 0
        state.psi_batch.psi_hat[...] = state.kernel_lin_psi_exp * state.psi_batch.psi_hat + state.kernel_nonlin_psi_exp * (state.model.Gamma * state.kernel_d2_dlap * state.psi_batch.psi3_hat - state.v_dot_grad_psi_hat)
        state.psi_batch.psi_hat[0, 0] = state.psi_hat_00
        state.psi[...] = state._payload_mgr.real(state._payload_mgr.ifftn(state.psi_batch.psi_hat))
        state.t += state.model.dt