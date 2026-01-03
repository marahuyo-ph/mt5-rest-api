from fastapi import APIRouter
import MetaTrader5 as mt5
from datetime import datetime
from models import SymbolPropertyResponse

router = APIRouter(prefix="/symbols")


@router.get(
    "/total",
    description="Get the number of all financial instruments in the MetaTrader 5 terminal.",
    response_description="Integer value.",
)
def copy_rates() -> int:
    return mt5.symbols_total()


@router.get(
    "/",
    description="Get all financial instruments from the MetaTrader 5 terminal.",
    response_model=list[SymbolPropertyResponse],
)
def symbols_get(group: str | None = None):
    symbols = None

    if group:
        symbols = mt5.symbols_get(group)
    else:
        symbols = mt5.symbols_get()

    if not symbols:
        return mt5.last_error()

    return [
        {"name": symbol._asdict()["name"], "info": symbol._asdict()}
        for symbol in symbols
    ]


@router.get("/{symbol}")
def symbol_info(symbol: str):
    current_symbol = mt5.symbol_info(symbol)

    if not current_symbol:
        return mt5.last_error()

    return current_symbol._asdict()


@router.get("/{symbol}/last-tick")
def symbol_info_tick(symbol: str):
    last_tick = mt5.symbol_info_tick(symbol)

    if not last_tick:
        return mt5.last_error()

    return last_tick._asdict()


@router.post("/{symbol}/enable")
def symbol_select(symbol: str, enable: bool | None = None):
    return mt5.symbol_select(symbol, enable)
