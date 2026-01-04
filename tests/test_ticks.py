from fastapi.testclient import TestClient
import MetaTrader5 as mt5  # type: ignore
from datetime import datetime, timedelta
import pandas as pd  # type: ignore
import pytest


def test_ticks_from_valid(client: TestClient):
    """Test copy_ticks_from endpoint with valid parameters."""
    # Get data from MT5 directly
    now = datetime.now()
    count = 100
    flags = mt5.COPY_TICKS_ALL
    
    mt5_ticks = mt5.copy_ticks_from("EURUSD", now, count, flags)
    
    # Skip test if MT5 data is not available
    if mt5_ticks is None:
        pytest.skip("MT5 data not available")
    
    # Get data from API
    response = client.get(f"/ticks/from/EURUSD/{now.isoformat()}/{count}?flags={flags}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) == len(mt5_ticks), f"Expected {len(mt5_ticks)} ticks, got {len(json_data)}"
    
    # Convert MT5 ticks to DataFrame for comparison
    df_mt5 = pd.DataFrame(mt5_ticks)
    
    # Verify each tick has required fields
    required_fields = ["time", "bid", "ask", "last", "volume", "time_msc", "flags", "volume_real"]
    for tick in json_data:
        assert isinstance(tick, dict), "Each tick should be a dictionary"
        for field in required_fields:
            assert field in tick, f"Tick should contain '{field}' field"
    
    # Verify data matches MT5
    for i, api_tick in enumerate(json_data):
        mt5_tick = df_mt5.iloc[i]
        assert api_tick["time"] == int(mt5_tick["time"]), f"Tick {i}: time mismatch"
        assert api_tick["bid"] == mt5_tick["bid"], f"Tick {i}: bid price mismatch"
        assert api_tick["ask"] == mt5_tick["ask"], f"Tick {i}: ask price mismatch"
        assert api_tick["last"] == mt5_tick["last"], f"Tick {i}: last price mismatch"
        assert api_tick["volume"] == int(mt5_tick["volume"]), f"Tick {i}: volume mismatch"
        assert api_tick["time_msc"] == int(mt5_tick["time_msc"]), f"Tick {i}: time_msc mismatch"
        assert api_tick["flags"] == int(mt5_tick["flags"]), f"Tick {i}: flags mismatch"
        assert api_tick["volume_real"] == mt5_tick["volume_real"], f"Tick {i}: volume_real mismatch"


def test_ticks_from_bid_flag(client: TestClient):
    """Test copy_ticks_from endpoint with BID flag."""
    now = datetime.now()
    count = 50
    flags = mt5.TICK_FLAG_BID
    
    # Get data from MT5 directly
    mt5_ticks = mt5.copy_ticks_from("EURUSD", now, count, flags)
    
    # Skip test if MT5 data is not available
    if mt5_ticks is None:
        pytest.skip("MT5 data not available")
    
    # Get data from API
    response = client.get(f"/ticks/from/EURUSD/{now.isoformat()}/{count}?flags={flags}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) == len(mt5_ticks), f"Expected {len(mt5_ticks)} ticks, got {len(json_data)}"
    
    # Verify data matches MT5
    df_mt5 = pd.DataFrame(mt5_ticks)
    for i, api_tick in enumerate(json_data):
        mt5_tick = df_mt5.iloc[i]
        assert api_tick["bid"] == mt5_tick["bid"], f"Tick {i}: bid price mismatch"
        assert api_tick["flags"] == int(mt5_tick["flags"]), f"Tick {i}: flags mismatch"


def test_ticks_from_ask_flag(client: TestClient):
    """Test copy_ticks_from endpoint with ASK flag."""
    now = datetime.now()
    count = 50
    flags = mt5.TICK_FLAG_ASK
    
    # Get data from MT5 directly
    mt5_ticks = mt5.copy_ticks_from("EURUSD", now, count, flags)
    
    # Skip test if MT5 data is not available
    if mt5_ticks is None:
        pytest.skip("MT5 data not available")
    
    # Get data from API
    response = client.get(f"/ticks/from/EURUSD/{now.isoformat()}/{count}?flags={flags}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) == len(mt5_ticks), f"Expected {len(mt5_ticks)} ticks, got {len(json_data)}"
    
    # Verify data matches MT5
    df_mt5 = pd.DataFrame(mt5_ticks)
    for i, api_tick in enumerate(json_data):
        mt5_tick = df_mt5.iloc[i]
        assert api_tick["ask"] == mt5_tick["ask"], f"Tick {i}: ask price mismatch"
        assert api_tick["flags"] == int(mt5_tick["flags"]), f"Tick {i}: flags mismatch"


def test_ticks_range_valid(client: TestClient):
    """Test copy_ticks_range endpoint with valid date range."""
    # Set up date range (last 30 minutes)
    date_to = datetime.now()
    date_from = date_to - timedelta(minutes=30)
    flags = mt5.COPY_TICKS_ALL
    
    # Get data from MT5 directly
    mt5_ticks = mt5.copy_ticks_range("EURUSD", date_from, date_to, flags)
    
    # Skip test if MT5 data is not available
    if mt5_ticks is None:
        pytest.skip("MT5 data not available")
    
    # Get data from API
    response = client.get(
        f"/ticks/range/EURUSD/{date_from.isoformat()}/{date_to.isoformat()}?flags={flags}"
    )
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) == len(mt5_ticks), f"Expected {len(mt5_ticks)} ticks, got {len(json_data)}"
    
    # Convert MT5 ticks to DataFrame for comparison
    df_mt5 = pd.DataFrame(mt5_ticks)
    
    # Verify all required fields are present
    required_fields = ["time", "bid", "ask", "last", "volume", "time_msc", "flags", "volume_real"]
    for tick in json_data:
        for field in required_fields:
            assert field in tick, f"Tick should contain '{field}' field"
    
    # Verify data matches MT5
    for i, api_tick in enumerate(json_data):
        mt5_tick = df_mt5.iloc[i]
        assert api_tick["time"] == int(mt5_tick["time"]), f"Tick {i}: time mismatch"
        assert api_tick["bid"] == mt5_tick["bid"], f"Tick {i}: bid price mismatch"
        assert api_tick["ask"] == mt5_tick["ask"], f"Tick {i}: ask price mismatch"
        assert api_tick["last"] == mt5_tick["last"], f"Tick {i}: last price mismatch"
        assert api_tick["volume"] == int(mt5_tick["volume"]), f"Tick {i}: volume mismatch"
        assert api_tick["time_msc"] == int(mt5_tick["time_msc"]), f"Tick {i}: time_msc mismatch"
        assert api_tick["flags"] == int(mt5_tick["flags"]), f"Tick {i}: flags mismatch"
        assert api_tick["volume_real"] == mt5_tick["volume_real"], f"Tick {i}: volume_real mismatch"


def test_ticks_range_bid_flag(client: TestClient):
    """Test copy_ticks_range endpoint with BID flag."""
    # Set up date range (last 30 minutes)
    date_to = datetime.now()
    date_from = date_to - timedelta(minutes=30)
    flags = mt5.TICK_FLAG_BID
    
    # Get data from MT5 directly
    mt5_ticks = mt5.copy_ticks_range("EURUSD", date_from, date_to, flags)
    
    # Skip test if MT5 data is not available
    if mt5_ticks is None:
        pytest.skip("MT5 data not available")
    
    # Get data from API
    response = client.get(
        f"/ticks/range/EURUSD/{date_from.isoformat()}/{date_to.isoformat()}?flags={flags}"
    )
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response structure
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) == len(mt5_ticks), f"Expected {len(mt5_ticks)} ticks, got {len(json_data)}"
    
    # Verify data matches MT5
    df_mt5 = pd.DataFrame(mt5_ticks)
    for i, api_tick in enumerate(json_data):
        mt5_tick = df_mt5.iloc[i]
        assert api_tick["bid"] == mt5_tick["bid"], f"Tick {i}: bid price mismatch"
        assert api_tick["flags"] == int(mt5_tick["flags"]), f"Tick {i}: flags mismatch"


def test_ticks_from_invalid_symbol(client: TestClient):
    """Test copy_ticks_from endpoint with invalid symbol."""
    now = datetime.now()
    flags = mt5.COPY_TICKS_ALL
    response = client.get(f"/ticks/from/INVALIDSYMBOL/{now.isoformat()}/100?flags={flags}")
    
    # Should return error response
    assert response.status_code == 200  # API returns 200 with error details
    json_data = response.json()
    # Error response should have error fields
    assert isinstance(json_data, dict), "Error response should be a dictionary"


def test_ticks_from_zero_count(client: TestClient):
    """Test copy_ticks_from endpoint with zero count."""
    now = datetime.now()
    flags = mt5.COPY_TICKS_ALL
    response = client.get(f"/ticks/from/EURUSD/{now.isoformat()}/0?flags={flags}")
    
    assert response.status_code == 200
    json_data = response.json()
    # MT5 should return empty list or error
    assert isinstance(json_data, (list, dict))


def test_ticks_range_inverted_dates(client: TestClient):
    """Test copy_ticks_range endpoint with inverted date range."""
    # Set dates in reverse order (should fail or return empty)
    date_from = datetime.now()
    date_to = date_from - timedelta(minutes=30)
    flags = mt5.COPY_TICKS_ALL
    
    response = client.get(
        f"/ticks/range/EURUSD/{date_from.isoformat()}/{date_to.isoformat()}?flags={flags}"
    )
    
    assert response.status_code == 200
    json_data = response.json()
    # Should return error or empty list
    assert isinstance(json_data, (list, dict))
