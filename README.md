# HPFC

Basic usage

This project provides CPU/GPU-capable phase-field crystal simulation utilities.

Minimal example to run a short simulation and retrieve host arrays:

```python
from PFC2D_model import model_2D
from PFC2D_geometry import geometry_2D
from sHPFC import sHPFC
import numpy as np

model = model_2D(temp=-0.25, beta=1.5, Gamma=1.0, rho0=1.0, Gamma_s=0.75, dt=0.05)
geometry = geometry_2D(shape=(64, 64), Lx=8.0, Ly=8.0)

psi0 = np.random.randn(64, 64) * 0.1

sim = sHPFC(psi0=psi0, model=model, geometry=geometry)
sim.Timestep_sHPFC()

# obtain host-side numpy arrays regardless of backend
psi_host = sim._payload_mgr.to_numpy(sim.psi)
f_host = sim._payload_mgr.to_numpy(sim.f)
```

Configuration

- Control the preferred backends via environment variables before importing modules:
	- `SHPFC_ARRAY_BACKEND=auto|cupy|numpy`
	- `SHPFC_FFT_BACKEND=auto|cupy|pyfftw|fftw|numpy`

See `notebooks/` for example simulation setups and `tests/benchmarks/` for the benchmarking runner.