import matplotlib.pyplot as plt
import pandas as pd


def plot_anomalies(df: pd.DataFrame):
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    if "Anomaly" not in df.columns:
        raise ValueError("Anomaly column not found.")

    fig, ax = plt.subplots(figsize=(14, 6))

    # Price line
    ax.plot(
        df["Date"],
        df["Close"],
        color="steelblue",
        linewidth=2,
        alpha=0.8,
        label="Close Price",
    )

    # Anomaly points
    anomalies = df[df["Anomaly"] == -1]

    ax.scatter(
        anomalies["Date"],
        anomalies["Close"],
        color="red",
        s=120,
        edgecolors="black",
        linewidth=1.5,
        label="Anomaly",
        zorder=5,
    )

    ax.set_title("Stock Price with Detected Anomalies")

    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")

    ax.legend()

    ax.grid(True)

    fig.tight_layout()

    return fig



def plot_price_history(df: pd.DataFrame):
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = ["Date", "Close"]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(
        df["Date"],
        df["Close"],
        color="steelblue",
        linewidth=2,
        label="Close Price",
    )

    ax.set_title("Historical Stock Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")

    ax.grid(True)
    ax.legend()

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig


def plot_forecast(historical_df: pd.DataFrame,forecast_df: pd.DataFrame):
    if historical_df.empty:
        raise ValueError("Historical DataFrame is empty.")

    if forecast_df.empty:
        raise ValueError("Forecast DataFrame is empty.")

    fig, ax = plt.subplots(figsize=(14, 6))

    # Historical Prices
    ax.plot(
        historical_df["Date"],
        historical_df["Close"],
        color="royalblue",
        linewidth=2,
        label="Historical",
    )

    # Forecast Prices
    ax.plot(
        forecast_df["Date"],
        forecast_df["Predicted_Close"],
        color="crimson",
        linewidth=3,
        linestyle="--",
        marker="o",
        markersize=5,
        label="Forecast",
    )

    # Forecast start line
    forecast_start = forecast_df["Date"].iloc[0]

    ax.axvline(
        x=forecast_start,
        color="black",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
    )

    # Highlight forecast region
    ax.axvspan(
        forecast_start,
        forecast_df["Date"].iloc[-1],
        color="red",
        alpha=0.08,
    )

    # Forecast label
    ax.text(
        forecast_start,
        historical_df["Close"].max(),
        "Forecast Start",
        fontsize=10,
        color="black",
        rotation=90,
        va="top",
        ha="right",
    )

    ax.set_title("30-Day Stock Price Forecast")

    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")

    ax.grid(alpha=0.3)

    ax.legend(loc="upper left")

    fig.autofmt_xdate()

    fig.tight_layout()

    return fig