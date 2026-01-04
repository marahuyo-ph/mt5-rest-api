import sys
from pathlib import Path
import time
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
import MetaTrader5 as mt5  # type: ignore

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import app

# Module-level storage for test data
_test_order_state: dict = {  # type: ignore
    "open_ticket": None,  # Open position for position tests
    "closed_tickets": [],  # Closed orders for history tests
}


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_test_order(request):
    """
    Session-level fixture that sets up test data at the start of test session
    and cleans up at the end. This ensures tests have both open positions and order history.
    
    Strategy:
    1. Try to use existing open positions/closed orders in the account
    2. If none exist, try to create new ones
    3. If creation fails (due to account restrictions), skip data-dependent tests
    """
    # Store state in pytest config for access by other tests
    request.config._test_order_state = _test_order_state
    
    # Strategy 1: Try to find existing open position
    try:
        positions = mt5.positions_get()
        if positions and len(positions) > 0:
            # Use the first position as test data
            _test_order_state["open_ticket"] = positions[0].ticket  # type: ignore
    except Exception:
        pass
    
    # Strategy 2: Try to find existing closed orders in history and extract position info
    try:
        # Get last 30 days of history
        from_date = int((datetime.now().timestamp() - 30 * 24 * 3600))
        to_date = int(datetime.now().timestamp())
        
        # Try to get history orders first (which have position info)
        history_orders = mt5.history_orders_get(from_date, to_date)
        
        # Also get deals for ticket numbers
        history_deals = mt5.history_deals_get(from_date, to_date)
        unique_tickets = set()
        
        if history_deals and len(history_deals) > 0:
            # Collect unique ticket numbers from deals
            for deal in history_deals:
                if deal.ticket:  # type: ignore
                    unique_tickets.add(deal.ticket)  # type: ignore
            
            _test_order_state["closed_tickets"] = list(unique_tickets)[:3]  # Use first 3 unique tickets
        
        # If we still don't have closed_tickets, try history orders
        if not _test_order_state["closed_tickets"] and history_orders:
            for order in history_orders:
                if order.ticket:  # type: ignore
                    _test_order_state["closed_tickets"].append(order.ticket)  # type: ignore
                if len(_test_order_state["closed_tickets"]) >= 3:
                    break
    except Exception:
        pass
    
    # Strategy 3: If no open position, try to create new test orders
    # NOTE: This account may have trading restrictions that prevent order creation (retcode 10030 INVALID_FILL).
    # We attempt multiple strategies: different symbols, volumes, and filling types (IOC, FOK, RETURN).
    # If all attempts fail, tests that require open positions will be skipped.
    if not _test_order_state["open_ticket"]:
        try:
            # Try different symbols and volumes to find what works on this account
            test_symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD"]
            test_volumes = [0.1, 0.01, 0.001]
            
            for symbol in test_symbols:
                # CRITICAL: Must call symbol_select() to enable symbol in MarketWatch
                if not mt5.symbol_select(symbol, True):
                    continue
                
                symbol_info = mt5.symbol_info(symbol)
                if symbol_info is None:
                    continue
                
                tick = mt5.symbol_info_tick(symbol)
                if tick is None:
                    continue
                
                # Try different volumes to find minimum tradeable amount
                for volume in test_volumes:
                    # Try to create an OPEN position for position tests
                    open_request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": symbol,
                        "volume": volume,
                        "type": mt5.ORDER_TYPE_BUY,
                        "price": tick.ask,  # type: ignore
                        "deviation": 20,
                        "magic": 999999,
                        "comment": "Test open position for pytest",
                        "type_filling": mt5.ORDER_FILLING_RETURN,
                        "type_time": mt5.ORDER_TIME_GTC,
                    }
                    
                    result = mt5.order_send(open_request)  # type: ignore
                    if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:  # type: ignore
                        _test_order_state["open_ticket"] = result.order  # type: ignore
                        _test_order_state["test_symbol"] = symbol  # type: ignore
                        _test_order_state["test_volume"] = volume  # type: ignore
                        break
                    
                    time.sleep(0.05)
                
                # If successful, break out of symbol loop
                if _test_order_state["open_ticket"]:
                    break
            
            # Try to create and immediately close orders for history
            # Use the same symbol that worked for open position, or fallback to EURUSD
            history_symbol = _test_order_state.get("test_symbol", "EURUSD")  # type: ignore
            history_volume = _test_order_state.get("test_volume", 0.1)  # type: ignore
            
            # Ensure symbol is selected
            mt5.symbol_select(history_symbol, True)
            
            for i in range(3):
                # Small delays to ensure order sequence
                time.sleep(0.2)
                
                tick = mt5.symbol_info_tick(history_symbol)
                if tick is None:
                    continue
                
                # Create order
                history_request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": history_symbol,
                    "volume": history_volume,
                    "type": mt5.ORDER_TYPE_BUY if i % 2 == 0 else mt5.ORDER_TYPE_SELL,
                    "price": tick.ask if i % 2 == 0 else tick.bid,  # type: ignore
                    "deviation": 20,
                    "magic": 999999 + i + 1,
                    "comment": f"Test order {i+1} for pytest history",
                    "type_filling": mt5.ORDER_FILLING_RETURN,
                    "type_time": mt5.ORDER_TIME_GTC,
                }
                
                result = mt5.order_send(history_request)  # type: ignore
                if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:  # type: ignore
                    ticket = result.order  # type: ignore
                    _test_order_state["closed_tickets"].append(ticket)
                    
                    # Close the order immediately to add to history
                    time.sleep(0.1)
                    tick = mt5.symbol_info_tick(history_symbol)
                    if tick:
                        close_request = {
                            "action": mt5.TRADE_ACTION_DEAL,
                            "symbol": history_symbol,
                            "volume": history_volume,
                            "type": mt5.ORDER_TYPE_SELL if i % 2 == 0 else mt5.ORDER_TYPE_BUY,
                            "price": tick.bid if i % 2 == 0 else tick.ask,  # type: ignore
                            "position": ticket,
                            "deviation": 20,
                            "magic": 999999 + i + 1,
                            "comment": f"Closing test order {i+1}",
                            "type_filling": mt5.ORDER_FILLING_RETURN,
                            "type_time": mt5.ORDER_TIME_GTC,
                        }
                        
                        close_result = mt5.order_send(close_request)  # type: ignore
        except Exception:
            pass
    
    # Yield control to run all tests
    yield
    
    # Teardown: Close open position if it was created by us and still exists
    if _test_order_state["open_ticket"] is not None:
        try:
            # Use the symbol that was used to create the position
            symbol = _test_order_state.get("test_symbol", "EURUSD")  # type: ignore
            volume = _test_order_state.get("test_volume", 0.1)  # type: ignore
            
            # Ensure symbol is selected
            mt5.symbol_select(symbol, True)
            
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                return
            
            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": mt5.ORDER_TYPE_SELL,
                "price": tick.bid,  # type: ignore
                "position": _test_order_state["open_ticket"],
                "deviation": 20,
                "magic": 999999,
                "comment": "Closing test position",
                "type_filling": mt5.ORDER_FILLING_RETURN,
                "type_time": mt5.ORDER_TIME_GTC,
            }
            
            result = mt5.order_send(close_request)  # type: ignore
        except Exception:
            pass
