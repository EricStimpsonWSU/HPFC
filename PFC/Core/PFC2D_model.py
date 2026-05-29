"""Container for PFC model parameters in 2D."""

from __future__ import annotations

import warnings


_MISSING = object()


def resolve_model_parameter(model: object, name: str):
	value = getattr(model, name, _MISSING)
	if value is not _MISSING:
		return value
	raise AttributeError(f"{type(model).__name__!s} has no attribute {name!r}")


class model_2D:
	def __init__(self, temp: float, beta: float, Gamma: float, rho0: float, Gamma_s: float, dt: float) -> None:
		self.temp = float(temp)
		self.beta = float(beta)
		self.rho0 = float(rho0)
		self.Gamma_s = float(Gamma_s)
		self.Gamma = float(Gamma)
		self.dt = float(dt)


class model_2D_CPU(model_2D):
	def __init__(self, *args, **kwargs) -> None:
		warnings.warn(
			"model_2D_CPU is deprecated and will be removed in a future release; use model_2D instead.",
			DeprecationWarning,
			stacklevel=2,
		)
		super().__init__(*args, **kwargs)


class model_1D:
	def __init__(self, *args, **kwargs) -> None:
		raise NotImplementedError(
			"1D PFC models are not yet supported. Only 2D models are currently available. Use model_2D instead."
		)


class model_3D:
	def __init__(self, *args, **kwargs) -> None:
		raise NotImplementedError(
			"3D PFC models are not yet supported. Only 2D models are currently available. Use model_2D instead."
		)
