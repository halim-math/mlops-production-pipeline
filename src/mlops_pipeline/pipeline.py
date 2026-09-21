import argparse
from pathlib import Path

from mlops_pipeline.training.train import train


def run_pipeline(config: str, data: str) -> None:
    Path("artifacts").mkdir(exist_ok=True)
    metrics = train(config, data)
    print("Pipeline completed with quality gates passed.")
    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/training.yaml")
    parser.add_argument("--data", default="data/processed/train.csv")
    args = parser.parse_args()
    run_pipeline(args.config, args.data)


if __name__ == "__main__":
    main()
