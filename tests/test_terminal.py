from fastapi.testclient import TestClient
import MetaTrader5 as mt5  # type: ignore


def test_terminal(client: TestClient):
    """Test terminal info endpoint."""
    response = client.get("/terminal/info")
    assert response.status_code == 200

    terminal = mt5.terminal_info()

    if not terminal:
        return

    assert response.json() == terminal._asdict()
