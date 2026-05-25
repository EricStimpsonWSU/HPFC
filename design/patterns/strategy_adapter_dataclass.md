# Design Patterns: Strategy + Adapter + Dataclass (Python example)

This short example demonstrates the core patterns used in the `sHPFC` refactor: a `BackendAdapter` (adapter), a `KernelRules` dataclass, and `Stepper` strategy classes. The goal is to show a minimal, foobar-like Python sketch that is easy to test and adapt into the real codebase.

```python
from dataclasses import dataclass
import numpy as np

# Adapter: wraps array & FFT operations so steppers are backend-agnostic
class BackendAdapter:
    def __init__(self, xp=np, fft=None):
        self.xp = xp
        self.fft = fft or np.fft

    def array(self, v, dtype=None):
        return self.xp.asarray(v, dtype=dtype)

    def fftn(self, a):
        return self.fft.fftn(a)

    def ifftn(self, a):
        return self.fft.ifftn(a)

# Dataclass: kernel bundle encapsulating model expressions
@dataclass
class KernelRules:
    lin_mu_kernel: np.ndarray
    lin_f_kernel: np.ndarray
    lin_psi_exp: np.ndarray
    nonlin_psi_exp: np.ndarray

    @staticmethod
    def from_model(model, geometry):
        # Minimal placeholder: real code would build ETD kernels from model+geometry
        kshape = geometry['shape']
        lin_mu = np.ones(kshape)
        lin_f = np.zeros(kshape)
        lin_psi_exp = np.exp(-0.1 * np.ones(kshape) * model['dt'])
        nonlin_psi_exp = (lin_psi_exp - 1) / (-0.1)
        return KernelRules(lin_mu, lin_f, lin_psi_exp, nonlin_psi_exp)

# State container: owns fields and the backend adapter
class SimulationState:
    def __init__(self, psi0, backend: BackendAdapter, kernels: KernelRules):
        self.backend = backend
        self.kernels = kernels
        self.psi = backend.array(psi0)
        self.psi_hat = backend.fftn(self.psi)

# Strategy: stepper interface
class Stepper:
    def step(self, state: SimulationState):
        raise NotImplementedError

# Concrete strategy: standard PFC
class StdPFCStepper(Stepper):
    def step(self, state: SimulationState):
        k = state.kernels
        xp = state.backend.xp
        # non-linear term (placeholder)
        nonlin = xp.power(state.psi, 3)
        nonlin_hat = state.backend.fftn(nonlin)
        state.psi_hat = k.lin_psi_exp * state.psi_hat + k.nonlin_psi_exp * nonlin_hat
        state.psi = state.backend.ifftn(state.psi_hat).real

# Example usage
if __name__ == '__main__':
    model = {'dt': 0.01}
    geometry = {'shape': (4,4)}
    psi0 = np.zeros((4,4))
    backend = BackendAdapter()
    kernels = KernelRules.from_model(model, geometry)
    state = SimulationState(psi0, backend, kernels)
    stepper = StdPFCStepper()
    stepper.step(state)
    print('psi mean:', state.psi.mean())
```

Notes
- In the real refactor: `BackendAdapter` will be the `ArrayBackend` in `HPFC/backend.py` and `KernelRules` will be a dataclass built from `model` and `geometry`.
- `Stepper` classes should be lightweight and operate on `SimulationState` without allocating new arrays on the hot path.
