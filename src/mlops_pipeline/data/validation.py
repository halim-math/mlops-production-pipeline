from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class DataQualityReport:
    rows: int
    duplicate_rows: int
    missing_fraction: float
    target_rate: float
    valid: bool
    errors: tuple[str, ...]


def validate_training_frame(
    frame: pd.DataFrame,
    *,
    required_columns: list[str],
    target: str,
    max_missing_fraction: float = 0.02,
) -> DataQualityReport:
    errors: list[str] = []
    missing_columns = sorted(set(required_columns) - set(frame.columns))
    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")

    if frame.empty:
        errors.append("Dataset is empty")

    duplicate_rows = int(frame.duplicated().sum()) if not frame.empty else 0
    missing_fraction = float(frame.isna().mean().max()) if not frame.empty else 1.0

    if missing_fraction > max_missing_fraction:
        errors.append(
            f"Missing fraction {missing_fraction:.4f} exceeds {max_missing_fraction:.4f}"
        )

    target_rate = float("nan")
    if target in frame.columns and not frame.empty:
        unique = set(frame[target].dropna().unique().tolist())
        if not unique.issubset({0, 1}):
            errors.append(f"Target {target!r} is not binary: {sorted(unique)}")
        target_rate = float(frame[target].mean())
        if target_rate < 0.01 or target_rate > 0.99:
            errors.append(f"Target prevalence is suspicious: {target_rate:.4f}")

    return DataQualityReport(
        rows=len(frame),
        duplicate_rows=duplicate_rows,
        missing_fraction=missing_fraction,
        target_rate=target_rate,
        valid=not errors,
        errors=tuple(errors),
    )


def assert_training_frame(**kwargs: object) -> DataQualityReport:
    report = validate_training_frame(**kwargs)  # type: ignore[arg-type]
    if not report.valid:
        raise ValueError("; ".join(report.errors))
    return report
