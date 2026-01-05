# MT5-REST-API

A comprehensive REST API for MetaTrader5 terminal operations, built with FastAPI. This project provides seamless integration with MetaTrader5, enabling programmatic access to trading data, account information, market quotes, and order management through HTTP endpoints.

## 🎯 Overview

MT5-REST-API bridges the gap between MetaTrader5 and modern web applications by exposing a complete REST interface to the MetaTrader5 terminal. Whether you need real-time market data, account management, trade execution, or historical analysis, this API provides a robust and well-documented interface.

> **Note**: This project is an enhancement of [FishTools/fishing-net](https://github.com/FishTools/fishing-net), extending and improving upon the original codebase.

## ✨ Key Features

- **Account Management**: Retrieve detailed account information including balance, equity, margin details, and trading permissions
- **Symbol Information**: Access comprehensive symbol data including spreads, swap information, and trading parameters
- **Market Data**: Get real-time quotes, OHLC bars, and tick data for any trading instrument
- **Order Management**: Query active pending orders with filtering capabilities
- **Position Management**: Retrieve and manage open positions with detailed statistics
- **Trade History**: Access complete trading history including executed orders and deals
- **Terminal Status**: Monitor MetaTrader5 terminal connection status and configuration
- **Calculations**: Margin and profit calculations for trade planning
- **Type Safety**: Full Pydantic model support for request/response validation
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc documentation
- **Error Handling**: Comprehensive error responses with detailed error codes

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- MetaTrader5 client installed and running
- An active trading account connection in MT5

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/marahuyo-ph/mt5-rest-api.git
   cd mt5-rest-api
   ```

2. **Set up Python environment**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip with venv
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. **Run the server**
   ```bash
   fastapi dev src/main.py # or
   fastapi run src/main.py # run in production
   ```

4. **Access the API**
   - **Swagger UI**: http://localhost:8000/api/v1/docs
   - **ReDoc**: http://localhost:8000/api/v1/redoc
   - **OpenAPI Schema**: http://localhost:8000/api/v1/openapi.json

## 📚 API Endpoints

### Account Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/accounts/info` | GET | Retrieve detailed account information including balance, equity, and trading permissions |

### Symbols
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/symbols/total` | GET | Get the total count of available financial instruments |
| `/symbols/` | GET | Retrieve all symbols with optional filtering by group pattern |
| `/symbols/{symbol}/select` | PUT | Select/enable a symbol for trading operations |
| `/symbols/{symbol}/info` | GET | Get detailed information for a specific symbol |
| `/symbols/{symbol}/ticks/{direction}` | GET | Retrieve tick history for a symbol with optional filtering |

### Market Data & Rates
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/rates/from/{symbol}/{timeframe}/{date_from}/{count}` | GET | Get OHLC bars from a specified date |
| `/rates/range/{symbol}/{timeframe}/{date_from}/{date_to}` | GET | Get OHLC bars within a date range |
| `/rates/latest/{symbol}/{timeframe}/{count}` | GET | Get the latest N bars for a symbol |

### Orders (Pending)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/orders/total` | GET | Get count of active pending orders |
| `/orders/` | GET | Retrieve active pending orders with optional filtering |
| `/orders/calculate-margin` | POST | Calculate required margin for a potential trade |
| `/orders/calculate-profit` | POST | Calculate potential profit for a trade scenario |

### Positions (Open)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/positions/total` | GET | Get count of open positions |
| `/positions/` | GET | Retrieve open positions with optional filtering |

### Trading History
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/history/orders/total` | GET | Get total count of historical orders |
| `/history/orders/` | GET | Retrieve executed orders from history with optional filtering |
| `/history/deals/total` | GET | Get total count of deals |
| `/history/deals/` | GET | Retrieve deals from history with optional filtering |

### Terminal Information
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/terminal/info` | GET | Get MetaTrader5 terminal status and configuration |

## 🔧 Configuration

### Environment Setup

The API requires MetaTrader5 to be initialized before requests can be processed. The initialization is handled automatically in `src/main.py`:

```python
if not mt5.initialize():
    print("MT5 not initialized")
    exit(code=1)
```

### Server Configuration

The FastAPI server is configured with:
- **Title**: MetaTrader5 REST API
- **Version**: 0.1.0
- **OpenAPI Version**: 3.1.0
- **Docs Path**: `/api/v1/docs`
- **ReDoc Path**: `/api/v1/redoc`
- **OpenAPI Schema**: `/api/v1/openapi.json`

### Servers

- Local Development: `http://localhost:8000`
- Alternative Localhost: `http://127.0.0.1:8000`

## 📦 Project Structure

```
mt5-rest-api/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── account.py              # Account management endpoints
│   ├── symbol.py               # Symbol information endpoints
│   ├── rates.py                # Market data endpoints
│   ├── ticks.py                # Tick data endpoints
│   ├── terminal.py             # Terminal status endpoints
│   ├── history.py              # Trading history endpoints
│   ├── position.py             # Position management endpoints
│   ├── order.py                # Order management endpoints
│   ├── errors.py               # Error handling and response models
│   └── models/
│       ├── __init__.py
│       ├── account.py          # Account data models
│       ├── order.py            # Order data models
│       ├── position.py         # Position data models
│       ├── rate.py             # OHLC bar models
│       ├── symbol.py           # Symbol info models
│       ├── terminal.py         # Terminal info models
│       ├── tick.py             # Tick data models
│       ├── deal.py             # Deal data models
│       └── trade.py            # Trade request models
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # pytest configuration
│   ├── test_account.py
│   ├── test_symbol.py
│   ├── test_rates.py
│   ├── test_ticks.py
│   ├── test_terminal.py
│   ├── test_history.py
│   ├── test_order.py
│   ├── test_position.py
├── typings/
│   └── MetaTrader5/            # Type stubs for MetaTrader5
├── pyproject.toml              # Project configuration
├── pyrightconfig.json          # Pyright type checking configuration
└── README.md                   # This file
```

## 🧪 Testing

The project includes comprehensive test coverage using pytest:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_account.py

# Run with coverage
pytest --cov=src
```

### Test Files
- `test_account.py` - Account management tests
- `test_symbol.py` - Symbol endpoint tests
- `test_rates.py` - Market data endpoint tests
- `test_ticks.py` - Tick data endpoint tests
- `test_terminal.py` - Terminal status tests
- `test_history.py` - Trading history tests
- `test_order.py` - Order management tests
- `test_position.py` - Position management tests

## 📝 Data Models

### Account Information
```python
AccountProperty(
    login: int,
    server: str,
    trader: str,
    currency: str,
    balance: float,
    profit: float,
    equity: float,
    margin: float,
    margin_free: float,
    margin_level: float,
    leverage: int,
    trade_allowed: bool,
    trade_expert: bool,
    # ... and more fields
)
```

### Symbol Information
```python
SymbolProperty(
    name: str,
    bid: float,
    ask: float,
    spread: int,
    volume: int,
    trade_mode: int,
    margin_initial: float,
    margin_maintenance: float,
    swap_long: float,
    swap_short: float,
    # ... and more fields
)
```

### OHLC Rate
```python
Rate(
    time: int,           # Unix timestamp
    open: float,
    high: float,
    low: float,
    close: float,
    tick_volume: int,
    spread: int,
    real_volume: int
)
```

### Order
```python
Order(
    ticket: int,
    time_setup: int,
    type: int,
    state: int,
    symbol: str,
    volume_initial: float,
    volume_current: float,
    price_open: float,
    sl: float,           # Stop Loss
    tp: float,           # Take Profit
    magic: int,
    comment: str,
    # ... and more fields
)
```

### Position
```python
Position(
    ticket: int,
    time: int,
    type: int,
    symbol: str,
    volume: float,
    price_open: float,
    price_current: float,
    profit: float,
    swap: float,
    magic: int,
    # ... and more fields
)
```

## 🔌 Usage Examples

### Get Account Information
```bash
curl http://localhost:8000/accounts/info
```

### Get All Symbols
```bash
curl http://localhost:8000/symbols/
```

### Get OHLC Bars for a Symbol
```bash
curl "http://localhost:8000/rates/from/EURUSD/240/2024-01-01/100"
```

### Get Active Orders
```bash
curl http://localhost:8000/orders/
```

### Get Open Positions
```bash
curl http://localhost:8000/positions/
```

### Get Terminal Status
```bash
curl http://localhost:8000/terminal/info
```

### Calculate Required Margin
```bash
curl -X POST http://localhost:8000/orders/calculate-margin \
  -H "Content-Type: application/json" \
  -d '{
    "action": 0,
    "symbol": "EURUSD",
    "volume": 1.0,
    "price": 1.0850
  }'
```

## 🛠️ Development

### Installation for Development

```bash
# Install with development dependencies
uv sync
# or
pip install -e ".[dev]"
```

### Code Quality

The project uses:
- **Pyright**: For static type checking (strict mode)
- **Pytest**: For unit testing
- **Pydantic**: For data validation

### Type Checking

```bash
# Run Pyright type checker
pyright src/

# Or using pylance
pylance check src/
```

## 🤝 Architecture

### Design Patterns

1. **Router-based Modular Design**: Each feature area (accounts, symbols, orders, etc.) has its own router module
2. **Model-View Pattern**: Pydantic models for data validation and serialization
3. **Error Handling**: Centralized error handling with custom error responses
4. **Type Safety**: Full type hints throughout the codebase

### Technology Stack

- **Framework**: FastAPI 0.128.0+
- **Server**: Uvicorn (included with FastAPI[standard])
- **Validation**: Pydantic
- **Data Processing**: Pandas, NumPy
- **Trading Library**: MetaTrader5
- **HTTP Client**: HTTPX
- **Testing**: Pytest, Pytest-asyncio
- **Type Checking**: Pyright
- **Python**: 3.12+

## 📋 Requirements

```toml
[project]
name = "mt5-rest-api"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi[standard]>=0.128.0",
    "httpx>=0.28.1",
    "metatrader5>=5.0.5430",
    "numpy>=2.4.0",
    "pandas>=2.3.3",
]

[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.23.0",
]
```

## 🐛 Error Handling

The API uses the official MetaTrader5 error system and returns structured error responses using [`mt5.last_error()`](https://www.mql5.com/en/docs/python_metatrader5/mt5lasterror_py) when operations fail. All MetaTrader5-related errors return a **500 Internal Server Error** status code.

Error response format:

```json
{
  "code": -1,
  "message": "Failed to retrieve account information"
}
```

### Common Error Codes

| Code | Constant | Description |
|------|----------|-------------|
| 1 | RES_S_OK | Generic success |
| -1 | RES_E_FAIL | Generic fail |
| -2 | RES_E_INVALID_PARAMS | Invalid arguments/parameters |
| -3 | RES_E_NO_MEMORY | No memory condition |
| -4 | RES_E_NOT_FOUND | No history |
| -5 | RES_E_INVALID_VERSION | Invalid version |
| -6 | RES_E_AUTH_FAILED | Authorization failed |
| -7 | RES_E_UNSUPPORTED | Unsupported method |
| -8 | RES_E_AUTO_TRADING_DISABLED | Auto-trading disabled |
| -10000 | RES_E_INTERNAL_FAIL | Internal IPC general error |

For a complete list of error codes, see the [official MT5 Python documentation](https://www.mql5.com/en/docs/python_metatrader5/mt5lasterror_py).

### HTTP Status Codes

- `200`: Successful request
- `400`: Bad request (invalid parameters)
- `500`: Internal server error (MT5 operation failed)

## 📄 API Documentation

Comprehensive API documentation is automatically generated and available at:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

Each endpoint includes:
- Summary and detailed description
- Request/response examples
- Status code documentation
- Error response specifications

## 🔐 Security Notes

- This API should be deployed with appropriate authentication mechanisms in production
- Ensure MetaTrader5 terminal is running in a secure environment
- Use HTTPS in production environments
- Implement rate limiting for production deployments
- Consider implementing API key authentication

## 📈 Performance Considerations

- The API directly communicates with the MetaTrader5 terminal
- Response times depend on MT5 terminal performance and network latency
- For high-frequency data requests, consider implementing caching strategies
- Historical data queries may take time depending on the date range requested

## 🤜 Contributing

Contributions are welcome! Please ensure:
- Code passes type checking with Pyright
- All tests pass
- New features include appropriate tests
- Code follows the existing style and patterns

## 📝 License

MIT License - see LICENSE file for details

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@example.com
- Visit: https://github.com/marahuyo-ph/mt5-rest-api

## 🗺️ Roadmap

Future enhancements:
- [ ] Authentication via basic auth

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MetaTrader5 Documentation](https://www.metatrader5.com/en/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)

---

**MT5-REST-API** - Bridging MetaTrader5 with Modern Web Applications
