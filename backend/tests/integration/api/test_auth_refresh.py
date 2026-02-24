"""Integration tests for POST /auth/refresh endpoint."""
import pytest
from fastapi import status


class TestAuthRefresh:
    """Integration tests for token refresh."""

    def test_refresh_validRefreshToken_returns200WithNewAccessToken(self, client, test_user):
        """Test sending valid refresh token returns new access token."""
        # Arrange
        from src.utils.jwt_handler import jwt_handler
        
        refresh_token = jwt_handler.create_refresh_token(user_id=test_user.id)
        
        # Act
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] != refresh_token
        assert "user" in data

    def test_refresh_invalidRefreshToken_returns401Unauthorized(self, client):
        """Test refresh with invalid token returns 401."""
        # Act
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid.token.here"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_accessTokenAsRefreshToken_returns401Unauthorized(self, client, test_user):
        """Test using access token as refresh token returns 401."""
        # Arrange
        from src.utils.jwt_handler import jwt_handler
        
        access_token = jwt_handler.create_access_token(
            user_id=test_user.id,
            email=test_user.email,
            role=test_user.role.value
        )
        
        # Act
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": access_token}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_expiredRefreshToken_returns401Unauthorized(self, client, test_user):
        """Test expired refresh token returns 401."""
        # Arrange - create expired refresh token
        from jose import jwt
        from datetime import datetime, timedelta
        from src.config.settings import get_settings
        
        settings = get_settings()
        expired_payload = {
            "sub": str(test_user.id),
            "type": "refresh",
            "exp": datetime.utcnow() - timedelta(days=1),  # Expired
            "iat": datetime.utcnow()
        }
        expired_token = jwt.encode(
            expired_payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        # Act
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": expired_token}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_missingRefreshToken_returns401Unauthorized(self, client):
        """Test refresh without token returns 401."""
        # Act
        response = client.post("/api/v1/auth/refresh", json={})
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_returnsUserData(self, client, test_user):
        """Test refresh response includes user data."""
        # Arrange
        from src.utils.jwt_handler import jwt_handler
        
        refresh_token = jwt_handler.create_refresh_token(user_id=test_user.id)
        
        # Act
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        user = response.json()["user"]
        assert user["id"] == str(test_user.id)
        assert user["email"] == test_user.email

    def test_refresh_newAccessTokenIsValid(self, client, test_user):
        """Test new access token can be used for authenticated requests."""
        # Arrange
        from src.utils.jwt_handler import jwt_handler
        
        refresh_token = jwt_handler.create_refresh_token(user_id=test_user.id)
        
        # Act - get new access token
        refresh_response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        new_access_token = refresh_response.json()["access_token"]
        
        # Use new token to get /auth/me
        auth_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {new_access_token}"}
        )
        
        # Assert
        assert refresh_response.status_code == status.HTTP_200_OK
        assert auth_response.status_code == status.HTTP_200_OK
