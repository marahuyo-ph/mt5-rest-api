from fastapi import APIRouter
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from datetime import datetime
from .errors import ErrorResponse
from .models import Order, Deal

router = APIRouter(prefix="/history", tags=["history"])


@router.get(
    "/orders/total",
    summary="Get the number of orders in trading history within the specified interval.",
    status_code=200,
)
def history_orders_total() -> int:
    return mt5.history_orders_total() or 0


@router.get(
    "/orders/",
    summary="Get orders from trading history with the ability to filter by ticket or position.",
    status_code=200,
    response_model=list[Order],
)
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
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.model_validate(mt5.last_error()).model_dump(),
        )

    return [Order(**order._asdict()) for order in orders]


@router.get(
    "/deals/total",
    summary="Get the number of deals in trading history within the specified interval.",
    status_code=200,
)
def history_deals_total() -> int:
    return mt5.history_deals_total() or 0


@router.get(
    "/deals/",
    summary="Get deals from trading history within the specified interval with the ability to filter by ticket or position.",
    status_code=200,
    response_model=list[Deal],
)
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
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.model_validate(mt5.last_error()).model_dump(),
        )

    return [Deal(**deal._asdict()) for deal in deals]
