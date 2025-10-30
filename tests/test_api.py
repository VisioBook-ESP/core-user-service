"""
Basic test for the FastAPI application.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_ready_endpoint():
    """Test the readiness check endpoint."""
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "READY"}


def test_users_endpoint():
    """Test the users list endpoint."""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    # Should return a list (even if empty with mock data)
    assert isinstance(response.json(), list)


def test_docs_endpoint():
    """Test that API docs are accessible."""
    response = client.get("/api/docs")
    assert response.status_code == 200
    # Should contain HTML for Swagger UI
    assert "swagger-ui" in response.text.lower() or "openapi" in response.text.lower()
