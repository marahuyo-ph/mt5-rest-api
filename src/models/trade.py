from pydantic import BaseModel, Field
from enum import IntEnum
from typing import Optional
import MetaTrader5 as mt5 # type: ignore


# Trade Request Action Enumerations
class TradeAction(IntEnum):
    """Trade action enumeration"""

    DEAL = mt5.TRADE_ACTION_DEAL  # Place a deal (market order)
    PENDING = mt5.TRADE_ACTION_PENDING  # Place a pending order
    SLTP = mt5.TRADE_ACTION_SLTP  # Modify Stop Loss and Take Profit of a position
    MODIFY = mt5.TRADE_ACTION_MODIFY  # Modify a pending order
    REMOVE = mt5.TRADE_ACTION_REMOVE  # Cancel a pending order
    CLOSE_BY = mt5.TRADE_ACTION_CLOSE_BY  # Close a position by an opposite one


class OrderType(IntEnum):
    """Order type enumeration"""

    BUY = mt5.ORDER_TYPE_BUY  # Market buy order
    SELL = mt5.ORDER_TYPE_SELL  # Market sell order
    BUY_LIMIT = mt5.ORDER_TYPE_BUY_LIMIT  # Buy limit order
    SELL_LIMIT = mt5.ORDER_TYPE_SELL_LIMIT  # Sell limit order
    BUY_STOP = mt5.ORDER_TYPE_BUY_STOP  # Buy stop order
    SELL_STOP = mt5.ORDER_TYPE_SELL_STOP  # Sell stop order
    BUY_STOP_LIMIT = mt5.ORDER_TYPE_BUY_STOP_LIMIT  # Buy stop limit order
    SELL_STOP_LIMIT = mt5.ORDER_TYPE_SELL_STOP_LIMIT  # Sell stop limit order
    CLOSE_BY = mt5.ORDER_TYPE_CLOSE_BY  # Close by (hedge) order


class OrderFilling(IntEnum):
    """Order filling type enumeration"""

    FOK = mt5.ORDER_FILLING_FOK  # Fill or Kill (FOK)
    IOC = mt5.ORDER_FILLING_IOC  # Immediate or Cancel (IOC)
    BOC = mt5.ORDER_FILLING_BOC  # Book or Cancel (BOC)
    RETURN = mt5.ORDER_FILLING_RETURN  # Return (default)


class OrderTime(IntEnum):
    """Order time (expiration) type enumeration"""

    GTC = mt5.ORDER_TIME_GTC  # Good Till Canceled
    DAY = mt5.ORDER_TIME_DAY  # Good Till End of Day
    SPECIFIED = mt5.ORDER_TIME_SPECIFIED  # Good Till Specified Time
    SPECIFIED_DAY = mt5.ORDER_TIME_SPECIFIED_DAY  # Good Till Specified Day


class OrderState(IntEnum):
    """Order state enumeration"""

    STARTED = mt5.ORDER_STATE_STARTED  # Order just placed
    PLACED = mt5.ORDER_STATE_PLACED  # Order placed on the exchange
    CANCELED = mt5.ORDER_STATE_CANCELED  # Order has been canceled
    PARTIAL = mt5.ORDER_STATE_PARTIAL  # Order has been partially filled
    FILLED = mt5.ORDER_STATE_FILLED  # Order has been filled
    REJECTED = mt5.ORDER_STATE_REJECTED  # Order has been rejected
    EXPIRED = mt5.ORDER_STATE_EXPIRED  # Order has expired
    REQUEST_ADD = mt5.ORDER_STATE_REQUEST_ADD  # Order is in request queue
    REQUEST_MODIFY = mt5.ORDER_STATE_REQUEST_MODIFY  # Order is in modify request queue
    REQUEST_CANCEL = mt5.ORDER_STATE_REQUEST_CANCEL  # Order is in cancel request queue


class DealType(IntEnum):
    """Deal type enumeration"""

    BUY = mt5.DEAL_TYPE_BUY  # Buy deal
    SELL = mt5.DEAL_TYPE_SELL  # Sell deal
    BUY_CANCELED = mt5.DEAL_TYPE_BUY_CANCELED  # Canceled buy deal
    SELL_CANCELED = mt5.DEAL_TYPE_SELL_CANCELED  # Canceled sell deal
    BALANCE = mt5.DEAL_TYPE_BUY  # Balance
    CREDIT = mt5.DEAL_TYPE_BUY  # Credit
    CHARGE = mt5.DEAL_TYPE_BUY  # Charge
    CORRECTION = mt5.DEAL_TYPE_BUY  # Correction
    BONUS = mt5.DEAL_TYPE_BUY  # Bonus
    COMMISSION = mt5.DEAL_TYPE_BUY  # Commission


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
    magic: int = Field(
        default=0, json_schema_extra={"summary": "Expert Advisor ID (magic number)"}
    )
    order: int = Field(
        default=0, json_schema_extra={"summary": "Order ticket (for modifications)"}
    )
    symbol: str  # Trade symbol
    volume: float  # Requested volume in lots
    price: float = Field(default=0.0, json_schema_extra={"summary": "Order price"})
    stoplimit: float = Field(
        default=0.0, json_schema_extra={"summary": "StopLimit price"}
    )
    sl: float = Field(default=0.0, json_schema_extra={"summary": "Stop Loss level"})
    tp: float = Field(default=0.0, json_schema_extra={"summary": "Take Profit level"})
    deviation: float = Field(
        default=0.0, json_schema_extra={"summary": "Max price deviation in points"}
    )
    type: OrderType  # Order type
    type_filling: OrderFilling  # Order filling type
    type_time: OrderTime  # Order expiration type
    expiration: int = Field(
        default=0, json_schema_extra={"summary": "Order expiration time (datetime)"}
    )
    comment: str = Field(default="", json_schema_extra={"summary": "Order comment"})
    position: int = Field(default=0, json_schema_extra={"summary": "Position ticket"})
    position_by: int = Field(
        default=0, json_schema_extra={"summary": "Opposite position ticket"}
    )


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
    comment: str = Field(
        default="", json_schema_extra={"summary": "Return code description"}
    )


class TradeResult(BaseModel):
    """
    MqlTradeResult structure for trade request execution results.
    Returned by OrderSend() and OrderSendAsync() functions.
    """

    retcode: int  # Trade server return code
    deal: int = Field(
        default=0, json_schema_extra={"summary": "Deal ticket if executed"}
    )
    order: int = Field(
        default=0, json_schema_extra={"summary": "Order ticket if placed"}
    )
    volume: float = Field(
        default=0.0, json_schema_extra={"summary": "Deal volume confirmed by broker"}
    )
    price: float = Field(
        default=0.0, json_schema_extra={"summary": "Deal price confirmed by broker"}
    )
    bid: float = Field(default=0.0, json_schema_extra={"summary": "Current Bid price"})
    ask: float = Field(default=0.0, json_schema_extra={"summary": "Current Ask price"})
    comment: str = Field(default="", json_schema_extra={"summary": "Broker comment"})
    request_id: int = Field(default=0, json_schema_extra={"summary": "Request ID"})
    retcode_external: int = Field(
        default=0, json_schema_extra={"summary": "External system error code"}
    )


class TradeTransaction(BaseModel):
    """
    MqlTradeTransaction structure describing a trade transaction.
    Received by OnTradeTransaction() event handler.
    """

    deal: int = Field(default=0, json_schema_extra={"summary": "Deal ticket"})
    order: int = Field(default=0, json_schema_extra={"summary": "Order ticket"})
    symbol: str = Field(default="", json_schema_extra={"summary": "Trade symbol"})
    type: TradeTransactionType  # Trade transaction type
    order_type: Optional[OrderType] = Field(
        default=None, json_schema_extra={"summary": "Order type"}
    )
    order_state: Optional[OrderState] = Field(
        default=None, json_schema_extra={"summary": "Order state"}
    )
    deal_type: Optional[DealType] = Field(
        default=None, json_schema_extra={"summary": "Deal type"}
    )
    time_type: Optional[OrderTime] = Field(
        default=None, json_schema_extra={"summary": "Order time type"}
    )
    time_expiration: int = Field(
        default=0, json_schema_extra={"summary": "Order expiration time (datetime)"}
    )
    price: float = Field(
        default=0.0, json_schema_extra={"summary": "Order/deal/position price"}
    )
    price_trigger: float = Field(
        default=0.0, json_schema_extra={"summary": "Stop limit activation price"}
    )
    price_sl: float = Field(
        default=0.0, json_schema_extra={"summary": "Stop Loss level"}
    )
    price_tp: float = Field(
        default=0.0, json_schema_extra={"summary": "Take Profit level"}
    )
    volume: float = Field(default=0.0, json_schema_extra={"summary": "Volume in lots"})
    position: int = Field(default=0, json_schema_extra={"summary": "Position ticket"})
    position_by: int = Field(
        default=0, json_schema_extra={"summary": "Opposite position ticket"}
    )
