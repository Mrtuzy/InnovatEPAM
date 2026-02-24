"""
Unit tests for authentication middleware.

Tests cover:
- Valid token validation
- Expired token handling
- Missing token handling
- Invalid token handling
- Tampered token handling
"""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

# These imports will fail until implementation
from src.api.middleware.auth_middleware import auth_middleware


class TestAuthMiddleware:
    """Test suite for authentication middleware."""

    @pytest.fixture
    def valid_access_token(self, mocker):
        """Generate valid access token for testing."""
        from src.utils.jwt_handler import jwt_handler
        user_id = uuid4()
        return jwt_handler.create_access_token(user_id, "test@example.com", "submitter")

    @pytest.fixture
    def expired_token(self, mocker):
        """Generate expired token for testing."""
        # Mock JWT to create expired token
        mocker.patch('src.utils.jwt_handler.settings.ACCESS_TOKEN_EXPIRE_MINUTES', -1)
        from src.utils.jwt_handler import jwt_handler
        user_id = uuid4()
        return jwt_handler.create_access_token(user_id, "test@example.com", "submitter")

    def test_getCurrentUserId_validToken_returnsUserId(self, valid_access_token):
        """Test valid token returns user ID."""
        # Arrange
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=valid_access_token
        )
        
        # Act
        user_id = auth_middleware.get_current_user_id(credentials)
        
        # Assert
        assert user_id is not None
        assert isinstance(user_id, str)
        # Should be valid UUID string
        from uuid import UUID
        UUID(user_id)  # Will raise if invalid

    def test_getCurrentUserId_invalidToken_raises401(self):
        """Test invalid token raises 401 Unauthorized."""
        # Arrange
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid.token.here"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_middleware.get_current_user_id(credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "invalid" in exc_info.value.detail.lower()

    def test_getCurrentUserId_expiredToken_raises401(self, expired_token):
        """Test expired token raises 401 Unauthorized."""
        # Arrange
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=expired_token
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_middleware.get_current_user_id(credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_getCurrentUserId_missingToken_raises401(self):
        """Test missing token raises 401 Unauthorized."""
        # Arrange
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=""
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_middleware.get_current_user_id(credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_getCurrentUserId_tamperedToken_raises401(self, valid_access_token):
        """Test tampered token raises 401 Unauthorized."""
        # Arrange
        tampered_token = valid_access_token[:-5] + "12345"
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=tampered_token
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_middleware.get_current_user_id(credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_getCurrentUserPayload_validToken_returnsPayload(self, valid_access_token):
        """Test valid token returns full user payload."""
        # Arrange
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=valid_access_token
        )
        
        # Act
        payload = auth_middleware.get_current_user_payload(credentials)
        
        # Assert
        assert payload is not None
        assert "id" in payload
        assert "email" in payload
        assert "role" in payload
        assert payload["email"] == "test@example.com"
        assert payload["role"] in ["submitter", "admin"]

    def test_getCurrentUserPayload_invalidToken_raises401(self):
        """Test invalid token raises 401 when getting payload."""
        # Arrange
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid.token"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_middleware.get_current_user_payload(credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_getCurrentUserPayload_refreshToken_raises401(self):
        """Test refresh token cannot be used for authentication."""
        # Arrange
        from src.utils.jwt_handler import jwt_handler
        user_id = uuid4()
        refresh_token = jwt_handler.create_refresh_token(user_id)
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=refresh_token
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_middleware.get_current_user_payload(credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authMiddleware_hasWWWAuthenticateHeader_returns401WithHeader(self):
        """Test 401 responses include WWW-Authenticate header."""
        # Arrange
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_middleware.get_current_user_id(credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.headers is not None
        assert "WWW-Authenticate" in exc_info.value.headers
        assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"

    def test_getCurrentUserId_tokenWithoutSub_raises401(self, mocker):
        """Test token without 'sub' claim raises 401."""
        # Arrange - create token without 'sub' claim
        from jose import jwt
        from src.config.settings import get_settings
        settings = get_settings()
        
        payload = {
            "email": "test@example.com",
            "role": "submitter",
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }
        # Missing 'sub' claim
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_middleware.get_current_user_id(credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
