from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from datetime import datetime
import pandas as pd  # type: ignore
from .errors import ErrorResponse
from .models import Rate

router = APIRouter(prefix="/rates", tags=["rates"])


@router.get(
    "/from/{symbol}/{timeframe}/{date_from}/{count}",
    summary="Get OHLC bars from the MetaTrader 5 terminal starting from the specified date",
    description="Retrieves OHLC (Open, High, Low, Close) bars starting from a specified date. Returns an array of bar data with time, open, high, low, close prices, and volume.",
    status_code=200,
    response_model=list[Rate],
    responses={
        200: {
            "description": "Bars retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "time": 1704067200,
                            "open": 1.0825,
                            "high": 1.0890,
                            "low": 1.0815,
                            "close": 1.0850,
                            "tick_volume": 15000,
                            "spread": 10,
                            "real_volume": 50000000,
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
            "description": "Failed to retrieve bars",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to copy rates from terminal",
                    }
                }
            },
        },
    },
)
def copy_rates_from(
    symbol: str = Path(..., description="Symbol name (e.g., 'EURUSD')"),
    timeframe: int = Path(..., description="Timeframe in minutes (e.g., 1, 5, 15, 60, 1440)"),
    date_from: datetime = Path(..., description="Start date for bars in ISO 8601 format"),
    count: int = Path(..., description="Number of bars to retrieve (max typically 1000)"),
):
    rates = mt5.copy_rates_from(symbol, timeframe, date_from, count)

    if rates is None:
        error = ErrorResponse.model_validate(mt5.last_error())
        return JSONResponse(
            status_code=500,
            content=error.model_dump(),
        )

    df = pd.DataFrame(rates)

    return df.to_dict(orient="records")


@router.get(
    "/from-pos/{symbol}/{timeframe}/{start_pos}/{count}",
    summary="Get OHLC bars starting from the specified position index",
    description="Retrieves OHLC bars starting from a specified index position in the terminal's bar history. Useful for paginated bar retrieval.",
    status_code=200,
    response_model=list[Rate],
    responses={
        200: {
            "description": "Bars retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "time": 1704067200,
                            "open": 1.0825,
                            "high": 1.0890,
                            "low": 1.0815,
                            "close": 1.0850,
                            "tick_volume": 15000,
                            "spread": 10,
                            "real_volume": 50000000,
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
                        "message": "Invalid position or count parameters",
                    }
                }
            },
        },
        500: {
            "description": "Failed to retrieve bars",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to copy rates from position",
                    }
                }
            },
        },
    },
)
def copy_rates_from_pos(
    symbol: str = Path(..., description="Symbol name (e.g., 'EURUSD')"),
    timeframe: int = Path(..., description="Timeframe in minutes"),
    start_pos: int = Path(..., description="Starting position index (0-based)"),
    count: int = Path(..., description="Number of bars to retrieve"),
):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count)

    if rates is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    df = pd.DataFrame(rates)

    return df.to_dict(orient="records")


@router.get(
    "/range/{symbol}/{timeframe}/{date_from}/{date_to}",
    summary="Get OHLC bars within a specified date range",
    description="Retrieves OHLC bars for a specific date range. Both start and end dates are included in the result.",
    status_code=200,
    response_model=list[Rate],
    responses={
        200: {
            "description": "Bars retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "time": 1704067200,
                            "open": 1.0825,
                            "high": 1.0890,
                            "low": 1.0815,
                            "close": 1.0850,
                            "tick_volume": 15000,
                            "spread": 10,
                            "real_volume": 50000000,
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
            "description": "Failed to retrieve bars",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to copy rates for range",
                    }
                }
            },
        },
    },
)
def copy_rates_range(
    symbol: str = Path(..., description="Symbol name (e.g., 'EURUSD')"),
    timeframe: int = Path(..., description="Timeframe in minutes"),
    date_from: datetime = Path(..., description="Start date in ISO 8601 format"),
    date_to: datetime = Path(..., description="End date in ISO 8601 format"),
):
    rates = mt5.copy_rates_range(symbol, timeframe, date_from, date_to)

    if rates is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    df = pd.DataFrame(rates)

    return df.to_dict(orient="records")
