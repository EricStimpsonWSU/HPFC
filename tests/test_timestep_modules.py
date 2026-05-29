from __future__ import annotations


def test_split_timestep_modules_import_and_bind(simple_model, simple_geometry, psi0, force_numpy_backend):
    from PFC.stdPFC.sim_pfc_std import make_sim as make_std_sim
    from PFC.sHPFC.sim_shpfc_std import make_sim as make_shpfc_sim
    from PFC.sHPFC.sim_shpfc_div_vpsi import make_sim as make_div_sim
    from PFC.sHPFC.sim_shpfc_psigradmu import make_sim as make_psigradmu_sim

    std_sim = make_std_sim(psi0, model=simple_model, geometry=simple_geometry)
    shpfc_sim = make_shpfc_sim(psi0, model=simple_model, geometry=simple_geometry)
    div_sim = make_div_sim(psi0, model=simple_model, geometry=simple_geometry)
    gradmu_sim = make_psigradmu_sim(psi0, model=simple_model, geometry=simple_geometry)

    assert hasattr(std_sim, "step")
    assert hasattr(shpfc_sim, "step")
    assert hasattr(shpfc_sim, "std_step")
    assert hasattr(div_sim, "step")
    assert hasattr(div_sim, "std_step")
    assert hasattr(gradmu_sim, "step")
    assert hasattr(gradmu_sim, "std_step")