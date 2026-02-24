"""Integration tests for GET /auth/me endpoint."""
import pytest
from fastapi import status


class TestAuthMe:
    """Integration tests for getting current user profile."""

    def test_authMe_authenticatedUser_returns200WithUserProfile(self, client, auth_headers):
        """Test authenticated request returns current user profile."""
        # Act
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        user = response.json()
        assert "id" in user
        assert "email" in user
        assert "full_name" in user
        assert "role" in user
        assert "is_active" in user

    def test_authMe_unauthenticatedRequest_returns401Unauthorized(self, client):
        """Test unauthenticated request returns 401."""
        # Act
        response = client.get("/api/v1/auth/me")
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authMe_invalidToken_returns401Unauthorized(self, client):
        """Test invalid token returns 401."""
        # Act
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authMe_expiredToken_returns401Unauthorized(self, client, test_user):
        """Test expired token returns 401."""
        # Arrange - create expired access token
        from jose import jwt
        from datetime import datetime, timedelta
        from src.config.settings import get_settings
        
        settings = get_settings()
        expired_payload = {
            "sub": str(test_user.id),
            "email": test_user.email,
            "role": test_user.role.value,
            "type": "access",
            "exp": datetime.utcnow() - timedelta(minutes=1),  # Expired
            "iat": datetime.utcnow()
        }
        expired_token = jwt.encode(
            expired_payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        # Act
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authMe_refreshTokenAsAccessToken_returns401Unauthorized(self, client, test_user):
        """Test using refresh token as access token returns 401."""
        # Arrange
        from src.utils.jwt_handler import jwt_handler
        
        refresh_token = jwt_handler.create_refresh_token(user_id=test_user.id)
        
        # Act
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {refresh_token}"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authMe_returnsCorrectUserData(self, client, test_user, auth_headers):
        """Test /auth/me returns the authenticated user's data."""
        # Act
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        user = response.json()
        assert user["id"] == str(test_user.id)
        assert user["email"] == test_user.email
        assert user["full_name"] == test_user.full_name
        assert user["role"] == test_user.role.value

    def test_authMe_noPasswordInResponse(self, client, auth_headers):
        """Test response doesn't include password hash."""
        # Act
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        user = response.json()
        assert "hashed_password" not in user
        assert "password" not in user

    def test_authMe_includesTimestamps(self, client, auth_headers):
        """Test response includes created_at and updated_at timestamps."""
        # Act
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        user = response.json()
        assert "created_at" in user
        assert "updated_at" in user

    def test_authMe_adminUserProfile(self, client, test_admin_user):
        """Test /auth/me returns correct role for admin user."""
        # Arrange
        from src.utils.jwt_handler import jwt_handler
        
        access_token = jwt_handler.create_access_token(
            user_id=test_admin_user.id,
            email=test_admin_user.email,
            role=test_admin_user.role.value
        )
        
        # Act
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        user = response.json()
        assert user["role"] == "admin"

    def test_authMe_bearerSchemeRequired(self, client, test_user):
        """Test Bearer scheme is required in Authorization header."""
        # Arrange - use invalid auth scheme
        from src.utils.jwt_handler import jwt_handler
        
        access_token = jwt_handler.create_access_token(
            user_id=test_user.id,
            email=test_user.email,
            role=test_user.role.value
        )
        
        # Act
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Basic {access_token}"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
