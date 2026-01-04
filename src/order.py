from fastapi import APIRouter
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from .models import TradeRequest, Order
from pydantic import BaseModel
from .errors import ErrorResponse

router = APIRouter(prefix="/orders", tags=["orders"])


class CalculateMarginRequest(BaseModel):
    action: int
    symbol: str
    volume: float
    price: float


class CalculateProfitRequest(BaseModel):
    action: int
    symbol: str
    volume: float
    price_open: float
    price_close: float


@router.get(
    "/total",
    summary="Get the number of active orders.",
    status_code=200,
)
def orders_total():
    return mt5.orders_total()


@router.get(
    "/",
    summary="Get active orders with the ability to filter by symbol or ticket.",
    status_code=200,
)
def orders_get(
    symbol: str | None = None, group: str | None = None, ticket: int | None = None
):
    orders: tuple[mt5.Order, ...] | None = None

    if symbol:
        orders = mt5.orders_get(symbol=symbol)
    elif group:
        orders = mt5.orders_get(group=group)
    elif ticket:
        orders = mt5.orders_get(ticket=ticket)
    else:
        orders = mt5.orders_get()

    if orders is None:
        return JSONResponse(
            status_code=500, content=ErrorResponse.model_validate(mt5.last_error()).model_dump()
        )

    return [Order(**order._asdict()) for order in orders]


@router.post(
    "/calculate-margin",
    summary="Return margin in the account currency to perform a specified trading operation.",
    status_code=200,
)
def orders_calc_margin(payload: CalculateMarginRequest):
    margin = mt5.order_calc_margin(
        payload.action, payload.symbol, payload.volume, payload.price
    )

    if not margin:
        return JSONResponse(
            status_code=500, content=ErrorResponse.model_validate(mt5.last_error()).model_dump()
        )

    return margin


@router.post(
    "/calculate-profit",
    summary="Return profit in the account currency for a specified trading operation.",
    status_code=200,
)
def orders_calc_profit(payload: CalculateProfitRequest):
    profit = mt5.order_calc_profit(
        payload.action,
        payload.symbol,
        payload.volume,
        payload.price_open,
        payload.price_close,
    )

    if not profit:
        return JSONResponse(
            status_code=500, content=ErrorResponse.model_validate(mt5.last_error()).model_dump()
        )

    return profit


@router.post(
    "/check",
    summary="Check funds sufficiency for performing a required trading operation. Check result are returned as the TradeCheckResult structure.",
    status_code=200,
)
def orders_check(payload: TradeRequest):
    check_result = mt5.order_check(
        mt5.TradeRequest(
            {
                "action": payload.action,
                "magic": payload.magic,
                "order": payload.order,
                "symbol": payload.symbol,
                "volume": payload.volume,
                "price": payload.price,
                "stoplimit": payload.stoplimit,
                "sl": payload.sl,
                "tp": payload.tp,
                "deviation": payload.deviation,
                "type": payload.type,
                "type_filling": payload.type_filling,
                "type_time": payload.type_time,
                "expiration": payload.expiration,
                "comment": payload.comment,
                "position": payload.position,
                "position_by": payload.position_by,
            }
        )
    )

    if not check_result:
        return JSONResponse(
            status_code=500, content=ErrorResponse.model_validate(mt5.last_error()).model_dump()
        )

    return check_result


@router.post(
    "/send",
    summary="Send a request to perform a trading operation from the terminal to the trade server. The function is similar to OrderSend.",
    status_code=201,
)
def orders_send(payload: TradeRequest):
    result = mt5.order_send(
        mt5.TradeRequest(
            {
                "action": payload.action,
                "magic": payload.magic,
                "order": payload.order,
                "symbol": payload.symbol,
                "volume": payload.volume,
                "price": payload.price,
                "stoplimit": payload.stoplimit,
                "sl": payload.sl,
                "tp": payload.tp,
                "deviation": payload.deviation,
                "type": payload.type,
                "type_filling": payload.type_filling,
                "type_time": payload.type_time,
                "expiration": payload.expiration,
                "comment": payload.comment,
                "position": payload.position,
                "position_by": payload.position_by,
            }
        )
    )

    if not result:
        return JSONResponse(
            status_code=500, content=ErrorResponse.model_validate(mt5.last_error()).model_dump()
        )

    return result
