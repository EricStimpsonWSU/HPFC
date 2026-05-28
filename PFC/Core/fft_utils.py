"""Small helpers for DC-mode and batched FFT operations.

Keep these utilities minimal and backend-agnostic: functions operate on
NumPy/CuPy-compatible arrays or via the existing `BackendPayloadManager` for
batched FFT helpers used by the simulation.
"""
from __future__ import annotations

from typing import Tuple

import numpy as np


def get_dc_mode(field_hat: np.ndarray) -> complex:
	"""Return the DC (zero-frequency) mode from a Fourier-space array."""
	return field_hat.flat[0]


def set_dc_mode(field_hat: np.ndarray, value: complex) -> None:
	"""Set the DC (zero-frequency) mode in-place on a Fourier-space array."""
	field_hat.flat[0] = value


def batched_fftn(payload_mgr, arr, axes: Tuple[int, ...] = (-2, -1)):
	arr_backend = payload_mgr.asarray(arr)
	return payload_mgr.fftn(arr_backend, axes=axes)


def batched_ifftn_real(payload_mgr, arr_hat, axes: Tuple[int, ...] = (-2, -1)):
	arr_hat_backend = payload_mgr.asarray(arr_hat)
	return payload_mgr.real(payload_mgr.ifftn(arr_hat_backend, axes=axes))
