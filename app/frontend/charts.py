import pandas as pd
import plotly.graph_objects as go


def plot_history(df: pd.DataFrame):
    """
    Plot historical stock prices.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            name="Close Price",
            line=dict(width=2),
        )
    )

    fig.update_layout(
        title="Historical Stock Price",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        hovermode="x unified",
        height=550,
    )

    return fig


def plot_technicals(df: pd.DataFrame):
    """
    Plot technical indicators.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            name="Close",
            line=dict(width=2),
        )
    )

    if "SMA_20" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["SMA_20"],
                mode="lines",
                name="SMA 20",
            )
        )

    if "EMA_20" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["EMA_20"],
                mode="lines",
                name="EMA 20",
            )
        )

    if "BB_Upper" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["BB_Upper"],
                mode="lines",
                name="Upper Band",
                line=dict(dash="dot"),
            )
        )

    if "BB_Lower" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["BB_Lower"],
                mode="lines",
                name="Lower Band",
                line=dict(dash="dot"),
            )
        )

    fig.update_layout(
        title="Technical Indicators",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        hovermode="x unified",
        height=550,
    )

    return fig


def plot_prediction(
    history_df: pd.DataFrame,
    forecast_df: pd.DataFrame,
):
    """
    Plot historical price with forecast.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["Close"],
            mode="lines",
            name="Historical",
            line=dict(width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Predicted_Close"],
            mode="lines+markers",
            name="Forecast",
            line=dict(width=2),
        )
    )

    fig.add_vline(
        x=forecast_df["Date"].iloc[0],
        line_dash="dash",
    )

    fig.update_layout(
        title="30-Day Price Forecast",
        xaxis_title="Date",
        yaxis_title="Predicted Price",
        template="plotly_dark",
        hovermode="x unified",
        height=550,
    )

    return fig


def plot_anomalies(df: pd.DataFrame):
    """
    Plot detected anomalies.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            name="Close Price",
            line=dict(width=2),
        )
    )

    anomaly_df = df[df["Anomaly"] == -1]

    fig.add_trace(
        go.Scatter(
            x=anomaly_df["Date"],
            y=anomaly_df["Close"],
            mode="markers",
            name="Anomalies",
            marker=dict(
                size=10,
                color="red",
                symbol="x",
            ),
        )
    )

    fig.update_layout(
        title="Anomaly Detection",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        hovermode="x unified",
        height=550,
    )

    return fig