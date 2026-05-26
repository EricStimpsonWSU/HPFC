from __future__ import annotations

import pytest

from state import SimulationState
from steppers import SHPFCTimestepper, StdPFCTimestepper


def test_state_wrapper_and_std_stepper_delegate_to_simulation(simple_model, simple_geometry, psi0, force_numpy_backend):
    from sHPFC import sHPFC

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)

    state = SimulationState.from_simulation(sim)
    assert state.sim is sim

    stepper = StdPFCTimestepper(state)
    t0 = sim.t

    stepper.step()

    assert sim.t == pytest.approx(t0 + sim.model.dt)


def test_hydro_stepper_variants_advance_time(simple_model, simple_geometry, psi0, force_numpy_backend):
    from sHPFC import sHPFC

    sim = sHPFC(psi0, model=simple_model, geometry=simple_geometry)
    state = SimulationState.from_simulation(sim)
    stepper = SHPFCTimestepper(state)

    t0 = sim.t
    stepper.step_div_vpsi()
    assert sim.t == pytest.approx(t0 + sim.model.dt)

    t1 = sim.t
    stepper.step_psigradmu()
    assert sim.t == pytest.approx(t1 + sim.model.dt)