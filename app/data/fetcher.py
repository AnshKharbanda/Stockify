import requests
import yfinance as yf
import pandas as pd


SEARCH_URL = "https://query1.finance.yahoo.com/v1/finance/search"

def search_stock(query:str)->list[dict]:
    if not query.strip():
        raise ValueError("Search query cannot be empty.")
    
    
    params={
        "q":query,
        "quotesCount":5,
        "newsCount":0
    }
    
    headers={
        "User-Agent":"Mozilla/5.0"
    }
    
    try:
        response = requests.get(
            SEARCH_URL,
            params=params,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

    except requests.RequestException as e:
        raise RuntimeError("Failed to fetch stock search results.") from e

    data = response.json()

    quotes = data.get("quotes", [])
    results = []

    for stock in quotes:

        if stock.get("quoteType") != "EQUITY":
            continue
        
        exchange = stock.get("exchange", "")

        if exchange == "NSI":
            exchange = "NSE"
        elif exchange == "BSE":
            exchange = "BSE"

        results.append(
            {
                "ticker": stock.get("symbol"),
                "name": stock.get("shortname") or stock.get("longname"),
                "exchange": stock.get("exchange"),
            }
        )

    return results


def fetch_stock_data(ticker: str,period: str = "5y",interval: str = "1d",) -> pd.DataFrame:

    if not ticker.strip():
        raise ValueError("Ticker cannot be empty.")

    try:
        stock = yf.Ticker(ticker)

        history = stock.history(
            period=period,
            interval=interval,
            auto_adjust=True,
        )

    except Exception as e:
        raise RuntimeError(f"Failed to fetch historical data for '{ticker}'.") from e

    if history.empty:
        raise ValueError(f"No historical data found for '{ticker}'.")

    history.reset_index(inplace=True)

    return history

def fetch_company_info(ticker: str) -> dict:

    if not ticker.strip():
        raise ValueError("Ticker cannot be empty.")

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

    except Exception as e:
        raise RuntimeError(f"Failed to fetch company information for '{ticker}'.") from e

    if not info:
        raise ValueError(f"No company information found for '{ticker}'.")

    return {
        "ticker": ticker,
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "exchange": info.get("exchange"),
        "currency": info.get("currency"),
        "market_cap": info.get("marketCap"),
        "employees": info.get("fullTimeEmployees"),
        "website": info.get("website"),
        "summary": info.get("longBusinessSummary"),
    }
    
def test():
    stocks=search_stock("apple")
    stock=stocks[0]["ticker"]
    return fetch_stock_data(stock)