from pydantic import BaseModel
from enum import IntEnum
import MetaTrader5 as mt5


# Symbol Enumerations
class SymbolChartMode(IntEnum):
    """Symbol chart mode enumeration"""
    BID = 0  # Bars are based on Bid prices
    LAST = 1  # Bars are based on Last prices


class SymbolTradeMode(IntEnum):
    """Symbol trade mode enumeration"""
    DISABLED = 0  # Trade is disabled for the symbol
    LONGONLY = 1  # Allowed only long positions
    SHORTONLY = 2  # Allowed only short positions
    CLOSEONLY = 3  # Allowed only position close operations
    FULL = 4  # No trade restrictions


class SymbolTradeExecution(IntEnum):
    """Symbol trade execution enumeration"""
    REQUEST = 0  # Execution by request
    INSTANT = 1  # Instant execution
    MARKET = 2  # Market execution
    EXCHANGE = 3  # Exchange execution


class SymbolCalcMode(IntEnum):
    """Symbol calculation mode enumeration"""
    FOREX = mt5.SYMBOL_CALC_MODE_FOREX
    FOREX_NO_LEVERAGE = mt5.SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE
    FUTURES = mt5.SYMBOL_CALC_MODE_FUTURES
    CFD = mt5.SYMBOL_CALC_MODE_CFD
    CFDINDEX = mt5.SYMBOL_CALC_MODE_CFDINDEX
    CFDLEVERAGE = mt5.SYMBOL_CALC_MODE_CFDLEVERAGE
    EXCH_STOCKS = mt5.SYMBOL_CALC_MODE_EXCH_STOCKS
    EXCH_FUTURES = mt5.SYMBOL_CALC_MODE_EXCH_FUTURES
    EXCH_FUTURES_FORTS = mt5.SYMBOL_CALC_MODE_EXCH_FUTURES
    EXCH_BONDS = mt5.SYMBOL_CALC_MODE_EXCH_BONDS
    EXCH_STOCKS_MOEX = mt5.SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX
    EXCH_BONDS_MOEX = mt5.SYMBOL_CALC_MODE_EXCH_BONDS_MOEX
    SERV_COLLATERAL = mt5.SYMBOL_CALC_MODE_SERV_COLLATERAL


class SymbolSwapMode(IntEnum):
    """Symbol swap mode enumeration"""
    DISABLED = 0  # Swaps disabled
    POINTS = 1  # Swaps are charged in points
    CURRENCY_SYMBOL = 2  # Swaps in base currency
    CURRENCY_MARGIN = 3  # Swaps in margin currency
    CURRENCY_DEPOSIT = 4  # Swaps in deposit currency
    CURRENCY_PROFIT = 5  # Swaps in profit currency
    INTEREST_CURRENT = 6  # Annual interest from current price
    INTEREST_OPEN = 7  # Annual interest from open price
    REOPEN_CURRENT = 8  # Reopen at close price
    REOPEN_BID = 9  # Reopen at bid price


class DayOfWeek(IntEnum):
    """Day of week enumeration"""
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


class SymbolOrderGtcMode(IntEnum):
    """Symbol order GTC mode enumeration"""
    GTC = 0  # Valid until explicit cancellation
    DAILY = 1  # Valid during one trading day
    DAILY_EXCLUDING_STOPS = 2  # Daily, but preserve Stop Loss/Take Profit


class SymbolOptionMode(IntEnum):
    """Symbol option mode enumeration"""
    EUROPEAN = 0  # European option
    AMERICAN = 1  # American option


class SymbolOptionRight(IntEnum):
    """Symbol option right enumeration"""
    CALL = 0  # Call option - right to buy
    PUT = 1  # Put option - right to sell


class SymbolSector(IntEnum):
    """Symbol sector enumeration"""
    UNDEFINED = 0
    BASIC_MATERIALS = 1
    COMMUNICATION_SERVICES = 2
    CONSUMER_CYCLICAL = 3
    CONSUMER_DEFENSIVE = 4
    CURRENCY = 5
    CURRENCY_CRYPTO = 6
    ENERGY = 7
    FINANCIAL = 8
    HEALTHCARE = 9
    INDUSTRIALS = 10
    REAL_ESTATE = 11
    TECHNOLOGY = 12
    UTILITIES = 13


# Symbol Properties
class SymbolProperty(BaseModel):
    # Integer Properties
    subscription_delay: bool = False # Symbol data arrives with a delay
    select: bool  # Symbol is selected in Market Watch
    visible: bool  # Symbol is visible in Market Watch
    session_deals: int  # Number of deals in the current session
    session_buy_orders: int  # Number of Buy orders at the moment
    session_sell_orders: int  # Number of Sell orders at the moment
    volume: int  # Volume of the last deal
    volumehigh: int  # Maximal day volume
    volumelow: int  # Minimal day volume
    digits: int  # Digits after a decimal point
    spread: int  # Spread value in points
    spread_float: bool  # Indication of a floating spread
    ticks_bookdepth: int  # Maximal number of requests in Depth of Market
    trade_calc_mode: SymbolCalcMode  # Contract price calculation mode
    trade_mode: SymbolTradeMode  # Order execution type
    trade_stops_level: int  # Minimal indention in points for Stop orders
    trade_freeze_level: int  # Distance to freeze trade operations in points
    trade_exemode: SymbolTradeExecution  # Deal execution mode
    swap_mode: SymbolSwapMode  # Swap calculation model
    swap_rollover3days: DayOfWeek  # Day of week for 3-day swap rollover
    margin_hedged_use_leg: bool  # Hedging margin using larger leg
    expiration_mode: int  # Flags of allowed order expiration modes
    filling_mode: int  # Flags of allowed order filling modes
    order_mode: int  # Flags of allowed order types
    order_gtc_mode: SymbolOrderGtcMode  # Expiration of Stop Loss/Take Profit
    option_mode: SymbolOptionMode  # Option type
    option_right: SymbolOptionRight  # Option right (Call/Put)
    chart_mode: SymbolChartMode  # Price type for bar generation
    exist: bool | None = None  # Symbol with this name exists
    custom: bool  # It is a custom symbol
    sector: SymbolSector | None  = None # The sector of the economy
    time: int  # Time of the last quote (datetime)
    time_msc: int | None = None # Time of the last quote in milliseconds
    
    # Double Properties
    bid: float  # Bid - best sell offer
    bidhigh: float  # Maximal Bid of the day
    bidlow: float  # Minimal Bid of the day
    ask: float  # Ask - best buy offer
    askhigh: float  # Maximal Ask of the day
    asklow: float  # Minimal Ask of the day
    last: float  # Price of the last deal
    lasthigh: float  # Maximal Last of the day
    lastlow: float  # Minimal Last of the day
    volume_real: float  # Real volume of the last deal
    volumehigh_real: float  # Maximum real volume of the day
    volumelow_real: float  # Minimum real volume of the day
    option_strike: float  # Strike price of an option
    point: float  # Symbol point value
    trade_tick_value: float  # Value of tick
    trade_tick_value_profit: float  # Tick price for profitable position
    trade_tick_value_loss: float  # Tick price for losing position
    trade_tick_size: float  # Minimal price change
    trade_contract_size: float  # Trade contract size
    trade_accrued_interest: float  # Accrued coupon interest
    trade_face_value: float  # Face value of a bond
    trade_liquidity_rate: float  # Liquidity Rate
    volume_min: float  # Minimal volume for a deal
    volume_max: float  # Maximal volume for a deal
    volume_step: float  # Minimal volume change step
    volume_limit: float  # Maximum allowed aggregate volume
    swap_long: float  # Long swap value
    swap_short: float  # Short swap value
    swap_sunday: float | None = None  # Swap ratio for Sunday rollover
    swap_monday: float | None = None  # Swap ratio for Monday rollover
    swap_tuesday: float | None = None  # Swap ratio for Tuesday rollover
    swap_wednesday: float | None = None  # Swap ratio for Wednesday rollover
    swap_thursday: float | None = None  # Swap ratio for Thursday rollover
    swap_friday: float | None = None  # Swap ratio for Friday rollover
    swap_saturday: float | None = None  # Swap ratio for Saturday rollover
    margin_initial: float  # Initial margin for one lot
    margin_maintenance: float  # Maintenance margin
    margin_hedged: float  # Margin for hedged positions
    session_volume: float  # Summary volume of current session deals
    session_turnover: float  # Summary turnover of the current session
    session_interest: float  # Summary open interest
    session_buy_orders_volume: float  # Current volume of Buy orders
    session_sell_orders_volume: float  # Current volume of Sell orders
    session_open: float  # Open price of the current session
    session_close: float  # Close price of the current session
    session_aw: float  # Average weighted price of the current session
    session_price_settlement: float  # Settlement price of the current session
    session_price_limit_min: float  # Minimal price of the current session
    session_price_limit_max: float  # Maximal price of the current session
    price_change: float  # Change relative to previous day in %
    price_volatility: float  # Price volatility in %
    price_theoretical: float  # Theoretical option price
    price_delta: float | None = None # Option delta
    price_theta: float | None = None # Option theta
    price_gamma: float | None = None # Option gamma
    price_vega: float | None = None # Option vega
    price_rho: float | None = None # Option rho
    price_omega: float | None = None # Option omega (elasticity)
    price_sensitivity: float  # Option sensitivity
    
    # String Properties
    name: str  # Symbol name
    description: str  # Symbol description
    basis: str  # The underlying asset of a derivative
    category: str  # Category or sector name
    country: str | None = None  # The country of the financial symbol
    sector_name: str | None = None  # The sector name
    industry_name: str | None = None  # The industry name
    currency_base: str  # Basic currency of a symbol
    currency_profit: str  # Profit currency
    currency_margin: str  # Margin currency
    bank: str  # Feeder of the current quote
    exchange: str  # The name of the exchange
    formula: str  # Formula for custom symbol pricing
    isin: str  # ISIN code
    page: str  # Web page with symbol information
    path: str  # Path in the symbol tree
