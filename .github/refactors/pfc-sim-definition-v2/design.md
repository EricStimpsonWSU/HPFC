# Design Patterns After the `pfc-sim-definition` Refactor  
### (Adapter + Dataclass + Self‑Contained Variant Timesteppers)

This document shows how the **post‑refactor** PFC architecture is structured using three major patterns:

1. **Adapter** — `ArrayBackend` (unchanged)  
2. **Dataclass** — `KernelRules` (unchanged)  
3. **Variant‑Local Timesteppers** — each `sim_<model>_<variant>.py` defines its own timestepper class

This is a minimal, foobar‑style sketch that mirrors the **refactored** architecture.

---

## 1. Adapter Pattern — `ArrayBackend` (unchanged)

The backend adapter still provides a unified interface for:

- NumPy  
- PyFFTW  
- CuPy  

and exposes:

- array creation  
- FFTs  
- real/complex conversions  

This remains identical to the pre‑refactor Core.

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

The **Core remains backend‑agnostic**.

---

## 2. Dataclass Pattern — `KernelRules` (unchanged)

`KernelRules` still:

- builds linear operators  
- builds ETD kernels  
- computes Gaussian smoothing kernels  
- depends only on `model` + `geometry`  

Here is a minimal sketch consistent with the refactored architecture:

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

The **Core still owns all kernel construction**.

---

## 3. State Container — `SimulationState` (unchanged)

`SimulationState` still owns:

- ψ, ψ², ψ³, ψ⁴  
- μ, f  
- gradients  
- velocity fields  
- FFT buffers  
- k‑space operators  
- Gaussian smoothing kernels  
- the backend adapter  

Minimal sketch:

```python
class SimulationState:
    def __init__(self, psi0, backend: ArrayBackend, kernels: KernelRules):
        self.backend = backend
        self.kernels = kernels

        self.psi = backend.array(psi0)
        self.psi_hat = backend.fftn(self.psi, axes=(-2, -1))

        # Real code allocates many more fields.
```

The **Core remains the owner of all simulation buffers**.

---

## 4. Variant‑Local Timesteppers (NEW, post‑refactor)

After the refactor:

- **No timesteppers live in the Core**
- **Each variant sim file defines its own timestepper**
- **Each timestepper is fully self‑contained**
- **No shared base class**
- **No inheritance**
- **No cross‑variant reuse**

This is the new pattern.

### Example: `sim_pfc_std.py` (post‑refactor)

```python
class StdPFCTimestepper:
    def __init__(self, state):
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

        # Update time
        s.t += s.model.dt
```

This is the **new architecture**:

- The timestepper lives **inside the sim file**
- It is **variant‑specific**
- It is **explicit**
- It is **self‑contained**
- It mutates the shared `SimulationState`

---

## 5. Example Usage (Post‑Refactor)

```python
if __name__ == '__main__':
    model = {'dt': 0.01}
    geometry = {'shape': (4,4), 'k2': np.zeros((4,4))}
    psi0 = np.zeros((4,4))

    backend = ArrayBackend(np, np.fft)
    kernels = KernelRules.from_model(model, geometry)
    state = SimulationState(psi0, backend, kernels)

    # Local timestepper defined in this sim file
    stepper = StdPFCTimestepper(state)
    stepper.step()

    print('psi mean:', state.psi.mean())
```

This mirrors the **refactored** architecture:

- Backend + kernels + state come from the Core  
- The timestepper comes from the **variant sim file**  
- The sim file is the **complete model surface**  

---

## Notes (Post‑Refactor)

- `ArrayBackend` remains unchanged and continues to unify NumPy / FFTW / CuPy.
- `KernelRules` remains a dataclass bundling all linear and ETD kernels.
- `SimulationState` remains the owner of all buffers and fields.
- **Timesteppers are no longer shared**:
  - No `PFC.Core.steppers`
  - No shared base class
  - No inheritance
  - No cross‑variant reuse
- Each variant sim file now contains:
  - `build_model`
  - `build_geometry`
  - `build_lin_kernels`
  - `make_initial_state`
  - `make_sim`
  - **its own timestepper class**
  - exposed timestep method(s)
  - `BLOCKED_NAMES`

This is the **final architecture** after the `pfc-sim-definition-v2` refactor.
