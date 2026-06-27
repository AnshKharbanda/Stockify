from fastapi import APIRouter, HTTPException
import yfinance as yf
import pandas as pd
from app.analysis.engine import analyze_stock
from datetime import datetime
from app.model.modeltrain import analyze_stock_using_ml
from app.gpt.llm import generate_report

router = APIRouter()


@router.get("/analyze")
def analyze(symbol: str):
    df = yf.download(symbol, period="1y", progress=False, auto_adjust=True)
    if isinstance(df.columns,pd.MultiIndex):
        df.columns=df.columns.get_level_values(0)
        
    
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="Stock data not found")
    
    # indicators analysis
    result,analyzed_risk=analyze_stock(df)
    if result is None:
        raise HTTPException(status_code=500, detail="Analysis failed")
    
    # ml result
    ml_result=analyze_stock_using_ml(symbol)
    
    if ml_result:
        confidence,signal,risk,reasons=ml_result
    else:
        confidence,signal,risk,reasons=None,None,None,None
        
    final_risk=get_final_risk(risk,analyzed_risk)
    
    llm_input={
        "price":result["price"],
        "trend":result["signals"]["current_trend"],
        "momentum":result["signals"]["momentum_trend"],
        "volume":result["signals"]["volume_trend"],
        "signal":signal,
        "confidence":confidence,
        "risk":final_risk,
        "reasons":reasons
    }
    
    llm_report=generate_report(llm_input)
    return {
        "symbol": symbol,
        "time": datetime.now().isoformat(),
        "analysis": result,
        "machine analysis":{
            "confidence":confidence,
            "signal":signal,
            "risk":final_risk,
            "reason":reasons
        },
        "explanation":llm_report
    }
    
def get_final_risk(risk,analyzed_risk):
    if risk=="Red":
        return "high risk"
    elif analyzed_risk=="risky":
        return "medium risk"
    else:
        return "low risk"