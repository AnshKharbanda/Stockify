import streamlit as st
import yfinance as yf
from app.analysis.engine import analyze_stock
from app.model.modeltrain import analyze_stock_using_ml
from app.gpt.llm import generate_report
from datetime import datetime
import pandas as pd

st.title("📈 STOCKIFY")

symbol=st.text_input("Enter Stock Symbol (e.g. INFY.NS)")

if st.button("Analyze"):

    df=yf.download(symbol, period="1y", progress=False, auto_adjust=True)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns=df.columns.get_level_values(0)

    if df is None or df.empty:
        st.error("Stock data not found")
    else:
        result,rating=analyze_stock(df)
        ml_output=analyze_stock_using_ml(symbol)

        st.subheader("📊 Analysis")
        st.write(f"**Price:** {result['price']}")

        st.write("### Indicators")
        st.write(f"Moving Average: {result['indicators']['moving_average']}")
        st.write(f"RSI: {result['indicators']['relative_strength_index']}")
        st.write(f"Volume Ratio: {result['indicators']['volume_ratio']}")

        st.write("### Signals")
        st.write(f"Trend: {result['signals']['current_trend']}")
        st.write(f"Momentum: {result['signals']['momentum_trend']}")
        st.write(f"Volume: {result['signals']['volume_trend']}")

        st.write(f"Score: {result['score']}")
        st.write(f"Rating: {rating}")
        
        st.subheader("🤖 ML Analysis")

        confidence, signal, risk, reasons = ml_output

        ml_data = {
            "confidence": round(confidence, 2),
            "signal": signal,
            "risk_level": risk,
            "reasons": reasons
        }
        st.metric("Confidence", ml_data["confidence"])
        st.metric("Signal", ml_data["signal"])
        st.metric("Risk Level", ml_data["risk_level"])
        if ml_data["signal"] == "RED":
            st.error("⚠ High Risk Detected")
        else:
            st.success("✅ Normal Behavior")
        st.write("### Reasons")
        for r in reasons:
            st.write(f"- {r}")

        llm_input = {
            "trend":result["signals"]["current_trend"],
            "momentum":result["signals"]["momentum_trend"],
            "volume":result["signals"]["volume_trend"],
            "confidence":ml_data["confidence"],
            "risk":ml_data["risk_level"],
            "reasons":ml_data["reasons"]
        }
        llm_report = generate_report(llm_input)
        st.subheader("🧠 AI Explanation")
        st.write(llm_report)
        
        
        st.success("Analysis completed")