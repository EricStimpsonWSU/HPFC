"""Semantic batch wrappers for shared simulation buffers."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class PsiBatch:
    psi_poly: np.ndarray
    psi_hat_poly: np.ndarray

    @property
    def psi(self) -> np.ndarray:
        return self.psi_poly[0]

    @property
    def psi2(self) -> np.ndarray:
        return self.psi_poly[1]

    @property
    def psi3(self) -> np.ndarray:
        return self.psi_poly[2]

    @property
    def psi4(self) -> np.ndarray:
        return self.psi_poly[3]

    @property
    def psi_hat(self) -> np.ndarray:
        return self.psi_hat_poly[0]

    @property
    def psi2_hat(self) -> np.ndarray:
        return self.psi_hat_poly[1]

    @property
    def psi3_hat(self) -> np.ndarray:
        return self.psi_hat_poly[2]

    @property
    def psi4_hat(self) -> np.ndarray:
        return self.psi_hat_poly[3]


@dataclass(slots=True)
class VelBatch:
    vel: np.ndarray
    vel_hat: np.ndarray

    @property
    def v_x(self) -> np.ndarray:
        return self.vel[0]

    @property
    def v_y(self) -> np.ndarray:
        return self.vel[1]

    @property
    def v_x_hat(self) -> np.ndarray:
        return self.vel_hat[0]

    @property
    def v_y_hat(self) -> np.ndarray:
        return self.vel_hat[1]


@dataclass(slots=True)
class GradBatch:
    grad: np.ndarray
    grad_hat: np.ndarray

    @property
    def psi_x(self) -> np.ndarray:
        return self.grad[0]

    @property
    def psi_y(self) -> np.ndarray:
        return self.grad[1]

    @property
    def f_x(self) -> np.ndarray:
        return self.grad[2]

    @property
    def f_y(self) -> np.ndarray:
        return self.grad[3]

    @property
    def psi_x_hat(self) -> np.ndarray:
        return self.grad_hat[0]

    @property
    def psi_y_hat(self) -> np.ndarray:
        return self.grad_hat[1]

    @property
    def f_x_hat(self) -> np.ndarray:
        return self.grad_hat[2]

    @property
    def f_y_hat(self) -> np.ndarray:
        return self.grad_hat[3]


@dataclass(slots=True)
class PsiGradBatch:
    grad: np.ndarray
    grad_hat: np.ndarray

    @property
    def psi_x(self) -> np.ndarray:
        return self.grad[0]

    @property
    def psi_y(self) -> np.ndarray:
        return self.grad[1]

    @property
    def psi_x_hat(self) -> np.ndarray:
        return self.grad_hat[0]

    @property
    def psi_y_hat(self) -> np.ndarray:
        return self.grad_hat[1]


@dataclass(slots=True)
class GradMuBatch:
    grad_mu: np.ndarray
    grad_mu_hat: np.ndarray

    @property
    def mu_x(self) -> np.ndarray:
        return self.grad_mu[0]

    @property
    def mu_y(self) -> np.ndarray:
        return self.grad_mu[1]

    @property
    def mu_x_hat(self) -> np.ndarray:
        return self.grad_mu_hat[0]

    @property
    def mu_y_hat(self) -> np.ndarray:
        return self.grad_mu_hat[1]


@dataclass(slots=True)
class ForceBatch:
    force: np.ndarray
    force_hat: np.ndarray

    @property
    def force_x(self) -> np.ndarray:
        return self.force[0]

    @property
    def force_y(self) -> np.ndarray:
        return self.force[1]

    @property
    def force_x_hat(self) -> np.ndarray:
        return self.force_hat[0]

    @property
    def force_y_hat(self) -> np.ndarray:
        return self.force_hat[1]