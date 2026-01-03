from pydantic import BaseModel


# Rate/OHLC Structure
class Rate(BaseModel):
    """
    MqlRates structure for storing information about prices, volumes and spread.
    Contains OHLC (Open, High, Low, Close) data for a specific time period.
    """

    time: int  # Period start time (datetime)
    open: float  # Open price
    high: float  # The highest price of the period
    low: float  # The lowest price of the period
    close: float  # Close price
    tick_volume: int  # Tick volume
    spread: int  # Spread
    real_volume: int  # Trade volume
