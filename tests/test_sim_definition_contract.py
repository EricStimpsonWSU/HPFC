from __future__ import annotations

import builtins
import importlib
import sys

import pytest


VARIANT_SPECS = (
    ("PFC.stdPFC.sim_pfc_std", ("step",), ()),
    ("PFC.sHPFC.sim_shpfc_std", ("step", "std_step"), ("v_x", "v_y")),
    ("PFC.sHPFC.sim_shpfc_div_vpsi", ("step", "std_step"), ("v_x", "v_y", "div_vpsi_hat")),
    ("PFC.sHPFC.sim_shpfc_psigradmu", ("step", "std_step"), ("v_x", "v_y", "v_dot_grad_psi_hat")),
)


@pytest.mark.parametrize("module_path,public_methods,expected_fields", VARIANT_SPECS)
def test_canonical_sim_module_import_paths(
    module_path: str,
    public_methods: tuple[str, ...],
    expected_fields: tuple[str, ...],
) -> None:
    module = importlib.import_module(module_path)

    assert module.__name__ == module_path
    assert hasattr(module, "build_model")
    assert hasattr(module, "build_geometry")
    assert hasattr(module, "make_initial_state")
    assert hasattr(module, "make_sim")
    assert hasattr(module, "build_lin_kernels")


@pytest.mark.parametrize("module_path,public_methods,expected_fields", VARIANT_SPECS)
def test_consumer_assembly_contract_for_canonical_variants(
    module_path: str,
    public_methods: tuple[str, ...],
    expected_fields: tuple[str, ...],
    contract_model_kwargs,
    contract_geometry_kwargs,
    contract_psi0,
    force_numpy_backend,
) -> None:
    module = importlib.import_module(module_path)

    model = module.build_model(**contract_model_kwargs)
    geometry = module.build_geometry(**contract_geometry_kwargs)
    state = module.make_initial_state(contract_psi0, model=model, geometry=geometry)
    sim = module.make_sim(contract_psi0, model=model, geometry=geometry)

    assert state.model is model
    assert state.geometry is geometry
    assert state.psi.shape == contract_psi0.shape
    assert state.psi_hat.shape == contract_psi0.shape
    assert state.psi_hat_00 == pytest.approx(contract_psi0.mean() * contract_psi0.size)

    assert sim.model is model
    assert sim.geometry is geometry
    assert sim.psi.shape == contract_psi0.shape
    assert sim.backend_name in {"numpy", "cupy"}
    assert sim.backend_fft_name in {"numpy", "pyfftw", "cupy"}
    assert "arrays=" in sim.backend_summary
    assert "fft=" in sim.backend_summary
    for method_name in public_methods:
        assert hasattr(sim, method_name)
        assert callable(getattr(sim, method_name))

    for field_name in getattr(module, "BLOCKED_NAMES", ()):
        assert not hasattr(sim, field_name)

    for field_name in expected_fields:
        assert hasattr(sim, field_name)

    sim.step()

    assert sim.t == pytest.approx(contract_model_kwargs["dt"])
    assert sim.psi.shape == contract_psi0.shape
    assert sim.psi_hat.shape == contract_psi0.shape
    psi_hat_00 = sim._payload_mgr.to_numpy(sim.psi_hat[0, 0]).item()
    assert psi_hat_00 == pytest.approx(sim.psi_hat_00)

    for field_name in expected_fields:
        field_value = getattr(sim, field_name)
        assert field_value.shape == contract_psi0.shape


@pytest.mark.parametrize("module_path,public_methods,expected_fields", VARIANT_SPECS)
def test_canonical_sim_modules_do_not_import_legacy_sHPFC(
    module_path: str,
    public_methods: tuple[str, ...],
    expected_fields: tuple[str, ...],
) -> None:
    original_module = sys.modules.pop(module_path, None)
    original_sHPFC = sys.modules.pop("sHPFC", None)
    original_import = builtins.__import__

    def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "sHPFC" or name.startswith("sHPFC."):
            raise AssertionError("canonical sim modules should not import legacy sHPFC")
        return original_import(name, globals, locals, fromlist, level)

    builtins.__import__ = guarded_import
    try:
        module = importlib.import_module(module_path)
    finally:
        builtins.__import__ = original_import
        if original_module is not None:
            sys.modules[module_path] = original_module
        if original_sHPFC is not None:
            sys.modules["sHPFC"] = original_sHPFC
        else:
            sys.modules.pop("sHPFC", None)

    assert module.__name__ == module_path


def test_backend_payload_manager_is_importable_from_canonical_payload_module() -> None:
    from PFC.Core.payload import BackendPayloadManager

    assert BackendPayloadManager.__name__ == "BackendPayloadManager"


def test_make_sim_logs_backend_summary(
    contract_model_kwargs,
    contract_geometry_kwargs,
    contract_psi0,
    force_numpy_backend,
    caplog,
) -> None:
    module = importlib.import_module("PFC.stdPFC.sim_pfc_std")
    model = module.build_model(**contract_model_kwargs)
    geometry = module.build_geometry(**contract_geometry_kwargs)

    caplog.set_level("INFO")
    module.make_sim(contract_psi0, model=model, geometry=geometry)

    assert any("Created simulation with backend" in record.message for record in caplog.records)
