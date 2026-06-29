from fastapi import FastAPI

from app.routes.stock import stock_router

app = FastAPI(
    title="Stockify API",
    version="1.0.0",
)

app.include_router(stock_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Stockify API"
    }