from fastapi import APIRouter
import MetaTrader5 as mt5
from datetime import datetime
from errors import ErrorResponse

router = APIRouter(prefix="/history")


@router.get("/orders/total")
def history_orders_total():
    return mt5.history_orders_total()


@router.get("/orders/")
def history_orders_get(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    group: str | None = None,
    ticket: int | None = None,
    position: int | None = None,
):
    orders: tuple[mt5.Order, ...] | None = None

    if date_from and date_to and group:
        orders = mt5.history_orders_get(
            date_from=date_from, date_to=date_to, group=group
        )
    elif ticket:
        orders = mt5.history_orders_get(ticket=ticket)
    elif position:
        orders = mt5.history_orders_get(position=position)
    else:
        return {"Invalid query": "Invalid query parameters"}

    if not orders:
        return ErrorResponse.model_validate(mt5.last_error())

    return [order._asdict() for order in orders]


@router.get("/deals/total")
def history_deals_total():
    return mt5.history_deals_total()


@router.get("/deals/")
def history_deals_get(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    group: str | None = None,
    ticket: int | None = None,
    position: int | None = None,
):
    deals: tuple[mt5.Deal, ...] | None = None

    if date_from and date_to and group:
        deals = mt5.history_deals_get(date_from=date_from, date_to=date_to, group=group)
    elif ticket:
        deals = mt5.history_deals_get(ticket=ticket)
    elif position:
        deals = mt5.history_deals_get(position=position)
    else:
        return {"Invalid query": "Invalid query parameters"}

    if not deals:
        return ErrorResponse.model_validate(mt5.last_error())

    return [deal._asdict() for deal in deals]
