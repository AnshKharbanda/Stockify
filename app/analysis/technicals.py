import pandas as pd

# Configuration

SMA_WINDOW = 20
EMA_WINDOW = 20

RSI_WINDOW = 14

MACD_SHORT = 12
MACD_LONG = 26
MACD_SIGNAL = 9

BB_WINDOW = 20
BB_STD = 2


# Private Helper Functions

def _calculate_sma(df: pd.DataFrame) -> pd.DataFrame:
    df[f"SMA_{SMA_WINDOW}"] = (
        df["Close"]
        .rolling(window=SMA_WINDOW)
        .mean()
    )

    return df


def _calculate_ema(df: pd.DataFrame) -> pd.DataFrame:
    df[f"EMA_{EMA_WINDOW}"] = (
        df["Close"]
        .ewm(span=EMA_WINDOW, adjust=False)
        .mean()
    )

    return df


def _calculate_rsi(df: pd.DataFrame) -> pd.DataFrame:
    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=RSI_WINDOW).mean()
    avg_loss = loss.rolling(window=RSI_WINDOW).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = 100 - (100 / (1 + rs))

    return df


def _calculate_macd(df: pd.DataFrame) -> pd.DataFrame:
    ema_short = (
        df["Close"]
        .ewm(span=MACD_SHORT, adjust=False)
        .mean()
    )

    ema_long = (
        df["Close"]
        .ewm(span=MACD_LONG, adjust=False)
        .mean()
    )

    df["MACD"] = ema_short - ema_long

    df["MACD_Signal"] = (
        df["MACD"]
        .ewm(span=MACD_SIGNAL, adjust=False)
        .mean()
    )

    df["MACD_Histogram"] = (
        df["MACD"] - df["MACD_Signal"]
    )

    return df


def _calculate_bollinger_bands(df: pd.DataFrame) -> pd.DataFrame:
    sma = (
        df["Close"]
        .rolling(window=BB_WINDOW)
        .mean()
    )

    std = (
        df["Close"]
        .rolling(window=BB_WINDOW)
        .std()
    )

    df["BB_Middle"] = sma

    df["BB_Upper"] = sma + (BB_STD * std)

    df["BB_Lower"] = sma - (BB_STD * std)

    return df



# Public Function
def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    df = df.copy()

    df = _calculate_sma(df)
    df = _calculate_ema(df)
    df = _calculate_rsi(df)
    df = _calculate_macd(df)
    df = _calculate_bollinger_bands(df)

    return df