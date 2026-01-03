from fastapi import APIRouter
import MetaTrader5 as mt5
from models import TerminalProperty

router = APIRouter(prefix="/terminal")


@router.get(
    "/info",
    description="Get the connected MetaTrader 5 client terminal status and settings.",
    response_model=TerminalProperty,
    tags=["terminal"]
)
def terminal_info():
    info = mt5.terminal_info()

    if not info:
        return mt5.last_error()

    return TerminalProperty(**info._asdict())
