"""Container for PFC model parameters in 2D."""

from __future__ import annotations

import warnings


_MISSING = object()


def resolve_model_parameter(model: object, name: str):
    """Resolve a parameter from either a flat model or a nested hydro config."""

    value = getattr(model, name, _MISSING)
    if value is not _MISSING:
        return value

    hydro = getattr(model, "hydro", _MISSING)
    if hydro is not _MISSING:
        value = getattr(hydro, name, _MISSING)
        if value is not _MISSING:
            return value

    raise AttributeError(f"{type(model).__name__!s} has no attribute {name!r}")


class model_2D:
    """Backend-agnostic 2D PFC model parameters.
    
    Encapsulates thermodynamic and dynamic parameters for 2D phase-field crystal
    simulations.
    """

    def __init__(
        self,
        temp: float,
        beta: float,
        Gamma: float,
        rho0: float,
        Gamma_s: float,
        dt: float,
    ) -> None:
        # Model parameters.
        self.temp = float(temp)
        self.beta = float(beta)

        # Dynamics parameters.
        self.rho0 = float(rho0)
        self.Gamma_s = float(Gamma_s)
        self.Gamma = float(Gamma)
        self.dt = float(dt)


class model_2D_CPU(model_2D):
    """Deprecated compatibility shim for model_2D.

    Prefer model_2D for new code.
    """

    def __init__(self, *args, **kwargs) -> None:
        warnings.warn(
            "model_2D_CPU is deprecated and will be removed in a future "
            "release; use model_2D instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class model_1D:
    """Graceful stub for 1D PFC model parameters.
    
    1D simulations are not currently supported. This class exists to provide
    a clear error message when instantiation is attempted.
    """

    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "1D PFC models are not yet supported. "
            "Only 2D models are currently available. "
            "Use model_2D instead."
        )


class model_3D:
    """Graceful stub for 3D PFC model parameters.
    
    3D simulations are not currently supported. This class exists to provide
    a clear error message when instantiation is attempted.
    """

    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "3D PFC models are not yet supported. "
            "Only 2D models are currently available. "
            "Use model_2D instead."
        )
