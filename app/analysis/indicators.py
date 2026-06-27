import pandas as pd

# to covert series->float
def _get_scalar(value):
    if hasattr(value, "iloc"):
        value=value.iloc[0]
    return value

# mean average of 200 days
def calculate_ma(df,window=200):
    if df is None or df.empty or len(df)<window:
        return None

    ma=df['Close'].rolling(window=window).mean()
    value=_get_scalar(ma.iloc[-1])

    if pd.isna(value):
        return None

    return float(value)


# RSI
def calculate_rsi(df,window=14):
    if df is None or df.empty or len(df) < window:
        return None

    delta=df['Close'].diff()

    gains=delta.where(delta > 0, 0)
    loss=-delta.where(delta < 0, 0)

    avg_gain=gains.rolling(window=window).mean()
    avg_loss=loss.rolling(window=window).mean()

    mean_loss=_get_scalar(avg_loss.iloc[-1])

    if pd.isna(mean_loss):
        return None

    if mean_loss==0:
        return 100.0

    rs=avg_gain/avg_loss
    rsi=100-(100 / (1 + rs))

    value=_get_scalar(rsi.iloc[-1])

    if pd.isna(value):
        return None

    return float(value)


# volume indicator
def calculate_vol_trend(df,window=20):
    if df is None or df.empty or len(df) < window:
        return None

    mean_vol=df['Volume'].rolling(window=window).mean()

    latest_mean=_get_scalar(mean_vol.iloc[-1])
    latest_vol=_get_scalar(df['Volume'].iloc[-1])

    if pd.isna(latest_mean) or latest_mean == 0:
        return None

    vol_index=latest_vol / latest_mean

    return float(vol_index)