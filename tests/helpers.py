from __future__ import annotations

import numpy as np


def assert_allclose(actual, expected, *, rtol: float = 1e-7, atol: float = 1e-12) -> None:
    np.testing.assert_allclose(actual, expected, rtol=rtol, atol=atol)