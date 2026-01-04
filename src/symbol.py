from fastapi import APIRouter
import MetaTrader5 as mt5  # type: ignore
from pydantic import BaseModel
from models import SymbolProperty, Tick
from errors import ErrorResponse


class SymbolPropertyResponse(BaseModel):
    name: str
    info: SymbolProperty


router = APIRouter(prefix="/symbols", tags=["symbol"])


@router.get(
    "/total",
    summary="Get the number of all financial instruments in the MetaTrader 5 terminal.",
)
def symbols_total() -> int:
    return mt5.symbols_total()


@router.get(
    "/",
    summary="Get all financial instruments from the MetaTrader 5 terminal.",
)
def symbols_get(group: str | None = None):
    symbols = None

    if group:
        symbols = mt5.symbols_get(group)
    else:
        symbols = mt5.symbols_get()

    if not symbols:
        return ErrorResponse.model_validate(mt5.last_error())

    return [
        SymbolPropertyResponse(
            **{"name": symbol._asdict()["name"], "info": symbol._asdict()}
        )
        for symbol in symbols
    ]


@router.get("/{symbol}", summary="Get data on the specified financial instrument.")
def symbol_info(symbol: str):
    current_symbol = mt5.symbol_info(symbol)

    if not current_symbol:
        return ErrorResponse.model_validate(mt5.last_error())

    return SymbolProperty(**current_symbol._asdict())


@router.get("/{symbol}/last-tick", summary="Get the last tick for the specified financial instrument.")
def symbol_info_tick(symbol: str):
    last_tick = mt5.symbol_info_tick(symbol)

    if not last_tick:
        return ErrorResponse.model_validate(mt5.last_error())

    return Tick(**last_tick._asdict())


@router.put("/{symbol}/enable", summary="Select a symbol in the MarketWatch window or remove a symbol from the window.")
def symbol_select(symbol: str, enable: bool | None = None):
    return mt5.symbol_select(symbol, enable)
