"""
Tests for request validation errors (422).
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _auth_admin() -> dict:
    """Helper to get admin Authorization header."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@visiobook.com", "password": "admin123"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


class TestLoginValidation:
    """Test login request validation."""

    def test_login_missing_email(self):
        response = client.post("/api/v1/auth/login", json={"password": "test"})
        assert response.status_code == 422

    def test_login_missing_password(self):
        response = client.post("/api/v1/auth/login", json={"email": "test@example.com"})
        assert response.status_code == 422

    def test_login_empty_body(self):
        response = client.post("/api/v1/auth/login", json={})
        assert response.status_code == 422

    def test_login_invalid_email_format(self):
        response = client.post(
            "/api/v1/auth/login", json={"email": "not-email", "password": "test"}
        )
        assert response.status_code == 422


class TestRegisterValidation:
    """Test register request validation."""

    def test_register_missing_email(self):
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "testuser", "password": "password123"},
        )
        assert response.status_code == 422

    def test_register_missing_username(self):
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        )
        assert response.status_code == 422

    def test_register_missing_password(self):
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "username": "testuser"},
        )
        assert response.status_code == 422

    def test_register_password_too_short(self):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "12345",
            },
        )
        assert response.status_code == 422

    def test_register_username_too_short(self):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "ab",
                "password": "password123",
            },
        )
        assert response.status_code == 422

    def test_register_username_too_long(self):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "a" * 51,
                "password": "password123",
            },
        )
        assert response.status_code == 422

    def test_register_invalid_email_format(self):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "username": "testuser",
                "password": "password123",
            },
        )
        assert response.status_code == 422

    def test_register_duplicate_email_409(self):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "admin@visiobook.com",
                "username": "uniqueuser999",
                "password": "password123",
            },
        )
        assert response.status_code == 409

    def test_register_duplicate_username_409(self):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "unique999@example.com",
                "username": "admin",
                "password": "password123",
            },
        )
        assert response.status_code == 409


class TestCreateUserValidation:
    """Test POST /api/v1/users validation (admin endpoint)."""

    def test_create_user_invalid_email(self):
        response = client.post(
            "/api/v1/users",
            json={
                "email": "not-email",
                "username": "testuser",
                "password": "password123",
            },
            headers=_auth_admin(),
        )
        assert response.status_code == 422

    def test_create_user_password_too_short(self):
        response = client.post(
            "/api/v1/users",
            json={
                "email": "valid@example.com",
                "username": "testuser",
                "password": "12345",
            },
            headers=_auth_admin(),
        )
        assert response.status_code == 422

    def test_create_user_username_too_short(self):
        response = client.post(
            "/api/v1/users",
            json={
                "email": "valid@example.com",
                "username": "ab",
                "password": "password123",
            },
            headers=_auth_admin(),
        )
        assert response.status_code == 422

    def test_create_user_empty_body(self):
        response = client.post("/api/v1/users", json={}, headers=_auth_admin())
        assert response.status_code == 422


class TestRefreshValidation:
    """Test refresh request validation."""

    def test_refresh_missing_token(self):
        response = client.post("/api/v1/auth/refresh", json={})
        assert response.status_code == 422

    def test_refresh_empty_body(self):
        response = client.post("/api/v1/auth/refresh")
        assert response.status_code == 422
