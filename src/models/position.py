from pydantic import BaseModel, Field
from enum import IntEnum
from typing import Optional


# Position Type Enumeration
class PositionType(IntEnum):
    """Position type enumeration"""
    BUY = 0  # Buy position
    SELL = 1  # Sell position


# Position Reason Enumeration
class PositionReason(IntEnum):
    """Position reason enumeration"""
    CLIENT = 0  # Position opened from desktop terminal
    MOBILE = 1  # Position opened from mobile application
    WEB = 2  # Position opened from web platform
    EXPERT = 3  # Position opened from MQL5 program


# Position Model
class Position(BaseModel):
    """
    Position model containing all position properties.
    Retrieved using PositionGet...() functions.
    """
    
    # Integer Properties
    ticket: int  # Position ticket (unique number)
    time: int  # Position open time (datetime)
    time_msc: int  # Position open time in milliseconds since 01.01.1970
    time_update: int = Field(default=0, description="Position change time (datetime)")
    time_update_msc: int = Field(default=0, description="Position change time in milliseconds since 01.01.1970")
    type: PositionType  # Position type (BUY or SELL)
    magic: int = Field(default=0, description="Position magic number")
    identifier: int = Field(default=0, description="Position identifier (unique throughout lifetime)")
    reason: Optional[PositionReason] = Field(default=None, description="Position opening reason")
    
    # Double Properties
    volume: float  # Position volume
    price_open: float  # Position open price
    sl: float  # Stop Loss level
    tp: float  # Take Profit level
    price_current: float = Field(default=0.0, description="Current price of position symbol")
    swap: float = Field(default=0.0, description="Cumulative swap")
    profit: float = Field(default=0.0, description="Current profit/loss")
    
    # String Properties
    symbol: str  # Position symbol
    comment: str = Field(default="", description="Position comment")
    external_id: str = Field(default="", description="External position identifier")
