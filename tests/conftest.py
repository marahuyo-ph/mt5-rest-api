import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)
