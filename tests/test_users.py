"""
Tests for user CRUD endpoints – error paths and RBAC.
"""

import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

FAKE_UUID = str(uuid.uuid4())


def _login(user_type: str = "admin") -> dict:
    """Helper to login and return tokens."""
    credentials = {
        "admin": {"email": "admin@visiobook.com", "password": "admin123"},
        "user": {"email": "user@visiobook.com", "password": "user123"},
    }
    response = client.post("/api/v1/auth/login", json=credentials[user_type])
    assert response.status_code == 200
    return response.json()


def _auth(user_type: str = "admin") -> dict:
    """Helper to get Authorization header."""
    return {"Authorization": f"Bearer {_login(user_type)['access_token']}"}


# ── GET /api/v1/users (admin-only) ──────────────────────────────────


class TestListUsers:
    """Test GET /api/v1/users."""

    def test_list_users_as_admin(self):
        response = client.get("/api/v1/users", headers=_auth("admin"))
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_users_as_user_forbidden(self):
        response = client.get("/api/v1/users", headers=_auth("user"))
        assert response.status_code == 403
        assert "Accès refusé" in response.json()["detail"]

    def test_list_users_no_token(self):
        response = client.get("/api/v1/users")
        assert response.status_code == 401


# ── GET /api/v1/users/me ────────────────────────────────────────────


class TestGetMe:
    """Test GET /api/v1/users/me."""

    def test_get_me_success(self):
        response = client.get("/api/v1/users/me", headers=_auth("admin"))
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "uuid" in data
            assert "email" in data
            assert "password" not in data

    def test_get_me_no_token(self):
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401

    def test_get_me_invalid_token(self):
        response = client.get("/api/v1/users/me", headers={"Authorization": "Bearer garbage"})
        assert response.status_code == 401


# ── GET /api/v1/users/{user_uuid} ───────────────────────────────────


class TestGetUserByUUID:
    """Test GET /api/v1/users/{user_uuid}."""

    def test_get_nonexistent_user_404(self):
        response = client.get(f"/api/v1/users/{FAKE_UUID}", headers=_auth("admin"))
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_other_user_as_regular_user_forbidden(self):
        response = client.get(f"/api/v1/users/{FAKE_UUID}", headers=_auth("user"))
        assert response.status_code == 403

    def test_get_user_no_token(self):
        response = client.get(f"/api/v1/users/{FAKE_UUID}")
        assert response.status_code == 401


# ── POST /api/v1/users (admin-only) ─────────────────────────────────


class TestCreateUser:
    """Test POST /api/v1/users."""

    def test_create_user_as_regular_user_forbidden(self):
        response = client.post(
            "/api/v1/users",
            json={
                "email": "new@example.com",
                "username": "newuser",
                "password": "password123",
            },
            headers=_auth("user"),
        )
        assert response.status_code == 403

    def test_create_user_no_token(self):
        response = client.post(
            "/api/v1/users",
            json={
                "email": "new@example.com",
                "username": "newuser",
                "password": "password123",
            },
        )
        assert response.status_code == 401

    def test_create_user_duplicate_email_409(self):
        response = client.post(
            "/api/v1/users",
            json={
                "email": "admin@visiobook.com",
                "username": "uniqueusername",
                "password": "password123",
            },
            headers=_auth("admin"),
        )
        assert response.status_code == 409

    def test_create_user_duplicate_username_409(self):
        response = client.post(
            "/api/v1/users",
            json={
                "email": "unique@example.com",
                "username": "admin",
                "password": "password123",
            },
            headers=_auth("admin"),
        )
        assert response.status_code == 409


# ── PUT /api/v1/users/me ────────────────────────────────────────────


class TestUpdateMe:
    """Test PUT /api/v1/users/me."""

    def test_update_me_no_token(self):
        response = client.put("/api/v1/users/me", json={"first_name": "Test"})
        assert response.status_code == 401

    def test_update_me_change_role_forbidden(self):
        response = client.put(
            "/api/v1/users/me",
            json={"role": "admin"},
            headers=_auth("user"),
        )
        assert response.status_code == 403
        assert "role" in response.json()["detail"].lower()


# ── PUT /api/v1/users/{user_uuid} ───────────────────────────────────


class TestUpdateUser:
    """Test PUT /api/v1/users/{user_uuid}."""

    def test_update_nonexistent_user_404(self):
        response = client.put(
            f"/api/v1/users/{FAKE_UUID}",
            json={"first_name": "Ghost"},
            headers=_auth("admin"),
        )
        assert response.status_code == 404

    def test_update_other_user_as_regular_user_forbidden(self):
        response = client.put(
            f"/api/v1/users/{FAKE_UUID}",
            json={"first_name": "Hacker"},
            headers=_auth("user"),
        )
        assert response.status_code == 403

    def test_update_user_no_token(self):
        response = client.put(f"/api/v1/users/{FAKE_UUID}", json={"first_name": "Ghost"})
        assert response.status_code == 401


# ── DELETE /api/v1/users/{user_uuid} (admin-only) ───────────────────


class TestDeleteUser:
    """Test DELETE /api/v1/users/{user_uuid}."""

    def test_delete_nonexistent_user_404(self):
        response = client.delete(f"/api/v1/users/{FAKE_UUID}", headers=_auth("admin"))
        assert response.status_code == 404

    def test_delete_user_as_regular_user_forbidden(self):
        response = client.delete(f"/api/v1/users/{FAKE_UUID}", headers=_auth("user"))
        assert response.status_code == 403

    def test_delete_user_no_token(self):
        response = client.delete(f"/api/v1/users/{FAKE_UUID}")
        assert response.status_code == 401


# ── DELETE /api/v1/users/me ──────────────────────────────────────────


class TestDeleteMe:
    """Test DELETE /api/v1/users/me."""

    def test_delete_me_no_token(self):
        response = client.delete("/api/v1/users/me")
        assert response.status_code == 401


# ── GET /api/v1/users/resolve-user ──────────────────────────────────


class TestResolveUser:
    """Test GET /api/v1/users/resolve-user."""

    def test_resolve_user_success(self):
        response = client.get("/api/v1/users/resolve-user", headers=_auth("admin"))
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert "userId" in response.json()

    def test_resolve_user_no_token(self):
        response = client.get("/api/v1/users/resolve-user")
        assert response.status_code == 401

    def test_resolve_user_invalid_token(self):
        response = client.get(
            "/api/v1/users/resolve-user",
            headers={"Authorization": "Bearer garbage"},
        )
        assert response.status_code == 401


# ── Happy-path CRUD (create → read → update → delete) ───────────────


class TestUserCRUDHappyPath:
    """Full lifecycle: admin creates a user, reads, updates, and deletes it."""

    def test_full_lifecycle(self):
        headers = _auth("admin")

        # Create
        resp = client.post(
            "/api/v1/users",
            json={
                "email": "lifecycle@test.com",
                "username": "lifecycleuser",
                "password": "password123",
                "first_name": "Life",
                "last_name": "Cycle",
            },
            headers=headers,
        )
        assert resp.status_code == 201
        user = resp.json()
        assert user["email"] == "lifecycle@test.com"
        assert user["username"] == "lifecycleuser"
        assert user["first_name"] == "Life"
        assert "password" not in user
        user_uuid = user["uuid"]

        # Read by UUID (admin)
        resp = client.get(f"/api/v1/users/{user_uuid}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["uuid"] == user_uuid

        # Update by UUID (admin)
        resp = client.put(
            f"/api/v1/users/{user_uuid}",
            json={"first_name": "Updated", "last_name": "Name"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["first_name"] == "Updated"

        # Delete
        resp = client.delete(f"/api/v1/users/{user_uuid}", headers=headers)
        assert resp.status_code == 204

        # Confirm deleted
        resp = client.get(f"/api/v1/users/{user_uuid}", headers=headers)
        assert resp.status_code == 404

    def test_update_my_profile_success(self):
        """Test user can update their own profile."""
        headers = _auth("user")

        resp = client.put(
            "/api/v1/users/me",
            json={"first_name": "Updated"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["first_name"] == "Updated"

    def test_get_own_profile_by_uuid(self):
        """Test user can view their own profile by UUID."""
        headers = _auth("user")

        # Get own UUID from /me
        resp = client.get("/api/v1/users/me", headers=headers)
        assert resp.status_code == 200
        my_uuid = resp.json()["uuid"]

        # Access by UUID
        resp = client.get(f"/api/v1/users/{my_uuid}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["uuid"] == my_uuid
