"""Backend-aware sHPFC simulation container (CPU/GPU unified).

This module implements the sHPFC layer responsible for owning FFT payload arrays
and routing all FFT operations through the backend adapter from backend.py.
This design enables seamless CPU/GPU execution with identical code.

Supported Configuration (2D):
  - Uses model_2D and geometry_2D as inputs (backend-agnostic)
  - Kernels (from PFC2D_kernels) are NumPy arrays that are converted to the
    active backend namespace during initialization for efficient math
  - All FFT/IFFT calls routed through BackendPayloadManager adapter
  - Supports both NumPy and CuPy backends transparently
  
Key Design Points:
  - Backend choice is made in sHPFC.__init__, not in kernels or geometry
  - Kernel location: Gaussian kernel is in PFC2D_kernels.gaussian_kernel_fft
    (formerly in convolution.py; moved during PR-3)
  - No direct imports of convolution module; all FFTs use backend adapter
  - K-space geometry arrays (KX, KY, k2) are stored as self attributes
    after conversion to backend arrays to avoid mixing NumPy/CuPy arrays

Methods:
  - calc_mu(psi_hat_is_current): compute chemical potential
  - calc_f(psi_hat_is_current): compute free energy density
  - Timestep_stdPFC(): standard phase-field crystal timestep (2D)
  - Timestep_sHPFC(): hydrodynamic phase-field crystal timestep (2D)

Example:
  from PFC2D_model import model_2D
  from PFC2D_geometry import geometry_2D
  from sHPFC import sHPFC
  import numpy as np

  model = model_2D(temp=-0.3, beta=1.0, dt=0.01, Gamma=1.0, rho0=1.0, Gamma_s=1.0)
  geometry = geometry_2D(shape=(64, 64), Lx=L, Ly=L)
  psi0 = np.random.randn(64, 64) * 0.1
  
  sim = sHPFC(psi0, model=model, geometry=geometry)
  for i in range(1000):
    sim.Timestep_sHPFC()
    # Access: sim.psi, sim.mu, sim.f, sim.v_x, sim.v_y, sim.div_v, etc.
"""

from __future__ import annotations

import numpy as np

import backend
from PFC2D_model import model_2D
from PFC2D_geometry import geometry_2D
from kernel_rules import KernelRules
from state import SimulationState
from steppers import SHPFCTimestepper, StdPFCTimestepper


class BackendPayloadManager:
  """Manages FFT operations and array allocation via backend adapter.

  This class abstracts all low-level FFT and array operations so sHPFC
  can work transparently with NumPy (CPU) or CuPy (GPU) arrays.
  
  The manager provides:
    - FFT wrappers (fftn, ifftn) that delegate to the active backend
    - Array allocation helpers (zeros, empty, asarray) that use backend
    - Type conversion utilities (real, to_numpy) for result processing
  
  Backend selection is automatic based on availability and environment
  variables (SHPFC_ARRAY_BACKEND, SHPFC_FFT_BACKEND); see backend.py.
  
  Attributes:
    backend: ArrayBackend instance from backend.py (NumPy, CuPy, etc.)
  """

  def __init__(self, backend_adapter: backend.ArrayBackend | None = None):
    self.backend = backend_adapter or backend.resolve_backend()

  # FFT wrappers
  def fftn(self, a, s=None, axes=None, norm=None, out=None):
    return self.backend.fft.fftn(a, s=s, axes=axes, norm=norm)

  def ifftn(self, a, s=None, axes=None, norm=None, out=None):
    return self.backend.fft.ifftn(a, s=s, axes=axes, norm=norm)

  # Allocation / conversion helpers
  def array(self, value, *, dtype=None, copy: bool = False):
    return self.backend.array(value, dtype=dtype, copy=copy)

  def asarray(self, value, *, dtype=None):
    return self.backend.asarray(value, dtype=dtype)

  def zeros(self, shape, *, dtype=None):
    return self.backend.zeros(shape, dtype=dtype)

  def empty(self, shape, *, dtype=None):
    return self.backend.empty(shape, dtype=dtype)

  def real(self, a):
    return self.backend.xp.real(a)

  def to_numpy(self, a):
    return self.backend.to_numpy(a)


class sHPFC:
  """Stateful sHPFC simulation object (backend-aware, 2D-only).

  This class owns and manages all payload arrays used in the phase-field crystal
  simulation (psi, mu, f, velocity, div_v, etc.) and routes all FFT operations
  through the backend adapter from backend.py. This design supports both CPU
  (NumPy) and GPU (CuPy) execution with identical code.
  
  Initialization:
    - Accepts a 2D initial condition psi0 (NumPy array)
    - Converts to backend namespace (NumPy or CuPy per resolve_backend())
    - Pre-allocates all working buffers in the active backend
    - Converts kernel arrays (lin_mu_kernel, lin_f_kernel, gaussian_kernel, etc.)
      to backend namespace for efficient math
    - Converts geometry k-space arrays (KX, KY, k2) to backend namespace
    
  Core Fields (backend arrays):
    - psi: order parameter (real)
    - psi_hat: Fourier transform of psi (complex)
    - mu, f: chemical potential and free energy density (real)
    - mu_hat, f_hat: Fourier transforms (complex)
    - v_x, v_y: velocity components (real, hydrodynamic path only)
    - div_v: velocity divergence (real, hydrodynamic path only)
    - (many working arrays used internally for batched operations)
    
  Kernel Location Note:
    The Gaussian kernel was moved from convolution.py to PFC2D_kernels.gaussian_kernel_fft
    during PR-3. It is automatically converted to backend arrays during initialization.
    
  Timestep Methods:
    - Timestep_stdPFC(): standard PFC dynamics (no hydrodynamics)
    - Timestep_sHPFC(): hybrid PFC with hydrodynamics (includes velocity coupling)
    
  Constraint: 2D only (1D/3D will be handled by model/geometry stubs with
    graceful failure messages).
  """

  def __getattr__(self, name: str):
    state = object.__getattribute__(self, "__dict__").get("state")
    if state is not None and hasattr(state, name):
      return getattr(state, name)
    raise AttributeError(name)

  def __setattr__(self, name: str, value) -> None:
    if name in {"_payload_mgr", "model", "geometry", "kernels", "state", "std_stepper", "shpfc_stepper"}:
      object.__setattr__(self, name, value)
      return
    state = object.__getattribute__(self, "__dict__").get("state")
    if state is not None and hasattr(state, name):
      setattr(state, name, value)
      return
    object.__setattr__(self, name, value)

  def __init__(
    self,
    psi0: np.ndarray,
    *,
    model: model_2D,
    geometry: geometry_2D,
  ) -> None:
    # Backend adapter for FFT operations and allocations.
    self._payload_mgr = BackendPayloadManager()
    self.model = model

    # Geometry and convolution kernels.
    self.geometry = geometry

    # Precompute convolution kernels for the linear parts of the dynamics
    self.kernels = KernelRules(model=self.model, geometry=self.geometry)
    self.state = SimulationState(self._payload_mgr, self.model, self.geometry, self.kernels, psi0)
    self.std_stepper = StdPFCTimestepper(self.state)
    self.shpfc_stepper = SHPFCTimestepper(self.state)

  def __getitem__(self, key: str):
    return getattr(self, key)

  def __setitem__(self, key: str, value) -> None:
    setattr(self, key, value)

  # Fused kernel: compute n2, n3, n4 from n in one pass
  def calc_poly_psi(self):
    # powers(self.psi, self.psi2, self.psi3, self.psi4)
    self.psi2[...] = self.psi**2
    self.psi3[...] = self.psi2 * self.psi
    self.psi4[...] = self.psi3 * self.psi
    
    self._psi_hat_poly[...] = self._payload_mgr.fftn(self._psi_poly, axes=(-2, -1))

  def calc_mu(self, *, psi_hat_is_current: bool = False) -> None:
    if not psi_hat_is_current:
      self.calc_poly_psi()
    # lin_mu_hat(self.kernels.lin_mu_kernel, self.psi_hat, self.lin_mu_hat)
    self.lin_mu_hat[...] = self.kernels.lin_mu_kernel * self.psi_hat
    
    self.lin_mu[...] = self._payload_mgr.real(self._payload_mgr.ifftn(self.lin_mu_hat))
    
    # mu(self.lin_mu, self.psi3, self.mu)
    self.mu[...] = self.lin_mu + self.psi3

  def calc_f(self, *, psi_hat_is_current: bool = False) -> None:
    if not psi_hat_is_current:
      self.calc_poly_psi()
    
    # lin_f_hat(self.kernels.lin_f_kernel, self.psi_hat, self.lin_f_hat)
    self.lin_f_hat[...] = self.kernels.lin_f_kernel * self.psi_hat
    
    self.lin_f[...] = self._payload_mgr.real(self._payload_mgr.ifftn(self.lin_f_hat))
    
    # f(self.lin_f, self.psi, self.psi2, self.psi4, self.model.beta, self.model.temp, self.f)
    self.f[...] = self.lin_f * self.psi + 0.5 * (self.model.beta + self.model.temp) * self.psi2 + 0.25 * self.psi4

  def calc_StructureTensor(self, *, psi_xy_is_current: bool = False) -> None:
    """Calculate the structure tensor of the current psi field."""
    # Compute gradients in Fourier space
    if not psi_xy_is_current:
      self.calc_poly_psi()
      self.psi_x[...] = self._payload_mgr.real(self._payload_mgr.ifftn(1j * self.KX * self.psi_hat))
      self.psi_y[...] = self._payload_mgr.real(self._payload_mgr.ifftn(1j * self.KY * self.psi_hat))

    # Compute structure tensor components
    S_xx = self.psi_x**2
    S_yy = self.psi_y**2
    S_xy = self.psi_x * self.psi_y

    # Smooth the structure tensor with the Gaussian kernel
    self.S_xx = self._payload_mgr.real(self._payload_mgr.ifftn(self._payload_mgr.fftn(S_xx) * self.kernels.gaussian_kernel))
    self.S_yy = self._payload_mgr.real(self._payload_mgr.ifftn(self._payload_mgr.fftn(S_yy) * self.kernels.gaussian_kernel))
    self.S_xy = self._payload_mgr.real(self._payload_mgr.ifftn(self._payload_mgr.fftn(S_xy) * self.kernels.gaussian_kernel))

    # # Stack into a single array for output
    # structure_tensor = np.stack((S_xx_smooth, S_xy_smooth, S_yy_smooth), axis=-1)
    # return structure_tensor

  def Timestep_stdPFC(self) -> None:
    self.std_stepper.step()

  def Timestep_sHPFC(self) -> None:
    self.shpfc_stepper.step()

  def Timestep_sHPFC_div_vpsi(self) -> None:
    self.shpfc_stepper.step_div_vpsi()

  def Timestep_sHPFC_psigradmu(self) -> None:
    self.shpfc_stepper.step_psigradmu()

import cupy as cp
powers = cp.ElementwiseKernel(
  'float64 x',
  'float64 x2, float64 x3, float64 x4',
  'double a = x; double a2 = a*a; x2 = a2; x3 = a2*a; x4 = a2*a2;',
    'compute_powers'
)

grads = cp.ElementwiseKernel(
  'complex128 d_dx, complex128 d_dy, complex128 field_hat',
  'complex128 field_x_hat, complex128 field_y_hat',
  'field_x_hat = d_dx * field_hat; field_y_hat = d_dy * field_hat;',
    'compute_grads'
)

force = cp.ElementwiseKernel(
  'float64 mu, float64 psi_x, float64 psi_y, float64 f_x, float64 f_y',
  'float64 force_x, float64 force_y',
  'force_x = mu * psi_x - f_x; force_y = mu * psi_y - f_y;',
    'compute_force'
)

v_hat = cp.ElementwiseKernel(
  'float64 lin_v_exp, float64 nonlin_v_exp, float64 rho0, complex128 kernel_gaussian, complex128 v_x_hat, complex128 force_x_hat, complex128 v_y_hat, complex128 force_y_hat',
  'complex128 v_x_hat_out, complex128 v_y_hat_out',
  'v_x_hat_out = lin_v_exp * v_x_hat + 1 / rho0 * nonlin_v_exp * kernel_gaussian * force_x_hat; v_y_hat_out = lin_v_exp * v_y_hat + nonlin_v_exp * 1 / rho0 * kernel_gaussian * force_y_hat;',
    'compute_v_hat'
)

v_dot_grad_psi = cp.ElementwiseKernel(
  'float64 v_x, float64 v_y, float64 psi_x, float64 psi_y',
  'float64 v_dot_grad_psi',
  'v_dot_grad_psi = v_x * psi_x + v_y * psi_y;',
    'compute_v_dot_grad_psi'
)

psi_hat = cp.ElementwiseKernel(
  'float64 kernel_lin_psi_exp, float64 kernel_nonlin_psi_exp, float64 Gamma, float64 kernel_d2_dlap, complex128 psi_hat, complex128 psi3_hat, complex128 v_dot_grad_psi_hat',
  'complex128 psi_hat_out',
  'psi_hat_out = kernel_lin_psi_exp * psi_hat + kernel_nonlin_psi_exp * (Gamma * kernel_d2_dlap * psi3_hat - v_dot_grad_psi_hat);',
    'compute_psi_hat'
)

lin_mu_hat = cp.ElementwiseKernel(
  'float64 lin_mu_kernel, complex128 psi_hat',
  'complex128 lin_mu_hat',
  'lin_mu_hat = lin_mu_kernel * psi_hat;',
    'compute_lin_mu_hat'
)

mu = cp.ElementwiseKernel(
  'float64 lin_mu, float64 psi3',
  'float64 mu',
  'mu = lin_mu + psi3;',
    'compute_mu'
)

lin_f_hat = cp.ElementwiseKernel(
  'float64 lin_f_kernel, complex128 psi_hat',
  'complex128 lin_f_hat',
  'lin_f_hat = lin_f_kernel * psi_hat;',
    'compute_lin_f_hat'
)

f = cp.ElementwiseKernel(
  'float64 lin_f, float64 psi, float64 psi2, float64 psi4, float64 beta, float64 temp',
  'float64 f',
  'f = lin_f * psi + 0.5 * (beta + temp) * psi2 + 0.25 * psi4;',
    'compute_f'
)
