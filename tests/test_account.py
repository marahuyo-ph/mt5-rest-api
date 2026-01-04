from fastapi.testclient import TestClient
import MetaTrader5 as mt5 # type: ignore

def test_account(client: TestClient):
    """Test account info endpoint."""
    response = client.get("/accounts/info")
    assert response.status_code == 200
    account = mt5.account_info()
    
    if not account:
        return 
    
    assert response.json() == account._asdict()