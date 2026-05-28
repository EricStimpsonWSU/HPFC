"""Backend/FFT payload helpers for the shared core."""

from __future__ import annotations

from PFC.Core import backend


class BackendPayloadManager:
	def __init__(self, backend_adapter: backend.ArrayBackend | None = None):
		self.backend = backend_adapter or backend.resolve_backend()

	def fftn(self, a, s=None, axes=None, norm=None, out=None):
		return self.backend.fft.fftn(a, s=s, axes=axes, norm=norm)

	def ifftn(self, a, s=None, axes=None, norm=None, out=None):
		return self.backend.fft.ifftn(a, s=s, axes=axes, norm=norm)

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
