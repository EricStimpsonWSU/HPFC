"""CPU simulation container for 2D geometry."""

from __future__ import annotations

import warnings

import numpy as np


class geometry_2D:
	def __init__(self, shape: tuple[int, int], Lx: float, Ly: float) -> None:
		self.shape = shape
		self.Lx = float(Lx)
		self.Ly = float(Ly)
		self.dx = Lx / shape[0]
		self.dy = Ly / shape[1]
		self.x = np.linspace(0, Lx, shape[0], endpoint=False)
		self.y = np.linspace(0, Ly, shape[1], endpoint=False)
		self.X, self.Y = np.meshgrid(self.x, self.y)
		self.kx = 2 * np.pi * np.fft.fftfreq(shape[0], d=self.dx)
		self.ky = 2 * np.pi * np.fft.fftfreq(shape[1], d=self.dy)
		self.KX, self.KY = np.meshgrid(self.kx, self.ky)
		self.k2 = self.KX**2 + self.KY**2
		self.w = 2 * np.pi


class geometry_2D_CPU(geometry_2D):
	def __init__(self, *args, **kwargs) -> None:
		warnings.warn(
			"geometry_2D_CPU is deprecated and will be removed in a future release; use geometry_2D instead.",
			DeprecationWarning,
			stacklevel=2,
		)
		super().__init__(*args, **kwargs)


class geometry_1D:
	def __init__(self, *args, **kwargs) -> None:
		raise NotImplementedError(
			"1D geometry is not yet supported. Only 2D geometry is currently available. Use geometry_2D instead."
		)


class geometry_3D:
	def __init__(self, *args, **kwargs) -> None:
		raise NotImplementedError(
			"3D geometry is not yet supported. Only 2D geometry is currently available. Use geometry_2D instead."
		)
