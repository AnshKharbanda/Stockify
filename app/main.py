from fastapi import FastAPI

from app.routes.stock import stock_router
from app.routes.analysis import router as analysis_router
from app.routes.report import router as report_router

app = FastAPI(
    title="Stockify API",
    version="1.0.0",
)

app.include_router(stock_router)
app.include_router(analysis_router)
app.include_router(report_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Stockify API"
    }