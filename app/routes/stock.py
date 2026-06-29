from fastapi import APIRouter, HTTPException

from app.data.fetcher import search_stock,fetch_stock_data,fetch_company_info

stock_router = APIRouter(prefix="/stocks",tags=["Stocks"])


@stock_router.get("/search")
def search_stock_endpoint(query: str):
    try:
        return search_stock(query)

    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

    except RuntimeError as e:
        raise HTTPException(status_code=500,detail=str(e))


@stock_router.get("/history/{ticker}")
def get_stock_history(ticker: str):
    try:
        df = fetch_stock_data(ticker)
        
        # Serialize dataframe into Json
        df["Date"] = df["Date"].astype(str)
        return df.to_dict(orient="records")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@stock_router.get("/company/{ticker}")
def get_company_info(ticker: str):
    try:
        return fetch_company_info(ticker)

    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

    except RuntimeError as e:
        raise HTTPException(status_code=500,detail=str(e))