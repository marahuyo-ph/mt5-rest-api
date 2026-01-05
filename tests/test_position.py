from fastapi.testclient import TestClient
import MetaTrader5 as mt5  # type: ignore
import pytest


def test_positions_total(client: TestClient):
    """Test positions_total endpoint."""
    # Get data from MT5
    mt5_total = mt5.positions_total()

    # Get data from API
    response = client.get("/positions/total")

    assert response.status_code == 200, "Status code should be 200"
    api_total = response.json()

    # Verify response is an integer
    assert isinstance(api_total, int), "Response should be an integer"

    # Compare with MT5
    assert api_total == mt5_total, f"Expected {mt5_total} positions, got {api_total}"


def test_positions_get_all(client: TestClient):
    """Test positions_get endpoint without filters."""
    # Get data from MT5
    mt5_positions = mt5.positions_get()

    # Get data from API
    response = client.get("/positions/")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # If no positions, should return empty list (MT5 returns empty tuple)
    if mt5_positions is None or len(mt5_positions) == 0:
        # Empty positions should return empty list
        assert isinstance(json_data, list), (
            "Empty response should be a list"
        )
        assert len(json_data) == 0, "Should be empty list"
    else:
        # Verify response structure
        assert isinstance(json_data, list), "Response should be a list"
        assert len(json_data) == len(mt5_positions), (
            f"Expected {len(mt5_positions)} positions, got {len(json_data)}"
        )

        # Verify required fields are present
        required_fields = ["ticket", "symbol", "type", "volume", "price_open"]
        for position in json_data:
            assert isinstance(position, dict), "Each position should be a dictionary"
            for field in required_fields:
                assert field in position, f"Position should contain '{field}' field"


def test_positions_get_by_symbol(client: TestClient):
    """Test positions_get endpoint with symbol filter."""
    symbol = "EURUSD"

    # Get data from MT5
    mt5_positions = mt5.positions_get(symbol=symbol)

    # Get data from API
    response = client.get(f"/positions/?symbol={symbol}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # If no positions, should return empty list
    if mt5_positions is None or len(mt5_positions) == 0:
        assert isinstance(json_data, list), "Empty response should be a list"
        assert len(json_data) == 0, "Should be empty list"
    else:
        # Verify response structure
        assert isinstance(json_data, list), "Response should be a list"
        assert len(json_data) == len(mt5_positions), (
            f"Expected {len(mt5_positions)} positions, got {len(json_data)}"
        )

        # Verify all positions are for the specified symbol
        for position in json_data:
            assert position.get("symbol") == symbol, (
                f"Position should be for symbol {symbol}"
            )


def test_positions_get_by_group(client: TestClient):
    """Test positions_get endpoint with group filter."""
    group = "Forex*"

    # Get data from MT5
    mt5_positions = mt5.positions_get(group=group)

    # Get data from API
    response = client.get(f"/positions/?group={group}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Response should be list or error dict
    assert isinstance(json_data, (list, dict)), "Response should be list or error dict"


def test_positions_get_by_ticket(client: TestClient, request):
    """Test positions_get endpoint with ticket filter."""
    # Use the test open position from the fixture
    if not hasattr(request.config, "_test_order_state"):
        pytest.skip("Test order state not available")

    ticket = request.config._test_order_state.get("open_ticket")

    if not ticket:
        pytest.skip("No test open position available")

    # Get data from API
    response = client.get(f"/positions/?ticket={ticket}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Should return single position or list with one element or error
    if isinstance(json_data, list):
        assert len(json_data) <= 1, "Should return at most one position"
        if len(json_data) == 1:
            assert json_data[0]["ticket"] == ticket, (
                "Returned position ticket should match"
            )
    else:
        assert isinstance(json_data, dict), "Response should be list or dict"


def test_positions_structure(client: TestClient, request):
    """Test that position response has correct structure."""
    # Use the test open position from the fixture
    if not hasattr(request.config, "_test_order_state"):
        pytest.skip("Test order state not available")

    ticket = request.config._test_order_state.get("open_ticket")
    if not ticket:
        pytest.skip("No test open position available")

    # Get MT5 data for comparison
    mt5_position = mt5.positions_get(ticket=ticket)
    if not mt5_position or len(mt5_position) == 0:
        pytest.skip("Position not found in MT5")

    # Get data from API
    response = client.get(f"/positions/?ticket={ticket}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Verify structure matches MT5
    if isinstance(json_data, list) and len(json_data) > 0:
        api_position = json_data[0]
        mt5_pos = mt5_position[0]
        mt5_dict = mt5_pos._asdict()

        # Verify key fields match
        assert api_position["ticket"] == mt5_dict["ticket"], "Position ticket mismatch"
        assert api_position["symbol"] == mt5_dict["symbol"], "Position symbol mismatch"
        assert api_position["type"] == mt5_dict["type"], "Position type mismatch"
        assert api_position["volume"] == mt5_dict["volume"], "Position volume mismatch"
        assert api_position["price_open"] == mt5_dict["price_open"], (
            "Position price_open mismatch"
        )


def test_positions_numeric_fields(client: TestClient, request):
    """Test that numeric fields in positions are proper types."""
    # Use the test open position from the fixture
    if not hasattr(request.config, "_test_order_state"):
        pytest.skip("Test order state not available")

    ticket = request.config._test_order_state.get("open_ticket")
    if not ticket:
        pytest.skip("No test open position available")

    # Get data from API
    response = client.get(f"/positions/?ticket={ticket}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    if isinstance(json_data, list) and len(json_data) > 0:
        # Verify numeric fields are correct types
        numeric_fields = [
            "ticket",
            "type",
            "magic",
            "time_update",
            "time_update_msc",
            "volume",
            "price_open",
            "price_current",
            "swap",
            "profit",
        ]

        for position in json_data:
            for field in numeric_fields:
                if field in position:
                    value = position[field]
                    assert isinstance(value, (int, float)), (
                        f"Field '{field}' should be numeric, got {type(value)}"
                    )


def test_positions_string_fields(client: TestClient, request):
    """Test that string fields in positions are proper types."""
    # Use the test open position from the fixture
    if not hasattr(request.config, "_test_order_state"):
        pytest.skip("Test order state not available")

    ticket = request.config._test_order_state.get("open_ticket")
    if not ticket:
        pytest.skip("No test open position available")

    # Get data from API
    response = client.get(f"/positions/?ticket={ticket}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    if isinstance(json_data, list) and len(json_data) > 0:
        # Verify string fields are correct types
        string_fields = ["symbol", "comment", "external_id"]

        for position in json_data:
            for field in string_fields:
                if field in position:
                    value = position[field]
                    assert isinstance(value, str), (
                        f"Field '{field}' should be string, got {type(value)}"
                    )


def test_positions_buy_sell_types(client: TestClient, request):
    """Test that positions have correct buy/sell type values."""
    # Use the test open position from the fixture
    if not hasattr(request.config, "_test_order_state"):
        pytest.skip("Test order state not available")

    ticket = request.config._test_order_state.get("open_ticket")
    if not ticket:
        pytest.skip("No test open position available")

    # Get data from API
    response = client.get(f"/positions/?ticket={ticket}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    if isinstance(json_data, list) and len(json_data) > 0:
        # Valid position types
        valid_types = [mt5.ORDER_TYPE_BUY, mt5.ORDER_TYPE_SELL]

        for position in json_data:
            position_type = position.get("type")
            assert position_type in valid_types, (
                f"Position type {position_type} is not valid"
            )


def test_positions_profit_calculation(client: TestClient, request):
    """Test that profit values are reasonable."""
    # Use the test open position from the fixture
    if not hasattr(request.config, "_test_order_state"):
        pytest.skip("Test order state not available")

    ticket = request.config._test_order_state.get("open_ticket")
    if not ticket:
        pytest.skip("No test open position available")

    # Get data from API
    response = client.get(f"/positions/?ticket={ticket}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Verify profit values are numeric
    for position in json_data:
        profit = position.get("profit")
        if profit is not None:
            assert isinstance(profit, (int, float)), "Profit should be numeric"


def test_positions_empty_response_handling(client: TestClient):
    """Test handling when no positions exist."""
    # Get all positions to check if any exist
    mt5_total = mt5.positions_total()

    if mt5_total > 0:
        pytest.skip("Positions exist, cannot test empty response")

    # Get data from API
    response = client.get("/positions/")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Should return empty list when no positions
    assert isinstance(json_data, list), "Should return empty list when no positions"
    assert len(json_data) == 0, "Should be empty list"


def test_positions_consistency(client: TestClient):
    """Test that position counts and data are consistent."""
    # Get total count
    response_total = client.get("/positions/total")
    assert response_total.status_code == 200
    total = response_total.json()

    # Get positions list
    response_list = client.get("/positions/")
    assert response_list.status_code == 200
    positions = response_list.json()

    # If positions exist, verify count matches
    if isinstance(positions, list) and len(positions) > 0:
        assert len(positions) == total, (
            f"Position count mismatch: total={total}, list={len(positions)}"
        )
