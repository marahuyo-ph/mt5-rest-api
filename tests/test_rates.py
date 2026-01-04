from fastapi.testclient import TestClient
import MetaTrader5 as mt5  # type: ignore
from datetime import datetime, timedelta
import pandas as pd  # type: ignore
import pytest


def test_rates_from_valid(client: TestClient):
    """Test copy_rates_from endpoint with valid parameters."""
    # Get data from MT5 directly
    now = datetime.now()
    count = 20
    mt5_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_D1, now, count)
    
    # Skip test if MT5 data is not available
    if mt5_rates is None:
        pytest.skip("MT5 data not available")
    
    # Get data from API
    response = client.get(f"/rates/from/EURUSD/{mt5.TIMEFRAME_D1}/{now.isoformat()}/{count}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) == count, f"Expected {count} rates, got {len(json_data)}"
    
    # Convert MT5 rates to DataFrame for comparison
    df_mt5 = pd.DataFrame(mt5_rates)
    
    # Verify each rate has required fields
    required_fields = ["time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume"]
    for rate in json_data:
        assert isinstance(rate, dict), "Each rate should be a dictionary"
        for field in required_fields:
            assert field in rate, f"Rate should contain '{field}' field"
    
    # Verify data matches MT5
    for i, api_rate in enumerate(json_data):
        mt5_rate = df_mt5.iloc[i]
        assert api_rate["time"] == int(mt5_rate["time"]), f"Rate {i}: time mismatch"
        assert api_rate["open"] == mt5_rate["open"], f"Rate {i}: open price mismatch"
        assert api_rate["high"] == mt5_rate["high"], f"Rate {i}: high price mismatch"
        assert api_rate["low"] == mt5_rate["low"], f"Rate {i}: low price mismatch"
        assert api_rate["close"] == mt5_rate["close"], f"Rate {i}: close price mismatch"
        assert api_rate["tick_volume"] == int(mt5_rate["tick_volume"]), f"Rate {i}: tick_volume mismatch"
        assert api_rate["spread"] == int(mt5_rate["spread"]), f"Rate {i}: spread mismatch"
        assert api_rate["real_volume"] == int(mt5_rate["real_volume"]), f"Rate {i}: real_volume mismatch"


def test_rates_from_pos_valid(client: TestClient):
    """Test copy_rates_from_pos endpoint with valid parameters."""
    count = 10
    start_pos = 0
    
    # Get data from MT5 directly
    mt5_rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_D1, start_pos, count)
    
    # Skip test if MT5 data is not available
    if mt5_rates is None:
        pytest.skip("MT5 data not available")
    
    # Get data from API
    response = client.get(f"/rates/from-pos/EURUSD/{mt5.TIMEFRAME_D1}/{start_pos}/{count}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) == count, f"Expected {count} rates, got {len(json_data)}"
    
    # Convert MT5 rates to DataFrame for comparison
    df_mt5 = pd.DataFrame(mt5_rates)
    
    # Verify data matches MT5
    for i, api_rate in enumerate(json_data):
        mt5_rate = df_mt5.iloc[i]
        assert api_rate["time"] == int(mt5_rate["time"]), f"Rate {i}: time mismatch"
        assert api_rate["open"] == mt5_rate["open"], f"Rate {i}: open price mismatch"
        assert api_rate["high"] == mt5_rate["high"], f"Rate {i}: high price mismatch"
        assert api_rate["low"] == mt5_rate["low"], f"Rate {i}: low price mismatch"
        assert api_rate["close"] == mt5_rate["close"], f"Rate {i}: close price mismatch"
        assert api_rate["tick_volume"] == int(mt5_rate["tick_volume"]), f"Rate {i}: tick_volume mismatch"
        assert api_rate["spread"] == int(mt5_rate["spread"]), f"Rate {i}: spread mismatch"
        assert api_rate["real_volume"] == int(mt5_rate["real_volume"]), f"Rate {i}: real_volume mismatch"


def test_rates_range_valid(client: TestClient):
    """Test copy_rates_range endpoint with valid date range."""
    # Set up date range (last 30 days)
    date_to = datetime.now()
    date_from = date_to - timedelta(days=30)
    
    # Get data from MT5 directly
    mt5_rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_D1, date_from, date_to)
    
    # Skip test if MT5 data is not available
    if mt5_rates is None:
        pytest.skip("MT5 data not available")
    
    # Get data from API
    response = client.get(
        f"/rates/range/EURUSD/{mt5.TIMEFRAME_D1}/{date_from.isoformat()}/{date_to.isoformat()}"
    )
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) == len(mt5_rates), f"Expected {len(mt5_rates)} rates, got {len(json_data)}"
    
    # Convert MT5 rates to DataFrame for comparison
    df_mt5 = pd.DataFrame(mt5_rates)
    
    # Verify data matches MT5
    for i, api_rate in enumerate(json_data):
        mt5_rate = df_mt5.iloc[i]
        assert api_rate["time"] == int(mt5_rate["time"]), f"Rate {i}: time mismatch"
        assert api_rate["open"] == mt5_rate["open"], f"Rate {i}: open price mismatch"
        assert api_rate["high"] == mt5_rate["high"], f"Rate {i}: high price mismatch"
        assert api_rate["low"] == mt5_rate["low"], f"Rate {i}: low price mismatch"
        assert api_rate["close"] == mt5_rate["close"], f"Rate {i}: close price mismatch"
        assert api_rate["tick_volume"] == int(mt5_rate["tick_volume"]), f"Rate {i}: tick_volume mismatch"
        assert api_rate["spread"] == int(mt5_rate["spread"]), f"Rate {i}: spread mismatch"
        assert api_rate["real_volume"] == int(mt5_rate["real_volume"]), f"Rate {i}: real_volume mismatch"


def test_rates_from_invalid_symbol(client: TestClient):
    """Test copy_rates_from endpoint with invalid symbol."""
    now = datetime.now()
    response = client.get(f"/rates/from/INVALIDSYMBOL/{mt5.TIMEFRAME_D1}/{now.isoformat()}/20")
    
    # Should return error response
    assert response.status_code == 200  # API returns 200 with error details
    json_data = response.json()
    # Error response should have error fields
    assert isinstance(json_data, dict), "Error response should be a dictionary"


def test_rates_from_zero_count(client: TestClient):
    """Test copy_rates_from endpoint with zero count."""
    now = datetime.now()
    response = client.get(f"/rates/from/EURUSD/{mt5.TIMEFRAME_D1}/{now.isoformat()}/0")
    
    assert response.status_code == 200
    json_data = response.json()
    # MT5 should return empty list or error
    assert isinstance(json_data, (list, dict))