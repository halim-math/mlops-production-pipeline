import pytest

from mlops_pipeline.training.metrics import EvaluationMetrics, enforce_quality_gates


def test_quality_gate_rejects_bad_candidate() -> None:
    metrics = EvaluationMetrics(
        f1=0.5,
        roc_auc=0.6,
        brier_score=0.4,
        train_test_f1_gap=0.3,
    )
    gates = {
        "min_f1": 0.72,
        "min_roc_auc": 0.78,
        "max_brier_score": 0.22,
        "max_train_test_f1_gap": 0.12,
    }
    with pytest.raises(RuntimeError):
        enforce_quality_gates(metrics, gates)
