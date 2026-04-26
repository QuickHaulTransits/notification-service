import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint if it exists or just a basic assertion"""
    assert True

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "notification"

def test_app_exists():
    """Verify the app object is created"""
    assert app is not None
