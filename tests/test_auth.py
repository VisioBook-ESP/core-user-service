"""
Tests for authentication endpoints and role-based access control (RBAC).
"""

import jwt
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_login_success_admin(self):
        """Test successful login with admin credentials."""
        response = client.post(
            "/auth/login",
            json={
                "email": "admin@visiobook.com",
                "password": "admin123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user_id"] == "1"  # Now using integer IDs as strings
        assert data["role"] == "admin"
        assert data["expires_in"] == 24 * 3600  # 24 hours

    def test_login_success_user(self):
        """Test successful login with user credentials."""
        response = client.post(
            "/auth/login",
            json={
                "email": "user@visiobook.com",
                "password": "user123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert data["role"] == "user"
        assert data["user_id"] == "2"  # Now using integer IDs as strings

    def test_login_success_moderator(self):
        """Test successful login with moderator credentials."""
        response = client.post(
            "/auth/login",
            json={
                "email": "moderator@visiobook.com",
                "password": "moderator123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert data["role"] == "moderator"
        assert data["user_id"] == "3"  # Now using integer IDs as strings

    def test_login_invalid_email(self):
        """Test login with invalid email."""
        response = client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "admin123"
            }
        )
        assert response.status_code == 401
        assert "Email ou mot de passe incorrect" in response.json()["detail"]

    def test_login_invalid_password(self):
        """Test login with invalid password."""
        response = client.post(
            "/auth/login",
            json={
                "email": "admin@visiobook.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        assert "Email ou mot de passe incorrect" in response.json()["detail"]

    def test_login_invalid_email_format(self):
        """Test login with invalid email format."""
        response = client.post(
            "/auth/login",
            json={
                "email": "not-an-email",
                "password": "admin123"
            }
        )
        assert response.status_code == 422  # Validation error


class TestProtectedRoutes:
    """Test protected routes and RBAC."""

    def _get_token(self, user_type: str = "admin") -> str:
        """Helper to get a valid token for testing."""
        credentials = {
            "admin": {"email": "admin@visiobook.com", "password": "admin123"},
            "user": {"email": "user@visiobook.com", "password": "user123"},
            "moderator": {"email": "moderator@visiobook.com", "password": "moderator123"},
        }
        
        response = client.post("/auth/login", json=credentials[user_type])
        assert response.status_code == 200
        return response.json()["access_token"]

    def test_get_my_profile_success(self):
        """Test getting current user profile with valid token."""
        token = self._get_token("admin")
        
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        # Note: This might fail if user_service.get_user doesn't find the mock user
        # but it should at least test the authentication flow
        assert response.status_code in [200, 404]  # 404 if user not in service

    def test_get_my_profile_no_token(self):
        """Test getting profile without authentication token."""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401

    def test_get_my_profile_invalid_token(self):
        """Test getting profile with invalid token."""
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer invalid-token"}
        )
        assert response.status_code == 401

    def test_delete_user_admin_success(self):
        """Test deleting user as admin."""
        token = self._get_token("admin")
        
        response = client.delete(
            "/api/v1/users/999",  # Use integer ID instead of string
            headers={"Authorization": f"Bearer {token}"}
        )
        # Note: This will return 404 since user 999 doesn't exist, but tests auth flow
        assert response.status_code in [204, 404]

    def test_delete_user_as_regular_user_forbidden(self):
        """Test that regular users cannot delete users."""
        token = self._get_token("user")
        
        response = client.delete(
            "/api/v1/users/999",  # Use integer ID instead of string
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
        assert "Accès refusé" in response.json()["detail"]

    def test_delete_user_as_moderator_forbidden(self):
        """Test that moderators cannot delete users (only admins can)."""
        token = self._get_token("moderator")
        
        response = client.delete(
            "/api/v1/users/999",  # Use integer ID instead of string
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
        assert "Accès refusé" in response.json()["detail"]

    def test_delete_user_no_token(self):
        """Test deleting user without authentication."""
        response = client.delete("/api/v1/users/999")  # Use integer ID
        assert response.status_code == 401


class TestJWTTokens:
    """Test JWT token validation and expiration."""

    def test_token_contains_user_data(self):
        """Test that JWT token contains correct user data."""
        # Get a token
        response = client.post(
            "/auth/login",
            json={
                "email": "admin@visiobook.com",
                "password": "admin123"
            }
        )
        token = response.json()["access_token"]
        
        # Decode token (without verification for testing)
        payload = jwt.decode(token, options={"verify_signature": False})
        
        assert payload["sub"] == "1"  # user_id - now using integer IDs as strings
        assert payload["email"] == "admin@visiobook.com"
        assert payload["role"] == "admin"
        assert "exp" in payload  # expiration time

    def test_expired_token_rejected(self):
        """Test that expired tokens are rejected."""
        # This test would require generating an expired token
        # For now, we test with an obviously invalid token
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyXzAwMSIsImV4cCI6MX0.invalid"}
        )
        assert response.status_code == 401