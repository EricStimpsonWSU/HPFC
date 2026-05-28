# HPFC

Basic usage

This project provides CPU/GPU-capable phase-field crystal simulation utilities.

Canonical example to run a short simulation with the per-simulation module surface:

```python
from HPFC.sim_shpfc_std import build_geometry, build_model, make_sim
import numpy as np

model = build_model(temp=-0.25, beta=1.5, Gamma=1.0, rho0=1.0, Gamma_s=0.75, dt=0.05)
geometry = build_geometry(shape=(64, 64), Lx=8.0, Ly=8.0)

psi0 = np.random.randn(64, 64) * 0.1

sim = make_sim(psi0=psi0, model=model, geometry=geometry)
sim.Timestep_sHPFC()

# obtain host-side numpy arrays regardless of backend
psi_host = sim._payload_mgr.to_numpy(sim.psi)
f_host = sim._payload_mgr.to_numpy(sim.f)
```

The canonical import surface is one module per simulation variant:

- `HPFC.sim_pfc_std` for the standard PFC baseline.
- `HPFC.sim_shpfc_std` for standard sHPFC.
- `HPFC.sim_shpfc_div_vpsi` for the `div(v psi)` hydrodynamic variant.
- `HPFC.sim_shpfc_psigradmu` for the `psi * grad(mu)` hydrodynamic variant.

For custom assembly, the consumer workflow is:
`build_model` -> `build_geometry` -> `make_initial_state` -> `make_sim` -> timestep method.

Configuration

- Control the preferred backends via environment variables before importing modules:
	- `SHPFC_ARRAY_BACKEND=auto|cupy|numpy`
	- `SHPFC_FFT_BACKEND=auto|cupy|pyfftw|fftw|numpy`

See `notebooks/` for example simulation setups and `tests/benchmarks/` for the benchmarking runner.