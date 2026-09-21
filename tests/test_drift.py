import numpy as np
import pandas as pd

from mlops_pipeline.monitoring.drift import population_stability_index


def test_identical_distribution_has_low_psi() -> None:
    rng = np.random.default_rng(42)
    values = pd.Series(rng.normal(size=5000), name="x")
    result = population_stability_index(values, values.copy())
    assert result.psi < 0.01
    assert not result.drifted


def test_shifted_distribution_is_detected() -> None:
    rng = np.random.default_rng(42)
    reference = pd.Series(rng.normal(0, 1, 5000), name="x")
    current = pd.Series(rng.normal(2, 1, 5000), name="x")
    result = population_stability_index(reference, current, threshold=0.2)
    assert result.drifted
