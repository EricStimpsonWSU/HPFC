# Design Patterns in the Current PFC Core  
### (Adapter + Dataclass + Centralized Timesteppers)

This document shows how the **current** PFC Core is structured using three major patterns:

1. **Adapter** — `ArrayBackend`  
2. **Dataclass** — `KernelRules`  
3. **Centralized Timesteppers** — `StdPFCTimestepper`, `SHPFCTimestepper` in `PFC.Core.steppers`

This is a simplified, foobar‑style sketch that mirrors the architecture as it exists today.

---

## 1. Adapter Pattern — `ArrayBackend`

In the real code, `ArrayBackend` wraps:

- NumPy  
- PyFFTW  
- CuPy  

and exposes a unified interface for:

- array creation  
- FFTs  
- real/complex conversions  
- backend detection  

Here is a minimal sketch consistent with the current Core:

```python
class ArrayBackend:
    def __init__(self, xp, fft):
        self.xp = xp
        self.fft = fft

    def array(self, v, dtype=None):
        return self.xp.asarray(v, dtype=dtype)

    def fftn(self, a, axes=None):
        return self.fft.fftn(a, axes=axes)

    def ifftn(self, a, axes=None):
        return self.fft.ifftn(a, axes=axes)

    def real(self, a):
        return self.xp.real(a)
```

This is exactly what the Core does:  
**steppers never touch NumPy or CuPy directly — they only use the adapter.**

---

## 2. Dataclass Pattern — `KernelRules`

In the real code, `KernelRules`:

- builds all linear operators  
- builds ETD kernels  
- computes Gaussian smoothing kernels  
- exposes k‑space derivative operators  
- is constructed from `model` + `geometry`  

Here is a minimal sketch consistent with the current Core:

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class KernelRules:
    lin_dpsi: np.ndarray
    lin_mu_kernel: np.ndarray
    lin_f_kernel: np.ndarray
    lin_v_kernel: np.ndarray
    lin_psi_exp: np.ndarray
    nonlin_psi_exp: np.ndarray

    @staticmethod
    def from_model(model, geometry):
        k2 = geometry["k2"]
        dt = model["dt"]

        lin_mu = (k2 + 1.0)**2
        lin_f = np.zeros_like(k2)
        lin_dpsi = -k2 * lin_mu

        lin_psi_exp = np.exp(lin_dpsi * dt)
        nonlin_psi_exp = (lin_psi_exp - 1) / lin_dpsi

        return KernelRules(
            lin_dpsi, lin_mu, lin_f, np.zeros_like(k2),
            lin_psi_exp, nonlin_psi_exp
        )
```

This mirrors the real `KernelRules` behavior:  
**a dataclass bundling all linear and ETD kernels.**

---

## 3. State Container — `SimulationState`

In the real code, `SimulationState` owns:

- ψ, ψ², ψ³, ψ⁴  
- μ, f  
- gradients  
- velocity fields (allocated lazily)  
- FFT buffers  
- k‑space operators  
- Gaussian smoothing kernels  
- the backend adapter  

Here is a minimal sketch:

```python
class SimulationState:
    def __init__(self, psi0, backend: ArrayBackend, kernels: KernelRules):
        self.backend = backend
        self.kernels = kernels

        self.psi = backend.array(psi0)
        self.psi_hat = backend.fftn(self.psi, axes=(-2, -1))

        # In the real code, many more fields are allocated here.
```

This matches the current Core:  
**the state owns all buffers and fields; steppers mutate the state.**

---

## 4. Centralized Timesteppers (Current State)

Right now, timesteppers live in:

```
PFC/Core/steppers.py
```

They are **not** variant‑local yet.  
They are **not** strategy objects attached to sim files.  
They are **shared classes** that operate on `SimulationState`.

Here is a minimal sketch consistent with the current architecture:

```python
class StdPFCTimestepper:
    def __init__(self, state: SimulationState):
        self.state = state

    def step(self):
        s = self.state
        k = s.kernels
        xp = s.backend.xp

        # Nonlinear term (placeholder)
        nonlin = xp.power(s.psi, 3)
        nonlin_hat = s.backend.fftn(nonlin, axes=(-2, -1))

        # ETD update
        s.psi_hat = k.lin_psi_exp * s.psi_hat + k.nonlin_psi_exp * nonlin_hat
        s.psi = s.backend.ifftn(s.psi_hat, axes=(-2, -1)).real

        # In the real code: update t, compute μ, f, gradients, etc.
```

This reflects the **current** design:

- steppers are centralized  
- steppers mutate the shared state  
- steppers rely on `ArrayBackend` and `KernelRules`  
- sim files simply instantiate the stepper  

---

## 5. Example Usage (Current Architecture)

```python
if __name__ == '__main__':
    model = {'dt': 0.01}
    geometry = {'shape': (4,4), 'k2': np.zeros((4,4))}
    psi0 = np.zeros((4,4))

    backend = ArrayBackend(np, np.fft)
    kernels = KernelRules.from_model(model, geometry)
    state = SimulationState(psi0, backend, kernels)

    stepper = StdPFCTimestepper(state)
    stepper.step()

    print('psi mean:', state.psi.mean())
```

This mirrors how the real code works today.

---

## Notes (Current State)

- `ArrayBackend` in the real code is more complete and handles:
  - NumPy  
  - PyFFTW  
  - CuPy  
  - backend selection  
  - FFT normalization  
- `KernelRules` in the real code builds:
  - k‑space derivative operators  
  - Gaussian smoothing kernels  
  - ETD kernels  
  - linear operators for ψ, μ, f, v  
- `SimulationState` allocates:
  - ψ, ψ², ψ³, ψ⁴  
  - μ, f  
  - gradients  
  - velocity fields  
  - FFT buffers  
  - k‑space operators  
- Timesteppers are currently **centralized** and **shared**, not variant‑local.

---
