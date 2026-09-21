from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    rng = np.random.default_rng(42)
    rows = 5000
    tenure = rng.integers(0, 121, rows)
    spend = np.clip(rng.normal(85, 35, rows), 5, 300)
    tickets = rng.poisson(1.8, rows)
    contracts = rng.choice(
        ["month-to-month", "one-year", "two-year"],
        size=rows,
        p=[0.55, 0.3, 0.15],
    )
    contract_risk = np.select(
        [contracts == "month-to-month", contracts == "one-year"],
        [0.9, 0.2],
        default=-0.5,
    )
    logit = -1.4 - 0.015 * tenure + 0.009 * spend + 0.28 * tickets + contract_risk
    probability = 1 / (1 + np.exp(-logit))
    churn = rng.binomial(1, probability)

    frame = pd.DataFrame(
        {
            "tenure_months": tenure,
            "monthly_spend": spend.round(2),
            "support_tickets": tickets,
            "contract_type": contracts,
            "churn": churn,
        }
    )
    path = Path("data/processed/train.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    print(f"wrote {len(frame)} rows to {path}")


if __name__ == "__main__":
    main()
