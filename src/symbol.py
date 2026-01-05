from fastapi import APIRouter
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
    summary="Get the number of all financial instruments in the MetaTrader 5 terminal.",
)
def symbols_total() -> int:
    return mt5.symbols_total() or 0


@router.get(
    "/",
    summary="Get all financial instruments from the MetaTrader 5 terminal.",
    status_code=200,
    response_model=list[SymbolPropertyResponse],
)
def symbols_get(group: str | None = None):
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
    response_model=SymbolProperty,
)
def symbol_info(symbol: str):
    current_symbol = mt5.symbol_info(symbol)

    if not current_symbol:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.model_validate(mt5.last_error()).model_dump(),
        )

    return SymbolProperty(**current_symbol._asdict())


@router.get(
    "/{symbol}/last-tick",
    summary="Get the last tick for the specified financial instrument.",
    status_code=200,
    response_model=Tick,
)
def symbol_info_tick(symbol: str):
    last_tick = mt5.symbol_info_tick(symbol)

    if not last_tick:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.model_validate(mt5.last_error()).model_dump(),
        )

    return Tick(**last_tick._asdict())


@router.put(
    "/{symbol}/enable",
    summary="Select a symbol in the MarketWatch window or remove a symbol from the window.",
)
def symbol_select(symbol: str, enable: bool | None = None) -> bool:
    return mt5.symbol_select(symbol, enable) or False
