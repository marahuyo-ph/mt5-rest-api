from fastapi import APIRouter
import MetaTrader5 as mt5  # type: ignore
from models import AccountProperty
from errors import ErrorResponse

router = APIRouter(prefix="/accounts", tags=["account"])


@router.get(
    "/info",
    summary="Get info on the current trading account.",
    response_model=AccountProperty,
)
def get_acc_info():
    account = mt5.account_info()

    if not account:
        return ErrorResponse.model_validate(mt5.last_error())

    # Convert the account named tuple to AccountProperty model
    return AccountProperty(**account._asdict())
