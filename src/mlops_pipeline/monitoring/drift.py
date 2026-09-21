from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DriftResult:
    feature: str
    psi: float
    drifted: bool


def population_stability_index(
    reference: pd.Series,
    current: pd.Series,
    *,
    bins: int = 10,
    threshold: float = 0.2,
) -> DriftResult:
    feature = reference.name or "feature"
    quantiles = np.unique(np.quantile(reference.dropna(), np.linspace(0, 1, bins + 1)))
    if len(quantiles) < 3:
        return DriftResult(feature=feature, psi=0.0, drifted=False)

    ref_hist, _ = np.histogram(reference.dropna(), bins=quantiles)
    cur_hist, _ = np.histogram(current.dropna(), bins=quantiles)
    ref_dist = np.clip(ref_hist / max(ref_hist.sum(), 1), 1e-6, None)
    cur_dist = np.clip(cur_hist / max(cur_hist.sum(), 1), 1e-6, None)
    psi = float(np.sum((cur_dist - ref_dist) * np.log(cur_dist / ref_dist)))
    return DriftResult(feature=feature, psi=psi, drifted=psi >= threshold)


def detect_numeric_drift(
    reference: pd.DataFrame,
    current: pd.DataFrame,
    threshold: float = 0.2,
) -> list[DriftResult]:
    common = [
        column
        for column in reference.select_dtypes(include="number").columns
        if column in current.columns
    ]
    return [
        population_stability_index(reference[c], current[c], threshold=threshold)
        for c in common
    ]
