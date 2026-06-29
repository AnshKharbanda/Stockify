from fastapi import APIRouter, HTTPException

from app.llm.generate_report import generate_stock_report

router = APIRouter(prefix="/report",tags=["Report"])


@router.get("/{ticker}")
def get_stock_report(ticker: str):
    try:
        report = generate_stock_report(ticker)

        return {
            "ticker": ticker.upper(),
            "report": report,
        }

    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

    except RuntimeError as e:
        raise HTTPException(status_code=500,detail=str(e))

    except Exception:
        raise HTTPException(status_code=500,detail="Unexpected server error.")