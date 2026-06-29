import pandas as pd
from sklearn.ensemble import IsolationForest


FEATURE_COLUMNS = [
    "Daily_Return",
    "Volatility_7",
    "Volume_Change",
    "High_Low_Range",
    "Open_Close_Diff",
]


def detect_anomalies(
    df: pd.DataFrame,
    contamination: float = 0.005,
    random_state: int = 42,
) -> pd.DataFrame:
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    if not (0 < contamination < 0.5):
        raise ValueError("contamination must be between 0 and 0.5.")

    missing_columns = [
        col for col in FEATURE_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing feature columns: {missing_columns}"
        )

    df = df.copy()

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=random_state,
    )

    X = df[FEATURE_COLUMNS]

    df["Anomaly"] = model.fit_predict(X)

    df["Anomaly_Score"] = model.decision_function(X)

    return df