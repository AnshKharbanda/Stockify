import pandas as pd


def _get_scalar(value):
    if hasattr(value, "iloc"):
        value=value.iloc[0]
    return value


def trend_signal(price, ma):
    price=_get_scalar(price)
    ma=_get_scalar(ma)

    if price is None or ma is None or pd.isna(price) or pd.isna(ma):
        return None

    if price>ma:
        return "uptrend"
    elif price<ma:
        return "downtrend"
    else:
        return "neutral"


def momentum_signal(rsi):
    rsi=_get_scalar(rsi)

    if rsi is None or pd.isna(rsi):
        return None

    if rsi>70:
        return "overbought"
    elif rsi<30:
        return "oversold"
    else:
        return "healthy"


def volume_signal(volume_ratio):
    volume_ratio=_get_scalar(volume_ratio)

    if volume_ratio is None or pd.isna(volume_ratio):
        return None

    if volume_ratio>=1.5:
        return "strong"
    elif volume_ratio<0.8:
        return "weak"
    else:
        return "normal"