import MetaTrader5 as mt5  # type: ignore
from fastapi import FastAPI
from .account import router as account_router
from .symbol import router as symbol_router
from .rates import router as rates_router
from .ticks import router as tick_router
from .terminal import router as terminal_router
from .history import router as history_router
from .position import router as position_router
from .order import router as order_router

if not mt5.initialize():
    print("MT5 not initialized")
    exit(code=1)

app = FastAPI(
    title="MetaTrader5 REST API",
    version="0.1.0",
    description="A comprehensive REST API for MetaTrader5 terminal operations, providing endpoints for account management, trading operations, market data retrieval, and historical analysis.",
    contact={
        "name": "MT5 REST API Support",
        "url": "https://github.com/marahuyo-ph/mt5-rest-api",
        "email": "karlalferezfx@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local development server",
        },
        {
            "url": "http://127.0.0.1:8000",
            "description": "Local development server (localhost alternative)",
        },
    ],
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_version="3.1.0",
)

app.include_router(account_router)
app.include_router(symbol_router)
app.include_router(rates_router)
app.include_router(tick_router)
app.include_router(terminal_router)
app.include_router(history_router)
app.include_router(position_router)
app.include_router(order_router)
