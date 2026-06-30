from fastapi import APIRouter, HTTPException

from app.data.fetcher import fetch_stock_data
from app.data.preprocessing import clean_data,create_features,prepare_data
from app.analysis.technicals import calculate_technicals
from app.models.anomaly import detect_anomalies
from app.models.prediction import predict_stock
from app.utils.serialization import dataframe_to_json
import numpy as np
import pandas as pd

router = APIRouter(prefix="/analysis",tags=["Analysis"])


def preprocess_stock_data(ticker: str):
    df = fetch_stock_data(ticker)

    df = clean_data(df)
    df = create_features(df)
    df = prepare_data(df)

    return df


@router.get("/{ticker}")
def get_complete_analysis(ticker: str):
    try:
        df = preprocess_stock_data(ticker)

        technicals = calculate_technicals(df)
        anomalies = detect_anomalies(df)
        forecast = predict_stock(df)

        return {
            "technicals": dataframe_to_json(technicals),
            "anomalies": dataframe_to_json(anomalies),
            "forecast": dataframe_to_json(forecast),
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/technical/{ticker}")
def get_technical_analysis(ticker: str):
    try:
        df = preprocess_stock_data(ticker)

        technicals = calculate_technicals(df)
        
        # print(technicals.isna().sum())
        # print(np.isinf(technicals.select_dtypes(include="number")).sum())

        return dataframe_to_json(technicals)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/anomalies/{ticker}")
def get_anomaly_analysis(ticker: str):
    try:
        df = preprocess_stock_data(ticker)

        anomalies = detect_anomalies(df)

        return dataframe_to_json(anomalies)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/prediction/{ticker}")
def get_prediction(ticker: str):
    try:
        df = preprocess_stock_data(ticker)

        forecast = predict_stock(df)

        return dataframe_to_json(forecast)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )