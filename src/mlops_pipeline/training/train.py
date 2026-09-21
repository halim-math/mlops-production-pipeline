import argparse
import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
from sklearn.model_selection import train_test_split

from mlops_pipeline.data.validation import assert_training_frame
from mlops_pipeline.training.metrics import enforce_quality_gates, evaluate_binary_classifier
from mlops_pipeline.training.model import build_model


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def train(config_path: str, data_path: str = "data/processed/train.csv") -> dict[str, float]:
    cfg = load_config(config_path)
    frame = pd.read_csv(data_path)
    assert_training_frame(
        frame=frame,
        required_columns=cfg["data"]["required_columns"],
        target=cfg["data"]["target"],
    )

    target = cfg["data"]["target"]
    x = frame.drop(columns=[target])
    y = frame[target]
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=cfg["data"]["test_size"],
        random_state=cfg["project"]["random_state"],
        stratify=y,
    )

    model = build_model(cfg["model"]["params"])
    mlflow.set_experiment(cfg["mlflow"]["experiment_name"])

    with mlflow.start_run() as run:
        mlflow.log_params(cfg["model"]["params"])
        mlflow.log_param("data_rows", len(frame))
        mlflow.log_param("data_columns", len(frame.columns))

        model.fit(x_train, y_train)
        metrics = evaluate_binary_classifier(model, x_train, y_train, x_test, y_test)
        metric_dict = {
            "f1": metrics.f1,
            "roc_auc": metrics.roc_auc,
            "brier_score": metrics.brier_score,
            "train_test_f1_gap": metrics.train_test_f1_gap,
        }
        mlflow.log_metrics(metric_dict)
        enforce_quality_gates(metrics, cfg["quality_gates"])

        artifact_dir = Path("artifacts")
        artifact_dir.mkdir(parents=True, exist_ok=True)
        model_path = artifact_dir / "model.joblib"
        joblib.dump(model, model_path)
        (artifact_dir / "metrics.json").write_text(
            json.dumps(metric_dict, indent=2), encoding="utf-8"
        )

        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name=cfg["mlflow"]["registered_model_name"],
        )
        mlflow.set_tag("quality_gate", "passed")
        mlflow.set_tag("run_id", run.info.run_id)

    return metric_dict


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/training.yaml")
    parser.add_argument("--data", default="data/processed/train.csv")
    args = parser.parse_args()
    metrics = train(args.config, args.data)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
