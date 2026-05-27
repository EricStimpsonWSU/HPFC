from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from tests.baselines.reference_cases import (
    STEP_COUNTS,
    VARIANT_METHODS,
    build_simulation,
    baseline_filename,
    collect_snapshot,
    load_snapshot,
)


BASELINE_DIR = Path(__file__).resolve().parent / "baselines" / "data"


def _assert_snapshot_matches(actual: dict[str, np.ndarray | float | str | int], expected: dict[str, np.ndarray]) -> None:
    for key, actual_value in actual.items():
        assert key in expected, f"missing baseline key: {key}"
        expected_value = expected[key]
        if isinstance(actual_value, np.ndarray):
            np.testing.assert_allclose(actual_value, expected_value, rtol=1e-12, atol=1e-15)
        else:
            if np.isscalar(expected_value):
                if isinstance(actual_value, float):
                    assert actual_value == pytest.approx(expected_value, rel=1e-12, abs=1e-15)
                else:
                    assert actual_value == expected_value.item() if hasattr(expected_value, "item") else expected_value
            else:
                assert actual_value == expected_value


@pytest.mark.parametrize("variant", list(VARIANT_METHODS))
@pytest.mark.parametrize("steps", STEP_COUNTS)
def test_baseline_files_match_current_behavior(variant: str, steps: int, force_numpy_backend):
    baseline_path = BASELINE_DIR / baseline_filename(variant, steps)
    assert baseline_path.exists(), f"missing baseline file: {baseline_path}"

    simulation = build_simulation(variant)
    timestep_method = getattr(simulation, VARIANT_METHODS[variant])
    for _ in range(steps):
        timestep_method()

    actual = collect_snapshot(simulation, variant, steps)
    expected = load_snapshot(baseline_path)
    _assert_snapshot_matches(actual, expected)
