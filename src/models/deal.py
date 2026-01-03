from pydantic import BaseModel, Field
from enum import IntEnum
from typing import Optional


# Deal Type Enumeration
class DealType(IntEnum):
    """Deal type enumeration"""

    BUY = 0  # Buy
    SELL = 1  # Sell
    BALANCE = 2  # Balance
    CREDIT = 3  # Credit
    CHARGE = 4  # Additional charge
    CORRECTION = 5  # Correction
    BONUS = 6  # Bonus
    COMMISSION = 7  # Additional commission
    COMMISSION_DAILY = 8  # Daily commission
    COMMISSION_MONTHLY = 9  # Monthly commission
    COMMISSION_AGENT_DAILY = 10  # Daily agent commission
    COMMISSION_AGENT_MONTHLY = 11  # Monthly agent commission
    INTEREST = 12  # Interest rate
    BUY_CANCELED = 13  # Canceled buy deal
    SELL_CANCELED = 14  # Canceled sell deal
    DIVIDEND = 15  # Dividend operations
    DIVIDEND_FRANKED = 16  # Franked dividend operations
    TAX = 17  # Tax charges


# Deal Entry Enumeration
class DealEntry(IntEnum):
    """Deal entry enumeration"""

    IN = 0  # Entry in (position opening)
    OUT = 1  # Entry out (position closing)
    INOUT = 2  # Reverse (position reversal)
    OUT_BY = 3  # Close by opposite position


# Deal Reason Enumeration
class DealReason(IntEnum):
    """Deal reason enumeration"""

    CLIENT = 0  # Deal executed from desktop terminal
    MOBILE = 1  # Deal executed from mobile application
    WEB = 2  # Deal executed from web platform
    EXPERT = 3  # Deal executed from MQL5 program
    SL = 4  # Deal executed by Stop Loss
    TP = 5  # Deal executed by Take Profit
    SO = 6  # Deal executed by Stop Out
    ROLLOVER = 7  # Deal executed due to rollover
    VMARGIN = 8  # Deal executed after variation margin charge
    SPLIT = 9  # Deal executed after price split
    CORPORATE_ACTION = 10  # Deal executed due to corporate action


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
    magic: int = Field(default=0, description="Deal magic number")
    reason: Optional[DealReason] = Field(
        default=None, description="Deal execution reason"
    )
    position_id: int = Field(default=0, description="Position identifier")

    # Double Properties
    volume: float  # Deal volume
    price: float  # Deal price
    commission: float = Field(default=0.0, description="Deal commission")
    swap: float = Field(default=0.0, description="Cumulative swap on close")
    profit: float = Field(default=0.0, description="Deal profit/loss")
    fee: float = Field(default=0.0, description="Deal fee charged immediately")
    sl: float = Field(default=0.0, description="Stop Loss level")
    tp: float = Field(default=0.0, description="Take Profit level")

    # String Properties
    symbol: str  # Deal symbol
    comment: str = Field(default="", description="Deal comment")
    external_id: str = Field(default="", description="External deal identifier")
