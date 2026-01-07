from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from pydantic import BaseModel
from .models import SymbolProperty, Tick
from .errors import ErrorResponse


class SymbolPropertyResponse(BaseModel):
    name: str
    info: SymbolProperty


router = APIRouter(prefix="/symbols", tags=["symbol"])


@router.get(
    "/total",
    summary="Get the number of all financial instruments",
    description="Retrieves the total count of all financial instruments (symbols) available in the MetaTrader5 terminal.",
    responses={
        200: {
            "description": "Total symbol count retrieved successfully",
            "content": {
                "application/json": {
                    "example": 3000
                }
            },
        },
        500: {
            "description": "Failed to retrieve symbol count",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve symbol count",
                    }
                }
            },
        },
    },
)
def symbols_total() -> int:
    return mt5.symbols_total() or 0


@router.get(
    "/",
    summary="Get all financial instruments from the MetaTrader5 terminal",
    description="Retrieves a list of all financial instruments (symbols) available in the MetaTrader5 terminal. Can be filtered by group pattern to retrieve specific symbol groups.",
    status_code=200,
    response_model=list[SymbolPropertyResponse],
    responses={
        200: {
            "description": "Symbols retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "EURUSD",
                            "info": {
                                "name": "EURUSD",
                                "custom": False,
                                "chart_mode": 0,
                                "select": True,
                                "visible": True,
                                "session_deals": 15000,
                                "session_buy_orders": 150,
                                "session_sell_orders": 140,
                                "volume": 50000000,
                                "volumehigh": 55000000,
                                "volumelow": 45000000,
                                "time": 1704067200,
                                "digits": 5,
                                "spread": 10,
                                "spread_real": 10,
                                "trade_mode": 1,
                                "start_time": 0,
                                "expiration_time": 0,
                                "trade_stops": 0,
                                "trade_freeze_level": 0,
                                "trade_execution_mode": 0,
                                "swap_mode": 1,
                                "swap_long": -2.5,
                                "swap_short": -2.8,
                                "swap_sunday": 3.0,
                                "swap_monday": 0.0,
                                "swap_tuesday": 0.0,
                                "swap_wednesday": 0.0,
                                "swap_thursday": 0.0,
                                "swap_friday": 0.0,
                                "swap_saturday": 0.0,
                                "margin_initial": 0.0,
                                "margin_maintenance": 0.0,
                                "session_interest": 0.0,
                                "ticks_booksize": 0,
                                "trade_calc_mode": 0,
                                "mode": 1,
                                "bid": 1.0850,
                                "ask": 1.0852,
                                "last": 1.0850,
                                "session_volume": 50000000,
                                "session_open": 1.0825,
                                "session_close": 0.0,
                                "session_high": 1.0890,
                                "session_low": 1.0815,
                                "volume_real": 50000000,
                                "price_open": 1.0825,
                                "settle": 0.0,
                                "price_high": 1.0890,
                                "price_low": 1.0815,
                                "price_weighted_avg": 1.0850,
                            },
                        }
                    ]
                }
            },
        },
        500: {
            "description": "Failed to retrieve symbols",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve symbols",
                    }
                }
            },
        },
    },
)
def symbols_get(group: str | None = Query(None, description="Symbol group filter (e.g., 'Forex', 'Indices')")):
    symbols = None

    if group:
        symbols = mt5.symbols_get(group)
    else:
        symbols = mt5.symbols_get()

    if not symbols:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.model_validate(mt5.last_error()).model_dump(),
        )

    return [
        SymbolPropertyResponse(
            **{"name": symbol._asdict()["name"], "info": symbol._asdict()}
        )
        for symbol in symbols
    ]


@router.get(
    "/{symbol}",
    summary="Get data on the specified financial instrument.",
    status_code=200,
)
def symbol_info(symbol: str):
    current_symbol = mt5.symbol_info(symbol)

    if current_symbol is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    return SymbolProperty(**current_symbol._asdict())


@router.get(
    "/{symbol}/last-tick",
    summary="Get the last tick for the specified financial instrument.",
    status_code=200,
    response_model=list[Tick]
)
def symbol_info_tick(symbol: str):
    last_tick = mt5.symbol_info_tick(symbol)

    if last_tick is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    return Tick(**last_tick._asdict())


@router.put(
    "/{symbol}/enable",
    summary="Select a symbol in the MarketWatch window or remove a symbol from the window.",
)
def symbol_select(symbol: str, enable: bool | None = None) -> bool:
    return mt5.symbol_select(symbol, enable) or False
