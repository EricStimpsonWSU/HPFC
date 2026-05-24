"""Backend helpers for CPU/GPU-aware array code in sHPFC.

Default priority:
1. CuPy arrays + cuFFT.
2. NumPy arrays + PyFFTW.
3. Plain NumPy arrays + NumPy FFTs.

Use environment variables or explicit arguments to override the default.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
import sys
from typing import Any #, Literal

try:
    import numpy as np
except ImportError:
    print(
        "\n[sHPFC ERROR] NumPy is not installed. Cannot proceed with sHPFC backend initialization.",
        file=sys.stderr,
    )
    print(
        "Install NumPy with: pip install numpy",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    import cupy as cp
except Exception:
    cp = None  # type: ignore[assignment]

try:
    import pyfftw
    import pyfftw.interfaces.numpy_fft as fftw_np

    pyfftw.interfaces.cache.enable()
    _HAS_FFTW = True
except Exception:
    fftw_np = None  # type: ignore[assignment]
    _HAS_FFTW = False


def _print_cupy_install_instructions() -> None:
    """Print installation instructions for CuPy."""
    print(
        "\n[sHPFC WARNING] CuPy is not available in this environment.",
        file=sys.stderr,
    )
    print("  To enable GPU acceleration, install CuPy:", file=sys.stderr)
    print("    - CUDA must be installed first", file=sys.stderr)
    print("    - pip install cupy-cuda11x (replace 11x with your CUDA version)", file=sys.stderr)
    print("    - For more details: https://docs.cupy.dev/en/stable/install.html", file=sys.stderr)
    print("  Falling back to NumPy...\n", file=sys.stderr)


def _print_pyfftw_install_instructions() -> None:
    """Print installation instructions for PyFFTW."""
    print(
        "\n[sHPFC WARNING] PyFFTW is not available in this environment.",
        file=sys.stderr,
    )
    print("  To enable faster FFT performance, install PyFFTW:", file=sys.stderr)
    print("    - pip install pyfftw", file=sys.stderr)
    print("  Falling back to NumPy FFT...\n", file=sys.stderr)


BackendName = ["auto", "numpy", "cupy"]# Literal["auto", "numpy", "cupy"]
FFTBackendName = ["auto", "numpy", "pyfftw", "fftw", "cupy"] #Literal["auto", "numpy", "pyfftw", "fftw", "cupy"]

ARRAY_BACKEND_ENV = "SHPFC_ARRAY_BACKEND"
FFT_BACKEND_ENV = "SHPFC_FFT_BACKEND"


@dataclass(frozen=True)
class ArrayBackend:
    """Resolved array namespace plus a few convenience helpers."""

    name: str
    fft_name: str
    xp: Any
    fft: Any
    is_gpu: bool
    uses_fftw: bool

    def array(self, value, *, dtype=None, copy: bool = False):
        return self.xp.array(value, dtype=dtype, copy=copy)

    def asarray(self, value, *, dtype=None):
        return self.xp.asarray(value, dtype=dtype)

    def zeros(self, shape, *, dtype=None):
        return self.xp.zeros(shape, dtype=dtype)

    def ones(self, shape, *, dtype=None):
        return self.xp.ones(shape, dtype=dtype)

    def empty(self, shape, *, dtype=None):
        return self.xp.empty(shape, dtype=dtype)

    def linspace(self, start, stop, num, *, endpoint: bool = True, dtype=None):
        return self.xp.linspace(start, stop, num, endpoint=endpoint, dtype=dtype)

    def meshgrid(self, *arrays, indexing: str = "xy"):
        return self.xp.meshgrid(*arrays, indexing=indexing)

    def fftfreq(self, n: int, *, d: float = 1.0):
        return self.xp.fft.fftfreq(n, d=d)

    def to_numpy(self, value):
        if self.is_gpu:
            return cp.asnumpy(value)  # type: ignore[union-attr]
        return np.asarray(value)

    def summary(self) -> str:
        return f"arrays={self.name}, fft={self.fft_name}"


def _resolve_numpy_backend() -> ArrayBackend:
    return ArrayBackend(
        name="numpy",
        fft_name="numpy",
        xp=np,
        fft=np.fft,
        is_gpu=False,
        uses_fftw=False,
    )


def _resolve_numpy_fftw_backend() -> ArrayBackend | None:
    """Resolve NumPy + PyFFTW backend, or None if PyFFTW is not available."""
    if not _HAS_FFTW:
        return None
    return ArrayBackend(
        name="numpy",
        fft_name="pyfftw",
        xp=np,
        fft=fftw_np,
        is_gpu=False,
        uses_fftw=True,
    )


def _resolve_cupy_backend() -> ArrayBackend | None:
    """Resolve CuPy backend, or None if CuPy is not available."""
    if cp is None:
        return None
    return ArrayBackend(
        name="cupy",
        fft_name="cupy",
        xp=cp,
        fft=cp.fft,
        is_gpu=True,
        uses_fftw=False,
    )


def _normalize_backend_name(value: str, *, kind: str) -> str:
    normalized = value.strip().lower()
    if kind == "array" and normalized in {"auto", "numpy", "cupy"}:
        return normalized
    if kind == "fft" and normalized in {"auto", "numpy", "pyfftw", "fftw", "cupy"}:
        return normalized
    raise ValueError(f"Unsupported {kind} backend: {value!r}")


def _read_env_backend(name: str, *, default: str, kind: str) -> str:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return _normalize_backend_name(raw, kind=kind)


def resolve_backend(
    preferred: BackendName | None = None,
    *,
    fft_preferred: FFTBackendName | None = None,
) -> ArrayBackend:
    """Return the resolved backend with graceful fallback.

    Args:
        preferred: Array backend preference. If None, reads
            ``SHPFC_ARRAY_BACKEND`` and defaults to ``auto``.
        fft_preferred: FFT engine preference. If None, reads
            ``SHPFC_FFT_BACKEND`` and defaults to ``auto``.

    Selection rules:
        - array=auto prefers CuPy, then NumPy.
        - fft=auto prefers cuFFT when arrays are CuPy, otherwise PyFFTW, then NumPy.
        - array=numpy with fft=pyfftw gives the CPU/PyFFTW path.
        - array=numpy with fft=numpy gives the plain NumPy path.
        
    Fallback behavior:
        - If a requested backend is unavailable, installation instructions are printed
          and the next available runtime by priority is used.
    """
    array_choice = _normalize_backend_name(
        preferred if preferred is not None else _read_env_backend(ARRAY_BACKEND_ENV, default="auto", kind="array"),
        kind="array",
    )
    fft_choice = _normalize_backend_name(
        fft_preferred if fft_preferred is not None else _read_env_backend(FFT_BACKEND_ENV, default="auto", kind="fft"),
        kind="fft",
    )

    if array_choice == "cupy":
        backend = _resolve_cupy_backend()
        if backend is not None:
            if fft_choice == "numpy":
                raise ValueError("fft=numpy requires array=numpy")
            return backend
        # CuPy requested but not available
        _print_cupy_install_instructions()
        # Fall back to NumPy
        if fft_choice in {"pyfftw", "fftw"}:
            backend = _resolve_numpy_fftw_backend()
            if backend is not None:
                return backend
            # PyFFTW requested but not available
            _print_pyfftw_install_instructions()
        return _resolve_numpy_backend()

    if array_choice == "numpy":
        if fft_choice in {"pyfftw", "fftw"}:
            backend = _resolve_numpy_fftw_backend()
            if backend is not None:
                return backend
            # PyFFTW explicitly requested but not available
            _print_pyfftw_install_instructions()
            return _resolve_numpy_backend()
        if fft_choice == "numpy":
            return _resolve_numpy_backend()
        if fft_choice == "cupy":
            raise ValueError("fft=cupy requires array=cupy")
        # fft_choice == "auto" with array=numpy
        backend = _resolve_numpy_fftw_backend()
        if backend is not None:
            return backend
        return _resolve_numpy_backend()

    # array_choice == "auto"
    backend = _resolve_cupy_backend()
    if backend is not None:
        return backend
    
    # CuPy not available, try PyFFTW if requested or on auto
    if fft_choice == "numpy":
        return _resolve_numpy_backend()
    
    if fft_choice in {"pyfftw", "fftw", "auto"}:
        backend = _resolve_numpy_fftw_backend()
        if backend is not None:
            return backend
    
    return _resolve_numpy_backend()


def is_cupy_available() -> bool:
    return cp is not None


def is_pyfftw_available() -> bool:
    return _HAS_FFTW


def array_backend_name(value) -> str:
    """Best-effort backend name for an existing array-like value."""
    module = type(value).__module__
    if module.startswith("cupy"):
        return "cupy"
    return "numpy"


def to_numpy(value):
    """Convert a NumPy or CuPy array to a NumPy array."""
    if cp is not None and type(value).__module__.startswith("cupy"):
        return cp.asnumpy(value)
    return np.asarray(value)


def print_environment(runtime: ArrayBackend | None = None) -> None:
    """Print the active backend and instructions for changing it."""
    runtime = runtime or resolve_backend()
    print("\n[sHPFC backend] Environment initialized:")
    print(f"  - CuPy available: {'yes' if cp is not None else 'no'}")
    print(f"  - PyFFTW available: {'yes' if _HAS_FFTW else 'no'}")
    print(f"  - Active backend: {runtime.summary()}")
    print("  - Selection priority: CuPy/cuFFT -> NumPy/PyFFTW -> NumPy/NumPy")
    print("  - Override with environment variables before importing sHPFC modules:")
    print(f"    - {ARRAY_BACKEND_ENV}=auto|cupy|numpy")
    print(f"    - {FFT_BACKEND_ENV}=auto|cupy|pyfftw|fftw|numpy")
    if cp is None:
        print("  - Note: CuPy is not installed. If GPU acceleration is desired:")
        print("    - Install CUDA if not already installed")
        print("    - Then: pip install cupy-cuda11x (replace 11x with your CUDA version)")
    if not _HAS_FFTW:
        print("  - Note: PyFFTW is not installed. For faster FFTs:")
        print("    - pip install pyfftw")
    print("  - Testing examples:")
    print(f"    - NumPy + PyFFTW: {ARRAY_BACKEND_ENV}=numpy and {FFT_BACKEND_ENV}=pyfftw")
    print(f"    - Plain NumPy:    {ARRAY_BACKEND_ENV}=numpy and {FFT_BACKEND_ENV}=numpy")
    print("  - Leave both unset for the default auto-selection.")
    print()


DEFAULT_BACKEND = resolve_backend()


print_environment(DEFAULT_BACKEND)