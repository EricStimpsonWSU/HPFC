from __future__ import annotations

from dataclasses import dataclass
import importlib

import numpy as np
import pytest


@dataclass(frozen=True)
class HydroModelConfig:
    rho0: float
    Gamma_s: float


@dataclass(frozen=True)
class SimpleModelContainer:
    temp: float
    beta: float
    Gamma: float
    dt: float
    rho0: float
    Gamma_s: float


def _build_small_psi0() -> np.ndarray:
    grid = np.arange(16, dtype=np.float64).reshape(4, 4)
    return 0.05 * (grid - grid.mean())


def test_minimal_model_container_shape_exposes_shared_and_namespaced_settings() -> None:
    model = SimpleModelContainer(
        temp=-0.25,
        beta=1.5,
        Gamma=1.0,
        dt=0.05,
        rho0=1.0,
        Gamma_s=0.75,
    )

    assert model.temp == -0.25
    assert model.beta == 1.5
    assert model.Gamma == 1.0
    assert model.dt == 0.05
    assert model.rho0 == 1.0
    assert model.Gamma_s == 0.75


@pytest.mark.parametrize("module_path", ("PFC.stdPFC.sim_pfc_std", "PFC.sHPFC.sim_shpfc_std"))
def test_existing_sim_assembly_can_consume_minimal_model_container(module_path: str) -> None:
    module = importlib.import_module(module_path)
    model = SimpleModelContainer(
        temp=-0.25,
        beta=1.5,
        Gamma=1.0,
        dt=0.05,
        rho0=1.0,
        Gamma_s=0.75,
    )
    geometry = module.build_geometry(shape=(4, 4), Lx=8.0, Ly=8.0)
    psi0 = _build_small_psi0()

    state = module.make_initial_state(psi0, model=model, geometry=geometry)
    sim = module.make_sim(psi0, model=model, geometry=geometry)

    assert state.model is model
    assert state.geometry is geometry
    assert state.psi.shape == psi0.shape

    assert sim.model is model
    assert sim.geometry is geometry
    assert sim.psi.shape == psi0.shape