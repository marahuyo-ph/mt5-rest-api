from fastapi import APIRouter
import MetaTrader5 as mt5  # type: ignore
from .models import Position
from .errors import ErrorResponse

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("/total", summary="Get the number of open positions.", status_code=200)
def positions_total():
    return mt5.positions_total()


@router.get(
    "/",
    summary="Get open positions with the ability to filter by symbol or ticket.",
    status_code=200,
)
def positions_get(
    symbol: str | None = None, group: str | None = None, ticket: int | None = None
):
    positions: tuple[mt5.Position, ...] | None = None

    if symbol:
        positions = mt5.positions_get(symbol=symbol)
    elif group:
        positions = mt5.positions_get(group=group)
    elif ticket:
        positions = mt5.positions_get(ticket=ticket)
    else:
        positions = mt5.positions_get()

    if not positions:
        return ErrorResponse.model_validate(mt5.last_error())

    return [Position(**position._asdict()) for position in positions]
