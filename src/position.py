from fastapi import APIRouter, Query
import MetaTrader5 as mt5  # type: ignore
from .models import Position
from .errors import ErrorResponse

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get(
    "/total",
    summary="Get the number of open positions",
    description="Retrieves the total count of currently open positions in the trading account.",
    responses={
        200: {
            "description": "Total position count retrieved successfully",
            "content": {
                "application/json": {
                    "example": 5
                }
            },
        },
        500: {
            "description": "Failed to retrieve position count",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve position count",
                    }
                }
            },
        },
    },
    status_code=200,
)
def positions_total() -> int:
    return mt5.positions_total() or 0


@router.get(
    "/",
    summary="Get open positions with optional filtering",
    description="Retrieves a list of open positions. Can be filtered by symbol name, group pattern, or ticket number. If no filter is provided, returns all open positions.",
    status_code=200,
    response_model=list[Position],
    responses={
        200: {
            "description": "Positions retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "ticket": 123456,
                            "time": 1704067200,
                            "type": 0,
                            "magic": 0,
                            "identifier": 0,
                            "reason": 0,
                            "volume": 1.0,
                            "price_open": 1.0850,
                            "sl": 1.0800,
                            "tp": 1.0900,
                            "price_current": 1.0860,
                            "swap": -2.50,
                            "profit": 100.0,
                            "symbol": "EURUSD",
                            "comment": "Buy position",
                            "external_id": "",
                            "time_update": 1704067300,
                            "time_msc": 1704067200000,
                            "time_update_msc": 1704067300000,
                        }
                    ]
                }
            },
        },
        500: {
            "description": "Failed to retrieve positions",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve positions",
                    }
                }
            },
        },
    },
)
def positions_get(
    symbol: str | None = Query(None, description="Filter by symbol name (e.g., 'EURUSD')"),
    group: str | None = Query(None, description="Filter by group pattern (e.g., 'Forex')"),
    ticket: int | None = Query(None, description="Filter by position ticket number"),
):
    positions: tuple[mt5.Position, ...] | None = None

    if symbol:
        positions = mt5.positions_get(symbol=symbol)
    elif group:
        positions = mt5.positions_get(group=group)
    elif ticket:
        positions = mt5.positions_get(ticket=ticket)
    else:
        positions = mt5.positions_get()

    if positions is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    return [Position(**position._asdict()) for position in positions]
