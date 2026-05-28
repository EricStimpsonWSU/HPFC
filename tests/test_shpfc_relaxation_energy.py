from __future__ import annotations

import math

import numpy as np
import pytest

from PFC2D_geometry import geometry_2D
from PFC2D_model import model_2D
from HPFC.sim_shpfc_std import make_sim as make_shpfc_sim


def _build_notebook_like_crystal_field(*, Mx: int = 8, My: int = 5, target_dx: float = 0.5):
    q1 = np.array([-3**0.5 / 2, -0.5])
    q2 = np.array([3**0.5 / 2, -0.5])
    q3 = np.array([0.0, 1.0])

    a = 4 * np.pi / 3**0.5
    h = 4 * np.pi

    psi_mean = -0.265
    A0 = 0.3162

    Lx = a * Mx
    Ly = h * My

    Nx = max(8, int(round(Lx / target_dx)))
    Ny = max(8, int(round(Ly / target_dx)))

    x = np.linspace(0.0, Lx, Nx, endpoint=False)
    y = np.linspace(0.0, Ly, Ny, endpoint=False)
    X, Y = np.meshgrid(x, y)

    psi = (
        psi_mean
        + A0 * np.exp(1j * (q1[0] * X + q1[1] * Y))
        + A0 * np.exp(-1j * (q1[0] * X + q1[1] * Y))
        + A0 * np.exp(1j * (q2[0] * X + q2[1] * Y))
        + A0 * np.exp(-1j * (q2[0] * X + q2[1] * Y))
        + A0 * np.exp(1j * (q3[0] * X + q3[1] * Y))
        + A0 * np.exp(-1j * (q3[0] * X + q3[1] * Y))
    ).real

    return psi, X, Y, Lx, Ly, Nx, Ny, psi_mean, (q1, q2, q3)


def _build_model(*, dt: float = 0.1) -> model_2D:
    return model_2D(
        temp=-0.2,
        beta=1.0,
        Gamma=1.0,
        rho0=2.0 ** (-6),
        Gamma_s=2.0 ** (-6),
        dt=dt,
    )


def _phase_energies(sim: sHPFC, stepper_name: str, *, frames: int = 3, sample_every: int = 10) -> list[float]:
    energies: list[float] = []
    sim.calc_f()
    energies.append(float(np.mean(sim._payload_mgr.to_numpy(sim.f))))

    stepper = getattr(sim, stepper_name)
    for _ in range(frames):
        for _ in range(sample_every):
            stepper()
        sim.calc_f()
        energies.append(float(np.mean(sim._payload_mgr.to_numpy(sim.f))))

    return energies


def _assert_nonincreasing(values: list[float], *, atol: float = 5e-8, rtol: float = 1e-9) -> None:
    arr = np.asarray(values, dtype=np.float64)
    deltas = np.diff(arr)
    tol = atol + rtol * np.maximum(1.0, np.abs(arr[:-1]))
    if np.any(deltas > tol):
        i = int(np.argmax(deltas - tol))
        raise AssertionError(
            f"Energy increased at sample {i}->{i+1}: "
            f"prev={arr[i]:.12e}, next={arr[i+1]:.12e}, delta={deltas[i]:.12e}, tol={tol[i]:.12e}"
        )


@pytest.mark.parametrize(
    "stepper_name",
    [
        "Timestep_stdPFC",
        "Timestep_sHPFC",
        "Timestep_sHPFC_div_vpsi",
        "Timestep_sHPFC_psigradmu",
    ],
)
def test_relaxation_energy_monotone_two_phase_for_timestep_variants(stepper_name: str, force_numpy_backend):
    psi, X, Y, Lx, Ly, Nx, Ny, psi_mean, q_vecs = _build_notebook_like_crystal_field(Mx=8, My=5, target_dx=0.5)

    model = _build_model(dt=0.1)
    geometry = geometry_2D((Nx, Ny), Lx, Ly)
    if stepper_name == "Timestep_stdPFC":
        from HPFC.sim_pfc_std import make_sim as make_std_sim

        sim = make_std_sim(psi0=psi, model=model, geometry=geometry)
    elif stepper_name == "Timestep_sHPFC":
        sim = make_shpfc_sim(psi0=psi, model=model, geometry=geometry)
    elif stepper_name == "Timestep_sHPFC_div_vpsi":
        from HPFC.sim_shpfc_div_vpsi import make_sim as make_div_sim

        sim = make_div_sim(psi0=psi, model=model, geometry=geometry)
    else:
        from HPFC.sim_shpfc_psigradmu import make_sim as make_psigradmu_sim

        sim = make_psigradmu_sim(psi0=psi, model=model, geometry=geometry)

    # Pass 1: compact refinement pass (30 total steps sampled every 10)
    energies_phase1 = _phase_energies(sim, stepper_name, frames=3, sample_every=10)
    _assert_nonincreasing(energies_phase1)

    # Approximate notebook-style amplitude refinement
    psi_after = sim._payload_mgr.to_numpy(sim.psi)
    A0_star = float((psi_after.max() - psi_after.min()) / 9.0)

    q1, q2, q3 = q_vecs
    psi_refined = (
        psi_mean
        + A0_star * np.exp(1j * (q1[0] * X + q1[1] * Y))
        + A0_star * np.exp(-1j * (q1[0] * X + q1[1] * Y))
        + A0_star * np.exp(1j * (q2[0] * X + q2[1] * Y))
        + A0_star * np.exp(-1j * (q2[0] * X + q2[1] * Y))
        + A0_star * np.exp(1j * (q3[0] * X + q3[1] * Y))
        + A0_star * np.exp(-1j * (q3[0] * X + q3[1] * Y))
    ).real

    # Pass 2: compact stable-amplitude pass (30 total steps sampled every 10)
    if stepper_name == "Timestep_stdPFC":
        sim2 = make_std_sim(psi0=psi_refined, model=_build_model(dt=0.1), geometry=geometry_2D((Nx, Ny), Lx, Ly))
    elif stepper_name == "Timestep_sHPFC":
        sim2 = make_shpfc_sim(psi0=psi_refined, model=_build_model(dt=0.1), geometry=geometry_2D((Nx, Ny), Lx, Ly))
    elif stepper_name == "Timestep_sHPFC_div_vpsi":
        sim2 = make_div_sim(psi0=psi_refined, model=_build_model(dt=0.1), geometry=geometry_2D((Nx, Ny), Lx, Ly))
    else:
        sim2 = make_psigradmu_sim(psi0=psi_refined, model=_build_model(dt=0.1), geometry=geometry_2D((Nx, Ny), Lx, Ly))
    energies_phase2 = _phase_energies(sim2, stepper_name, frames=3, sample_every=10)
    _assert_nonincreasing(energies_phase2)
