from fastapi import APIRouter
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from datetime import datetime
import pandas as pd  # type: ignore
from .errors import ErrorResponse, ErrorCodes
from .models import Tick

router = APIRouter(prefix="/ticks", tags=["ticks"])


@router.get(
    "/from/{symbol}/{date_from}/{count}",
    summary="Get ticks from the MetaTrader 5 terminal starting from the specified date.",
    status_code=200,
)
def copy_ticks_from(symbol: str, date_from: datetime, count: int, flags: int):
    ticks = mt5.copy_ticks_from(symbol, date_from, count, flags)

    if ticks is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    df = pd.DataFrame(ticks)

    return df.to_dict(orient="records")


@router.get(
    "/range/{symbol}/{date_from}/{date_to}",
    summary="Get ticks for the specified date range from the MetaTrader 5 terminal.",
    status_code=200,
)
def copy_ticks_range(symbol: str, date_from: datetime, date_to: datetime, flags: int):
    ticks = mt5.copy_ticks_range(symbol, date_from, date_to, flags)

    if ticks is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    df = pd.DataFrame(ticks)

    return df.to_dict(orient="records")
