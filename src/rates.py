from fastapi import APIRouter
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd

router = APIRouter(prefix="/rates")


@router.get("/from/{symbol}/{timeframe}/{date_from}/{count}")
def copy_rates_from(symbol: str, timeframe: int, date_from: datetime, count: int):
    rates = mt5.copy_rates_from(symbol, timeframe, date_from, count)

    if not rates:
        return mt5.last_error()

    df = pd.DataFrame(rates)

    return df.to_dict(orient="records")


@router.get("/from-pos/{symbol}/{timeframe}/{start_pos}/{count}")
def copy_rates_from_pos(symbol: str, timeframe: int, start_pos: int, count: int):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count)

    if rates is None:
        return mt5.last_error()

    df = pd.DataFrame(rates)

    return df.to_dict(orient="records")


@router.get("/range/{symbol}/{timeframe}/{date_from}/{date_to}")
def copy_rates_range(
    symbol: str, timeframe: int, date_from: datetime, date_to: datetime
):
    rates = mt5.copy_rates_range(symbol, timeframe, date_from, date_to)

    if rates is None:
        return mt5.last_error()

    df = pd.DataFrame(rates)

    return df.to_dict(orient="records")
