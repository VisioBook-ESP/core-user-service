"""
Tests for health, readiness, and docs endpoints.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health and readiness endpoints."""

    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "service" in data
        assert "version" in data

    def test_ready_endpoint(self):
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "READY"}

    def test_docs_endpoint(self):
        response = client.get("/api/docs")
        assert response.status_code == 200
        assert "swagger-ui" in response.text.lower() or "openapi" in response.text.lower()

    def test_openapi_schema(self):
        response = client.get("/api/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "paths" in data
        assert "info" in data

    def test_redoc_endpoint(self):
        response = client.get("/api/redoc")
        assert response.status_code == 200
