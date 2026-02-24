"""Integration tests for POST /auth/login endpoint."""
import pytest
from fastapi import status


class TestAuthLogin:
    """Integration tests for user login."""

    def test_login_validCredentials_returns200WithTokens(self, client, test_user):
        """Test successful login returns 200 with tokens."""
        # Act
        response = client.post(
            "/api/v1/auth/login",
            json={"email": test_user.email, "password": "TestPassword123!"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "user" in data
        assert data["user"]["email"] == test_user.email

    def test_login_invalidPassword_returns401Unauthorized(self, client, test_user):
        """Test login with wrong password returns 401."""
        # Act
        response = client.post(
            "/api/v1/auth/login",
            json={"email": test_user.email, "password": "WrongPassword123!"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_nonExistentEmail_returns401Unauthorized(self, client):
        """Test login with non-existent email returns 401."""
        # Act
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "Password123!"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_missingPassword_returns422ValidationError(self, client, test_user):
        """Test login without password returns validation error."""
        # Act
        response = client.post(
            "/api/v1/auth/login",
            json={"email": test_user.email}
        )
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_validCredentials_returnsUserData(self, client, test_user):
        """Test login returns complete user profile."""
        # Act
        response = client.post(
            "/api/v1/auth/login",
            json={"email": test_user.email, "password": "TestPassword123!"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        user = response.json()["user"]
        assert user["id"] == str(test_user.id)
        assert user["email"] == test_user.email
        assert user["full_name"] == test_user.full_name
        assert user["role"] == test_user.role.value

    def test_login_validCredentials_noPasswordInResponse(self, client, test_user):
        """Test login response doesn't include password hash."""
        # Act
        response = client.post(
            "/api/v1/auth/login",
            json={"email": test_user.email, "password": "TestPassword123!"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        user = response.json()["user"]
        assert "hashed_password" not in user
        assert "password" not in user

    def test_login_caseInsensitiveEmail_succeeds(self, client, test_user):
        """Test login with different email case succeeds."""
        # Act
        response = client.post(
            "/api/v1/auth/login",
            json={"email": test_user.email.upper(), "password": "TestPassword123!"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_login_genericErrorMessage_doesNotRevealUserExistence(self, client):
        """Test error message doesn't reveal if email exists."""
        # Act - non-existent email
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "this@email.does.not.exist.com", "password": "Pass123!"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error_msg = response.json()["detail"].lower()
        assert "email" not in error_msg
        assert "not found" not in error_msg
        assert "invalid credentials" in error_msg

    def test_login_activeUserOnly(self, client, db):
        """Test inactive user cannot login."""
        # Arrange - create and deactivate a user
        from src.models.user import User
        from src.utils.password_hasher import password_hasher
        
        hashed = password_hasher.hash_password("TestPassword123!")
        inactive_user = User(
            email="inactive@example.com",
            hashed_password=hashed,
            full_name="Inactive User",
            role="submitter"
        )
        inactive_user.is_active = False
        db.add(inactive_user)
        db.commit()
        
        # Act
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "inactive@example.com", "password": "TestPassword123!"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_tokenTypeBearer(self, client, test_user):
        """Test login response has bearer token type."""
        # Act
        response = client.post(
            "/api/v1/auth/login",
            json={"email": test_user.email, "password": "TestPassword123!"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["token_type"] == "bearer"

    def test_login_adminUser_succeeds(self, client, test_admin_user):
        """Test admin user can login."""
        # Act
        response = client.post(
            "/api/v1/auth/login",
            json={"email": test_admin_user.email, "password": "AdminPassword123!"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        user = response.json()["user"]
        assert user["role"] == "admin"
