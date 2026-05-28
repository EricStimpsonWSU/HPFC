from __future__ import annotations


def test_backend_mode_option_is_supported(pytestconfig) -> None:
    assert pytestconfig.getoption("--backend-mode") in {"cpu", "gpu", "both"}


def test_force_numpy_backend_honors_requested_mode(force_numpy_backend, backend_target: str) -> None:
    expected_backend = "cupy" if backend_target == "gpu" else "numpy"
    assert force_numpy_backend.name == expected_backend
