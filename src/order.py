from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from .models import TradeRequest, Order
from pydantic import BaseModel, Field
from .errors import ErrorResponse

router = APIRouter(prefix="/orders", tags=["orders"])


class CalculateMarginRequest(BaseModel):
    action: int = Field(..., description="Trade action type")
    symbol: str = Field(..., description="Symbol name (e.g., 'EURUSD')")
    volume: float = Field(..., description="Trade volume in lots")
    price: float = Field(..., description="Trade price")


class CalculateProfitRequest(BaseModel):
    action: int = Field(..., description="Trade action type")
    symbol: str = Field(..., description="Symbol name (e.g., 'EURUSD')")
    volume: float = Field(..., description="Trade volume in lots")
    price_open: float = Field(..., description="Opening price")
    price_close: float = Field(..., description="Closing price")


@router.get(
    "/total",
    summary="Get the number of active orders",
    description="Retrieves the total count of currently active pending orders in the trading account.",
    responses={
        200: {
            "description": "Total active orders count retrieved successfully",
            "content": {
                "application/json": {
                    "example": 3
                }
            },
        },
        500: {
            "description": "Failed to retrieve order count",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve active orders count",
                    }
                }
            },
        },
    },
    status_code=200,
)
def orders_total() -> int:
    return mt5.orders_total() or 0


@router.get(
    "/",
    summary="Get active pending orders with optional filtering",
    description="Retrieves a list of active pending orders. Can be filtered by symbol, group pattern, or order ticket. If no filter is provided, returns all active orders.",
    status_code=200,
    response_model=list[Order],
    responses={
        200: {
            "description": "Active orders retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "ticket": 789012,
                            "time_setup": 1704067200,
                            "type": 2,
                            "state": 0,
                            "magic": 0,
                            "time_expiration": 0,
                            "type_filling": 0,
                            "type_time": 0,
                            "reason": 0,
                            "volume_initial": 1.0,
                            "volume_current": 1.0,
                            "price_open": 1.0800,
                            "sl": 1.0750,
                            "tp": 1.0850,
                            "price_current": 1.0850,
                            "symbol": "EURUSD",
                            "comment": "Pending sell limit order",
                            "position_id": 0,
                            "position_by_id": 0,
                            "external_id": "",
                            "time_setup_msc": 1704067200000,
                        }
                    ]
                }
            },
        },
        500: {
            "description": "Failed to retrieve orders",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve active orders",
                    }
                }
            },
        },
    },
)
def orders_get(
    symbol: str | None = Query(None, description="Filter by symbol name (e.g., 'EURUSD')"),
    group: str | None = Query(None, description="Filter by group pattern (e.g., 'Forex')"),
    ticket: int | None = Query(None, description="Filter by order ticket number"),
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
            status_code=500,
            content=ErrorResponse.model_validate(mt5.last_error()).model_dump(),
        )

    return [Order(**order._asdict()) for order in orders]


@router.post(
    "/calculate-margin",
    summary="Calculate required margin for a trading operation",
    description="Returns the margin required in the account currency to perform a specified trading operation. Useful for position sizing calculations.",
    status_code=200,
    responses={
        200: {
            "description": "Margin calculated successfully",
            "content": {
                "application/json": {
                    "example": 1500.0
                }
            },
        },
        400: {
            "description": "Invalid trading parameters",
            "content": {
                "application/json": {
                    "example": {
                        "code": -2,
                        "message": "Invalid trading parameters",
                    }
                }
            },
        },
        500: {
            "description": "Failed to calculate margin",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to calculate margin",
                    }
                }
            },
        },
    },
)
def orders_calc_margin(payload: CalculateMarginRequest):
    margin = mt5.order_calc_margin(
        payload.action, payload.symbol, payload.volume, payload.price
    )

    if margin is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    return margin


@router.post(
    "/calculate-profit",
    summary="Calculate profit for a trading operation",
    description="Returns the profit in the account currency for a specified trading operation based on entry and exit prices. Useful for P&L calculations.",
    status_code=200,
    responses={
        200: {
            "description": "Profit calculated successfully",
            "content": {
                "application/json": {
                    "example": 250.50
                }
            },
        },
        400: {
            "description": "Invalid trading parameters",
            "content": {
                "application/json": {
                    "example": {
                        "code": -2,
                        "message": "Invalid trading parameters",
                    }
                }
            },
        },
        500: {
            "description": "Failed to calculate profit",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to calculate profit",
                    }
                }
            },
        },
    },
)
def orders_calc_profit(payload: CalculateProfitRequest):
    profit = mt5.order_calc_profit(
        payload.action,
        payload.symbol,
        payload.volume,
        payload.price_open,
        payload.price_close,
    )

    if profit is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    return profit


@router.post(
    "/check",
    summary="Check if a trading operation can be performed",
    description="Validates whether a trading operation can be executed given current market conditions and account status. Returns detailed check results including profit/loss and margin requirements.",
    status_code=200,
    responses={
        200: {
            "description": "Trade check completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "retcode": 0,
                        "balance": 10250.50,
                        "equity": 10250.50,
                        "profit": 0.0,
                        "margin": 1500.0,
                        "margin_free": 8750.50,
                        "margin_level": 683.67,
                        "comment": "Not enough money for operation",
                    }
                }
            },
        },
        400: {
            "description": "Invalid trade request parameters",
            "content": {
                "application/json": {
                    "example": {
                        "code": -2,
                        "message": "Invalid trade request",
                    }
                }
            },
        },
        500: {
            "description": "Failed to check trade",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to check trade",
                    }
                }
            },
        },
    },
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

    if check_result is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    return check_result


@router.post(
    "/send",
    summary="Send a trade request to the broker",
    description="Sends a trade request to the broker for execution. This endpoint handles order placement, position opening/closing, and modifications. Returns the execution result including order/deal tickets and status.",
    status_code=200,
    responses={
        200: {
            "description": "Trade request sent and executed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "retcode": 10009,
                        "deal": 123456789,
                        "order": 123456,
                        "volume": 1.0,
                        "price": 1.0850,
                        "bid": 1.0849,
                        "ask": 1.0851,
                        "comment": "Order executed",
                        "request_id": 0,
                        "retcode_external": 0,
                    }
                }
            },
        },
        400: {
            "description": "Invalid trade request parameters",
            "content": {
                "application/json": {
                    "example": {
                        "code": -2,
                        "message": "Invalid trade request",
                    }
                }
            },
        },
        500: {
            "description": "Failed to send trade request",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to send trade order",
                    }
                }
            },
        },
    },
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

    if result is None:
        return ErrorResponse.model_validate(mt5.last_error()).model_dump()

    return result
