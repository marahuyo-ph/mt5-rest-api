from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from datetime import datetime
from .errors import ErrorResponse, ErrorCodes
from .models import Order, Deal

router = APIRouter(prefix="/history", tags=["history"])


@router.get(
    "/orders/total",
    summary="Get the total count of orders in trading history",
    description="Retrieves the total number of orders recorded in the trading history of the account.",
    responses={
        200: {
            "description": "Total order count retrieved successfully",
            "content": {
                "application/json": {
                    "example": 150
                }
            },
        },
        500: {
            "description": "Failed to retrieve order count",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve history order count",
                    }
                }
            },
        },
    },
    status_code=200,
)
def history_orders_total() -> int:
    return mt5.history_orders_total() or 0


@router.get(
    "/orders/",
    summary="Get executed orders from trading history with optional filtering",
    description="Retrieves orders from the trading history. Can be filtered by date range, group, ticket, or position. At least one filter parameter is required.",
    status_code=200,
    response_model=list[Order],
    responses={
        200: {
            "description": "Historical orders retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "ticket": 123456,
                            "time_setup": 1704067200,
                            "type": 1,
                            "state": 2,
                            "magic": 0,
                            "time_expiration": 0,
                            "type_filling": 0,
                            "type_time": 0,
                            "reason": 1,
                            "volume_initial": 1.0,
                            "volume_current": 0.0,
                            "price_open": 1.0850,
                            "sl": 0.0,
                            "tp": 0.0,
                            "price_current": 1.0850,
                            "symbol": "EURUSD",
                            "comment": "Executed order",
                            "position_id": 123451,
                            "position_by_id": 0,
                            "external_id": "",
                            "time_setup_msc": 1704067200000,
                        }
                    ]
                }
            },
        },
        400: {
            "description": "No filter parameters provided",
            "content": {
                "application/json": {
                    "example": {
                        "code": -2,
                        "message": "At least one filter parameter is required",
                    }
                }
            },
        },
        500: {
            "description": "Failed to retrieve orders",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve history orders",
                    }
                }
            },
        },
    },
)
def history_orders_get(
    date_from: datetime | None = Query(None, description="Start date for history range (ISO 8601 format)"),
    date_to: datetime | None = Query(None, description="End date for history range (ISO 8601 format)"),
    group: str | None = Query(None, description="Group filter pattern (e.g., 'Forex')"),
    ticket: int | None = Query(None, description="Filter by specific order ticket number"),
    position: int | None = Query(None, description="Filter by position ID"),
):
    orders: tuple[mt5.Order, ...] | None = None

    if date_from and date_to and group:
        orders = mt5.history_orders_get(
            date_from=date_from, date_to=date_to, group=group
        )
    elif date_from and date_to:
        orders = mt5.history_orders_get(
            date_from=date_from, date_to=date_to
        )
    elif ticket:
        orders = mt5.history_orders_get(ticket=ticket)
    elif position:
        orders = mt5.history_orders_get(position=position)
    else:
        error = ErrorResponse.model_validate(
            (ErrorCodes.RES_E_INVALID_PARAMS, "At least one filter parameter is required")
        )
        return JSONResponse(
            status_code=400,
            content=error.model_dump(),
        )

    if orders is None:
        error = ErrorResponse.model_validate(mt5.last_error())
        return JSONResponse(
            status_code=500,
            content=error.model_dump(),
        )

    return [Order(**order._asdict()) for order in orders]


@router.get(
    "/deals/total",
    summary="Get the total count of deals in trading history",
    description="Retrieves the total number of deals (executed trades) recorded in the trading history of the account.",
    responses={
        200: {
            "description": "Total deal count retrieved successfully",
            "content": {
                "application/json": {
                    "example": 200
                }
            },
        },
        500: {
            "description": "Failed to retrieve deal count",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve history deal count",
                    }
                }
            },
        },
    },
    status_code=200,
)
def history_deals_total() -> int:
    return mt5.history_deals_total() or 0


@router.get(
    "/deals/",
    summary="Get executed deals from trading history with optional filtering",
    description="Retrieves deals from the trading history. Can be filtered by date range, group, ticket, or position. At least one filter parameter is required. Deals represent actual executed trades.",
    status_code=200,
    response_model=list[Deal],
    responses={
        200: {
            "description": "Historical deals retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "ticket": 123456789,
                            "order": 123456,
                            "time": 1704067200,
                            "time_msc": 1704067200000,
                            "type": 0,
                            "entry": 0,
                            "magic": 0,
                            "reason": 0,
                            "position_id": 123451,
                            "volume": 1.0,
                            "price": 1.0850,
                            "commission": -1.0,
                            "swap": -2.5,
                            "profit": 100.0,
                            "symbol": "EURUSD",
                            "comment": "Executed deal",
                            "external_id": "",
                        }
                    ]
                }
            },
        },
        400: {
            "description": "No filter parameters provided",
            "content": {
                "application/json": {
                    "example": {
                        "code": -2,
                        "message": "At least one filter parameter is required",
                    }
                }
            },
        },
        500: {
            "description": "Failed to retrieve deals",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve history deals",
                    }
                }
            },
        },
    },
)
def history_deals_get(
    date_from: datetime | None = Query(None, description="Start date for history range (ISO 8601 format)"),
    date_to: datetime | None = Query(None, description="End date for history range (ISO 8601 format)"),
    group: str | None = Query(None, description="Group filter pattern (e.g., 'Forex')"),
    ticket: int | None = Query(None, description="Filter by specific deal ticket number"),
    position: int | None = Query(None, description="Filter by position ID"),
):
    deals: tuple[mt5.Deal, ...] | None = None

    if date_from and date_to and group:
        deals = mt5.history_deals_get(date_from=date_from, date_to=date_to, group=group)
    elif date_from and date_to:
        deals = mt5.history_deals_get(date_from=date_from, date_to=date_to)
    elif ticket:
        deals = mt5.history_deals_get(ticket=ticket)
    elif position:
        deals = mt5.history_deals_get(position=position)
    else:
        error = ErrorResponse.model_validate(
            (ErrorCodes.RES_E_INVALID_PARAMS, "At least one filter parameter is required")
        )
        return JSONResponse(
            status_code=400,
            content=error.model_dump(),
        )

    if deals is None:
        error = ErrorResponse.model_validate(mt5.last_error())
        return JSONResponse(
            status_code=500,
            content=error.model_dump(),
        )

    return [Deal(**deal._asdict()) for deal in deals]
