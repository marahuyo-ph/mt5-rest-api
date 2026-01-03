from fastapi import APIRouter
import MetaTrader5 as mt5
from models import AccountProperty

router = APIRouter(prefix="/accounts")

@router.get(
    "/info",
    description="Get info on the current trading account.",
    tags=["account"],
    response_model=AccountProperty,
)
def get_acc_info():
    account = mt5.account_info()

    if not account:
        return mt5.last_error()

    return account._asdict()
