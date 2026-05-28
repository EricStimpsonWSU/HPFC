# Phase‑Field Crystal (PFC) Simulation Framework  
### Standard PFC and sHPFC Variants

This repository provides a clean, modular implementation of **2D Phase‑Field Crystal (PFC)** simulations, including:

- **Standard PFC** (non‑hydrodynamic)  
- **sHPFC (hydrodynamic PFC)**  
- **sHPFC div(v ψ)** variant  
- **sHPFC ψ·∇μ** variant  

The design emphasizes:

- **clarity** — each variant lives in a single `.py` file  
- **scientific auditability** — all model surfaces are explicit  
- **backend flexibility** — NumPy, PyFFTW, or CuPy  
- **clean separation** between Core and Variant layers  

---

# 1. Quick Start: Standard PFC Simulation

Below is the **minimal code** required to run a standard (non‑hydrodynamic) PFC simulation.

```python
import numpy as np
from PFC.stdPFC.sim_pfc_std import build_model, build_geometry, make_sim

# --- Define model parameters ---
model = build_model(
    temp=0.25,
    beta=1.0,
    Gamma=1.0,
    rho0=1.0,
    Gamma_s=1.0,
    dt=0.01,
)

# --- Define geometry ---
geometry = build_geometry(
    shape=(256, 256),
    Lx=100.0,
    Ly=100.0,
)

# --- Initial condition ---
psi0 = np.random.normal(0.0, 0.01, size=geometry.shape)

# --- Create simulation ---
sim = make_sim(psi0, model=model, geometry=geometry)

# --- Advance one timestep ---
sim.Timestep_stdPFC()

# --- Access fields ---
print(sim.psi)
print(sim.mu)
```

This is the simplest entry point into the framework.

---

# 2. Variant Overview & Startup Examples

Each variant lives in its own file and exposes a **single, explicit simulation surface**.  
This makes each model easy to read, audit, and modify independently.

---

## 2.1 Standard PFC (non‑hydrodynamic)

**File:** `stdPFC/sim_pfc_std.py`  
**Timestep:** `Timestep_stdPFC()`  
**Hydrodynamic fields:** *blocked*  

Use when you want the classical PFC dynamics without velocity fields.

```python
from PFC.stdPFC.sim_pfc_std import build_model, build_geometry, make_sim

sim = make_sim(psi0, model=model, geometry=geometry)
sim.Timestep_stdPFC()
```

---

## 2.2 sHPFC (standard hydrodynamic PFC)

**File:** `sHPFC/sim_shpfc_std.py`  
**Timestep:** `Timestep_sHPFC()`  
**Hydrodynamic fields:** *enabled*  

This variant includes the full hydrodynamic coupling.

```python
from PFC.sHPFC.sim_shpfc_std import build_model, build_geometry, make_sim

sim = make_sim(psi0, model=model, geometry=geometry)
sim.Timestep_sHPFC()
```

---

## 2.3 sHPFC div(v ψ) Variant

**File:** `sHPFC/sim_shpfc_div_vpsi.py`  
**Timestep:** `Timestep_sHPFC_div_vpsi()`  
**Hydrodynamic fields:** enabled  
**Nonlinear term:** uses divergence of vψ  

```python
from PFC.sHPFC.sim_shpfc_div_vpsi import build_model, build_geometry, make_sim

sim = make_sim(psi0, model=model, geometry=geometry)
sim.Timestep_sHPFC_div_vpsi()
```

---

## 2.4 sHPFC ψ·∇μ Variant

**File:** `sHPFC/sim_shpfc_psigradmu.py`  
**Timestep:** `Timestep_sHPFC_psigradmu()`  
**Hydrodynamic fields:** enabled  
**Nonlinear term:** uses ψ·∇μ  

```python
from PFC.sHPFC.sim_shpfc_psigradmu import build_model, build_geometry, make_sim

sim = make_sim(psi0, model=model, geometry=geometry)
sim.Timestep_sHPFC_psigradmu()
```

---

# 3. Architecture Overview

The framework is intentionally split into two layers:

---

## 3.1 Core Layer (shared across all variants)

Located in `PFC/Core/`, this layer contains:

### **Geometry**
- Grid construction  
- k‑space operators  
- FFT frequencies  

### **Model**
- PFC parameters  
- Hydrodynamic parameters  
- Parameter resolution logic  

### **Kernel Rules**
- Linear operators  
- ETD kernels  
- Gaussian smoothing kernels  

### **State**
- All simulation fields  
- FFT buffers  
- Polynomial ψ powers  
- Gradients, forces, structure tensor  

### **Backend**
- NumPy / PyFFTW / CuPy resolution  
- Unified array/FFT interface  

### **Payload Manager**
- Thin wrapper around backend FFTs and array ops  

### **Simulation Facade**
- Attribute forwarding  
- Name blocking for variant safety  

The Core layer is **variant‑agnostic** and contains all the heavy lifting.

---

## 3.2 Variant Layer (one file per model)

Each variant:

- defines its own `build_model()`  
- defines its own `build_lin_kernels()`  
- defines its own `make_sim()`  
- exposes only the timestep methods appropriate for that physics  
- blocks all other names via `VariantSimulationFacade`  

This ensures:

- **explicit model surfaces**  
- **no cross‑variant leakage**  
- **easy scientific auditing**  
- **easy future extension**  

Even though variants share structure, each file is intentionally self‑contained.

---

# 4. Design Philosophy

### ✔ Explicit over abstract  
Each variant is a standalone `.py` file containing the full model surface.

### ✔ Scientific auditability  
A researcher can open one file and see *exactly* what the model does.

### ✔ Backend flexibility  
The same code runs on CPU (NumPy), FFTW, or GPU (CuPy).

### ✔ Clean separation of concerns  
Core handles physics and numerics.  
Variants handle API and model semantics.

### ✔ Future‑proof  
As new PFC variants are added, each gets its own file with minimal coupling.

---

# 5. Future Directions

- Add a wiki with detailed derivations  
- Add visualization utilities  
- Add benchmark scripts  
- Add 3D geometry support  
- Add more hydrodynamic coupling models  
- Add unit tests for variant blocking rules  
