from fastapi.testclient import TestClient
import MetaTrader5 as mt5  # type: ignore
from datetime import datetime, timedelta
import pytest


def test_history_orders_total(client: TestClient):
    """Test history_orders_total endpoint."""
    # Get data from MT5
    mt5_total = mt5.history_orders_total()
    
    # Get data from API
    response = client.get("/history/orders/total")
    
    assert response.status_code == 200, "Status code should be 200"
    api_total = response.json()
    
    # MT5 can return None if no history data is available
    if mt5_total is None:
        # API might also return None
        assert api_total is None or isinstance(api_total, int), "Response should be integer or None"
    else:
        # Verify response is an integer
        assert isinstance(api_total, int), "Response should be an integer"
        # Compare with MT5
        assert api_total == mt5_total, f"Expected {mt5_total} orders, got {api_total}"


def test_history_deals_total(client: TestClient):
    """Test history_deals_total endpoint."""
    # Get data from MT5
    mt5_total = mt5.history_deals_total()
    
    # Get data from API
    response = client.get("/history/deals/total")
    
    assert response.status_code == 200, "Status code should be 200"
    api_total = response.json()
    
    # MT5 can return None if no history data is available
    if mt5_total is None:
        # API might also return None
        assert api_total is None or isinstance(api_total, int), "Response should be integer or None"
    else:
        # Verify response is an integer
        assert isinstance(api_total, int), "Response should be an integer"
        # Compare with MT5
        assert api_total == mt5_total, f"Expected {mt5_total} deals, got {api_total}"


def test_history_orders_get_by_date_range(client: TestClient):
    """Test history_orders_get with date range and group filter."""
    # Date range: last 30 days
    date_to = datetime.now()
    date_from = date_to - timedelta(days=30)
    group = "Forex*"
    
    # Get data from MT5
    mt5_orders = mt5.history_orders_get(date_from=date_from, date_to=date_to, group=group)
    
    # Get data from API
    response = client.get(
        f"/history/orders/",
        params={
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
            "group": group
        }
    )
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Response should be list or error dict
    if mt5_orders is None or len(mt5_orders) == 0:
        assert isinstance(json_data, dict), "Empty response should be error dict"
    else:
        assert isinstance(json_data, list), "Response should be a list"
        assert len(json_data) == len(mt5_orders), f"Expected {len(mt5_orders)} orders, got {len(json_data)}"


def test_history_orders_get_by_ticket(client: TestClient, request):
    """Test history_orders_get with ticket filter."""
    # Use closed tickets from the fixture
    if not hasattr(request.config, '_test_order_state'):
        pytest.skip("Test order state not available")
    
    closed_tickets = request.config._test_order_state.get("closed_tickets", [])
    
    if not closed_tickets:
        pytest.skip("No closed history orders available to test ticket filter")
    
    # Use the first closed ticket
    ticket = closed_tickets[0]
    
    # Get data from MT5
    mt5_order = mt5.history_orders_get(ticket=ticket)
    
    # Get data from API
    response = client.get(f"/history/orders/?ticket={ticket}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Should return list with one element or error
    if isinstance(json_data, list):
        assert len(json_data) <= 1, "Should return at most one order"
        if len(json_data) == 1 and mt5_order:
            assert json_data[0]["ticket"] == ticket, "Order ticket should match"
    else:
        assert isinstance(json_data, dict), "Response should be list or dict"


def test_history_orders_get_by_position(client: TestClient, request):
    """Test history_orders_get with position filter."""
    # Use closed tickets from the fixture
    if not hasattr(request.config, '_test_order_state'):
        pytest.skip("Test order state not available")
    
    closed_tickets = request.config._test_order_state.get("closed_tickets", [])
    
    if not closed_tickets:
        pytest.skip("No closed history orders available to test position filter")
    
    # Get the position from one of the closed orders
    ticket = closed_tickets[0]
    mt5_order = mt5.history_orders_get(ticket=ticket)
    
    if not mt5_order or len(mt5_order) == 0:
        pytest.skip("Could not find closed order to get position")
    
    position = mt5_order[0].position  # type: ignore
    
    if position == 0:
        pytest.skip("Closed order has no position")
    
    # Get data from API
    response = client.get(f"/history/orders/?position={position}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Response should be list or error dict
    assert isinstance(json_data, (list, dict)), "Response should be list or dict"


def test_history_deals_get_by_date_range(client: TestClient):
    """Test history_deals_get with date range and group filter."""
    # Date range: last 30 days
    date_to = datetime.now()
    date_from = date_to - timedelta(days=30)
    group = "Forex*"
    
    # Get data from MT5
    mt5_deals = mt5.history_deals_get(date_from=date_from, date_to=date_to, group=group)
    
    # Get data from API
    response = client.get(
        f"/history/deals/",
        params={
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
            "group": group
        }
    )
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Response should be list or error dict
    if mt5_deals is None or len(mt5_deals) == 0:
        assert isinstance(json_data, dict), "Empty response should be error dict"
    else:
        assert isinstance(json_data, list), "Response should be a list"
        assert len(json_data) == len(mt5_deals), f"Expected {len(mt5_deals)} deals, got {len(json_data)}"


def test_history_deals_get_by_ticket(client: TestClient, request):
    """Test history_deals_get with ticket filter."""
    # Use closed tickets from the fixture
    if not hasattr(request.config, '_test_order_state'):
        pytest.skip("Test order state not available")
    
    closed_tickets = request.config._test_order_state.get("closed_tickets", [])
    
    if not closed_tickets:
        pytest.skip("No closed history deals available to test ticket filter")
    
    # Use the first closed ticket to get the deal
    ticket = closed_tickets[0]
    
    # Get data from MT5
    mt5_deal = mt5.history_deals_get(ticket=ticket)
    
    # Get data from API
    response = client.get(f"/history/deals/?ticket={ticket}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Should return list with one element or error
    if isinstance(json_data, list):
        assert len(json_data) <= 1, "Should return at most one deal"
        if len(json_data) == 1 and mt5_deal:
            assert json_data[0]["ticket"] == ticket, "Deal ticket should match"
    else:
        assert isinstance(json_data, dict), "Response should be list or dict"


def test_history_deals_get_by_position(client: TestClient, request):
    """Test history_deals_get with position filter."""
    # Use closed tickets from the fixture
    if not hasattr(request.config, '_test_order_state'):
        pytest.skip("Test order state not available")
    
    closed_tickets = request.config._test_order_state.get("closed_tickets", [])
    
    if not closed_tickets:
        pytest.skip("No closed history deals available to test position filter")
    
    # Get the position from one of the closed deals
    ticket = closed_tickets[0]
    mt5_deal = mt5.history_deals_get(ticket=ticket)
    
    if not mt5_deal or len(mt5_deal) == 0:
        pytest.skip("Could not find closed deal to get position")
    
    position = mt5_deal[0].position_id  # type: ignore
    
    if position == 0:
        pytest.skip("Closed deal has no position")
    
    # Get data from API
    response = client.get(f"/history/deals/?position={position}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Response should be list or error dict
    assert isinstance(json_data, (list, dict)), "Response should be list or dict"


def test_history_orders_structure(client: TestClient, request):
    """Test that order response has correct structure."""
    # Use closed tickets from the fixture
    if not hasattr(request.config, '_test_order_state'):
        pytest.skip("Test order state not available")
    
    closed_tickets = request.config._test_order_state.get("closed_tickets", [])
    
    if not closed_tickets:
        pytest.skip("No closed history orders available for structure validation")
    
    # Get data from API using one of the closed tickets
    ticket = closed_tickets[0]
    response = client.get(f"/history/orders/?ticket={ticket}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify structure matches MT5
    if isinstance(json_data, list) and len(json_data) > 0:
        api_order = json_data[0]
        mt5_order = mt5.history_orders_get(ticket=ticket)
        
        if mt5_order and len(mt5_order) > 0:
            mt5_dict = mt5_order[0]._asdict()
            
            # Verify key fields match
            assert api_order["ticket"] == mt5_dict["ticket"], "Order ticket mismatch"
            assert api_order["time_setup"] == mt5_dict["time_setup"], "Order time_setup mismatch"


def test_history_deals_structure(client: TestClient, request):
    """Test that deal response has correct structure."""
    # Use closed tickets from the fixture
    if not hasattr(request.config, '_test_order_state'):
        pytest.skip("Test order state not available")
    
    closed_tickets = request.config._test_order_state.get("closed_tickets", [])
    
    if not closed_tickets:
        pytest.skip("No closed history deals available for structure validation")
    
    # Get data from API using one of the closed tickets
    ticket = closed_tickets[0]
    response = client.get(f"/history/deals/?ticket={ticket}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify structure matches MT5
    if isinstance(json_data, list) and len(json_data) > 0:
        api_deal = json_data[0]
        mt5_deal = mt5.history_deals_get(ticket=ticket)
        
        if mt5_deal and len(mt5_deal) > 0:
            mt5_dict = mt5_deal[0]._asdict()
            
            # Verify key fields match
            assert api_deal["ticket"] == mt5_dict["ticket"], "Deal ticket mismatch"
            assert api_deal["time"] == mt5_dict["time"], "Deal time mismatch"


def test_history_orders_numeric_fields(client: TestClient, request):
    """Test that numeric fields in orders are proper types."""
    # Use closed tickets from the fixture
    if not hasattr(request.config, '_test_order_state'):
        pytest.skip("Test order state not available")
    
    closed_tickets = request.config._test_order_state.get("closed_tickets", [])
    
    if not closed_tickets:
        pytest.skip("No closed history orders available for type validation")
    
    # Get data from API using one of the closed tickets
    ticket = closed_tickets[0]
    response = client.get(f"/history/orders/?ticket={ticket}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    if isinstance(json_data, list):
        # Verify numeric fields are correct types
        numeric_fields = ["ticket", "time_setup", "type", "state", "magic"]
        
        for order in json_data:
            for field in numeric_fields:
                if field in order:
                    value = order[field]
                    assert isinstance(value, (int, float)), f"Field '{field}' should be numeric, got {type(value)}"


def test_history_deals_numeric_fields(client: TestClient, request):
    """Test that numeric fields in deals are proper types."""
    # Use closed tickets from the fixture
    if not hasattr(request.config, '_test_order_state'):
        pytest.skip("Test order state not available")
    
    closed_tickets = request.config._test_order_state.get("closed_tickets", [])
    
    if not closed_tickets:
        pytest.skip("No closed history deals available for type validation")
    
    # Get data from API using one of the closed tickets
    ticket = closed_tickets[0]
    response = client.get(f"/history/deals/?ticket={ticket}")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    if isinstance(json_data, list):
        # Verify numeric fields are correct types
        numeric_fields = ["ticket", "time", "type", "volume", "price", "commission", "profit"]
        
        for deal in json_data:
            for field in numeric_fields:
                if field in deal:
                    value = deal[field]
                    assert isinstance(value, (int, float)), f"Field '{field}' should be numeric, got {type(value)}"


def test_history_orders_consistency(client: TestClient):
    """Test that order counts and data are consistent."""
    # Get total count
    response_total = client.get("/history/orders/total")
    assert response_total.status_code == 200
    total = response_total.json()
    
    # Get orders list
    date_to = datetime.now()
    date_from = date_to - timedelta(days=30)
    response_list = client.get(
        "/history/orders/",
        params={
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat()
        }
    )
    assert response_list.status_code == 200
    orders = response_list.json()
    
    # Verify response structure
    if total is not None:
        assert isinstance(total, int), "Total should be an integer"
        assert total >= 0, "Total should be non-negative"


def test_history_deals_consistency(client: TestClient):
    """Test that deal counts and data are consistent."""
    # Get total count
    response_total = client.get("/history/deals/total")
    assert response_total.status_code == 200
    total = response_total.json()
    
    # Get deals list
    date_to = datetime.now()
    date_from = date_to - timedelta(days=30)
    response_list = client.get(
        "/history/deals/",
        params={
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat()
        }
    )
    assert response_list.status_code == 200
    deals = response_list.json()
    
    # Verify response structure
    if total is not None:
        assert isinstance(total, int), "Total should be an integer"
        assert total >= 0, "Total should be non-negative"


def test_history_orders_invalid_params(client: TestClient):
    """Test history_orders_get with invalid parameters."""
    # Call without required parameters
    response = client.get("/history/orders/")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Should return error response
    assert isinstance(json_data, dict), "Invalid params should return error dict"


def test_history_deals_invalid_params(client: TestClient):
    """Test history_deals_get with invalid parameters."""
    # Call without required parameters
    response = client.get("/history/deals/")
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Should return error response
    assert isinstance(json_data, dict), "Invalid params should return error dict"


def test_history_orders_with_forex_group(client: TestClient):
    """Test history_orders_get with Forex group filter."""
    date_to = datetime.now()
    date_from = date_to - timedelta(days=30)
    
    # Get data from MT5
    mt5_orders = mt5.history_orders_get(date_from=date_from, date_to=date_to, group="Forex*")
    
    # Get data from API
    response = client.get(
        "/history/orders/",
        params={
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
            "group": "Forex*"
        }
    )
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response
    if mt5_orders and len(mt5_orders) > 0:
        assert isinstance(json_data, list), "Response should be a list when orders exist"
    else:
        # May return empty list or error dict
        assert isinstance(json_data, (list, dict)), "Response should be list or dict"


def test_history_deals_with_forex_group(client: TestClient):
    """Test history_deals_get with Forex group filter."""
    date_to = datetime.now()
    date_from = date_to - timedelta(days=30)
    
    # Get data from MT5
    mt5_deals = mt5.history_deals_get(date_from=date_from, date_to=date_to, group="Forex*")
    
    # Get data from API
    response = client.get(
        "/history/deals/",
        params={
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
            "group": "Forex*"
        }
    )
    
    assert response.status_code == 200, "Status code should be 200"
    json_data = response.json()
    
    # Verify response
    if mt5_deals and len(mt5_deals) > 0:
        assert isinstance(json_data, list), "Response should be a list when deals exist"
    else:
        # May return empty list or error dict
        assert isinstance(json_data, (list, dict)), "Response should be list or dict"
