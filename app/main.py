from fastapi import FastAPI
from app.api.routes import router

app=FastAPI(
    title="AI Stock Analyzer",
    description="Stock analysis with ML-based anomaly detection",
    version="1.0.0"
)

app.include_router(router)