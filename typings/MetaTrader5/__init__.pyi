"""
Type stubs for MetaTrader5 module.
"""

from datetime import datetime
from typing import Any, Literal, NamedTuple, overload, TypedDict
import numpy as np

__version__: str
__author__: str

# Type definitions for bar/rate records with named fields
# Represents structured array with columns:
# - time: uint32 (bar timestamp)
# - open: float64 (opening price)
# - high: float64 (high price)
# - low: float64 (low price)
# - close: float64 (closing price)
# - tick_volume: uint64 (tick volume)
# - spread: int32 (spread)
# - real_volume: uint64 (real volume)

# Named tuple definitions
class AccountInfo(NamedTuple):
    login: int
    trade_mode: int
    leverage: int
    limit_orders: int
    balance: float
    credit: float
    profit: float
    equity: float
    margin: float
    margin_free: float
    margin_level: float
    margin_so_call: float
    margin_so_so: float
    assets: float
    liabilities: float
    commission_blocked: float
    name: str
    server: str
    currency: str
    path: str

class TerminalInfo(NamedTuple):
    pass

class SymbolInfo(NamedTuple):
    pass

class Tick(NamedTuple):
    pass

class Order(NamedTuple):
    pass

class Position(NamedTuple):
    pass

class Deal(NamedTuple):
    pass

class TradeRequest(TypedDict):
    action:int
    magic:int
    order:int
    symbol:str
    volume:float
    price:float
    stoplimit:float
    sl:float
    tp:float
    deviation:float
    type:int
    type_filling:int
    type_time:int
    expiration:int
    comment:str
    position:int
    position_by:int

class TradeCheckResult(TypedDict):
    pass

class TradeResult(TypedDict):
    pass

# Timeframe constants
TIMEFRAME_M1: int
TIMEFRAME_M2: int
TIMEFRAME_M3: int
TIMEFRAME_M4: int
TIMEFRAME_M5: int
TIMEFRAME_M6: int
TIMEFRAME_M10: int
TIMEFRAME_M12: int
TIMEFRAME_M15: int
TIMEFRAME_M20: int
TIMEFRAME_M30: int
TIMEFRAME_H1: int
TIMEFRAME_H2: int
TIMEFRAME_H4: int
TIMEFRAME_H3: int
TIMEFRAME_H6: int
TIMEFRAME_H8: int
TIMEFRAME_H12: int
TIMEFRAME_D1: int
TIMEFRAME_W1: int
TIMEFRAME_MN1: int

# Tick copy flags
COPY_TICKS_ALL: int
COPY_TICKS_INFO: int
COPY_TICKS_TRADE: int

# Tick flags
TICK_FLAG_BID: int
TICK_FLAG_ASK: int
TICK_FLAG_LAST: int
TICK_FLAG_VOLUME: int
TICK_FLAG_BUY: int
TICK_FLAG_SELL: int

# Position type constants
POSITION_TYPE_BUY: int
POSITION_TYPE_SELL: int

# Position reason constants
POSITION_REASON_CLIENT: int
POSITION_REASON_MOBILE: int
POSITION_REASON_WEB: int
POSITION_REASON_EXPERT: int

# Order type constants
ORDER_TYPE_BUY: int
ORDER_TYPE_SELL: int
ORDER_TYPE_BUY_LIMIT: int
ORDER_TYPE_SELL_LIMIT: int
ORDER_TYPE_BUY_STOP: int
ORDER_TYPE_SELL_STOP: int
ORDER_TYPE_BUY_STOP_LIMIT: int
ORDER_TYPE_SELL_STOP_LIMIT: int
ORDER_TYPE_CLOSE_BY: int

# Order state constants
ORDER_STATE_STARTED: int
ORDER_STATE_PLACED: int
ORDER_STATE_CANCELED: int
ORDER_STATE_PARTIAL: int
ORDER_STATE_FILLED: int
ORDER_STATE_REJECTED: int
ORDER_STATE_EXPIRED: int
ORDER_STATE_REQUEST_ADD: int
ORDER_STATE_REQUEST_MODIFY: int
ORDER_STATE_REQUEST_CANCEL: int

# Order filling mode constants
ORDER_FILLING_FOK: int
ORDER_FILLING_IOC: int
ORDER_FILLING_RETURN: int
ORDER_FILLING_BOC: int

# Order time mode constants
ORDER_TIME_GTC: int
ORDER_TIME_DAY: int
ORDER_TIME_SPECIFIED: int
ORDER_TIME_SPECIFIED_DAY: int

# Order reason constants
ORDER_REASON_CLIENT: int
ORDER_REASON_MOBILE: int
ORDER_REASON_WEB: int
ORDER_REASON_EXPERT: int
ORDER_REASON_SL: int
ORDER_REASON_TP: int
ORDER_REASON_SO: int

# Deal type constants
DEAL_TYPE_BUY: int
DEAL_TYPE_SELL: int
DEAL_TYPE_BALANCE: int
DEAL_TYPE_CREDIT: int
DEAL_TYPE_CHARGE: int
DEAL_TYPE_CORRECTION: int
DEAL_TYPE_BONUS: int
DEAL_TYPE_COMMISSION: int
DEAL_TYPE_COMMISSION_DAILY: int
DEAL_TYPE_COMMISSION_MONTHLY: int
DEAL_TYPE_COMMISSION_AGENT_DAILY: int
DEAL_TYPE_COMMISSION_AGENT_MONTHLY: int
DEAL_TYPE_INTEREST: int
DEAL_TYPE_BUY_CANCELED: int
DEAL_TYPE_SELL_CANCELED: int
DEAL_DIVIDEND: int
DEAL_DIVIDEND_FRANKED: int
DEAL_TAX: int

# Deal entry constants
DEAL_ENTRY_IN: int
DEAL_ENTRY_OUT: int
DEAL_ENTRY_INOUT: int
DEAL_ENTRY_OUT_BY: int

# Deal reason constants
DEAL_REASON_CLIENT: int
DEAL_REASON_MOBILE: int
DEAL_REASON_WEB: int
DEAL_REASON_EXPERT: int
DEAL_REASON_SL: int
DEAL_REASON_TP: int
DEAL_REASON_SO: int
DEAL_REASON_ROLLOVER: int
DEAL_REASON_VMARGIN: int
DEAL_REASON_SPLIT: int

# Trade action constants
TRADE_ACTION_DEAL: int
TRADE_ACTION_PENDING: int
TRADE_ACTION_SLTP: int
TRADE_ACTION_MODIFY: int
TRADE_ACTION_REMOVE: int
TRADE_ACTION_CLOSE_BY: int

# Symbol chart mode constants
SYMBOL_CHART_MODE_BID: int
SYMBOL_CHART_MODE_LAST: int

# Symbol calculation mode constants
SYMBOL_CALC_MODE_FOREX: int
SYMBOL_CALC_MODE_FUTURES: int
SYMBOL_CALC_MODE_CFD: int
SYMBOL_CALC_MODE_CFDINDEX: int
SYMBOL_CALC_MODE_CFDLEVERAGE: int
SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE: int
SYMBOL_CALC_MODE_EXCH_STOCKS: int
SYMBOL_CALC_MODE_EXCH_FUTURES: int
SYMBOL_CALC_MODE_EXCH_OPTIONS: int
SYMBOL_CALC_MODE_EXCH_OPTIONS_MARGIN: int
SYMBOL_CALC_MODE_EXCH_BONDS: int
SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX: int
SYMBOL_CALC_MODE_EXCH_BONDS_MOEX: int
SYMBOL_CALC_MODE_SERV_COLLATERAL: int

# Symbol trade mode constants
SYMBOL_TRADE_MODE_DISABLED: int
SYMBOL_TRADE_MODE_LONGONLY: int
SYMBOL_TRADE_MODE_SHORTONLY: int
SYMBOL_TRADE_MODE_CLOSEONLY: int
SYMBOL_TRADE_MODE_FULL: int

# Symbol trade execution constants
SYMBOL_TRADE_EXECUTION_REQUEST: int
SYMBOL_TRADE_EXECUTION_INSTANT: int
SYMBOL_TRADE_EXECUTION_MARKET: int
SYMBOL_TRADE_EXECUTION_EXCHANGE: int

# Symbol swap mode constants
SYMBOL_SWAP_MODE_DISABLED: int
SYMBOL_SWAP_MODE_POINTS: int
SYMBOL_SWAP_MODE_CURRENCY_SYMBOL: int
SYMBOL_SWAP_MODE_CURRENCY_MARGIN: int
SYMBOL_SWAP_MODE_CURRENCY_DEPOSIT: int
SYMBOL_SWAP_MODE_INTEREST_CURRENT: int
SYMBOL_SWAP_MODE_INTEREST_OPEN: int
SYMBOL_SWAP_MODE_REOPEN_CURRENT: int
SYMBOL_SWAP_MODE_REOPEN_BID: int

# Day of week constants
DAY_OF_WEEK_SUNDAY: int
DAY_OF_WEEK_MONDAY: int
DAY_OF_WEEK_TUESDAY: int
DAY_OF_WEEK_WEDNESDAY: int
DAY_OF_WEEK_THURSDAY: int
DAY_OF_WEEK_FRIDAY: int
DAY_OF_WEEK_SATURDAY: int

# Symbol order GTC mode constants
SYMBOL_ORDERS_GTC: int
SYMBOL_ORDERS_DAILY: int
SYMBOL_ORDERS_DAILY_NO_STOPS: int

# Symbol option right constants
SYMBOL_OPTION_RIGHT_CALL: int
SYMBOL_OPTION_RIGHT_PUT: int

# Symbol option mode constants
SYMBOL_OPTION_MODE_EUROPEAN: int
SYMBOL_OPTION_MODE_AMERICAN: int

# Account trade mode constants
ACCOUNT_TRADE_MODE_DEMO: int
ACCOUNT_TRADE_MODE_CONTEST: int
ACCOUNT_TRADE_MODE_REAL: int

# Account stopout mode constants
ACCOUNT_STOPOUT_MODE_PERCENT: int
ACCOUNT_STOPOUT_MODE_MONEY: int

# Account margin mode constants
ACCOUNT_MARGIN_MODE_RETAIL_NETTING: int
ACCOUNT_MARGIN_MODE_EXCHANGE: int
ACCOUNT_MARGIN_MODE_RETAIL_HEDGING: int

# Book type constants
BOOK_TYPE_SELL: int
BOOK_TYPE_BUY: int
BOOK_TYPE_SELL_MARKET: int
BOOK_TYPE_BUY_MARKET: int

# Trade return code constants
TRADE_RETCODE_REQUOTE: int
TRADE_RETCODE_REJECT: int
TRADE_RETCODE_CANCEL: int
TRADE_RETCODE_PLACED: int
TRADE_RETCODE_DONE: int
TRADE_RETCODE_DONE_PARTIAL: int
TRADE_RETCODE_ERROR: int
TRADE_RETCODE_TIMEOUT: int
TRADE_RETCODE_INVALID: int
TRADE_RETCODE_INVALID_VOLUME: int
TRADE_RETCODE_INVALID_PRICE: int
TRADE_RETCODE_INVALID_STOPS: int
TRADE_RETCODE_TRADE_DISABLED: int
TRADE_RETCODE_MARKET_CLOSED: int
TRADE_RETCODE_NO_MONEY: int
TRADE_RETCODE_PRICE_CHANGED: int
TRADE_RETCODE_PRICE_OFF: int
TRADE_RETCODE_INVALID_EXPIRATION: int
TRADE_RETCODE_ORDER_CHANGED: int
TRADE_RETCODE_TOO_MANY_REQUESTS: int
TRADE_RETCODE_NO_CHANGES: int
TRADE_RETCODE_SERVER_DISABLES_AT: int
TRADE_RETCODE_CLIENT_DISABLES_AT: int
TRADE_RETCODE_LOCKED: int
TRADE_RETCODE_FROZEN: int
TRADE_RETCODE_INVALID_FILL: int
TRADE_RETCODE_CONNECTION: int
TRADE_RETCODE_ONLY_REAL: int
TRADE_RETCODE_LIMIT_ORDERS: int
TRADE_RETCODE_LIMIT_VOLUME: int
TRADE_RETCODE_INVALID_ORDER: int
TRADE_RETCODE_POSITION_CLOSED: int
TRADE_RETCODE_INVALID_CLOSE_VOLUME: int
TRADE_RETCODE_CLOSE_ORDER_EXIST: int
TRADE_RETCODE_LIMIT_POSITIONS: int
TRADE_RETCODE_REJECT_CANCEL: int
TRADE_RETCODE_LONG_ONLY: int
TRADE_RETCODE_SHORT_ONLY: int
TRADE_RETCODE_CLOSE_ONLY: int
TRADE_RETCODE_FIFO_CLOSE: int

# Result code constants (function error codes)
RES_S_OK: int
RES_E_FAIL: int
RES_E_INVALID_PARAMS: int
RES_E_NO_MEMORY: int
RES_E_NOT_FOUND: int
RES_E_INVALID_VERSION: int
RES_E_AUTH_FAILED: int
RES_E_UNSUPPORTED: int
RES_E_AUTO_TRADING_DISABLED: int
RES_E_INTERNAL_FAIL: int
RES_E_INTERNAL_FAIL_SEND: int
RES_E_INTERNAL_FAIL_RECEIVE: int
RES_E_INTERNAL_FAIL_INIT: int
RES_E_INTERNAL_FAIL_CONNECT: int
RES_E_INTERNAL_FAIL_TIMEOUT: int

# Core functions
@overload
def initialize() -> bool: ...
@overload
def initialize(path: str) -> bool: ...
@overload
def initialize(
    path: str,
    *,
    login: int | None = None,
    password: str | None = None,
    server: str | None = None,
    timeout: int | None = None,
    portable: bool = False,
) -> bool: ...
def login(
    login: str, password: str | None, server: str | None, timeout: str | None
) -> bool: ...
def shutdown() -> None: ...
def version() -> tuple[int, int, str] | None: ...
def last_error() -> tuple[int, str]: ...
def account_info() -> AccountInfo | None: ...
def terminal_info() -> TerminalInfo | None: ...
def symbols_total() -> int: ...
def symbols_get(group: str | None = None) -> tuple[SymbolInfo] | None: ...
def symbol_info(symbol: str) -> SymbolInfo | None: ...
def symbol_info_tick(symbol: str) -> Tick | None: ...
def symbol_select(symbol: str, enable: bool | None) -> bool: ...
def market_book_add(symbol: str) -> bool: ...
def market_book_get(symbol: str) -> bool: ...
def market_book_release(symbol: str) -> bool: ...
def copy_rates_from(
    symbol: str, timeframe: int, date_from: int | datetime, count: int
) -> np.ndarray | None: ...
def copy_rates_from_pos(
    symbol: str, timeframe: int, start_pos: int, count: int
) -> np.ndarray | None: ...
def copy_rates_range(
    symbol: str, timeframe: int, date_from: int | datetime, date_to: int | datetime
) -> np.ndarray | None: ...
def copy_ticks_from(
    symbol: str, date_from: int | datetime, count: int, flags: int
) -> np.ndarray: ...
def copy_ticks_range(
    symbol: str, date_from: int | datetime, date_to: int | datetime, flags: int
) -> np.ndarray: ...
def orders_total() -> int: ...
@overload
def orders_get() -> tuple[Order, ...] | None: ...
@overload
def orders_get(*, symbol: str) -> tuple[Order, ...] | None: ...
@overload
def orders_get(*, group: str) -> tuple[Order, ...] | None: ...
@overload
def orders_get(*, ticket: int) -> tuple[Order, ...] | None: ...
def order_calc_margin(
    action: int, symbol: str, volume: float, price: float
) -> float: ...
def order_calc_profit(
    action: int, symbol: str, volume: float, price_open: float, price_close: float
) -> float: ...
def order_check(request: TradeRequest) -> TradeCheckResult: ...
def order_send(request: TradeRequest) -> TradeResult: ...
def positions_total() -> int: ...
@overload
def positions_get() -> tuple[Position, ...] | None: ...
@overload
def positions_get(*, symbol: str) -> tuple[Position, ...] | None: ...
@overload
def positions_get(*, group: str) -> tuple[Position, ...] | None: ...
@overload
def positions_get(*, ticket: int) -> tuple[Position, ...] | None: ...
def history_orders_total() -> int: ...
@overload
def history_orders_get(
    date_from: int | datetime, date_to: int | datetime, *, group: str | None = None
) -> tuple[Order, ...] | None: ...
@overload
def history_orders_get(*, ticket: int) -> tuple[Order, ...] | None: ...
@overload
def history_orders_get(*, position: int) -> tuple[Order, ...] | None: ...
def history_deals_total() -> int: ...
@overload
def history_deals_get(
    date_from: int | datetime, date_to: int | datetime, *, group: str | None = None
) -> tuple[Deal, ...] | None: ...
@overload
def history_deals_get(*, ticket: int) -> tuple[Deal, ...] | None: ...
@overload
def history_deals_get(*, position: int) -> tuple[Deal, ...] | None: ...

# Function signatures
def Close(
    symbol: str, *, comment: str | None = None, ticket: int | None = None
) -> bool | Literal["Partially"] | None: ...
def Buy(
    symbol: str,
    volume: float,
    price: float | None = None,
    *,
    comment: str | None = None,
    ticket: int | None = None,
) -> Any: ...
def Sell(
    symbol: str,
    volume: float,
    price: float | None = None,
    *,
    comment: str | None = None,
    ticket: int | None = None,
) -> Any: ...
