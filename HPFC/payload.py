"""Backend/FFT payload helpers extracted from sHPFC for reuse.

Provides a small adapter around the array/FFT backends used by the
simulation modules. This is a minimal, behavior-preserving extraction of the
original `BackendPayloadManager` to make the payload surface importable from
`HPFC.payload` for the Step 5 refactor.
"""
from __future__ import annotations

import numpy as np

from PFC.Core import backend


class BackendPayloadManager:
    """Manages FFT operations and array allocation via backend adapter.

    This is the extracted payload manager from `HPFC/sHPFC.py` and intentionally
    preserves the same public methods used across the codebase so the change is
    behavior-preserving.
    """

    def __init__(self, backend_adapter: backend.ArrayBackend | None = None):
        self.backend = backend_adapter or backend.resolve_backend()

    # FFT wrappers
    def fftn(self, a, s=None, axes=None, norm=None, out=None):
        return self.backend.fft.fftn(a, s=s, axes=axes, norm=norm)

    def ifftn(self, a, s=None, axes=None, norm=None, out=None):
        return self.backend.fft.ifftn(a, s=s, axes=axes, norm=norm)

    # Allocation / conversion helpers
    def array(self, value, *, dtype=None, copy: bool = False):
        return self.backend.array(value, dtype=dtype, copy=copy)

    def asarray(self, value, *, dtype=None):
        return self.backend.asarray(value, dtype=dtype)

    def zeros(self, shape, *, dtype=None):
        return self.backend.zeros(shape, dtype=dtype)

    def empty(self, shape, *, dtype=None):
        return self.backend.empty(shape, dtype=dtype)

    def real(self, a):
        return self.backend.xp.real(a)

    def to_numpy(self, a):
        return self.backend.to_numpy(a)
