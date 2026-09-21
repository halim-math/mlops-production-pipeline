from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = ["tenure_months", "monthly_spend", "support_tickets"]
CATEGORICAL_FEATURES = ["contract_type"]


def build_preprocessor() -> ColumnTransformer:
    numeric = Pipeline([("scale", StandardScaler())])
    categorical = Pipeline(
        [("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric, NUMERIC_FEATURES),
            ("categorical", categorical, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )
