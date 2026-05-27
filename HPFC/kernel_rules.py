"""Kernel and ETD rule provider for 2D PFC dynamics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np

from PFC2D_geometry import geometry_2D
from PFC2D_model import model_2D, resolve_model_parameter
import importlib
from types import ModuleType


def _to_spacing_tuple(spacing: float | Sequence[float], ndim: int) -> tuple[float, ...]:
    if np.isscalar(spacing):
        value = float(spacing)
        return (value,) * int(ndim)
    values = tuple(float(value) for value in spacing)
    if len(values) != int(ndim):
        raise ValueError(f"Expected {ndim} spacing values")
    return values


def _cell_volume(spacing: float | Sequence[float]) -> float:
    spacing_tuple = _to_spacing_tuple(spacing, 2)
    return float(np.prod(np.asarray(spacing_tuple, dtype=np.float64)))


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


@dataclass(slots=True)
class KernelRules:
    model: model_2D
    geometry: geometry_2D

    KX: np.ndarray = field(init=False)
    KY: np.ndarray = field(init=False)
    k2: np.ndarray = field(init=False)
    k4: np.ndarray = field(init=False)
    k6: np.ndarray = field(init=False)
    d_dx: np.ndarray = field(init=False)
    d_dy: np.ndarray = field(init=False)
    d2_dlap: np.ndarray = field(init=False)
    d4_dlap2: np.ndarray = field(init=False)
    d6_dlap3: np.ndarray = field(init=False)
    lin_dpsi: np.ndarray = field(init=False)
    lin_mu_kernel: np.ndarray = field(init=False)
    lin_f_kernel: np.ndarray = field(init=False)
    lin_v_kernel: np.ndarray = field(init=False)
    gaussian_kernel: np.ndarray = field(init=False)
    lin_psi_exp: np.ndarray = field(init=False)
    nonlin_psi_exp: np.ndarray = field(init=False)
    lin_v_exp: np.ndarray = field(init=False)
    nonlin_v_exp: np.ndarray = field(init=False)
    lin_dpsi_exp_kernel: np.ndarray = field(init=False)
    nonlin_dpsi_kernel: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        self.KX = self.geometry.KX
        self.KY = self.geometry.KY
        self.k2 = self.geometry.k2
        self.k4 = self.k2**2
        self.k6 = self.k2**3

        self.d_dx = +1j * self.KX
        self.d_dy = +1j * self.KY
        self.d2_dlap = -self.k2
        self.d4_dlap2 = self.k4
        self.d6_dlap3 = -self.k6

        # Delegate model-specific linear kernel construction to the simulation module
        # Prefer a `build_lin_kernels(model, geometry)` exported by the sim module
        # (e.g. HPFC.sim_pfc_std, HPFC.sim_shpfc_*) and fall back to the
        # legacy `sim_kernels.build_lin_kernels` provider for compatibility.
        sim_build = None
        try:
            sim_mod_name = getattr(self.model.__class__, "__module__", None)
            if sim_mod_name:
                sim_mod = importlib.import_module(sim_mod_name)
                sim_build = getattr(sim_mod, "build_lin_kernels", None)
        except Exception:
            sim_build = None

        if sim_build is None:
            from sim_kernels import build_lin_kernels as sim_build

        dt = self.model.dt
        gamma = self.model.Gamma
        self.lin_dpsi, self.lin_mu_kernel, self.lin_f_kernel, self.lin_v_kernel = sim_build(
            self.model, self.geometry
        )

        self.gaussian_kernel = gaussian_kernel_fft(self.k2, width=self.geometry.w)

        self.lin_psi_exp = self.buildLinearETD(dt, self.lin_dpsi)
        self.nonlin_psi_exp = self.buildNonlinearETD(dt, self.lin_dpsi)
        self.lin_v_exp = self.buildLinearETD(dt, self.lin_v_kernel)
        self.nonlin_v_exp = self.buildNonlinearETD(dt, self.lin_v_kernel)

        self.buildKernelsETD(dt=dt, Gamma=gamma)

    @staticmethod
    def buildLinearETD(
        dt: float,
        lin_kernel: np.ndarray,
    ) -> np.ndarray:
        return np.exp(lin_kernel * dt)

    @staticmethod
    def buildNonlinearETD(
        dt: float,
        lin_kernel: np.ndarray,
    ) -> np.ndarray:
        nonlin_kernel = np.ones_like(lin_kernel) * dt
        nonlin_kernel[lin_kernel != 0] = (
            (np.exp(lin_kernel[lin_kernel != 0] * dt) - 1) /
            lin_kernel[lin_kernel != 0]
        )
        return nonlin_kernel

    def buildKernelsETD(
        self,
        dt: float,
        Gamma: float,
    ) -> None:
        self.lin_dpsi_exp_kernel = np.exp(Gamma * dt * self.lin_dpsi)
        self.nonlin_dpsi_kernel = np.ones_like(self.k2) * self.model.Gamma * self.model.dt
        self.nonlin_dpsi_kernel[self.lin_dpsi != 0] = (
            (self.lin_dpsi_exp_kernel[self.lin_dpsi != 0] - 1) /
            self.lin_dpsi[self.lin_dpsi != 0]
        )