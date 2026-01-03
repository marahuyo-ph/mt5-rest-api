from fastapi import APIRouter
import MetaTrader5 as mt5
from models import CalculateMarginPayload, CalculateProfitPayload, TradeRequest

router = APIRouter(prefix="/orders")


@router.get("/total")
def orders_total():
    return mt5.orders_total()


@router.get("/")
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
        return mt5.last_error()

    return [order._asdict() for order in orders]


@router.post("/calculate-margin")
def orders_calc_margin(payload: CalculateMarginPayload):
    return mt5.order_calc_margin(
        payload.action, payload.symbol, payload.volume, payload.price
    )


@router.post("/calculate-profit")
def orders_calc_profit(payload: CalculateProfitPayload):
    return mt5.order_calc_profit(
        payload.action,
        payload.symbol,
        payload.volume,
        payload.price_open,
        payload.price_close,
    )


@router.post("/check")
def orders_check(payload: TradeRequest):
    return mt5.order_check(
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


@router.post("/send")
def orders_send(payload: TradeRequest):
    return mt5.order_send(
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
