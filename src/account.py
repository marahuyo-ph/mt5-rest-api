from fastapi import APIRouter
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from .models import AccountProperty
from .errors import ErrorResponse

router = APIRouter(prefix="/accounts", tags=["account"])


@router.get(
    "/info",
    summary="Get info on the current trading account",
    description="Retrieves detailed information about the currently connected trading account, including account balance, equity, margin details, and trading permissions from the MetaTrader5 terminal.",
    response_model=AccountProperty,
    status_code=200,
    responses={
        200: {
            "description": "Account information retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "login": 123456789,
                        "server": "DemoServer",
                        "trader": "Demo Account",
                        "currency": "USD",
                        "balance": 10000.0,
                        "profit": 250.50,
                        "equity": 10250.50,
                        "margin": 1500.0,
                        "margin_free": 8750.50,
                        "margin_level": 683.67,
                        "margin_so_mode": 0,
                        "trade_mode": 0,
                        "leverage": 100,
                        "limit_orders": 200,
                        "trade_allowed": True,
                        "trade_expert": True,
                    }
                }
            },
        },
        500: {
            "description": "Failed to retrieve account information",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve account information",
                    }
                }
            },
        },
    },
)
def get_acc_info():
    account = mt5.account_info()

    if not account:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.model_validate(mt5.last_error()).model_dump(),
        )

    # Convert the account named tuple to AccountProperty model
    return AccountProperty(**account._asdict())
