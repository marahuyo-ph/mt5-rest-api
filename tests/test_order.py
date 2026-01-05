from fastapi.testclient import TestClient
import MetaTrader5 as mt5  # type: ignore
import pytest


def test_orders_total(client: TestClient):
    """Test orders_total endpoint."""
    # Get data from MT5
    mt5_total = mt5.orders_total()

    # Get data from API
    response = client.get("/orders/total")

    assert response.status_code == 200, "Status code should be 200"
    api_total = response.json()

    # Verify response is an integer
    assert isinstance(api_total, int), "Response should be an integer"

    # Compare with MT5
    assert api_total == mt5_total, f"Expected {mt5_total} orders, got {api_total}"


def test_orders_get_all(client: TestClient):
    """Test orders_get endpoint without filters."""
    # Get data from MT5
    mt5_orders = mt5.orders_get()

    # Get data from API
    response = client.get("/orders/")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # If no orders, should return list
    if mt5_orders is None:
        assert isinstance(json_data, (list, dict)), (
            "Response should be list or error dict"
        )
    else:
        # Verify response structure
        assert isinstance(json_data, list), "Response should be a list"
        assert len(json_data) == len(mt5_orders), (
            f"Expected {len(mt5_orders)} orders, got {len(json_data)}"
        )

        # Verify required fields are present
        required_fields = ["ticket", "time_setup", "type", "state"]
        for order in json_data:
            assert isinstance(order, dict), "Each order should be a dictionary"
            for field in required_fields:
                assert field in order, f"Order should contain '{field}' field"


def test_orders_get_by_symbol(client: TestClient):
    """Test orders_get endpoint with symbol filter."""
    symbol = "EURUSD"

    # Get data from MT5
    mt5_orders = mt5.orders_get(symbol=symbol)

    # Get data from API
    response = client.get(f"/orders/?symbol={symbol}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # If no orders, should return list
    if mt5_orders is None:
        assert isinstance(json_data, (list, dict)), (
            "Response should be list or error dict"
        )
    else:
        # Verify response structure
        assert isinstance(json_data, list), "Response should be a list"
        assert len(json_data) == len(mt5_orders), (
            f"Expected {len(mt5_orders)} orders for {symbol}, got {len(json_data)}"
        )

        # Verify all orders are for the specified symbol
        for order in json_data:
            assert order.get("symbol") == symbol or order.get("symbol") is None, (
                f"Order should be for symbol {symbol}"
            )


def test_orders_get_by_group(client: TestClient):
    """Test orders_get endpoint with group filter."""
    group = "Forex*"

    # Get data from MT5
    mt5_orders = mt5.orders_get(group=group)

    # Get data from API
    response = client.get(f"/orders/?group={group}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Response should be list or error dict
    assert isinstance(json_data, (list, dict)), "Response should be list or error dict"


def test_orders_get_by_ticket(client: TestClient, request):
    """Test orders_get endpoint with ticket filter."""
    # Use the test open position from the fixture
    if not hasattr(request.config, "_test_order_state"):
        pytest.skip("Test order state not available")

    ticket = request.config._test_order_state.get("open_ticket")

    if not ticket:
        pytest.skip("No test open position available")

    # Get data from API
    response = client.get(f"/orders/?ticket={ticket}")

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Should return single order or list with one element
    if isinstance(json_data, list):
        assert len(json_data) <= 1, "Should return at most one order"
        if len(json_data) == 1:
            assert json_data[0]["ticket"] == ticket, (
                "Returned order ticket should match"
            )
    else:
        assert isinstance(json_data, dict), "Response should be list or dict"


def test_orders_calc_margin_valid(client: TestClient):
    """Test orders_calc_margin endpoint with valid parameters."""
    payload = {
        "action": mt5.ORDER_TYPE_BUY,
        "symbol": "EURUSD",
        "volume": 1.0,
        "price": 1.1000,
    }

    # Get data from MT5
    mt5_margin = mt5.order_calc_margin(
        payload["action"], payload["symbol"], payload["volume"], payload["price"]
    )

    # Skip test if MT5 margin calculation not available
    if mt5_margin is None:
        pytest.skip("MT5 margin calculation not available")

    # Get data from API
    response = client.post("/orders/calculate-margin", json=payload)

    assert response.status_code == 200, "Status code should be 200"
    api_margin = response.json()

    # Verify response is numeric
    assert isinstance(api_margin, (int, float)), "Response should be numeric"

    # Compare with MT5 (allowing for small floating point differences)
    assert abs(api_margin - mt5_margin) < 0.01, (
        f"Expected {mt5_margin}, got {api_margin}"
    )


def test_orders_calc_margin_invalid_symbol(client: TestClient):
    """Test orders_calc_margin endpoint with invalid symbol."""
    payload = {
        "action": mt5.ORDER_TYPE_BUY,
        "symbol": "INVALIDSYMBOL",
        "volume": 1.0,
        "price": 1.0,
    }

    # Get data from API
    response = client.post("/orders/calculate-margin", json=payload)

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Should return error or None
    assert isinstance(json_data, dict), "Error response should be a dictionary"


def test_orders_calc_profit_valid(client: TestClient):
    """Test orders_calc_profit endpoint with valid parameters."""
    payload = {
        "action": mt5.ORDER_TYPE_BUY,
        "symbol": "EURUSD",
        "volume": 1.0,
        "price_open": 1.1000,
        "price_close": 1.1100,
    }

    # Get data from MT5
    mt5_profit = mt5.order_calc_profit(
        payload["action"],
        payload["symbol"],
        payload["volume"],
        payload["price_open"],
        payload["price_close"],
    )

    # Skip test if MT5 profit calculation not available
    if mt5_profit is None:
        pytest.skip("MT5 profit calculation not available")

    # Get data from API
    response = client.post("/orders/calculate-profit", json=payload)

    assert response.status_code == 200, "Status code should be 200"
    api_profit = response.json()

    # Verify response is numeric
    assert isinstance(api_profit, (int, float)), "Response should be numeric"

    # Compare with MT5 (allowing for small floating point differences)
    assert abs(api_profit - mt5_profit) < 0.01, (
        f"Expected {mt5_profit}, got {api_profit}"
    )


def test_orders_calc_profit_invalid_symbol(client: TestClient):
    """Test orders_calc_profit endpoint with invalid symbol."""
    payload = {
        "action": mt5.ORDER_TYPE_BUY,
        "symbol": "INVALIDSYMBOL",
        "volume": 1.0,
        "price_open": 1.0,
        "price_close": 1.1,
    }

    # Get data from API
    response = client.post("/orders/calculate-profit", json=payload)

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Should return error or None
    assert isinstance(json_data, dict), "Error response should be a dictionary"


def test_orders_check_structure(client: TestClient):
    """Test orders_check endpoint structure."""
    payload = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": "EURUSD",
        "volume": 0.1,
        "type": mt5.ORDER_TYPE_BUY,
        "price": 1.1000,
        "magic": 123456,
        "order": 0,
        "stoplimit": 0.0,
        "sl": 0.0,
        "tp": 0.0,
        "deviation": 10,
        "type_filling": mt5.ORDER_FILLING_RETURN,
        "type_time": mt5.ORDER_TIME_GTC,
        "expiration": 0,
        "comment": "Test order",
        "position": 0,
        "position_by": 0,
    }

    # Get data from API
    response = client.post("/orders/check", json=payload)

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Response should be dictionary (either check result or error)
    assert isinstance(json_data, dict), "Response should be a dictionary"


def test_orders_send_structure(client: TestClient):
    """Test orders_send endpoint structure (without actually sending)."""
    # Note: This test validates the endpoint structure but doesn't verify order placement
    # since actual order sending requires proper trading conditions and capital

    payload = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": "EURUSD",
        "volume": 0.01,
        "type": mt5.ORDER_TYPE_BUY,
        "price": 1.1000,
        "magic": 0,
        "order": 0,
        "stoplimit": 0.0,
        "sl": 0.0,
        "tp": 0.0,
        "deviation": 10,
        "type_filling": mt5.ORDER_FILLING_RETURN,
        "type_time": mt5.ORDER_TIME_GTC,
        "expiration": 0,
        "comment": "Test order",
        "position": 0,
        "position_by": 0,
    }

    # Get data from API
    response = client.post("/orders/send", json=payload)

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Response should be dictionary (trade result or error)
    assert isinstance(json_data, dict), "Response should be a dictionary"


def test_orders_calc_margin_zero_volume(client: TestClient):
    """Test orders_calc_margin with zero volume."""
    payload = {
        "action": mt5.ORDER_TYPE_BUY,
        "symbol": "EURUSD",
        "volume": 0.0,
        "price": 1.1000,
    }

    # Get data from API
    response = client.post("/orders/calculate-margin", json=payload)

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Should handle zero volume gracefully
    assert isinstance(json_data, (int, float, dict)), (
        "Response should be numeric or error dict"
    )


def test_orders_calc_profit_zero_volume(client: TestClient):
    """Test orders_calc_profit with zero volume."""
    payload = {
        "action": mt5.ORDER_TYPE_BUY,
        "symbol": "EURUSD",
        "volume": 0.0,
        "price_open": 1.1000,
        "price_close": 1.1100,
    }

    # Get data from API
    response = client.post("/orders/calculate-profit", json=payload)

    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()

    # Should handle zero volume gracefully (likely returns 0 profit)
    assert isinstance(json_data, (int, float, dict)), (
        "Response should be numeric or error dict"
    )


def test_orders_different_order_types(client: TestClient):
    """Test margin calculation with different order types."""
    order_types = [mt5.ORDER_TYPE_BUY, mt5.ORDER_TYPE_SELL]

    for order_type in order_types:
        payload = {
            "action": order_type,
            "symbol": "EURUSD",
            "volume": 1.0,
            "price": 1.1000,
        }

        # Get data from API
        response = client.post("/orders/calculate-margin", json=payload)

        assert response.status_code == 200, (
            f"Status code should be 200 for order type {order_type}"
        )
        json_data = response.json()

        # Should return numeric value or error dict
        assert isinstance(json_data, (int, float, dict)), (
            f"Response should be numeric or error dict for order type {order_type}"
        )
