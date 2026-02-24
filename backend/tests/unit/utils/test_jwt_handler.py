"""
Unit tests for JWT handler utility.

Tests cover:
- Access token creation
- Refresh token creation
- Token validation
- Token expiration
- Token decoding
"""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from src.utils.jwt_handler import jwt_handler
from src.config.settings import get_settings

settings = get_settings()


class TestJWTHandler:
    """Test suite for JWT token handler."""

    def test_createAccessToken_validData_returnsToken(self):
        """Test creating access token with valid data."""
        # Arrange
        user_id = uuid4()
        email = "test@example.com"
        role = "submitter"
        
        # Act
        token = jwt_handler.create_access_token(user_id, email, role)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
        assert token.count(".") == 2  # JWT has 3 parts

    def test_createAccessToken_validData_containsCorrectPayload(self):
        """Test access token contains correct user data."""
        # Arrange
        user_id = uuid4()
        email = "test@example.com"
        role = "admin"
        
        # Act
        token = jwt_handler.create_access_token(user_id, email, role)
        payload = jwt_handler.decode_token(token)
        
        # Assert
        assert payload is not None
        assert payload["sub"] == str(user_id)
        assert payload["email"] == email
        assert payload["role"] == role
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload

    def test_createRefreshToken_validUserId_returnsToken(self):
        """Test creating refresh token with valid user ID."""
        # Arrange
        user_id = uuid4()
        
        # Act
        token = jwt_handler.create_refresh_token(user_id)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_createRefreshToken_validUserId_containsCorrectPayload(self):
        """Test refresh token contains correct data."""
        # Arrange
        user_id = uuid4()
        
        # Act
        token = jwt_handler.create_refresh_token(user_id)
        payload = jwt_handler.decode_token(token)
        
        # Assert
        assert payload is not None
        assert payload["sub"] == str(user_id)
        assert payload["type"] == "refresh"
        assert "exp" in payload
        assert "iat" in payload
        assert "email" not in payload  # Refresh token minimal

    def test_decodeToken_validToken_returnsPayload(self):
        """Test decoding valid token returns payload."""
        # Arrange
        user_id = uuid4()
        token = jwt_handler.create_access_token(user_id, "test@example.com", "submitter")
        
        # Act
        payload = jwt_handler.decode_token(token)
        
        # Assert
        assert payload is not None
        assert isinstance(payload, dict)
        assert payload["sub"] == str(user_id)

    def test_decodeToken_invalidToken_returnsNone(self):
        """Test decoding invalid token returns None."""
        # Arrange
        invalid_token = "invalid.token.here"
        
        # Act
        payload = jwt_handler.decode_token(invalid_token)
        
        # Assert
        assert payload is None

    def test_decodeToken_tamperedToken_returnsNone(self):
        """Test decoding tampered token returns None."""
        # Arrange
        user_id = uuid4()
        token = jwt_handler.create_access_token(user_id, "test@example.com", "submitter")
        tampered_token = token[:-5] + "12345"  # Modify signature
        
        # Act
        payload = jwt_handler.decode_token(tampered_token)
        
        # Assert
        assert payload is None

    def test_verifyAccessToken_validAccessToken_returnsPayload(self):
        """Test verifying valid access token returns payload."""
        # Arrange
        user_id = uuid4()
        token = jwt_handler.create_access_token(user_id, "test@example.com", "submitter")
        
        # Act
        payload = jwt_handler.verify_access_token(token)
        
        # Assert
        assert payload is not None
        assert payload["type"] == "access"
        assert payload["sub"] == str(user_id)

    def test_verifyAccessToken_refreshToken_returnsNone(self):
        """Test verifying refresh token as access token returns None."""
        # Arrange
        user_id = uuid4()
        refresh_token = jwt_handler.create_refresh_token(user_id)
        
        # Act
        payload = jwt_handler.verify_access_token(refresh_token)
        
        # Assert
        assert payload is None  # Wrong token type

    def test_verifyRefreshToken_validRefreshToken_returnsPayload(self):
        """Test verifying valid refresh token returns payload."""
        # Arrange
        user_id = uuid4()
        token = jwt_handler.create_refresh_token(user_id)
        
        # Act
        payload = jwt_handler.verify_refresh_token(token)
        
        # Assert
        assert payload is not None
        assert payload["type"] == "refresh"
        assert payload["sub"] == str(user_id)

    def test_verifyRefreshToken_accessToken_returnsNone(self):
        """Test verifying access token as refresh token returns None."""
        # Arrange
        user_id = uuid4()
        access_token = jwt_handler.create_access_token(user_id, "test@example.com", "submitter")
        
        # Act
        payload = jwt_handler.verify_refresh_token(access_token)
        
        # Assert
        assert payload is None  # Wrong token type

    def test_createAccessToken_defaultExpiration_hasCorrectTTL(self):
        """Test access token has correct expiration time."""
        # Arrange
        user_id = uuid4()
        
        # Act
        token = jwt_handler.create_access_token(user_id, "test@example.com", "submitter")
        payload = jwt_handler.decode_token(token)
        
        # Assert
        exp_time = datetime.fromtimestamp(payload["exp"])
        iat_time = datetime.fromtimestamp(payload["iat"])
        diff = exp_time - iat_time
        
        # Should be approximately 15 minutes
        assert diff.total_seconds() >= 14 * 60  # At least 14 min
        assert diff.total_seconds() <= 16 * 60  # At most 16 min

    def test_createRefreshToken_defaultExpiration_hasCorrectTTL(self):
        """Test refresh token has correct expiration time."""
        # Arrange
        user_id = uuid4()
        
        # Act
        token = jwt_handler.create_refresh_token(user_id)
        payload = jwt_handler.decode_token(token)
        
        # Assert
        exp_time = datetime.fromtimestamp(payload["exp"])
        iat_time = datetime.fromtimestamp(payload["iat"])
        diff = exp_time - iat_time
        
        # Should be approximately 7 days
        assert diff.total_seconds() >= 6.9 * 24 * 60 * 60  # At least 6.9 days
        assert diff.total_seconds() <= 7.1 * 24 * 60 * 60  # At most 7.1 days
