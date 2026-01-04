from fastapi import APIRouter
import MetaTrader5 as mt5  # type: ignore
from datetime import datetime
import pandas as pd  # type: ignore
from errors import ErrorResponse

router = APIRouter(prefix="/rates", tags=["rates"])


@router.get(
    "/from/{symbol}/{timeframe}/{date_from}/{count}",
    summary="Get bars from the MetaTrader 5 terminal starting from the specified date.",
    status_code=200,
)
def copy_rates_from(symbol: str, timeframe: int, date_from: datetime, count: int):
    rates = mt5.copy_rates_from(symbol, timeframe, date_from, count)

    if not rates:
        return ErrorResponse.model_validate(mt5.last_error())

    df = pd.DataFrame(rates)

    return df.to_dict(orient="records")


@router.get(
    "/from-pos/{symbol}/{timeframe}/{start_pos}/{count}",
    summary="Get bars from the MetaTrader 5 terminal starting from the specified index.",
    status_code=200,
)
def copy_rates_from_pos(symbol: str, timeframe: int, start_pos: int, count: int):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count)

    if rates is None:
        return ErrorResponse.model_validate(mt5.last_error())

    df = pd.DataFrame(rates)

    return df.to_dict(orient="records")


@router.get(
    "/range/{symbol}/{timeframe}/{date_from}/{date_to}",
    summary="Get bars in the specified date range from the MetaTrader 5 terminal.",
    status_code=200,
)
def copy_rates_range(
    symbol: str, timeframe: int, date_from: datetime, date_to: datetime
):
    rates = mt5.copy_rates_range(symbol, timeframe, date_from, date_to)

    if rates is None:
        return ErrorResponse.model_validate(mt5.last_error())

    df = pd.DataFrame(rates)

    return df.to_dict(orient="records")
