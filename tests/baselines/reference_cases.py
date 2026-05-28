from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sys
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PFC.Core import backend
from PFC.Core.PFC2D_geometry import geometry_2D
from PFC.stdPFC.sim_pfc_std import build_model as _build_std_model, make_sim as _make_std_sim
from PFC.sHPFC.sim_shpfc_std import build_model as _build_shpfc_std_model, make_sim as _make_shpfc_std_sim
from PFC.sHPFC.sim_shpfc_div_vpsi import build_model as _build_shpfc_div_model, make_sim as _make_shpfc_div_sim
from PFC.sHPFC.sim_shpfc_psigradmu import build_model as _build_shpfc_psigradmu_model, make_sim as _make_shpfc_psigradmu_sim


MODEL_KWARGS = {
    "temp": -0.25,
    "beta": 1.5,
    "Gamma": 1.0,
    "rho0": 1.0,
    "Gamma_s": 0.75,
    "dt": 0.05,
}

GEOMETRY_KWARGS = {
    "shape": (4, 4),
    "Lx": 8.0,
    "Ly": 8.0,
}

PSI0 = 0.1 * np.arange(16, dtype=np.float64).reshape(4, 4)

VARIANT_METHODS = {
    "stdPFC": "Timestep_stdPFC",
    "sHPFC": "Timestep_sHPFC",
    "sHPFC_div_vpsi": "Timestep_sHPFC_div_vpsi",
    "sHPFC_psigradmu": "Timestep_sHPFC_psigradmu",
}

STEP_COUNTS = (1, 2, 5)


@contextmanager
def backend_override(mode: str):
    if mode == "gpu":
        selected_backend = backend._resolve_cupy_backend()
        if selected_backend is None:
            raise RuntimeError("gpu baseline mode requires a working CuPy backend")
    else:
        selected_backend = backend._resolve_numpy_backend()

    original_resolve_backend = backend.resolve_backend
    backend.resolve_backend = lambda *args, **kwargs: selected_backend
    try:
        yield
    finally:
        backend.resolve_backend = original_resolve_backend


def build_simulation(variant: str = "stdPFC", *, backend_mode: str = "cpu"):
    with backend_override(backend_mode):
        if variant == "stdPFC":
            model = _build_std_model(**MODEL_KWARGS)
            make_sim = _make_std_sim
        elif variant == "sHPFC":
            model = _build_shpfc_std_model(**MODEL_KWARGS)
            make_sim = _make_shpfc_std_sim
        elif variant == "sHPFC_div_vpsi":
            model = _build_shpfc_div_model(**MODEL_KWARGS)
            make_sim = _make_shpfc_div_sim
        elif variant == "sHPFC_psigradmu":
            model = _build_shpfc_psigradmu_model(**MODEL_KWARGS)
            make_sim = _make_shpfc_psigradmu_sim
        else:
            model = _build_std_model(**MODEL_KWARGS)
            make_sim = _make_std_sim
        geometry = geometry_2D(**GEOMETRY_KWARGS)
        return make_sim(PSI0.copy(), model=model, geometry=geometry)


def run_variant(variant: str, steps: int, *, backend_mode: str = "cpu") -> sHPFC:
    simulation = build_simulation(variant, backend_mode=backend_mode)
    timestep_method_name = VARIANT_METHODS[variant]
    timestep_method = getattr(simulation, timestep_method_name)
    for _ in range(steps):
        timestep_method()
    return simulation


def _to_numpy(simulation: sHPFC, value):
    return simulation._payload_mgr.to_numpy(value)


def collect_snapshot(simulation: sHPFC, variant: str, steps: int) -> dict[str, np.ndarray | float | str | int]:
    snapshot: dict[str, np.ndarray | float | str | int] = {
        "variant": variant,
        "steps": int(steps),
        "t": float(simulation.t),
        "psi_hat_00": float(simulation.psi_hat_00),
        "psi": np.array(_to_numpy(simulation, simulation.psi), copy=True),
        "psi_hat": np.array(_to_numpy(simulation, simulation.psi_hat), copy=True),
    }

    if variant != "stdPFC":
        snapshot["v_x"] = np.array(_to_numpy(simulation, simulation.v_x), copy=True)
        snapshot["v_y"] = np.array(_to_numpy(simulation, simulation.v_y), copy=True)

    if variant == "sHPFC_div_vpsi":
        snapshot["div_vpsi_hat"] = np.array(_to_numpy(simulation, simulation.div_vpsi_hat), copy=True)
    elif variant == "sHPFC_psigradmu":
        snapshot["v_dot_grad_psi_hat"] = np.array(_to_numpy(simulation, simulation.v_dot_grad_psi_hat), copy=True)

    return snapshot


def snapshot_to_npy_payload(snapshot: dict[str, np.ndarray | float | str | int]) -> dict[str, np.ndarray]:
    payload: dict[str, np.ndarray] = {}
    for key, value in snapshot.items():
        if isinstance(value, np.ndarray):
            payload[key] = value
        elif isinstance(value, str):
            payload[key] = np.array(value)
        else:
            payload[key] = np.array(value)
    return payload


def assert_snapshots_equivalent(
    first: dict[str, np.ndarray | float | str | int],
    second: dict[str, np.ndarray | float | str | int],
    *,
    rtol: float = 1e-7,
    atol: float = 1e-9,
) -> None:
    for key, first_value in first.items():
        if key not in second:
            raise AssertionError(f"missing key in parity snapshot: {key}")
        second_value = second[key]
        if isinstance(first_value, np.ndarray):
            np.testing.assert_allclose(first_value, second_value, rtol=rtol, atol=atol)
        elif isinstance(first_value, float):
            np.testing.assert_allclose(np.array([first_value]), np.array([float(second_value)]), rtol=rtol, atol=atol)
        else:
            if first_value != second_value:
                raise AssertionError(f"snapshot mismatch at key={key}: {first_value!r} != {second_value!r}")


def baseline_filename(variant: str, steps: int) -> str:
    return f"{variant}_steps_{steps}.npz"


def baseline_paths(output_dir: Path) -> Iterable[tuple[str, int, Path]]:
    for variant in VARIANT_METHODS:
        for steps in STEP_COUNTS:
            yield variant, steps, output_dir / baseline_filename(variant, steps)


def generate_baselines(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written_paths: list[Path] = []
    for variant, steps, path in baseline_paths(output_dir):
        cpu_sim = run_variant(variant, steps, backend_mode="cpu")
        gpu_sim = run_variant(variant, steps, backend_mode="gpu")
        cpu_snapshot = collect_snapshot(cpu_sim, variant, steps)
        gpu_snapshot = collect_snapshot(gpu_sim, variant, steps)
        assert_snapshots_equivalent(cpu_snapshot, gpu_snapshot)
        np.savez_compressed(path, **snapshot_to_npy_payload(cpu_snapshot))
        written_paths.append(path)
    return written_paths


def load_snapshot(path: Path) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as data:
        return {key: data[key] for key in data.files}
