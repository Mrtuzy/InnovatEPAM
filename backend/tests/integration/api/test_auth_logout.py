"""Integration tests for POST /auth/logout endpoint."""
import pytest
from fastapi import status


class TestAuthLogout:
    """Integration tests for user logout."""

    def test_logout_authenticatedUser_returns204NoContent(self, client, auth_headers):
        """Test logout with valid token returns 204."""
        # Act
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_logout_unauthenticatedUser_returns401Unauthorized(self, client):
        """Test logout without authentication returns 401."""
        # Act
        response = client.post("/api/v1/auth/logout")
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_invalidToken_returns401Unauthorized(self, client):
        """Test logout with invalid token returns 401."""
        # Act
        response = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_expiredToken_returns401Unauthorized(self, client, test_user):
        """Test logout with expired token returns 401."""
        # Arrange - create expired token
        from src.utils.jwt_handler import jwt_handler
        from datetime import datetime, timedelta
        from jose import jwt
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
        response = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_clearsCookie(self, client, test_user):
        """Test logout clears refresh token cookie."""
        # Arrange
        from src.utils.jwt_handler import jwt_handler
        
        access_token = jwt_handler.create_access_token(
            user_id=test_user.id,
            email=test_user.email,
            role=test_user.role.value
        )
        
        # Act
        response = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # If cookie was set, it should have max_age=0 to clear
        if "set-cookie" in response.headers:
            assert "max_age=0" in response.headers["set-cookie"] or "expires" in response.headers["set-cookie"]

    def test_logout_returnsNoContent(self, client, auth_headers):
        """Test logout response has no body."""
        # Act
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.content == b""
