from __future__ import annotations


def test_split_timestep_modules_import_and_bind(simple_model, simple_geometry, psi0, force_numpy_backend):
    from HPFC.sim_shpfc_std import make_sim as make_shpfc_sim
    from state import SimulationState
    from timestep_hydro import SHPFCTimestepper
    from timestep_std import StdPFCTimestepper

    sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)
    state = SimulationState(sim._payload_mgr, sim.model, sim.geometry, sim.kernels, psi0)

    std_stepper = StdPFCTimestepper(state)
    hydro_stepper = SHPFCTimestepper(state)

    assert hasattr(std_stepper, "step")
    assert hasattr(hydro_stepper, "step")
    assert hasattr(hydro_stepper, "step_div_vpsi")
    assert hasattr(hydro_stepper, "step_psigradmu")