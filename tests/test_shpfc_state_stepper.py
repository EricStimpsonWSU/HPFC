from __future__ import annotations

import pytest

from state import SimulationState
from steppers import SHPFCTimestepper, StdPFCTimestepper


def test_state_wrapper_and_std_stepper_delegate_to_simulation(simple_model, simple_geometry, psi0, force_numpy_backend):
    from HPFC.sim_shpfc_std import make_sim as make_shpfc_sim

    sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)

    state = SimulationState(sim._payload_mgr, sim.model, sim.geometry, sim.kernels, psi0)
    assert state.psi.shape == psi0.shape
    assert state.kernel_d_dx.shape == psi0.shape

    stepper = StdPFCTimestepper(state)
    t0 = state.t

    stepper.step()

    assert state.t == pytest.approx(t0 + state.model.dt)


def test_hydro_stepper_variants_advance_time(simple_model, simple_geometry, psi0, force_numpy_backend):
    from HPFC.sim_shpfc_std import make_sim as make_shpfc_sim

    sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)
    state = SimulationState(sim._payload_mgr, sim.model, sim.geometry, sim.kernels, psi0)
    stepper = SHPFCTimestepper(state)

    t0 = state.t
    stepper.step_div_vpsi()
    assert state.t == pytest.approx(t0 + state.model.dt)

    t1 = state.t
    stepper.step_psigradmu()
    assert state.t == pytest.approx(t1 + state.model.dt)