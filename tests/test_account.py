from fastapi.testclient import TestClient
import pytest
import MetaTrader5 as mt5  # type: ignore


def test_account(client: TestClient):
    """Test account info endpoint."""
    response = client.get("/accounts/info")
    assert response.status_code == 200
    account = mt5.account_info()
    
    if not account:
        return 
    
    assert response.json() == account._asdict()


def test_orders_exist_with_ticket(request):
    """Verify that test order exists by querying its ticket."""
    if not hasattr(request.config, '_test_order_state'):
        pytest.skip("Test order state not available")
    
    open_ticket = request.config._test_order_state.get("open_ticket")
    
    if open_ticket is None:
        pytest.skip("Test open position was not created")
    
    order = mt5.orders_get(ticket=open_ticket)
    
    assert order is not None, f"Should be able to query order by ticket {open_ticket}"
    assert len(order) > 0, f"Order with ticket {open_ticket} should exist"