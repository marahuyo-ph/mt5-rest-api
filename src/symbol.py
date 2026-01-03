from fastapi import APIRouter
import MetaTrader5 as mt5
from datetime import datetime
from pydantic import BaseModel
from models import SymbolProperty, Tick


class SymbolPropertyResponse(BaseModel):
    name: str
    info: SymbolProperty


router = APIRouter(prefix="/symbols")


@router.get(
    "/total",
    description="Get the number of all financial instruments in the MetaTrader 5 terminal.",
    response_description="Integer value.",
    tags=["symbol"],
)
def symbols_total() -> int:
    return mt5.symbols_total()


@router.get(
    "/",
    description="Get all financial instruments from the MetaTrader 5 terminal.",
    tags=["symbol"],
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
        SymbolPropertyResponse(
            **{"name": symbol._asdict()["name"], "info": symbol._asdict()}
        )
        for symbol in symbols
    ]


@router.get("/{symbol}", tags=["symbol"])
def symbol_info(symbol: str):
    current_symbol = mt5.symbol_info(symbol)

    if not current_symbol:
        return mt5.last_error()

    return SymbolProperty(**current_symbol._asdict())


@router.get("/{symbol}/last-tick", tags=["symbol"])
def symbol_info_tick(symbol: str):
    last_tick = mt5.symbol_info_tick(symbol)

    if not last_tick:
        return mt5.last_error()

    return Tick(**last_tick._asdict())


@router.put(
    "/{symbol}/enable",
    tags=["symbol"],
)
def symbol_select(symbol: str, enable: bool | None = None):
    return mt5.symbol_select(symbol, enable)
