from pydantic import BaseModel

# Properties
class AccountProperty(BaseModel):
    pass
  
class TerminalProperty(BaseModel):
    pass
  
class SymbolProperty(BaseModel):
    pass
  
class Rate(BaseModel):
    pass
  
class Tick(BaseModel):
    pass
  
class Order(BaseModel):
    pass
  
class Position(BaseModel):
    pass
  
class Deal(BaseModel):
    pass

# request / response
class SymbolPropertyResponse(BaseModel):
    name:str
    info:SymbolProperty

class CalculateMarginPayload(BaseModel):
    action:int
    symbol:str
    volume:float
    price:float
    
class CalculateProfitPayload(BaseModel):
    action:int
    symbol:str
    volume:float
    price_open:float
    price_close:float
    
class TradeRequest(BaseModel):
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
  
class TradeCheckResultResponse(BaseModel):
    pass

class TradeResultResponse(BaseModel):
    pass