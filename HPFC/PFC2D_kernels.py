"""Container for PFC dynamics in 2D."""

from __future__ import annotations

import warnings

import numpy as np

from typing import Sequence, Iterable
from PFC2D_model import model_2D
from PFC2D_geometry import geometry_2D

def _to_spacing_tuple(spacing: float | Sequence[float], ndim: int) -> tuple[float, ...]:
  if np.isscalar(spacing):
    return (float(spacing),) * ndim
  spacing_tuple = tuple(float(s) for s in spacing)
  if len(spacing_tuple) != ndim:
    raise ValueError(f"Expected {ndim} spacing values, got {len(spacing_tuple)}")
  return spacing_tuple

def _cell_volume(spacing: Iterable[float]) -> float:
  return float(np.prod(tuple(spacing)))

def _normalize_kernel_hat_mean(kernel_hat: np.ndarray) -> np.ndarray:
  dc = kernel_hat.flat[0]
  if np.abs(dc) == 0:
    raise ValueError("Kernel has zero DC mode; cannot normalize for mean preservation")
  kernel_hat = kernel_hat / dc
  kernel_hat.flat[0] = 1.0 + 0.0j
  return kernel_hat

def gaussian_kernel_fft(
  k2: np.ndarray,
  *,
  width: float | None = None,
  dtype: np.dtype = np.float64,
) -> np.ndarray:
  if width is None:
    raise ValueError("provide width for gaussian kernel")
  else:
    width = float(width)
  if width <= 0:
    raise ValueError("width must be positive")
  k2 = np.asarray(k2, dtype=dtype)
  if k2.ndim == 0:
    raise ValueError("k2 must have at least one dimension")
  kernel_hat = np.exp(-0.5 * (width * width) * k2)
  kernel_hat = np.asarray(kernel_hat, dtype=np.complex128)
  kernel_hat.flat[0] = 1.0 + 0.0j
  return kernel_hat

class kernels:
  """Stateful 2D kernels for sHPFC simulation.
  
  This class handles generation of convolution kernels for 2D PFC dynamics.
  All outputs are numpy arrays regardless of backend selection.
  """

  def __init__(
    self,
    model: model_2D,
    geometry: geometry_2D,
  ) -> None:
    self.model = model
    self.geometry = geometry
    self.KX = geometry.KX
    self.KY = geometry.KY
    self.k2 = geometry.k2
    self.k4 = self.k2**2
    self.k6 = self.k2**3

    # Derivative kernels
    self.d_dx = +1j * self.KX
    self.d_dy = +1j * self.KY
    self.d2_dlap = -self.k2
    self.d4_dlap2 = self.k4
    self.d6_dlap3 = -self.k6

    # PFC linear kernels.
    temp = self.model.temp
    beta = self.model.beta
    Gamma = self.model.Gamma
    rho0 = self.model.rho0
    Gamma_s = self.model.Gamma_s
    dt = self.model.dt

    # Linear part of  dpsi/dt in Fourier space.
    self._lin_dpsi = Gamma * (
      (temp + beta) * self.d2_dlap +
      2 * beta * self.d4_dlap2 +
      beta * self.d6_dlap3
    )    
    
    # Linear part of chemical potential kernel
    self.lin_mu_kernel = (
      (temp + beta) +
      2 * beta * self.d2_dlap +
      beta * self.d4_dlap2
    )  
    
    # Linear part of free energy kernel
    self.lin_f_kernel = (
      0.5 * beta * (self.d4_dlap2 + 2 * self.d2_dlap)
    )

    # Linear part of the velocity update kernel.
    self.lin_v_kernel = (
      (Gamma_s / rho0) * self.d2_dlap
    )

    # Gaussian kernel for smoothing the velocity field in the hydrodynamic section of the notebook.
    self.gaussian_kernel = gaussian_kernel_fft(
      k2 = self.k2,
      width = self.geometry.w
    )

    # Precompute kernels for ETD updates.
    self.lin_psi_exp = self.buildLinearETD(dt, self._lin_dpsi)
    self.nonlin_psi_exp = self.buildNonlinearETD(dt, self._lin_dpsi)

    self.lin_v_exp = self.buildLinearETD(dt, self.lin_v_kernel)
    self.nonlin_v_exp = self.buildNonlinearETD(dt, self.lin_v_kernel)

    self.buildKernelsETD(dt, Gamma)
  
  # Kernels for exponential time differencing (ETD) updates...
  def buildLinearETD(
      self,
      dt: float,
      lin_kernel: np.ndarray,
  ) -> np.ndarray:
    return np.exp(lin_kernel * dt)
  
  def buildNonlinearETD(
      self,
      dt: float,
      lin_kernel: np.ndarray,
  ) -> np.ndarray:
    nonlin_kernel = np.ones_like(lin_kernel) * dt
    nonlin_kernel[lin_kernel != 0] = (
      ( np.exp(lin_kernel[lin_kernel != 0] * dt) - 1) /
        lin_kernel[lin_kernel != 0]
    )
    return nonlin_kernel

  def buildKernelsETD(
      self,
      dt: float,
      Gamma: float,
  ) -> None:
    # ...for the linear part of the psi update.
    self.lin_dpsi_exp_kernel = np.exp(Gamma * dt * self._lin_dpsi)
    # ...for the nonlinear part of the psi update.
    self.nonlin_dpsi_kernel = np.ones_like(self.k2) * self.model.Gamma * self.model.dt
    self.nonlin_dpsi_kernel[self._lin_dpsi != 0] = (
      ( self.lin_dpsi_exp_kernel[self._lin_dpsi != 0] - 1) /
        self._lin_dpsi[self._lin_dpsi != 0]
    )
  
  # Kernels for exponential time differencing (ETD) updates...
  def buildKernelsETD(
      self,
      dt: float,
      Gamma: float,
  ) -> None:
    # ...for the linear part of the psi update.
    self.lin_dpsi_exp_kernel = np.exp(Gamma * dt * self._lin_dpsi)
    # ...for the nonlinear part of the psi update.
    self.nonlin_dpsi_kernel = np.ones_like(self.k2) * self.model.Gamma * self.model.dt
    self.nonlin_dpsi_kernel[self._lin_dpsi != 0] = (
      ( self.lin_dpsi_exp_kernel[self._lin_dpsi != 0] - 1) /
        self._lin_dpsi[self._lin_dpsi != 0]
    )
    # self.mu_dpsi_exp_kernel = np.exp(self.model.dt * (-self.k2))


class kernels_2D_CPU(kernels):
  """Deprecated compatibility shim for kernels.

  Prefer kernels for new code.
  """

  def __init__(self, *args, **kwargs) -> None:
    warnings.warn(
      "kernels_2D_CPU is deprecated and will be removed in a future "
      "release; use kernels instead.",
      DeprecationWarning,
      stacklevel=2,
    )
    super().__init__(*args, **kwargs)