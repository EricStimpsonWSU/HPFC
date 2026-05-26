"""Simulation state owner for the staged `sHPFC` split."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from fields import ForceBatch, GradBatch, GradMuBatch, PsiBatch, PsiGradBatch, VelBatch


@dataclass
class SimulationState:
    """Own the simulation buffers and the helpers that operate on them."""

    _payload_mgr: Any
    model: Any
    geometry: Any
    kernels: Any
    psi0: np.ndarray

    def __post_init__(self) -> None:
        self.kernel_d_dx = self._payload_mgr.asarray(self.kernels.d_dx)
        self.kernel_d_dy = self._payload_mgr.asarray(self.kernels.d_dy)
        self.kernel_d2_dlap = self._payload_mgr.asarray(self.kernels.d2_dlap)
        self.kernel_lin_v_exp = self._payload_mgr.asarray(self.kernels.lin_v_exp)
        self.kernel_nonlin_v_exp = self._payload_mgr.asarray(self.kernels.nonlin_v_exp)
        self.kernel_gaussian = self._payload_mgr.asarray(self.kernels.gaussian_kernel)
        self.kernel_lin_psi_exp = self._payload_mgr.asarray(self.kernels.lin_psi_exp)
        self.kernel_nonlin_psi_exp = self._payload_mgr.asarray(self.kernels.nonlin_psi_exp)

        self.KX = self._payload_mgr.asarray(self.geometry.KX)
        self.KY = self._payload_mgr.asarray(self.geometry.KY)
        self.k2 = self._payload_mgr.asarray(self.geometry.k2)

        shape = self.psi0.shape
        self.psi_hat_00 = self.psi0.mean() * self.psi0.size

        self.lin_mu = self._payload_mgr.zeros(shape, dtype=np.float64)
        self.lin_f = self._payload_mgr.zeros(shape, dtype=np.float64)
        self.lin_mu_hat = self._payload_mgr.zeros(shape, dtype=np.complex128)
        self.lin_f_hat = self._payload_mgr.zeros(shape, dtype=np.complex128)

        self.mu = self._payload_mgr.zeros(shape, dtype=np.float64)
        self.f = self._payload_mgr.zeros(shape, dtype=np.float64)
        self.mu_hat = self._payload_mgr.zeros(shape, dtype=np.complex128)
        self.f_hat = self._payload_mgr.zeros(shape, dtype=np.complex128)

        self._psi_poly = self._payload_mgr.zeros((4, *shape), dtype=np.float64)
        self._psi_hat_poly = self._payload_mgr.zeros((4, *shape), dtype=np.complex128)
        self.psi_batch = PsiBatch(self._psi_poly, self._psi_hat_poly)
        self.psi = self.psi_batch.psi
        self.psi[...] = self._payload_mgr.asarray(self.psi0, dtype=np.float64)
        self.psi2 = self.psi_batch.psi2
        self.psi3 = self.psi_batch.psi3
        self.psi4 = self.psi_batch.psi4

        self.psi_hat = self.psi_batch.psi_hat
        self.psi2_hat = self.psi_batch.psi2_hat
        self.psi3_hat = self.psi_batch.psi3_hat
        self.psi4_hat = self.psi_batch.psi4_hat

        self._batch_v = self._payload_mgr.zeros((2, *shape), dtype=np.float64)
        self._batch_v_hat = self._payload_mgr.zeros((2, *shape), dtype=np.complex128)
        self.vel_batch = VelBatch(self._batch_v, self._batch_v_hat)
        self.v_x = self.vel_batch.v_x
        self.v_y = self.vel_batch.v_y

        self.v_x_hat = self.vel_batch.v_x_hat
        self.v_y_hat = self.vel_batch.v_y_hat

        self.div_v = self._payload_mgr.zeros(shape, dtype=np.float64)

        self._batch_grad = self._payload_mgr.zeros((4, *shape), dtype=np.float64)
        self._batch_grad_hat = self._payload_mgr.zeros((4, *shape), dtype=np.complex128)
        self.grad_batch = GradBatch(self._batch_grad, self._batch_grad_hat)
        self.psi_x = self.grad_batch.psi_x
        self.psi_y = self.grad_batch.psi_y
        self.f_x = self.grad_batch.f_x
        self.f_y = self.grad_batch.f_y

        self.psi_x_hat = self.grad_batch.psi_x_hat
        self.psi_y_hat = self.grad_batch.psi_y_hat
        self.f_x_hat = self.grad_batch.f_x_hat
        self.f_y_hat = self.grad_batch.f_y_hat

        self.grad_psi_batch = PsiGradBatch(self._batch_grad, self._batch_grad_hat)

        self._batch_grad_mu = self._payload_mgr.zeros((2, *shape), dtype=np.float64)
        self._batch_grad_mu_hat = self._payload_mgr.zeros((2, *shape), dtype=np.complex128)
        self.grad_mu_batch = GradMuBatch(self._batch_grad_mu, self._batch_grad_mu_hat)
        self.mu_x = self.grad_mu_batch.mu_x
        self.mu_y = self.grad_mu_batch.mu_y

        self.mu_x_hat = self.grad_mu_batch.mu_x_hat
        self.mu_y_hat = self.grad_mu_batch.mu_y_hat

        self._batch_force = self._payload_mgr.zeros((2, *shape), dtype=np.float64)
        self._batch_force_hat = self._payload_mgr.zeros((2, *shape), dtype=np.complex128)
        self.force_batch = ForceBatch(self._batch_force, self._batch_force_hat)
        self.force_x = self.force_batch.force_x
        self.force_y = self.force_batch.force_y
        self.force_x_hat = self.force_batch.force_x_hat
        self.force_y_hat = self.force_batch.force_y_hat

        self.v_dot_grad_psi = self._payload_mgr.zeros(shape, dtype=np.float64)
        self.v_dot_grad_psi_hat = self._payload_mgr.zeros(shape, dtype=np.complex128)
        self.div_vpsi_hat = self._payload_mgr.zeros(shape, dtype=np.complex128)

        self.nonlin_hat = self._payload_mgr.zeros(shape, dtype=np.complex128)
        self.psi1_hat = self._payload_mgr.zeros(shape, dtype=np.complex128)

        self.t = 0.0

    def calc_poly_psi(self) -> None:
        self.psi2[...] = self.psi**2
        self.psi3[...] = self.psi2 * self.psi
        self.psi4[...] = self.psi3 * self.psi
        self.psi_batch.psi_hat_poly[...] = self._payload_mgr.fftn(self._psi_poly, axes=(-2, -1))

    def calc_mu(self, *, psi_hat_is_current: bool = False) -> None:
        if not psi_hat_is_current:
            self.calc_poly_psi()
        self.lin_mu_hat[...] = self.kernels.lin_mu_kernel * self.psi_batch.psi_hat
        self.lin_mu[...] = self._payload_mgr.real(self._payload_mgr.ifftn(self.lin_mu_hat))
        self.mu[...] = self.lin_mu + self.psi3

    def calc_f(self, *, psi_hat_is_current: bool = False) -> None:
        if not psi_hat_is_current:
            self.calc_poly_psi()
        self.lin_f_hat[...] = self.kernels.lin_f_kernel * self.psi_batch.psi_hat
        self.lin_f[...] = self._payload_mgr.real(self._payload_mgr.ifftn(self.lin_f_hat))
        self.f[...] = self.lin_f * self.psi + 0.5 * (self.model.beta + self.model.temp) * self.psi2 + 0.25 * self.psi4

    def calc_StructureTensor(self, *, psi_xy_is_current: bool = False) -> None:
        if not psi_xy_is_current:
            self.calc_poly_psi()
            self.psi_x[...] = self._payload_mgr.real(self._payload_mgr.ifftn(1j * self.KX * self.psi_batch.psi_hat))
            self.psi_y[...] = self._payload_mgr.real(self._payload_mgr.ifftn(1j * self.KY * self.psi_batch.psi_hat))

        S_xx = self.psi_x**2
        S_yy = self.psi_y**2
        S_xy = self.psi_x * self.psi_y

        self.S_xx = self._payload_mgr.real(self._payload_mgr.ifftn(self._payload_mgr.fftn(S_xx) * self.kernels.gaussian_kernel))
        self.S_yy = self._payload_mgr.real(self._payload_mgr.ifftn(self._payload_mgr.fftn(S_yy) * self.kernels.gaussian_kernel))
        self.S_xy = self._payload_mgr.real(self._payload_mgr.ifftn(self._payload_mgr.fftn(S_xy) * self.kernels.gaussian_kernel))