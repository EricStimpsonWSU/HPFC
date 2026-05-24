from __future__ import annotations

import backend


def test_resolve_backend_falls_back_to_numpy_when_optional_backends_missing(monkeypatch):
    monkeypatch.setattr(backend, "_resolve_cupy_backend", lambda: None)
    monkeypatch.setattr(backend, "_resolve_numpy_fftw_backend", lambda: None)

    resolved = backend.resolve_backend(preferred="auto", fft_preferred="auto")

    assert resolved.name == "numpy"
    assert resolved.fft_name == "numpy"


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
        backend._normalize_backend_name("invalid", kind="array")
    except ValueError as exc:
        assert "Unsupported array backend" in str(exc)
    else:
        raise AssertionError("Expected invalid backend name to fail")
