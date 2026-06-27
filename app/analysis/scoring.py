
def score_stock(trend,momentum,volume):
    trend_map={
        "uptrend":4,
        "downtrend":-4,
        "neutral":0
    }

    momentum_map={
        "healthy":2,
        "oversold":1,
        "overbought":-2
    }

    volume_map={
        "strong":2,
        "normal":1,
        "weak":0
    }

    if trend not in trend_map or momentum not in momentum_map or volume not in volume_map:
        return None, None
    
    
    trend_score=trend_map.get(trend, 0)
    momentum_score=momentum_map.get(momentum, 0)
    volume_score=volume_map.get(volume, 0)

    score=trend_score+momentum_score+volume_score

    if score>=6:
        rating="good"
    elif score>=3:
        rating="average"
    else:
        rating="risky"
    
    return score,rating