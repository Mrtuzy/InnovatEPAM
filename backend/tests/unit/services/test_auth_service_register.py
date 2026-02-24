"""
Unit tests for AuthService registration logic.

Tests cover:
- Successful registration
- Duplicate email validation
- Password complexity requirements
- Input validation
- Email format validation
"""
import pytest
from uuid import UUID, uuid4
from unittest.mock import MagicMock

# These imports will fail until implementation
from src.services.auth_service import AuthService
from src.schemas.user_schemas import RegisterRequest
from src.models.user import User, UserRole


class TestAuthServiceRegister:
    """Test suite for AuthService registration logic."""

    def test_register_validData_returnsUser(self, auth_service, mock_user_repo):
        """Test registering with valid data returns user."""
        # Arrange
        request = RegisterRequest(
            email="test@example.com",
            password="SecurePass123!",
            full_name="Test User"
        )
        
        # Mock repository returning None (email not taken)
        mock_user_repo.get_by_email.return_value = None
        
        # Mock create_user to return a real User object
        created_user = User(
            email=request.email,
            hashed_password="$2b$12$hashed_password_mock",
            full_name=request.full_name,
            role="submitter"
        )
        mock_user_repo.create_user.return_value = created_user
        
        # Act
        user = auth_service.register_user(
            email=request.email,
            password=request.password,
            full_name=request.full_name
        )
        
        # Assert
        assert user is not None
        assert user.email == request.email.lower()
        assert user.full_name == request.full_name
        assert user.role == UserRole.SUBMITTER  # Default role
        assert isinstance(user.id, UUID)

    def test_register_duplicateEmail_raisesValueError(self, auth_service, mock_user_repo):
        """Test registering with duplicate email raises ValueError."""
        # Arrange
        email = "duplicate@example.com"
        
        # Mock repository returning existing user
        existing_user = MagicMock()
        mock_user_repo.get_by_email.return_value = existing_user
        
        # Act & Assert
        with pytest.raises(ValueError, match="email.*exists|already.*registered"):
            auth_service.register_user(
                email=email,
                password="SecurePass123!",
                full_name="Test User"
            )

    def test_register_invalidEmail_raisesValueError(self, auth_service):
        """Test registering with invalid email raises ValueError."""
        # Arrange
        invalid_emails = [
            "notanemail",
            "@example.com",
            "test@",
            "test..user@example.com",
        ]
        
        # Act & Assert  
        for email in invalid_emails:
            with pytest.raises(ValueError, match="email"):
                auth_service.register_user(
                    email=email,
                    password="SecurePass123!",
                    full_name="Test User"
                )

    def test_register_weakPassword_raisesValueError(self, auth_service):
        """Test registering with weak password raises ValueError."""
        # Arrange - passwords that don't meet requirements
        weak_passwords = [
            "short",  # Too short
            "nouppercase123!",  # No uppercase
            "NOLOWERCASE123!",  # No lowercase
            "NoNumbers!",  # No numbers
            "NoSpecial123",  # No special characters
            "Simple1",  # Too short even with requirements
        ]
        
        # Act & Assert
        for password in weak_passwords:
            with pytest.raises(ValueError, match="password"):
                auth_service.register_user(
                    email="test@example.com",
                    password=password,
                    full_name="Test User"
                )

    def test_register_validPassword_meetsComplexityRequirements(self, auth_service, mock_user_repo):
        """Test password complexity requirements are enforced."""
        # Arrange
        valid_passwords = [
            "SecurePass123!",
            "MyP@ssw0rd",
            "C0mpl3x!Pass",
            "Str0ng#Password",
        ]
        
        # Mock repository
        mock_user_repo.get_by_email.return_value = None
        
        # Mock create_user to return User objects
        def create_user_side_effect(**kwargs):
            return User(
                email=kwargs['email'],
                hashed_password=kwargs['hashed_password'],
                full_name=kwargs['full_name'],
                role=kwargs.get('role', 'submitter')
            )
        mock_user_repo.create_user.side_effect = create_user_side_effect
        
        # Act & Assert
        for password in valid_passwords:
            user = auth_service.register_user(
                email=f"test{valid_passwords.index(password)}@example.com",
                password=password,
                full_name="Test User"
            )
            assert user is not None

    def test_register_validData_passwordIsHashed(self, auth_service, mock_user_repo):
        """Test password is hashed before storage."""
        # Arrange
        plain_password = "SecurePass123!"
        mock_user_repo.get_by_email.return_value = None
        
        # Capture the arguments sent to create_user
        def create_user_side_effect(**kwargs):
            user = User(
                email=kwargs['email'],
                hashed_password=kwargs['hashed_password'],
                full_name=kwargs['full_name'],
                role=kwargs.get('role', 'submitter')
            )
            return user
        mock_user_repo.create_user.side_effect = create_user_side_effect
        
        # Act
        user = auth_service.register_user(
            email="test@example.com",
            password=plain_password,
            full_name="Test User"
        )
        
        # Assert
        assert user.hashed_password != plain_password
        assert len(user.hashed_password) == 60  # bcrypt hash length
        assert user.hashed_password.startswith("$2b$")

    def test_register_validData_defaultRoleIsSubmitter(self, auth_service, mock_user_repo):
        """Test default role is submitter."""
        # Arrange
        mock_user_repo.get_by_email.return_value = None
        
        def create_user_side_effect(**kwargs):
            return User(
                email=kwargs['email'],
                hashed_password=kwargs['hashed_password'],
                full_name=kwargs['full_name'],
                role=kwargs.get('role', 'submitter')
            )
        mock_user_repo.create_user.side_effect = create_user_side_effect
        
        # Act
        user = auth_service.register_user(
            email="test@example.com",
            password="SecurePass123!",
            full_name="Test User"
        )
        
        # Assert
        assert user.role == UserRole.SUBMITTER

    def test_register_emptyFullName_raisesValueError(self, auth_service):
        """Test registering with empty full name raises ValueError."""
        # Arrange
        invalid_names = ["", " ", "A"]
        
        # Act & Assert
        for name in invalid_names:
            with pytest.raises(ValueError, match="full_name|name"):
                auth_service.register_user(
                    email="test@example.com",
                    password="SecurePass123!",
                    full_name=name
                )

    def test_register_emailCaseInsensitive_convertsToLowercase(self, auth_service, mock_user_repo):
        """Test email is converted to lowercase."""
        # Arrange
        email = "Test@EXAMPLE.COM"
        mock_user_repo.get_by_email.return_value = None
        
        def create_user_side_effect(**kwargs):
            return User(
                email=kwargs['email'],
                hashed_password=kwargs['hashed_password'],
                full_name=kwargs['full_name'],
                role=kwargs.get('role', 'submitter')
            )
        mock_user_repo.create_user.side_effect = create_user_side_effect
        
        # Act
        user = auth_service.register_user(
            email=email,
            password="SecurePass123!",
            full_name="Test User"
        )
        
        # Assert
        assert user.email == email.lower()
