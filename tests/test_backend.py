from __future__ import annotations

from PFC.Core import backend


def test_resolve_backend_falls_back_to_numpy_when_optional_backends_missing(backend_resolution_mocks):
    backend_resolution_mocks()

    resolved = backend.resolve_backend(preferred="auto", fft_preferred="auto")

    assert resolved.name == "numpy"
    assert resolved.fft_name == "numpy"


def test_resolve_backend_prefers_cupy_when_available(backend_resolution_mocks, numpy_backend):
    cupy_backend = backend.ArrayBackend(
        name="cupy",
        fft_name="cupy",
        xp=numpy_backend.xp,
        fft=numpy_backend.fft,
        is_gpu=True,
        uses_fftw=False,
    )
    backend_resolution_mocks(cupy_backend=cupy_backend)

    resolved = backend.resolve_backend(preferred="auto", fft_preferred="auto")

    assert resolved.name == "cupy"
    assert resolved.fft_name == "cupy"


def test_resolve_backend_falls_back_from_cupy_to_numpy_when_cupy_is_unavailable(
    backend_resolution_mocks,
):
    backend_resolution_mocks()

    resolved = backend.resolve_backend(preferred="cupy", fft_preferred="auto")

    assert resolved.name == "numpy"
    assert resolved.fft_name == "numpy"


def test_resolve_backend_selects_pyfftw_when_requested(backend_resolution_mocks, numpy_backend):
    pyfftw_backend = backend.ArrayBackend(
        name="numpy",
        fft_name="pyfftw",
        xp=numpy_backend.xp,
        fft=numpy_backend.fft,
        is_gpu=False,
        uses_fftw=True,
    )
    backend_resolution_mocks(numpy_fftw_backend=pyfftw_backend)

    resolved = backend.resolve_backend(preferred="numpy", fft_preferred="pyfftw")

    assert resolved.name == "numpy"
    assert resolved.fft_name == "pyfftw"


def test_resolve_backend_honors_environment_variables_when_backend_is_available(
    monkeypatch, backend_resolution_mocks, numpy_backend
):
    pyfftw_backend = backend.ArrayBackend(
        name="numpy",
        fft_name="pyfftw",
        xp=numpy_backend.xp,
        fft=numpy_backend.fft,
        is_gpu=False,
        uses_fftw=True,
    )
    backend_resolution_mocks(numpy_fftw_backend=pyfftw_backend)
    monkeypatch.setenv(backend.ARRAY_BACKEND_ENV, "numpy")
    monkeypatch.setenv(backend.FFT_BACKEND_ENV, "pyfftw")

    resolved = backend.resolve_backend()

    assert resolved.name == "numpy"
    assert resolved.fft_name == "pyfftw"


def test_resolve_backend_rejects_incompatible_array_and_fft_selection():
    try:
        backend.resolve_backend(preferred="numpy", fft_preferred="cupy")
    except ValueError as exc:
        assert "fft=cupy requires array=cupy" in str(exc)
    else:
        raise AssertionError("Expected resolve_backend to reject fft=cupy with array=numpy")


def test_resolve_backend_honors_environment_variables(monkeypatch):
    monkeypatch.setenv(backend.ARRAY_BACKEND_ENV, "numpy")
    monkeypatch.setenv(backend.FFT_BACKEND_ENV, "pyfftw")
    monkeypatch.setattr(backend, "_resolve_numpy_fftw_backend", lambda: None)

    resolved = backend.resolve_backend()

    assert resolved.name == "numpy"
    assert resolved.fft_name == "numpy"


def test_resolve_backend_rejects_invalid_backend_name():
    try:
        backend.resolve_backend(preferred="invalid", fft_preferred="auto")
    except ValueError as exc:
        assert "Unsupported array backend" in str(exc)
    else:
        raise AssertionError("Expected invalid backend name to fail")
