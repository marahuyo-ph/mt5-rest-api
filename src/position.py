from fastapi import APIRouter
import MetaTrader5 as mt5
from models import Position

router = APIRouter(prefix="/positions")


@router.get("/total")
def positions_total():
    return mt5.positions_total()


@router.get("/")
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
        return mt5.last_error()

    return [Position(**position._asdict()) for position in positions]
