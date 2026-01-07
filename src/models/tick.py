from pydantic import BaseModel
from enum import IntEnum
import MetaTrader5 as mt5 # type: ignore


# Tick Flag Enumerations
class TickFlag(IntEnum):
    """Tick flag enumeration"""

    BID = mt5.TICK_FLAG_BID  # Tick has changed a Bid price
    ASK = mt5.TICK_FLAG_ASK  # Tick has changed an Ask price
    LAST = mt5.TICK_FLAG_LAST  # Tick has changed the last deal price
    VOLUME = mt5.TICK_FLAG_VOLUME  # Tick has changed a volume
    BUY =  mt5.TICK_FLAG_BUY  # Tick is a result of a buy deal
    SELL =  mt5.TICK_FLAG_SELL  # Tick is a result of a sell deal


# Tick Structure
class Tick(BaseModel):
    """
    MqlTick structure for storing the latest prices of a symbol.
    Designed for fast retrieval of the most requested information about current prices.
    """

    time: int  # Time of the last prices update (datetime)
    bid: float  # Current Bid price
    ask: float  # Current Ask price
    last: float  # Price of the last deal (Last)
    volume: int  # Volume for the current Last price
    time_msc: int  # Time of price last update in milliseconds
    flags: int  # Tick flags (combination of TickFlag values)
    volume_real: float  # Volume for the current Last price with greater accuracy
