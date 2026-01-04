import MetaTrader5 as mt5  # type: ignore
from fastapi import FastAPI
from account import router as account_router
from symbol import router as symbol_router
from rates import router as rates_router
from ticks import router as tick_router
from terminal import router as terminal_router
from history import router as history_router
from position import router as position_router
from order import router as order_router

if not mt5.initialize():
    print("MT5 not initialized")
    exit(code=1)

app = FastAPI()

app.include_router(account_router)
app.include_router(symbol_router)
app.include_router(rates_router)
app.include_router(tick_router)
app.include_router(terminal_router)
app.include_router(history_router)
app.include_router(position_router)
app.include_router(order_router)
