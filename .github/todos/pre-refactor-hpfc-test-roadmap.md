# Pre-Refactor HPFC Test Roadmap

Goal: add the smallest useful test suite around the current HPFC codebase before any major refactor, so behavior can be locked down first and refactoring can happen with confidence.

## Test Infrastructure

- [x] Add a test runner configuration for `pytest`.
- [x] Add a minimal dependency list for tests, including `pytest` and any optional backend packages used in the suite.
- [x] Add a shared test fixture layer for reusable 2D model and geometry objects.
- [x] Add a backend-mocking strategy so CPU-only environments can still exercise backend selection logic.
- [x] Add a small numerical comparison helper for floating-point assertions.

## Backend Resolution Tests

- [x] Verify `resolve_backend()` defaults to NumPy when no optional acceleration libraries are available.
- [x] Verify `resolve_backend()` prefers CuPy when it is available and `array=auto` is used.
- [x] Verify `resolve_backend()` falls back from CuPy to NumPy cleanly when CuPy is unavailable.
- [x] Verify `resolve_backend()` selects PyFFTW when requested and available.
- [x] Verify invalid backend names raise a clear `ValueError`.
- [x] Verify incompatible combinations such as `array=numpy` with `fft=cupy` fail fast.
- [x] Verify environment variables `SHPFC_ARRAY_BACKEND` and `SHPFC_FFT_BACKEND` are honored.

## Model Tests

- [x] Verify `model_2D` stores all parameters as floats.
- [x] Verify `model_2D_CPU` emits a deprecation warning and still initializes correctly.
- [x] Verify `model_1D` raises `NotImplementedError` with the expected message.
- [x] Verify `model_3D` raises `NotImplementedError` with the expected message.

## Geometry Tests

- [x] Verify `geometry_2D` computes `dx`, `dy`, `x`, and `y` correctly for a simple grid.
- [x] Verify `geometry_2D` builds `X`, `Y`, `KX`, `KY`, and `k2` with the expected shapes.
- [x] Verify `geometry_2D` frequency-space arrays are consistent with `numpy.fft.fftfreq`.
- [x] Verify `geometry_2D_CPU` issues a deprecation warning and matches `geometry_2D` behavior.
- [x] Verify `geometry_1D` and `geometry_3D` raise `NotImplementedError` with clear messages.

## Kernel Tests

- [x] Verify `gaussian_kernel_fft()` rejects missing width.
- [x] Verify `gaussian_kernel_fft()` rejects non-positive width.
- [x] Verify `gaussian_kernel_fft()` returns a complex array with the DC mode normalized to 1.
- [x] Verify `kernels` derives `d_dx`, `d_dy`, `d2_dlap`, `d4_dlap2`, and `d6_dlap3` from the supplied geometry.
- [x] Verify `kernels` computes `lin_mu_kernel`, `lin_f_kernel`, `lin_v_kernel`, `lin_psi_exp`, `nonlin_psi_exp`, `lin_v_exp`, and `nonlin_v_exp` with the expected shapes.
- [x] Verify `kernels` keeps the Gaussian kernel mean-preserving after normalization.

Additional kernel helper coverage:
- [x] Verify `_to_spacing_tuple` accepts scalars and sequences and rejects wrong-length inputs.
- [x] Verify `_cell_volume` multiplies spacing values.
- [x] Verify `_normalize_kernel_hat_mean` raises on zero DC mode.
- [x] Verify ETD helper `buildNonlinearETD` uses `dt` for zero lin_kernel entries and `(exp(lin*dt)-1)/lin` otherwise.
- [x] Verify `gaussian_kernel_fft` rejects scalar `k2` inputs.

## sHPFC Initialization Tests

- [x] Verify `sHPFC` accepts a simple 2D initial field and initializes every working buffer with the expected shape.
- [x] Verify `sHPFC` preserves the initial mean mode in `psi_hat_00`.
- [x] Verify `sHPFC` converts geometry and kernel arrays into the active backend namespace.
- [x] Verify `sHPFC` exposes the documented aliases for field batches such as `psi`, `psi_hat`, `v_x`, and `v_y`.
- [x] Verify `sHPFC` rejects unsupported geometry or model objects with a clear failure.

## sHPFC Behavior Tests

- [ ] Verify `calc_poly_psi()` updates `psi2`, `psi3`, `psi4`, and their Fourier transforms consistently.
- [ ] Verify `calc_mu()` computes the expected linear and nonlinear contributions for a known small field.
- [ ] Verify `calc_f()` computes the expected free-energy density for a known small field.
- [ ] Verify `calc_StructureTensor()` returns smoothed tensor components with the expected shapes.
- [ ] Verify `Timestep_stdPFC()` advances `psi` and `t` and preserves the zero mode.
- [ ] Verify `Timestep_sHPFC()` advances the state and updates the hydrodynamic buffers consistently.
- [ ] Verify `Timestep_sHPFC_div_vpsi()` uses the divergence-based update path and advances `t`.
- [ ] Verify `Timestep_sHPFC_psigradmu()` produces the same field-shape updates and increments time.

## Regression and Smoke Tests

- [ ] Add one tiny deterministic integration test for a few `Timestep_stdPFC()` steps on a small grid.
- [ ] Add one tiny deterministic integration test for a few `Timestep_sHPFC()` steps on a small grid.
- [ ] Add a notebook-equivalent smoke test that mirrors the current "perfect crystal relaxation" setup.
- [ ] Add a notebook-equivalent smoke test that mirrors the current "dislocation annihilation" setup.
- [ ] Add a regression test for any bug discovered while preparing the refactor so the bug stays fixed.

## Refactor Safety Checks

- [ ] Lock down public import paths so `HPFC` module names keep working during the refactor.
- [ ] Verify deprecated compatibility shims still emit warnings until they are intentionally removed.
- [ ] Capture any intentional numerical tolerances before changing kernels or timestep logic.
- [ ] Add a short note in the test README describing which tests must pass before refactoring a behavior.