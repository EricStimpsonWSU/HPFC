"""Canonical simulation definition surface for standard hydrodynamic PFC (hPFC).

This variant implements the linear part of the "Consistent Hydrodynamics for Phase
Field Crystals" model (excluding amplitude expansion), with:

    ∂t ψ = Γ_ρ ∇² ( μ + ½ α |v|² ) - Γ_J ∇·(ψ v)
    ρ₀ ∂t v = ⟨ - ψ ∇ μ ⟩ + Γ_S ∇² v - ρ₀ v (∇·v)
    μ = (∇² + q₀²)² ψ + r ψ + g ψ² + v₀ ψ³

The linear kernels here correspond to:

    μ_lin = [(∇² + q₀²)² + r] ψ
    (∂t ψ)_lin = Γ_ρ ∇² μ_lin
    (∂t v)_lin = (Γ_S / ρ₀) ∇² v

Nonlinear terms (g ψ², v₀ ψ³, ψ·∇μ, |v|², etc.) are handled in the timestepper.
"""

from __future__ import annotations

import logging
import numpy as np

from PFC.Core.PFC2D_geometry import geometry_2D
from PFC.Core.PFC2D_model import model_2D
from PFC.Core.kernel_rules import KernelRules
from PFC.Core._simulation_facade import VariantSimulationFacade
from PFC.Core.payload import BackendPayloadManager
from PFC.Core.state import SimulationState
from PFC.Core.steppers import SHPFCTimestepper, StdPFCTimestepper


LOGGER = logging.getLogger(__name__)

# Block all other timestep variants; this file defines the canonical hPFC surface.
BLOCKED_NAMES = {
    "Timestep_stdPFC",
    "Timestep_sHPFC",
    "Timestep_sHPFC_div_vpsi",
    "Timestep_sHPFC_psigradmu",
}


def build_lin_kernels(model: model_2D, geometry: geometry_2D):
    """Build linear kernels for the hPFC variant.

    Uses the final equations:

        μ = (∇² + q₀²)² ψ + r ψ + g ψ² + v₀ ψ³
        (∂t ψ)_lin = Γ_ρ ∇² μ_lin
        (∂t v)_lin = (Γ_S / ρ₀) ∇² v

    Here we construct only the linear parts in Fourier space.
    """
    # Parameters (attached by build_model below)
    r = model.r
    q0 = model.q0
    Gamma_rho = model.Gamma_rho
    Gamma_S = model.Gamma_S
    rho0 = model.rho0

    k2 = geometry.k2
    lap = -k2  # ∇² → -k² in Fourier space

    # Linear chemical potential operator:
    #   μ_lin = [(∇² + q₀²)² + r] ψ
    # In k-space: ( -k² + q₀² )² + r
    lin_mu_kernel = (lap + q0**2) ** 2 + r

    # Linear part of ψ dynamics:
    #   (∂t ψ)_lin = Γ_ρ ∇² μ_lin
    # In k-space: Γ_ρ (-k²) * lin_mu_kernel
    lin_dpsi = Gamma_rho * lap * lin_mu_kernel

    # For this hPFC variant, the "force" kernel used in other models is not
    # directly needed in the same way; we keep a placeholder zero kernel so
    # that the Core/state machinery remains satisfied.
    lin_f_kernel = np.zeros_like(k2, dtype=np.float64)

    # Linear velocity kernel:
    #   ρ₀ ∂t v = Γ_S ∇² v  →  (∂t v)_lin = (Γ_S / ρ₀) ∇² v
    # In k-space: (Γ_S / ρ₀) (-k²)
    lin_v_kernel = (Gamma_S / rho0) * lap

    return lin_dpsi, lin_mu_kernel, lin_f_kernel, lin_v_kernel


def build_model(
    *,
    r: float,
    g: float,
    v0: float,
    q0: float,
    Gamma_rho: float,
    Gamma_J: float,
    Gamma_S: float,
    rho0: float,
    alpha: float,
    dt: float,
) -> model_2D:
    """Build the hPFC model container.

    We reuse Core.model_2D for compatibility with KernelRules and SimulationState,
    but reinterpret its fields and attach hPFC-specific parameters explicitly.

    Mapping:
        temp   → r
        beta   → g
        Gamma  → Γ_ρ
        rho0   → ρ₀
        Gamma_s → Γ_S
    """
    base = model_2D(
        temp=r,
        beta=g,
        Gamma=Gamma_rho,
        rho0=rho0,
        Gamma_s=Gamma_S,
        dt=dt,
    )

    # Attach hPFC-specific parameters directly on the base model object so
    # callers can access them as `model.r`, `model.q0`, etc.
    base.r = r
    base.g = g
    base.v0 = v0
    base.q0 = q0
    base.Gamma_rho = Gamma_rho
    base.Gamma_J = Gamma_J
    base.Gamma_S = Gamma_S
    base.alpha = alpha

    return base


def build_geometry(*, shape: tuple[int, int], Lx: float, Ly: float) -> geometry_2D:
    """Build 2D geometry for the hPFC simulation."""
    return geometry_2D(shape=shape, Lx=Lx, Ly=Ly)


def make_initial_state(
    psi0: np.ndarray,
    *,
    model: model_2D,
    geometry: geometry_2D,
    payload_mgr: BackendPayloadManager | None = None,
) -> SimulationState:
    """Construct the initial SimulationState for hPFC."""
    payload_mgr = payload_mgr or BackendPayloadManager()
    kernels = KernelRules(model=model, geometry=geometry)
    return SimulationState(payload_mgr, model, geometry, kernels, psi0)


def make_sim(psi0: np.ndarray, *, model: model_2D, geometry: geometry_2D) -> VariantSimulationFacade:
    """Create a canonical hPFC simulation object.

    Exposes:
        - Timestep_hPFC()

    Blocks:
        - stdPFC and other sHPFC timestep variants via BLOCKED_NAMES.
    """
    state = make_initial_state(psi0, model=model, geometry=geometry)

    class _SimImpl:
        def __init__(self, state: SimulationState):
            self.state = state
            self.model = state.model
            self.geometry = state.geometry

            # Standard and hydrodynamic steppers; hPFC uses the hydrodynamic one.
            self.std_stepper = StdPFCTimestepper(self.state)
            self.shpfc_stepper = SHPFCTimestepper(self.state)

            backend_info = self.state._payload_mgr.backend
            self.backend_name = backend_info.name
            self.backend_fft_name = backend_info.fft_name
            self.backend_summary = backend_info.summary()
            self.backend_is_gpu = backend_info.is_gpu

            LOGGER.info("Created hPFC simulation with backend %s", self.backend_summary)

        def __getattr__(self, name: str):
            return getattr(self.state, name)

        def Timestep_hPFC(self) -> None:
            """Advance one timestep of the hPFC dynamics."""
            # For now we reuse the SHPFCTimestepper; in a dedicated hPFC
            # implementation this would be replaced with an hPFC-specific
            # timestepper that uses Γ_ρ, Γ_J, Γ_S, α, etc. explicitly.
            self.shpfc_stepper.step()

    return VariantSimulationFacade(_SimImpl(state), blocked_names=BLOCKED_NAMES)
