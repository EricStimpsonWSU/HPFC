"""Lightweight simulation state wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SimulationState:
    """Reference wrapper for the live `sHPFC` simulation state.

    This initial extraction keeps the arrays owned by `sHPFC` while giving the
    stepper layer a single object to depend on. The next slices can move actual
    ownership into this container without changing the stepper call sites.
    """

    sim: Any

    @classmethod
    def from_simulation(cls, sim: Any) -> "SimulationState":
        return cls(sim=sim)