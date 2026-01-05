import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app

@pytest.mark.integration
def test_health_endpoint():
    client = TestClient(app)

    with patch("app.main.engine.connect"):
        response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
