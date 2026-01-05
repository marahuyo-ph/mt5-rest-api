from fastapi import APIRouter
from fastapi.responses import JSONResponse
import MetaTrader5 as mt5  # type: ignore
from .models import Position
from .errors import ErrorResponse

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("/total", summary="Get the number of open positions.", status_code=200)
def positions_total() -> int:
    return mt5.positions_total() or 0


@router.get(
    "/",
    summary="Get open positions with the ability to filter by symbol or ticket.",
    status_code=200,
    response_model=list[Position],
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
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.model_validate(mt5.last_error()).model_dump(),
        )

    return [Position(**position._asdict()) for position in positions]
