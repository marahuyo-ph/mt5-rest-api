from pydantic import BaseModel, Field
from enum import IntEnum
from typing import Optional


# Trade Request Action Enumerations
class TradeAction(IntEnum):
    """Trade action enumeration"""

    DEAL = 1  # Place a deal (market order)
    PENDING = 2  # Place a pending order
    SLTP = 3  # Modify Stop Loss and Take Profit of a position
    MODIFY = 4  # Modify a pending order
    REMOVE = 5  # Cancel a pending order
    CLOSE_BY = 6  # Close a position by an opposite one


class OrderType(IntEnum):
    """Order type enumeration"""

    BUY = 0  # Market buy order
    SELL = 1  # Market sell order
    BUY_LIMIT = 2  # Buy limit order
    SELL_LIMIT = 3  # Sell limit order
    BUY_STOP = 4  # Buy stop order
    SELL_STOP = 5  # Sell stop order
    BUY_STOP_LIMIT = 6  # Buy stop limit order
    SELL_STOP_LIMIT = 7  # Sell stop limit order
    CLOSE_BY = 8  # Close by (hedge) order


class OrderFilling(IntEnum):
    """Order filling type enumeration"""

    FOK = 1  # Fill or Kill (FOK)
    IOC = 2  # Immediate or Cancel (IOC)
    BOC = 4  # Book or Cancel (BOC)
    RETURN = 0  # Return (default)


class OrderTime(IntEnum):
    """Order time (expiration) type enumeration"""

    GTC = 0  # Good Till Canceled
    DAY = 1  # Good Till End of Day
    SPECIFIED = 2  # Good Till Specified Time
    SPECIFIED_DAY = 3  # Good Till Specified Day


class OrderState(IntEnum):
    """Order state enumeration"""

    STARTED = 0  # Order just placed
    PLACED = 1  # Order placed on the exchange
    CANCELED = 2  # Order has been canceled
    PARTIAL = 3  # Order has been partially filled
    FILLED = 4  # Order has been filled
    REJECTED = 5  # Order has been rejected
    EXPIRED = 6  # Order has expired
    REQUEST_ADD = 7  # Order is in request queue
    REQUEST_MODIFY = 8  # Order is in modify request queue
    REQUEST_CANCEL = 9  # Order is in cancel request queue


class DealType(IntEnum):
    """Deal type enumeration"""

    BUY = 0  # Buy deal
    SELL = 1  # Sell deal
    BUY_CANCELED = 2  # Canceled buy deal
    SELL_CANCELED = 3  # Canceled sell deal
    BALANCE = 4  # Balance
    CREDIT = 5  # Credit
    CHARGE = 6  # Charge
    CORRECTION = 7  # Correction
    BONUS = 8  # Bonus
    COMMISSION = 9  # Commission


class TradeTransactionType(IntEnum):
    """Trade transaction type enumeration"""

    REQUEST = 0  # Trade request has been processed
    REQUEST_ADD = 1  # Trade request added
    REQUEST_UPDATE = 2  # Trade request updated
    REQUEST_CANCEL = 3  # Trade request canceled
    ORDER_ADD = 10  # Order added
    ORDER_UPDATE = 11  # Order updated
    ORDER_DELETE = 12  # Order deleted
    ORDER_STATE = 13  # Order state changed
    HISTORY_ADD = 20  # Order added to history
    HISTORY_UPDATE = 21  # Order updated in history
    HISTORY_DELETE = 22  # Order deleted from history
    DEAL_ADD = 30  # Deal added
    DEAL_UPDATE = 31  # Deal updated
    DEAL_DELETE = 32  # Deal deleted
    POSITION = 40  # Position opened/closed


# Trade Structures
class TradeRequest(BaseModel):
    """
    MqlTradeRequest structure for placing/modifying trade orders.
    Used with OrderSend() and OrderCheck() functions.
    """

    action: TradeAction  # Trade operation type
    magic: int = Field(default=0, summary="Expert Advisor ID (magic number)")
    order: int = Field(default=0, summary="Order ticket (for modifications)")
    symbol: str  # Trade symbol
    volume: float  # Requested volume in lots
    price: float = Field(default=0.0, summary="Order price")
    stoplimit: float = Field(default=0.0, summary="StopLimit price")
    sl: float = Field(default=0.0, summary="Stop Loss level")
    tp: float = Field(default=0.0, summary="Take Profit level")
    deviation: float = Field(default=0.0, summary="Max price deviation in points")
    type: OrderType  # Order type
    type_filling: OrderFilling  # Order filling type
    type_time: OrderTime  # Order expiration type
    expiration: int = Field(default=0, summary="Order expiration time (datetime)")
    comment: str = Field(default="", summary="Order comment")
    position: int = Field(default=0, summary="Position ticket")
    position_by: int = Field(default=0, summary="Opposite position ticket")


class TradeCheckResult(BaseModel):
    """
    MqlTradeCheckResult structure for trade request check results.
    Returned by OrderCheck() function before executing the order.
    """

    retcode: int  # Return code
    balance: float  # Balance after trade operation
    equity: float  # Equity after trade operation
    profit: float  # Floating profit after trade operation
    margin: float  # Required margin
    margin_free: float  # Free margin after trade operation
    margin_level: float  # Margin level percentage
    comment: str = Field(default="", summary="Return code description")


class TradeResult(BaseModel):
    """
    MqlTradeResult structure for trade request execution results.
    Returned by OrderSend() and OrderSendAsync() functions.
    """

    retcode: int  # Trade server return code
    deal: int = Field(default=0, summary="Deal ticket if executed")
    order: int = Field(default=0, summary="Order ticket if placed")
    volume: float = Field(default=0.0, summary="Deal volume confirmed by broker")
    price: float = Field(default=0.0, summary="Deal price confirmed by broker")
    bid: float = Field(default=0.0, summary="Current Bid price")
    ask: float = Field(default=0.0, summary="Current Ask price")
    comment: str = Field(default="", summary="Broker comment")
    request_id: int = Field(default=0, summary="Request ID")
    retcode_external: int = Field(default=0, summary="External system error code")


class TradeTransaction(BaseModel):
    """
    MqlTradeTransaction structure describing a trade transaction.
    Received by OnTradeTransaction() event handler.
    """

    deal: int = Field(default=0, summary="Deal ticket")
    order: int = Field(default=0, summary="Order ticket")
    symbol: str = Field(default="", summary="Trade symbol")
    type: TradeTransactionType  # Trade transaction type
    order_type: Optional[OrderType] = Field(default=None, summary="Order type")
    order_state: Optional[OrderState] = Field(default=None, summary="Order state")
    deal_type: Optional[DealType] = Field(default=None, summary="Deal type")
    time_type: Optional[OrderTime] = Field(default=None, summary="Order time type")
    time_expiration: int = Field(default=0, summary="Order expiration time (datetime)")
    price: float = Field(default=0.0, summary="Order/deal/position price")
    price_trigger: float = Field(default=0.0, summary="Stop limit activation price")
    price_sl: float = Field(default=0.0, summary="Stop Loss level")
    price_tp: float = Field(default=0.0, summary="Take Profit level")
    volume: float = Field(default=0.0, summary="Volume in lots")
    position: int = Field(default=0, summary="Position ticket")
    position_by: int = Field(default=0, summary="Opposite position ticket")
