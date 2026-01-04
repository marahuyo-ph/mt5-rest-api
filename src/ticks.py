from fastapi import APIRouter
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
from errors import ErrorResponse

router = APIRouter(prefix="/ticks",tags=["ticks"])

@router.get("/from/{symbol}/{date_from}/{count}")
def copy_ticks_from(symbol: str, date_from: datetime, count: int, flags: int):
    ticks = mt5.copy_ticks_from(symbol, date_from, count, flags)

    if ticks is None:
        return ErrorResponse.model_validate(mt5.last_error())

    df = pd.DataFrame(ticks)

    return df.to_dict(orient="records")


@router.get("/range/{symbol}/{date_from}/{date_to}")
def copy_ticks_range(symbol: str, date_from: datetime, date_to: datetime, flags: int):
    ticks = mt5.copy_ticks_range(symbol, date_from, date_to, flags)

    if ticks is None:
        return ErrorResponse.model_validate(mt5.last_error())

    df = pd.DataFrame(ticks)

    return df.to_dict(orient="records")
