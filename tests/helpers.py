from __future__ import annotations

import numpy as np


def to_numpy(value):
    if hasattr(value, "get"):
        return value.get()
    return np.asarray(value)


def assert_allclose(actual, expected, *, rtol: float = 1e-7, atol: float = 1e-12) -> None:
    np.testing.assert_allclose(to_numpy(actual), to_numpy(expected), rtol=rtol, atol=atol)