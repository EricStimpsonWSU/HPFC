from __future__ import annotations

import numpy as np

from fields import ForceBatch, GradBatch, GradMuBatch, PsiBatch, PsiGradBatch, VelBatch


def test_field_wrappers_expose_views_into_backing_arrays():
    psi_poly = np.zeros((4, 2, 2), dtype=np.float64)
    psi_hat_poly = np.zeros((4, 2, 2), dtype=np.complex128)
    vel = np.zeros((2, 2, 2), dtype=np.float64)
    vel_hat = np.zeros((2, 2, 2), dtype=np.complex128)
    grad = np.zeros((4, 2, 2), dtype=np.float64)
    grad_hat = np.zeros((4, 2, 2), dtype=np.complex128)
    grad_mu = np.zeros((2, 2, 2), dtype=np.float64)
    grad_mu_hat = np.zeros((2, 2, 2), dtype=np.complex128)
    force = np.zeros((2, 2, 2), dtype=np.float64)
    force_hat = np.zeros((2, 2, 2), dtype=np.complex128)

    psi_batch = PsiBatch(psi_poly, psi_hat_poly)
    vel_batch = VelBatch(vel, vel_hat)
    grad_batch = GradBatch(grad, grad_hat)
    grad_psi_batch = PsiGradBatch(grad, grad_hat)
    grad_mu_batch = GradMuBatch(grad_mu, grad_mu_hat)
    force_batch = ForceBatch(force, force_hat)

    psi_batch.psi[...] = 1.5
    vel_batch.v_x[...] = 2.5
    grad_batch.f_y_hat[...] = 3.5 + 1.0j
    grad_psi_batch.psi_y_hat[...] = 4.5 + 2.0j
    grad_mu_batch.mu_x[...] = 5.5
    force_batch.force_y_hat[...] = 6.5 + 3.0j

    assert psi_poly[0, 0, 0] == 1.5
    assert vel[0, 0, 0] == 2.5
    assert grad_hat[3, 0, 0] == 3.5 + 1.0j
    assert grad_hat[1, 0, 0] == 4.5 + 2.0j
    assert grad_mu[0, 0, 0] == 5.5
    assert force_hat[1, 0, 0] == 6.5 + 3.0j