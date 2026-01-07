from pydantic import BaseModel, Field
from enum import IntEnum
from typing import Optional
import MetaTrader5 as mt5 # type: ignore


# Deal Type Enumeration
class DealType(IntEnum):
    """Deal type enumeration"""

    BUY = mt5.DEAL_TYPE_BUY  # Buy
    SELL = mt5.DEAL_TYPE_SELL # Sell
    BALANCE = mt5.DEAL_TYPE_BALANCE  # Balance
    CREDIT = mt5.DEAL_TYPE_CREDIT  # Credit
    CHARGE = mt5.DEAL_TYPE_CHARGE  # Additional charge
    CORRECTION = mt5.DEAL_TYPE_CORRECTION  # Correction
    BONUS = mt5.DEAL_TYPE_BONUS  # Bonus
    COMMISSION = mt5.DEAL_TYPE_COMMISSION # Additional commission
    COMMISSION_DAILY = mt5.DEAL_TYPE_COMMISSION_DAILY  # Daily commission
    COMMISSION_MONTHLY = mt5.DEAL_TYPE_COMMISSION_MONTHLY  # Monthly commission
    COMMISSION_AGENT_DAILY = mt5.DEAL_TYPE_COMMISSION_AGENT_DAILY  # Daily agent commission
    COMMISSION_AGENT_MONTHLY = mt5.DEAL_TYPE_COMMISSION_AGENT_MONTHLY  # Monthly agent commission
    INTEREST = mt5.DEAL_TYPE_INTEREST  # Interest rate
    BUY_CANCELED = mt5.DEAL_TYPE_BUY_CANCELED  # Canceled buy deal
    SELL_CANCELED = mt5.DEAL_TYPE_SELL_CANCELED  # Canceled sell deal
    DIVIDEND = mt5.DEAL_DIVIDEND  # Dividend operations
    DIVIDEND_FRANKED = mt5.DEAL_DIVIDEND_FRANKED  # Franked dividend operations
    TAX = mt5.DEAL_TAX  # Tax charges


# Deal Entry Enumeration
class DealEntry(IntEnum):
    """Deal entry enumeration"""

    IN = mt5.DEAL_ENTRY_IN  # Entry in (position opening)
    OUT = mt5.DEAL_ENTRY_OUT  # Entry out (position closing)
    INOUT = mt5.DEAL_ENTRY_INOUT  # Reverse (position reversal)
    OUT_BY = mt5.DEAL_ENTRY_OUT_BY  # Close by opposite position


# Deal Reason Enumeration
class DealReason(IntEnum):
    """Deal reason enumeration"""

    CLIENT = mt5.DEAL_REASON_CLIENT  # Deal executed from desktop terminal
    MOBILE = mt5.DEAL_REASON_MOBILE  # Deal executed from mobile application
    WEB = mt5.DEAL_REASON_WEB  # Deal executed from web platform
    EXPERT = mt5.DEAL_REASON_EXPERT  # Deal executed from MQL5 program
    SL = mt5.DEAL_REASON_SL  # Deal executed by Stop Loss
    TP = mt5.DEAL_REASON_TP  # Deal executed by Take Profit
    SO = mt5.DEAL_REASON_SO  # Deal executed by Stop Out
    ROLLOVER = mt5.DEAL_REASON_ROLLOVER  # Deal executed due to rollover
    VMARGIN = mt5.DEAL_REASON_VMARGIN  # Deal executed after variation margin charge
    SPLIT = mt5.DEAL_REASON_SPLIT  # Deal executed after price split
    CORPORATE_ACTION =  -1  # Deal executed due to corporate action


# Deal Model
class Deal(BaseModel):
    """
    Deal model containing all deal properties.
    Retrieved using HistoryDealGet...() functions.
    """

    # Integer Properties
    ticket: int  # Deal ticket (unique number)
    order: int  # Deal order number
    time: int  # Deal time (datetime)
    time_msc: int  # Deal execution time in milliseconds since 01.01.1970
    type: DealType  # Deal type
    entry: DealEntry  # Deal entry type
    magic: int = Field(default=0, json_schema_extra={"summary": "Deal magic number"})
    reason: Optional[DealReason] = Field(
        default=None, json_schema_extra={"summary": "Deal execution reason"}
    )
    position_id: int = Field(
        default=0, json_schema_extra={"summary": "Position identifier"}
    )

    # Double Properties
    volume: float  # Deal volume
    price: float  # Deal price
    commission: float = Field(
        default=0.0, json_schema_extra={"summary": "Deal commission"}
    )
    swap: float = Field(
        default=0.0, json_schema_extra={"summary": "Cumulative swap on close"}
    )
    profit: float = Field(
        default=0.0, json_schema_extra={"summary": "Deal profit/loss"}
    )
    fee: float = Field(
        default=0.0, json_schema_extra={"summary": "Deal fee charged immediately"}
    )
    sl: float = Field(default=0.0, json_schema_extra={"summary": "Stop Loss level"})
    tp: float = Field(default=0.0, json_schema_extra={"summary": "Take Profit level"})

    # String Properties
    symbol: str  # Deal symbol
    comment: str = Field(default="", json_schema_extra={"summary": "Deal comment"})
    external_id: str = Field(
        default="", json_schema_extra={"summary": "External deal identifier"}
    )
