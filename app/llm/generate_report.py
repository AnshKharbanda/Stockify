from app.data.fetcher import fetch_company_info,fetch_stock_data

from app.data.preprocessing import clean_data,create_features,prepare_data

from app.analysis.technicals import calculate_technicals
from app.models.anomaly import detect_anomalies
from app.models.prediction import predict_stock

from app.llm.prompts import build_stock_prompt

from openai import OpenAI

import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment variables.")

client = OpenAI(api_key=api_key)


def generate_stock_report(ticker: str) -> str:
    """
    Generate an AI-powered stock analysis report.
    """

    # Fetch company information
    company_info = fetch_company_info(ticker)

    # Fetch historical stock data
    df = fetch_stock_data(ticker)

    # Preprocess data
    df = clean_data(df)
    df = create_features(df)
    df = prepare_data(df)

    # Perform analysis
    technicals = calculate_technicals(df)
    anomalies = detect_anomalies(df)
    forecast = predict_stock(df)

    # Latest technical indicators
    latest_technicals = technicals.iloc[-1].to_dict()

    # Detected anomalies only
    anomaly_points = (
        anomalies[anomalies["Anomaly"] == -1][["Date", "Close"]]
        .to_dict(orient="records")
    )

    # Forecast data
    forecast_points = forecast.to_dict(orient="records")

    # Build prompt
    prompt = build_stock_prompt(
        company_info=company_info,
        technicals=latest_technicals,
        anomalies=anomaly_points,
        forecast=forecast_points,
    )

    # Generate report
    try:
        response = client.responses.create(
            model="gpt-5.5",
            input=prompt,
        )

        if not response.output_text:
            return (
                "Unable to generate the report at the moment. "
                "The language model returned an empty response."
            )

        return response.output_text

    except Exception as e:

        print(f"LLM Error: {e}")

        return (
            "Unable to generate the AI report at the moment. "
            "Please try again later."
        )