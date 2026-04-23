"""
Tests for authentication endpoints and role-based access control (RBAC).
"""

import uuid

import jwt
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_login_success_admin(self):
        """Test successful login with admin credentials."""
        response = client.post(
            "/api/v1/auth/login", json={"email": "admin@visiobook.com", "password": "admin123"}
        )
        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_success_user(self):
        """Test successful login with user credentials."""
        response = client.post(
            "/api/v1/auth/login", json={"email": "user@visiobook.com", "password": "user123"}
        )
        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_invalid_email(self):
        """Test login with invalid email."""
        response = client.post(
            "/api/v1/auth/login", json={"email": "nonexistent@example.com", "password": "admin123"}
        )
        assert response.status_code == 401
        assert "Email ou mot de passe incorrect" in response.json()["detail"]

    def test_login_invalid_password(self):
        """Test login with invalid password."""
        response = client.post(
            "/api/v1/auth/login", json={"email": "admin@visiobook.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Email ou mot de passe incorrect" in response.json()["detail"]

    def test_login_invalid_email_format(self):
        """Test login with invalid email format."""
        response = client.post(
            "/api/v1/auth/login", json={"email": "not-an-email", "password": "admin123"}
        )
        assert response.status_code == 422  # Validation error


class TestProtectedRoutes:
    """Test protected routes and RBAC."""

    def _get_token(self, user_type: str = "admin") -> str:
        """Helper to get a valid token for testing."""
        credentials = {
            "admin": {"email": "admin@visiobook.com", "password": "admin123"},
            "user": {"email": "user@visiobook.com", "password": "user123"},
        }

        response = client.post("/api/v1/auth/login", json=credentials[user_type])
        assert response.status_code == 200
        return response.json()["access_token"]

    def test_get_my_profile_success(self):
        """Test getting current user profile with valid token."""
        token = self._get_token("admin")

        response = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code in [200, 404]

    def test_get_my_profile_no_token(self):
        """Test getting profile without authentication token."""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401

    def test_get_my_profile_invalid_token(self):
        """Test getting profile with invalid token."""
        response = client.get("/api/v1/users/me", headers={"Authorization": "Bearer invalid-token"})
        assert response.status_code == 401

    def test_delete_user_admin_success(self):
        """Test deleting user as admin."""
        token = self._get_token("admin")

        response = client.delete(
            "/api/v1/users/999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code in [204, 404]

    def test_delete_user_as_regular_user_forbidden(self):
        """Test that regular users cannot delete users."""
        token = self._get_token("user")

        response = client.delete(
            "/api/v1/users/999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403
        assert "Accès refusé" in response.json()["detail"]

    def test_delete_user_no_token(self):
        """Test deleting user without authentication."""
        response = client.delete("/api/v1/users/999")
        assert response.status_code == 401


class TestJWTTokens:
    """Test JWT token validation and expiration."""

    def test_token_contains_user_data(self):
        """Test that JWT token contains correct user data (UUID in sub claim)."""
        response = client.post(
            "/api/v1/auth/login", json={"email": "admin@visiobook.com", "password": "admin123"}
        )
        token = response.json()["access_token"]

        payload = jwt.decode(token, options={"verify_signature": False})

        uuid.UUID(payload["sub"])  # raises ValueError if not a valid UUID
        assert payload["iss"] == "core-user-service"
        assert "exp" in payload

    def test_expired_token_rejected(self):
        """Test that expired tokens are rejected."""
        invalid_token = (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9." "eyJzdWIiOiJ1c2VyXzAwMSIsImV4cCI6MX0.invalid"
        )
        response = client.get(
            "/api/v1/users/me", headers={"Authorization": f"Bearer {invalid_token}"}
        )
        assert response.status_code == 401


class TestRefreshTokens:
    """Test refresh token flow."""

    def _login(self, user_type: str = "admin") -> dict:
        credentials = {
            "admin": {"email": "admin@visiobook.com", "password": "admin123"},
            "user": {"email": "user@visiobook.com", "password": "user123"},
        }
        response = client.post("/api/v1/auth/login", json=credentials[user_type])
        assert response.status_code == 200
        return response.json()

    def test_login_returns_refresh_token(self):
        """Test that login returns both access and refresh tokens."""
        data = self._login()
        assert "access_token" in data
        assert "refresh_token" in data
        assert len(data["refresh_token"]) > 0

    def test_refresh_returns_new_tokens(self):
        """Test that POST /auth/refresh returns new access + refresh tokens."""
        data = self._login()
        old_refresh = data["refresh_token"]

        response = client.post(
            "/api/v1/auth/refresh", json={"refresh_token": old_refresh}
        )
        assert response.status_code == 200
        new_data = response.json()
        assert "access_token" in new_data
        assert "refresh_token" in new_data
        assert new_data["refresh_token"] != old_refresh  # rotation

    def test_refresh_revokes_old_token(self):
        """Test that using a refresh token revokes it (cannot be reused)."""
        data = self._login()
        old_refresh = data["refresh_token"]

        # First refresh: should succeed
        response = client.post(
            "/api/v1/auth/refresh", json={"refresh_token": old_refresh}
        )
        assert response.status_code == 200

        # Second refresh with same token: should fail
        response = client.post(
            "/api/v1/auth/refresh", json={"refresh_token": old_refresh}
        )
        assert response.status_code == 401

    def test_refresh_invalid_token(self):
        """Test that an invalid refresh token is rejected."""
        response = client.post(
            "/api/v1/auth/refresh", json={"refresh_token": "invalid-token"}
        )
        assert response.status_code == 401

    def test_logout_revokes_refresh_token(self):
        """Test that logout revokes the refresh token."""
        data = self._login()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        # Logout
        response = client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": refresh_token},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 204

        # Try to use the revoked refresh token
        response = client.post(
            "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
        )
        assert response.status_code == 401

    def test_logout_requires_auth(self):
        """Test that logout requires authentication."""
        response = client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": "some-token"},
        )
        assert response.status_code == 401

    def test_new_access_token_is_valid(self):
        """Test that the new access token from refresh works on protected routes."""
        data = self._login()

        # Refresh
        response = client.post(
            "/api/v1/auth/refresh", json={"refresh_token": data["refresh_token"]}
        )
        new_access = response.json()["access_token"]

        # Use new access token
        response = client.get(
            "/api/v1/users/me", headers={"Authorization": f"Bearer {new_access}"}
        )
        assert response.status_code in [200, 404]


class TestJWKSEndpoint:
    """Test JWKS endpoint."""

    def test_jwks_endpoint(self):
        """Test that JWKS endpoint returns valid key set."""
        response = client.get("/api/v1/auth/.well-known/jwks.json")
        assert response.status_code == 200
        data = response.json()
        assert "keys" in data
        assert len(data["keys"]) == 1
        key = data["keys"][0]
        assert key["kty"] == "RSA"
        assert key["use"] == "sig"
        assert key["alg"] == "RS256"
        assert "n" in key
        assert "e" in key
        assert "kid" in key
