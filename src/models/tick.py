from pydantic import BaseModel
from enum import IntEnum


# Tick Flag Enumerations
class TickFlag(IntEnum):
    """Tick flag enumeration"""

    BID = 1  # Tick has changed a Bid price
    ASK = 2  # Tick has changed an Ask price
    LAST = 4  # Tick has changed the last deal price
    VOLUME = 8  # Tick has changed a volume
    BUY = 16  # Tick is a result of a buy deal
    SELL = 32  # Tick is a result of a sell deal


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
