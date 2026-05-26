"""Simulation state owner for the staged `sHPFC` split."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


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
        self.psi = self._psi_poly[0]
        self.psi[...] = self._payload_mgr.asarray(self.psi0, dtype=np.float64)
        self.psi2 = self._psi_poly[1]
        self.psi3 = self._psi_poly[2]
        self.psi4 = self._psi_poly[3]

        self._psi_hat_poly = self._payload_mgr.zeros((4, *shape), dtype=np.complex128)
        self.psi_hat = self._psi_hat_poly[0]
        self.psi2_hat = self._psi_hat_poly[1]
        self.psi3_hat = self._psi_hat_poly[2]
        self.psi4_hat = self._psi_hat_poly[3]

        self._batch_v = self._payload_mgr.zeros((2, *shape), dtype=np.float64)
        self.v_x = self._batch_v[0]
        self.v_y = self._batch_v[1]

        self._batch_v_hat = self._payload_mgr.zeros((2, *shape), dtype=np.complex128)
        self.v_x_hat = self._batch_v_hat[0]
        self.v_y_hat = self._batch_v_hat[1]

        self.div_v = self._payload_mgr.zeros(shape, dtype=np.float64)

        self._batch_grad = self._payload_mgr.zeros((4, *shape), dtype=np.float64)
        self.psi_x = self._batch_grad[0]
        self.psi_y = self._batch_grad[1]
        self.f_x = self._batch_grad[2]
        self.f_y = self._batch_grad[3]

        self._batch_grad_hat = self._payload_mgr.zeros((4, *shape), dtype=np.complex128)
        self.psi_x_hat = self._batch_grad_hat[0]
        self.psi_y_hat = self._batch_grad_hat[1]
        self.f_x_hat = self._batch_grad_hat[2]
        self.f_y_hat = self._batch_grad_hat[3]

        self._batch_grad_psi = self._batch_grad[:2]
        self._batch_grad_psi_hat = self._batch_grad_hat[:2]

        self._batch_grad_mu = self._payload_mgr.zeros((2, *shape), dtype=np.float64)
        self.mu_x = self._batch_grad_mu[0]
        self.mu_y = self._batch_grad_mu[1]

        self._batch_grad_mu_hat = self._payload_mgr.zeros((2, *shape), dtype=np.complex128)
        self.mu_x_hat = self._batch_grad_mu_hat[0]
        self.mu_y_hat = self._batch_grad_mu_hat[1]

        self._batch_force = self._payload_mgr.zeros((2, *shape), dtype=np.float64)
        self.force_x = self._batch_force[0]
        self.force_y = self._batch_force[1]

        self._batch_force_hat = self._payload_mgr.zeros((2, *shape), dtype=np.complex128)
        self.force_x_hat = self._batch_force_hat[0]
        self.force_y_hat = self._batch_force_hat[1]

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
        self._psi_hat_poly[...] = self._payload_mgr.fftn(self._psi_poly, axes=(-2, -1))

    def calc_mu(self, *, psi_hat_is_current: bool = False) -> None:
        if not psi_hat_is_current:
            self.calc_poly_psi()
        self.lin_mu_hat[...] = self.kernels.lin_mu_kernel * self.psi_hat
        self.lin_mu[...] = self._payload_mgr.real(self._payload_mgr.ifftn(self.lin_mu_hat))
        self.mu[...] = self.lin_mu + self.psi3

    def calc_f(self, *, psi_hat_is_current: bool = False) -> None:
        if not psi_hat_is_current:
            self.calc_poly_psi()
        self.lin_f_hat[...] = self.kernels.lin_f_kernel * self.psi_hat
        self.lin_f[...] = self._payload_mgr.real(self._payload_mgr.ifftn(self.lin_f_hat))
        self.f[...] = self.lin_f * self.psi + 0.5 * (self.model.beta + self.model.temp) * self.psi2 + 0.25 * self.psi4

    def calc_StructureTensor(self, *, psi_xy_is_current: bool = False) -> None:
        if not psi_xy_is_current:
            self.calc_poly_psi()
            self.psi_x[...] = self._payload_mgr.real(self._payload_mgr.ifftn(1j * self.KX * self.psi_hat))
            self.psi_y[...] = self._payload_mgr.real(self._payload_mgr.ifftn(1j * self.KY * self.psi_hat))

        S_xx = self.psi_x**2
        S_yy = self.psi_y**2
        S_xy = self.psi_x * self.psi_y

        self.S_xx = self._payload_mgr.real(self._payload_mgr.ifftn(self._payload_mgr.fftn(S_xx) * self.kernels.gaussian_kernel))
        self.S_yy = self._payload_mgr.real(self._payload_mgr.ifftn(self._payload_mgr.fftn(S_yy) * self.kernels.gaussian_kernel))
        self.S_xy = self._payload_mgr.real(self._payload_mgr.ifftn(self._payload_mgr.fftn(S_xy) * self.kernels.gaussian_kernel))