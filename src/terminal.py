from fastapi import APIRouter
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from .models import TerminalProperty
from .errors import ErrorResponse

router = APIRouter(prefix="/terminal", tags=["terminal"])


@router.get(
    "/info",
    summary="Get the connected MetaTrader 5 client terminal status and settings.",
    response_model=TerminalProperty,
    status_code=200,
)
def terminal_info():
    info = mt5.terminal_info()

    if not info:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.model_validate(mt5.last_error()).model_dump(),
        )

    return TerminalProperty(**info._asdict())
