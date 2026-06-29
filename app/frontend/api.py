import requests


BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 30


def _get(endpoint: str, params: dict | None = None):
    """
    Send GET request to FastAPI backend.
    """

    try:
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            params=params,
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"API request failed: {e}"
        ) from e


def search_stock(query: str):
    return _get(
        "/stocks/search",
        params={"query": query},
    )


def get_company(ticker: str):
    return _get(
        f"/stocks/company/{ticker}",
    )


def get_history(ticker: str):
    return _get(
        f"/stocks/history/{ticker}",
    )


def get_technicals(ticker: str):
    return _get(
        f"/analysis/technical/{ticker}",
    )


def get_anomalies(ticker: str):
    return _get(
        f"/analysis/anomalies/{ticker}",
    )


def get_prediction(ticker: str):
    return _get(
        f"/analysis/prediction/{ticker}",
    )


def get_complete_analysis(ticker: str):
    return _get(
        f"/analysis/{ticker}",
    )


def get_report(ticker: str):
    return _get(
        f"/report/{ticker}",
    )