import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def create_features(df):
    df=df.copy()

    df['returns']=df['Close'].pct_change()
    df['ma_20']=df['Close'].rolling(20).mean()
    df['ma_distance']=(df['Close'] - df['ma_20'])/df['ma_20']
    df['volatility']=df['returns'].rolling(20).std()
    df['volume_ratio']=df['Volume']/df['Volume'].rolling(20).mean()

    df = df.dropna()

    return df[['returns','volatility','ma_distance','volume_ratio']]


def train_model():
    stocks=[
        "RELIANCE.NS", "TCS.NS", "INFY.NS",
        "HDFCBANK.NS", "ICICIBANK.NS",
        "SBIN.NS", "ITC.NS", "LT.NS"
    ]

    all_data=[]

    for s in stocks:
        df=yf.download(s, period="5y", progress=False)
        if isinstance(df.columns,pd.MultiIndex):
            df.columns=df.columns.get_level_values(0)
        if df is None or df.empty:
            continue

        features=create_features(df)
        all_data.append(features)

    X=pd.concat(all_data)

    scaler=StandardScaler()
    X_scaled=scaler.fit_transform(X)

    model=IsolationForest(contamination=0.05, random_state=42)
    model.fit(X_scaled)

    return model,scaler


model,scaler = train_model()

def score_to_confidence(score):
    return 1/(1 + np.exp(score * 5))


def analyze_stock_using_ml(symbol: str):
    df=yf.download(symbol, period="1y", progress=False)
    if isinstance(df.columns,pd.MultiIndex):
        df.columns=df.columns.get_level_values(0)

    if df is None or df.empty:
        return None

    features=create_features(df)

    if features.empty:
        return None

    latest=features.iloc[-1:].values
    latest_scaled=scaler.transform(latest)

    score=model.decision_function(latest_scaled)[0]

    confidence=score_to_confidence(score)
    confidence=round(confidence,2)

    # signal
    if confidence>0.7:
        signal="RED"   # red signal
    else:
        signal="GREEN" # green signal

    risk=get_risk_level(float(confidence))
    
    reasons=get_reason(features)
    
    return float(confidence),signal,risk,reasons



def get_risk_level(confidence:float):
    if confidence is None:
        return None
    
    if confidence>=0.75:
        return "high"
    elif confidence>=0.5:
        return "medium"
    else:
        return "low"
    
    
def get_reason(features):
    reasons=[]
    
    latest=features.iloc[-1]
    
    if latest['volume_ratio']>1.8:
        reasons.append("high volume spike")
        
    if abs(latest['ma_distance'])>0.1:
        reasons.append("change from trend")
        
    if not reasons:
        reasons.append("no abnormal patterns detected")
        
    return reasons