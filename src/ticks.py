from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from datetime import datetime
import pandas as pd  # type: ignore
from .errors import ErrorResponse
from .models import Tick

router = APIRouter(prefix="/ticks", tags=["ticks"])


@router.get(
    "/from/{symbol}/{date_from}/{count}",
    summary="Get tick data starting from the specified date",
    description="Retrieves tick data (bid/ask prices and volume) from the MetaTrader5 terminal starting from a specified date. Ticks represent individual price changes in the market.",
    status_code=200,
    response_model=list[Tick],
    responses={
        200: {
            "description": "Ticks retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "time": 1704067200,
                            "bid": 1.0850,
                            "ask": 1.0852,
                            "last": 1.0850,
                            "volume": 100,
                            "time_msc": 1704067200000,
                            "flags": 0,
                        }
                    ]
                }
            },
        },
        400: {
            "description": "Invalid parameters provided",
            "content": {
                "application/json": {
                    "example": {
                        "code": -2,
                        "message": "Invalid date or count parameters",
                    }
                }
            },
        },
        500: {
            "description": "Failed to retrieve ticks",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to copy ticks from terminal",
                    }
                }
            },
        },
    },
)
def copy_ticks_from(
    symbol: str = Path(..., description="Symbol name (e.g., 'EURUSD')"),
    date_from: datetime = Path(..., description="Start date in ISO 8601 format"),
    count: int = Path(..., description="Number of ticks to retrieve"),
    flags: int = Query(..., description="Flags controlling tick data type (COPY_TICKS_ALL=0, COPY_TICKS_INFO=1, COPY_TICKS_TRADE=2)"),
):
    ticks = mt5.copy_ticks_from(symbol, date_from, count, flags)

    if ticks is None:
        error = ErrorResponse.model_validate(mt5.last_error())
        return JSONResponse(
            status_code=500,
            content=error.model_dump(),
        )

    df = pd.DataFrame(ticks)

    return df.to_dict(orient="records")


@router.get(
    "/range/{symbol}/{date_from}/{date_to}",
    summary="Get tick data for the specified date range",
    description="Retrieves tick data for a specific date range. Both start and end dates are included in the result. Ticks represent individual price changes in the market.",
    status_code=200,
    response_model=list[Tick],
    responses={
        200: {
            "description": "Ticks retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "time": 1704067200,
                            "bid": 1.0850,
                            "ask": 1.0852,
                            "last": 1.0850,
                            "volume": 100,
                            "time_msc": 1704067200000,
                            "flags": 0,
                        }
                    ]
                }
            },
        },
        400: {
            "description": "Invalid date range provided",
            "content": {
                "application/json": {
                    "example": {
                        "code": -2,
                        "message": "Invalid date range",
                    }
                }
            },
        },
        500: {
            "description": "Failed to retrieve ticks",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to copy ticks for range",
                    }
                }
            },
        },
    },
)
def copy_ticks_range(
    symbol: str = Path(..., description="Symbol name (e.g., 'EURUSD')"),
    date_from: datetime = Path(..., description="Start date in ISO 8601 format"),
    date_to: datetime = Path(..., description="End date in ISO 8601 format"),
    flags: int = Query(..., description="Flags controlling tick data type (COPY_TICKS_ALL=0, COPY_TICKS_INFO=1, COPY_TICKS_TRADE=2)"),
):
    ticks = mt5.copy_ticks_range(symbol, date_from, date_to, flags)

    if ticks is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    df = pd.DataFrame(ticks)

    return df.to_dict(orient="records")
