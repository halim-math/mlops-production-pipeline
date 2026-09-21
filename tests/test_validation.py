import pandas as pd

from mlops_pipeline.data.validation import validate_training_frame


def test_valid_frame_passes() -> None:
    frame = pd.DataFrame(
        {
            "tenure_months": [1, 2, 3, 4],
            "monthly_spend": [10.0, 20.0, 30.0, 40.0],
            "support_tickets": [0, 1, 0, 2],
            "contract_type": ["one-year"] * 4,
            "churn": [0, 1, 0, 1],
        }
    )
    report = validate_training_frame(
        frame,
        required_columns=list(frame.columns),
        target="churn",
    )
    assert report.valid
    assert report.rows == 4


def test_missing_required_column_fails() -> None:
    frame = pd.DataFrame({"churn": [0, 1]})
    report = validate_training_frame(
        frame,
        required_columns=["monthly_spend", "churn"],
        target="churn",
    )
    assert not report.valid
    assert any("monthly_spend" in error for error in report.errors)
