from pydantic import BaseModel, Field
from enum import IntEnum
from typing import Optional


# Order Reason Enumeration
class OrderReason(IntEnum):
    """Order reason enumeration"""

    CLIENT = 0  # Order placed from desktop terminal
    MOBILE = 1  # Order placed from mobile application
    WEB = 2  # Order placed from web platform
    EXPERT = 3  # Order placed from MQL5 program
    SL = 4  # Order placed as result of Stop Loss activation
    TP = 5  # Order placed as result of Take Profit activation
    SO = 6  # Order placed as result of Stop Out event


# Order Model
class Order(BaseModel):
    """
    Order model containing all order properties.
    Retrieved using PositionGet...() functions.
    """

    # Integer Properties
    ticket: int  # Order ticket (unique number)
    time_setup: int  # Order setup time (datetime)
    type: int  # Order type
    state: int  # Order state
    time_expiration: int = Field(default=0, summary="Order expiration time (datetime)")
    time_done: int = Field(
        default=0, summary="Order execution/cancellation time (datetime)"
    )
    time_setup_msc: int = Field(
        default=0, summary="Order setup time in milliseconds since 01.01.1970"
    )
    time_done_msc: int = Field(
        default=0, summary="Order execution time in milliseconds since 01.01.1970"
    )
    type_filling: int  # Order filling type
    type_time: int  # Order lifetime type
    magic: int = Field(default=0, summary="Expert Advisor ID (magic number)")
    reason: Optional[OrderReason] = Field(
        default=None, summary="Order placement reason"
    )
    position_id: int = Field(default=0, summary="Position identifier")
    position_by_id: int = Field(default=0, summary="Opposite position identifier")

    # Double Properties
    volume_initial: float  # Order initial volume
    volume_current: float  # Order current volume
    price_open: float  # Order opening price
    sl: float  # Stop Loss value
    tp: float  # Take Profit value
    price_current: float = Field(default=0.0, summary="Current price of order symbol")
    price_stoplimit: float = Field(
        default=0.0, summary="Limit order price for StopLimit"
    )

    # String Properties
    symbol: str  # Order symbol
    comment: str = Field(default="", summary="Order comment")
    external_id: str = Field(default="", summary="External order identifier")
