from pydantic import BaseModel
from enum import IntEnum


# Account Enumerations
class AccountTradeMode(IntEnum):
    """Account trade mode enumeration"""

    DEMO = 0  # Demo account
    CONTEST = 1  # Contest account
    REAL = 2  # Real account


class AccountStopoutMode(IntEnum):
    """Account stop out mode enumeration"""

    PERCENT = 0  # Account stop out mode in percents
    MONEY = 1  # Account stop out mode in money


class AccountMarginMode(IntEnum):
    """Account margin mode enumeration"""

    RETAIL_NETTING = 0  # OTC markets, netting mode (one position per symbol)
    EXCHANGE = 1  # Exchange markets with discounts
    RETAIL_HEDGING = 2  # Exchange markets with hedging (multiple positions per symbol)


# Account Properties
class AccountProperty(BaseModel):
    # Integer Properties
    login: int  # Account number
    trade_mode: AccountTradeMode  # Account trade mode (ENUM_ACCOUNT_TRADE_MODE)
    leverage: int  # Account leverage
    limit_orders: int  # Maximum allowed number of active pending orders
    margin_so_mode: AccountStopoutMode  # Mode for setting the minimal allowed margin (ENUM_ACCOUNT_STOPOUT_MODE)
    trade_allowed: bool  # Allowed trade for the current account
    trade_expert: bool  # Allowed trade for an Expert Advisor
    margin_mode: AccountMarginMode  # Margin calculation mode (ENUM_ACCOUNT_MARGIN_MODE)
    currency_digits: int  # The number of decimal places in the account currency
    fifo_close: (
        bool  # Indication showing that positions can only be closed by FIFO rule
    )
    hedge_allowed: bool | None = None  # Allowed opposite positions on a single symbol

    # Double Properties
    balance: float  # Account balance in the deposit currency
    credit: float  # Account credit in the deposit currency
    profit: float  # Current profit of an account in the deposit currency
    equity: float  # Account equity in the deposit currency
    margin: float  # Account margin used in the deposit currency
    margin_free: float  # Free margin of an account in the deposit currency
    margin_level: float  # Account margin level in percents
    margin_so_call: float  # Margin call level
    margin_so_so: float  # Margin stop out level
    margin_initial: float  # Initial margin reserved to cover pending orders
    margin_maintenance: float  # Maintenance margin for open positions
    assets: float  # The current assets of an account
    liabilities: float  # The current liabilities on an account
    commission_blocked: float  # The current blocked commission amount on an account

    # String Properties
    name: str  # Client name
    server: str  # Trade server name
    currency: str  # Account currency
    company: str  # Name of a company that serves the account
