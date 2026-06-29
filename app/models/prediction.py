import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def predict_stock(df: pd.DataFrame,forecast_days: int = 30,order: tuple = (5, 1, 0),) -> pd.DataFrame:
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    if "Close" not in df.columns or "Date" not in df.columns:
        raise ValueError("DataFrame must contain 'Date' and 'Close' columns.")

    model = ARIMA(
        df["Close"],
        order=order,
    )

    fitted_model = model.fit()

    predictions = fitted_model.forecast(
        steps=forecast_days
    )

    future_dates = pd.date_range(
        start=df["Date"].iloc[-1] + pd.offsets.BDay(1),
        periods=forecast_days,
        freq="B",
    )

    forecast_df = pd.DataFrame(
        {
            "Date": future_dates,
            "Predicted_Close": predictions.values,
        }
    )

    return forecast_df