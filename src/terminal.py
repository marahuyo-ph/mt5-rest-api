from fastapi import APIRouter
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from .models import TerminalProperty
from .errors import ErrorResponse

router = APIRouter(prefix="/terminal", tags=["terminal"])


@router.get(
    "/info",
    summary="Get the connected MetaTrader 5 client terminal status and settings",
    description="Retrieves detailed information about the currently connected MetaTrader5 terminal, including connection status, server information, and terminal configuration settings.",
    response_model=TerminalProperty,
    status_code=200,
    responses={
        200: {
            "description": "Terminal information retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "connected": True,
                        "trade_allowed": True,
                        "trade_expert": True,
                        "dlls_allowed": True,
                        "lib_logs_allowed": True,
                        "positioned": True,
                        "trade_mode": 0,
                        "server": "DemoServer",
                        "language": "en",
                        "path": "C:\\Program Files\\MetaTrader 5",
                        "data_path": "C:\\Users\\User\\AppData\\Roaming\\MetaQuotes\\Terminal\\1234567890",
                        "commondata_path": "C:\\Users\\User\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common",
                        "build": 4567,
                        "maxbars": 100000,
                        "infotimeout": 100,
                        "symbol_select_timeout": 100,
                        "pulldata_timeout": 100,
                        "community_timeout": 100,
                    }
                }
            },
        },
        500: {
            "description": "Failed to retrieve terminal information",
            "content": {
                "application/json": {
                    "example": {
                        "code": -1,
                        "message": "Failed to retrieve terminal information",
                    }
                }
            },
        },
    },
)
def terminal_info():
    info = mt5.terminal_info()

    if not info:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.model_validate(mt5.last_error()).model_dump(),
        )

    return TerminalProperty(**info._asdict())
