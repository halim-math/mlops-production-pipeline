from dataclasses import dataclass

import numpy as np
from sklearn.metrics import brier_score_loss, f1_score, roc_auc_score


@dataclass(frozen=True)
class EvaluationMetrics:
    f1: float
    roc_auc: float
    brier_score: float
    train_test_f1_gap: float


def evaluate_binary_classifier(model, x_train, y_train, x_test, y_test) -> EvaluationMetrics:
    train_pred = model.predict(x_train)
    test_pred = model.predict(x_test)
    test_prob = model.predict_proba(x_test)[:, 1]
    return EvaluationMetrics(
        f1=float(f1_score(y_test, test_pred)),
        roc_auc=float(roc_auc_score(y_test, test_prob)),
        brier_score=float(brier_score_loss(y_test, test_prob)),
        train_test_f1_gap=float(
            abs(f1_score(y_train, train_pred) - f1_score(y_test, test_pred))
        ),
    )


def enforce_quality_gates(metrics: EvaluationMetrics, gates: dict[str, float]) -> None:
    failures: list[str] = []
    if metrics.f1 < gates["min_f1"]:
        failures.append(f"f1={metrics.f1:.4f} < {gates['min_f1']:.4f}")
    if metrics.roc_auc < gates["min_roc_auc"]:
        failures.append(f"roc_auc={metrics.roc_auc:.4f} < {gates['min_roc_auc']:.4f}")
    if metrics.brier_score > gates["max_brier_score"]:
        failures.append(
            f"brier={metrics.brier_score:.4f} > {gates['max_brier_score']:.4f}"
        )
    if metrics.train_test_f1_gap > gates["max_train_test_f1_gap"]:
        failures.append(
            "train_test_f1_gap="
            f"{metrics.train_test_f1_gap:.4f} > {gates['max_train_test_f1_gap']:.4f}"
        )
    if failures:
        raise RuntimeError("Model rejected by quality gates: " + "; ".join(failures))
