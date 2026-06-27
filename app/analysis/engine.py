import pandas as pd
from app.analysis.indicators import calculate_ma, calculate_rsi, calculate_vol_trend
from app.analysis.signals import trend_signal, momentum_signal, volume_signal
from app.analysis.scoring import score_stock


def _get_scalar(value):
    if hasattr(value, "iloc"):
        value=value.iloc[0]
    return value


def analyze_stock(df):
    if df is None or df.empty:
        return None

    # FIX price extraction
    price=_get_scalar(df['Close'].iloc[-1])

    if price is None or pd.isna(price):
        return None

    price=float(price)

    # indicators
    ma=calculate_ma(df)
    rsi=calculate_rsi(df)
    vol_ratio=calculate_vol_trend(df)
    
    # round
    price=round(price, 2)
    ma=round(ma, 2) if ma else None
    rsi=round(rsi, 2) if rsi else None
    vol_ratio=round(vol_ratio, 2) if vol_ratio else None

    # signals
    trend=trend_signal(price, ma)
    momentum=momentum_signal(rsi)
    volume=volume_signal(vol_ratio)

    # scoring
    score,rating=score_stock(trend, momentum, volume)

    result = {
        "price":price,
        "indicators":{
            "moving_average":ma,
            "relative_strength_index":rsi,
            "volume_ratio":vol_ratio
        },
        "signals":{
            "current_trend":trend,
            "momentum_trend":momentum,
            "volume_trend":volume
        }
    }

    if score and rating:
        result["score"]=score

    return result,rating