"""
Unit tests for AuthService login logic.

Tests cover:
- Successful login with valid credentials
- Failed login with invalid credentials
- Generic error messages for security
- Token generation
- Account not found handling
"""
import pytest
from uuid import uuid4
from unittest.mock import MagicMock

# These imports will fail until implementation
from src.services.auth_service import AuthService
from src.models.user import UserRole


class TestAuthServiceLogin:
    """Test suite for AuthService login logic."""

    def test_login_validCredentials_returnsUserAndTokens(
        self, auth_service, mock_user_repo, mocker
    ):
        """Test login with valid credentials returns user and tokens."""
        # Arrange
        email = "test@example.com"
        password = "SecurePass123!"
        
        mock_user = MagicMock()
        mock_user.id = uuid4()
        mock_user.email = email
        mock_user.role = UserRole.SUBMITTER
        mock_user.hashed_password = "$2b$12$hash"
        mock_user.is_active = True
        
        mock_user_repo.get_by_email.return_value = mock_user
        mocker.patch('src.services.auth_service.password_hasher.verify_password', return_value=True)
        
        # Act
        result = auth_service.authenticate_user(email, password)
        
        # Assert
        assert result is not None
        assert result["user"] == mock_user
        assert "access_token" in result
        assert "refresh_token" in result
        assert isinstance(result["access_token"], str)
        assert isinstance(result["refresh_token"], str)

    def test_login_incorrectPassword_raisesValueError(
        self, auth_service, mock_user_repo, mocker
    ):
        """Test login with incorrect password raises ValueError."""
        # Arrange
        email = "test@example.com"
        password = "WrongPassword!"
        
        mock_user = MagicMock()
        mock_user.hashed_password = "$2b$12$hash"
        mock_user.is_active = True
        
        mock_user_repo.get_by_email.return_value = mock_user
        mocker.patch('src.services.auth_service.password_hasher.verify_password', return_value=False)
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid credentials"):
            auth_service.authenticate_user(email, password)

    def test_login_nonExistentEmail_raisesValueError(
        self, auth_service, mock_user_repo
    ):
        """Test login with non-existent email raises ValueError."""
        # Arrange
        email = "nonexistent@example.com"
        password = "SecurePass123!"
        
        mock_user_repo.get_by_email.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid credentials"):
            auth_service.authenticate_user(email, password)

    def test_login_genericErrorMessage_doesNotRevealUserExistence(
        self, auth_service, mock_user_repo
    ):
        """Test error message doesn't reveal if email exists (security)."""
        # Arrange - Non-existent email
        email = "nonexistent@example.com"
        password = "SecurePass123!"
        
        mock_user_repo.get_by_email.return_value = None
        
        # Act & Assert
        try:
            auth_service.authenticate_user(email, password)
            assert False, "Should raise ValueError"
        except ValueError as e:
            # Error should not say "email not found"
            assert "email" not in str(e).lower()
            assert "not found" not in str(e).lower()
            assert "Invalid credentials" in str(e)

    def test_login_inactiveUser_raisesValueError(
        self, auth_service, mock_user_repo
    ):
        """Test login with inactive user raises ValueError."""
        # Arrange
        email = "inactive@example.com"
        password = "SecurePass123!"
        
        mock_user = MagicMock()
        mock_user.is_active = False
        
        mock_user_repo.get_by_email.return_value = mock_user
        
        # Act & Assert
        with pytest.raises(ValueError, match="Account.*inactive|disabled"):
            auth_service.authenticate_user(email, password)

    def test_login_validCredentials_generatesAccessToken(
        self, auth_service, mock_user_repo, mocker
    ):
        """Test login generates valid access token."""
        # Arrange
        mock_user = MagicMock()
        mock_user.id = uuid4()
        mock_user.email = "test@example.com"
        mock_user.role = UserRole.ADMIN
        mock_user.is_active = True
        
        mock_user_repo.get_by_email.return_value = mock_user
        mocker.patch('src.services.auth_service.password_hasher.verify_password', return_value=True)
        
        # Act
        result = auth_service.authenticate_user("test@example.com", "SecurePass123!")
        
        # Assert
        access_token = result["access_token"]
        assert access_token is not None
        assert len(access_token) > 0
        assert access_token.count(".") == 2  # JWT format

    def test_login_validCredentials_generatesRefreshToken(
        self, auth_service, mock_user_repo, mocker
    ):
        """Test login generates valid refresh token."""
        # Arrange
        mock_user = MagicMock()
        mock_user.id = uuid4()
        mock_user.email = "test@example.com"
        mock_user.role = UserRole.SUBMITTER
        mock_user.is_active = True
        
        mock_user_repo.get_by_email.return_value = mock_user
        mocker.patch('src.services.auth_service.password_hasher.verify_password', return_value=True)
        
        # Act
        result = auth_service.authenticate_user("test@example.com", "SecurePass123!")
        
        # Assert
        refresh_token = result["refresh_token"]
        assert refresh_token is not None
        assert len(refresh_token) > 0
        assert refresh_token.count(".") == 2  # JWT format

    def test_login_caseInsensitiveEmail_authenticatesSuccessfully(
        self, auth_service, mock_user_repo, mocker
    ):
        """Test login with case-insensitive email works."""
        # Arrange
        stored_email = "test@example.com"
        login_email = "TEST@EXAMPLE.COM"
        
        mock_user = MagicMock()
        mock_user.id = uuid4()
        mock_user.email = stored_email
        mock_user.role = UserRole.SUBMITTER
        mock_user.is_active = True
        
        mock_user_repo.get_by_email.return_value = mock_user
        mocker.patch('src.services.auth_service.password_hasher.verify_password', return_value=True)
        
        # Act
        result = auth_service.authenticate_user(login_email, "SecurePass123!")
        
        # Assert
        assert result is not None
        assert result["user"].email.lower() == login_email.lower()

    def test_login_emptyPassword_raisesValueError(self, auth_service):
        """Test login with empty password raises ValueError."""
        # Arrange
        email = "test@example.com"
        password = ""
        
        # Act & Assert
        with pytest.raises(ValueError):
            auth_service.authenticate_user(email, password)
