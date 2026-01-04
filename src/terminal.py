from fastapi import APIRouter
import MetaTrader5 as mt5  # type: ignore
from .models import TerminalProperty
from .errors import ErrorResponse

router = APIRouter(prefix="/terminal", tags=["terminal"])


@router.get(
    "/info",
    summary="Get the connected MetaTrader 5 client terminal status and settings.",
    response_model=TerminalProperty,
    status_code=200
)
def terminal_info():
    info = mt5.terminal_info()

    if not info:
        return ErrorResponse.model_validate(mt5.last_error())

    return TerminalProperty(**info._asdict())
