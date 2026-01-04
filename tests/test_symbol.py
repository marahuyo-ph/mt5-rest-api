from fastapi.testclient import TestClient
import MetaTrader5 as mt5  # type: ignore
import pytest


def test_symbols_total(client: TestClient):
    """Test symbols_total endpoint."""
    # Get data from MT5
    mt5_total = mt5.symbols_total()
    
    # Get data from API
    response = client.get("/symbols/total")
    
    assert response.status_code == 200, "Status code should be 200"
    api_total = response.json()
    
    # Verify response is an integer
    assert isinstance(api_total, int), "Response should be an integer"
    
    # Compare with MT5
    assert api_total == mt5_total, f"Expected {mt5_total} symbols, got {api_total}"


def test_symbols_get_all(client: TestClient):
    """Test symbols_get endpoint without group filter."""
    # Get data from MT5
    mt5_symbols = mt5.symbols_get()
    
    # Skip test if MT5 data is not available
    if not mt5_symbols:
        pytest.skip("MT5 symbols not available")
    
    # Get data from API
    response = client.get("/symbols/")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) == len(mt5_symbols), f"Expected {len(mt5_symbols)} symbols, got {len(json_data)}"
    
    # Verify each symbol has required structure
    for i, api_symbol in enumerate(json_data):
        assert isinstance(api_symbol, dict), "Each symbol should be a dictionary"
        assert "name" in api_symbol, "Symbol should have 'name' field"
        assert "info" in api_symbol, "Symbol should have 'info' field"
        
        # Verify the name matches MT5
        mt5_symbol = mt5_symbols[i]
        assert api_symbol["name"] == mt5_symbol._asdict()["name"], f"Symbol {i}: name mismatch"


def test_symbols_get_with_group(client: TestClient):
    """Test symbols_get endpoint with group filter."""
    # Get data from MT5 with group filter
    group = "Forex"
    mt5_symbols = mt5.symbols_get(group)
    
    # Skip test if MT5 data is not available
    if not mt5_symbols:
        pytest.skip(f"MT5 symbols in group '{group}' not available")
    
    # Get data from API
    response = client.get(f"/symbols/?group={group}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) == len(mt5_symbols), f"Expected {len(mt5_symbols)} symbols in group '{group}', got {len(json_data)}"
    
    # Verify each symbol has required structure
    for i, api_symbol in enumerate(json_data):
        assert isinstance(api_symbol, dict), "Each symbol should be a dictionary"
        assert "name" in api_symbol, "Symbol should have 'name' field"
        assert "info" in api_symbol, "Symbol should have 'info' field"


def test_symbol_info_valid(client: TestClient):
    """Test symbol_info endpoint with valid symbol."""
    symbol = "EURUSD"
    
    # Get data from MT5
    mt5_symbol = mt5.symbol_info(symbol)
    
    # Skip test if MT5 data is not available
    if not mt5_symbol:
        pytest.skip(f"MT5 symbol '{symbol}' not available")
    
    # Get data from API
    response = client.get(f"/symbols/{symbol}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, dict), "Response should be a dictionary"
    
    # Verify key fields match MT5
    mt5_dict = mt5_symbol._asdict()
    assert json_data["name"] == mt5_dict["name"], "Symbol name mismatch"
    assert json_data["bid"] == mt5_dict["bid"], "Symbol bid mismatch"
    assert json_data["ask"] == mt5_dict["ask"], "Symbol ask mismatch"


def test_symbol_info_invalid(client: TestClient):
    """Test symbol_info endpoint with invalid symbol."""
    symbol = "INVALIDSYMBOL"
    
    # Get data from API
    response = client.get(f"/symbols/{symbol}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Should return error response
    assert isinstance(json_data, dict), "Response should be a dictionary"


def test_symbol_info_tick_valid(client: TestClient):
    """Test symbol_info_tick endpoint with valid symbol."""
    symbol = "EURUSD"
    
    # Get data from MT5
    mt5_tick = mt5.symbol_info_tick(symbol)
    
    # Skip test if MT5 data is not available
    if not mt5_tick:
        pytest.skip(f"MT5 tick for '{symbol}' not available")
    
    # Get data from API
    response = client.get(f"/symbols/{symbol}/last-tick")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, dict), "Response should be a dictionary"
    
    # Verify required fields are present
    required_fields = ["time", "bid", "ask", "last", "volume", "time_msc", "flags", "volume_real"]
    for field in required_fields:
        assert field in json_data, f"Tick should contain '{field}' field"
    
    # Verify key fields match MT5
    mt5_dict = mt5_tick._asdict()
    assert json_data["bid"] == mt5_dict["bid"], "Tick bid price mismatch"
    assert json_data["ask"] == mt5_dict["ask"], "Tick ask price mismatch"
    assert json_data["last"] == mt5_dict["last"], "Tick last price mismatch"


def test_symbol_info_tick_invalid(client: TestClient):
    """Test symbol_info_tick endpoint with invalid symbol."""
    symbol = "INVALIDSYMBOL"
    
    # Get data from API
    response = client.get(f"/symbols/{symbol}/last-tick")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Should return error response
    assert isinstance(json_data, dict), "Response should be a dictionary"


def test_symbol_select_enable(client: TestClient):
    """Test symbol_select endpoint to enable a symbol."""
    symbol = "EURUSD"
    
    # Enable symbol
    response = client.put(f"/symbols/{symbol}/enable?enable=true")
    
    assert response.status_code == 200, "Status code should be 200"
    result = response.json()
    
    # Result should be boolean
    assert isinstance(result, bool), "Response should be a boolean"


def test_symbol_select_disable(client: TestClient):
    """Test symbol_select endpoint to disable a symbol."""
    symbol = "EURUSD"
    
    # Disable symbol
    response = client.put(f"/symbols/{symbol}/enable?enable=false")
    
    assert response.status_code == 200, "Status code should be 200"
    result = response.json()
    
    # Result should be boolean
    assert isinstance(result, bool), "Response should be a boolean"


def test_symbol_select_default(client: TestClient):
    """Test symbol_select endpoint without enable parameter."""
    symbol = "EURUSD"
    
    # Call without enable parameter (should toggle or use default)
    response = client.put(f"/symbols/{symbol}/enable")
    
    assert response.status_code == 200, "Status code should be 200"
    result = response.json()
    
    # Result should be boolean
    assert isinstance(result, bool), "Response should be a boolean"


def test_multiple_symbols_info(client: TestClient):
    """Test querying multiple symbols."""
    symbols = ["EURUSD", "GBPUSD", "USDJPY"]
    
    for symbol in symbols:
        # Skip if symbol not available
        if not mt5.symbol_info(symbol):
            continue
        
        response = client.get(f"/symbols/{symbol}")
        assert response.status_code == 200, f"Failed to get info for {symbol}"
        
        json_data = response.json()
        assert isinstance(json_data, dict), f"Response for {symbol} should be a dictionary"
        assert "name" in json_data, f"Response for {symbol} should have 'name' field"
