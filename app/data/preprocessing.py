import pandas as pd
import numpy as np


def clean_data(df:pd.DataFrame)->pd.DataFrame:
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    df = df.copy()

    df.drop_duplicates(inplace=True)
    df.sort_values("Date", inplace=True)

    # Remove rows with missing dates
    df.dropna(subset=["Date"], inplace=True)

    # Forward-fill price columns
    price_cols = ["Open", "High", "Low", "Close"]

    for col in price_cols:
        if col in df.columns:
            df[col] = df[col].ffill()

    # Fill Volume using the average of the previous 7 trading days
    if "Volume" in df.columns:
        rolling_mean = (
            df["Volume"]
            .shift(1) #not include current row
            .rolling(window=7, min_periods=1)
            .mean()
        )

        df["Volume"] = df["Volume"].fillna(rolling_mean)

    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def create_features(df: pd.DataFrame,window:int=7) -> pd.DataFrame:
    df = df.copy()

    # Returns
    df["Daily_Return"] = df["Close"].pct_change()

    df["Log_Return"] = np.log(df["Close"] / df["Close"].shift(1))

    # Price-based features
    df["High_Low_Range"] = df["High"] - df["Low"]

    df["Open_Close_Diff"] = df["Close"] - df["Open"]

    # Volatility
    df["Volatility_{window}"] = (
        df["Daily_Return"]
        .rolling(window=window)
        .std()
    )

    # Volume
    df["Volume_Change"] = df["Volume"].pct_change()

    # Lag Features
    df["Close_Lag_1"] = df["Close"].shift(1)
    df["Close_Lag_2"] = df["Close"].shift(2)
    df["Close_Lag_3"] = df["Close"].shift(3)

    # Rolling Statistics
    df["Rolling_Mean_{window}"] = (
        df["Close"]
        .rolling(window=window)
        .mean()
    )

    df["Rolling_STD_{window}"] = (
        df["Close"]
        .rolling(window=window)
        .std()
    )

    return df


def prepare_data(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    if window < 2:
        raise ValueError("Window size must be at least 2.")

    df = df.copy()

    feature_columns = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Daily_Return",
        "Log_Return",
        "High_Low_Range",
        "Open_Close_Diff",
        f"Volatility_{window}",
        "Volume_Change",
        "Close_Lag_1",
        "Close_Lag_2",
        "Close_Lag_3",
        f"Rolling_Mean_{window}",
        f"Rolling_STD_{window}",
    ]

    df = df[feature_columns]

    df.dropna(inplace=True)

    df.reset_index(drop=True, inplace=True)

    return df