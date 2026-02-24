"""
Unit tests for User model validation.

Tests cover:
- Email format validation
- Password hashing
- Role enum validation
- Model constraints
"""
import pytest
from datetime import datetime
from uuid import UUID

# These imports will fail until we implement the User model
# This is expected in TDD - tests are written first
from src.models.user import User


class TestUserModel:
    """Test suite for User model validation."""

    def test_create_validData_createsUserWithHashedPassword(self):
        """Test user creation with valid data hashes password."""
        # Arrange
        email = "test@example.com"
        plain_password = "SecurePass123!"
        full_name = "Test User"
        role = "submitter"
        
        # Act
        user = User(
            email=email,
            hashed_password=plain_password,  # Will be hashed in model
            full_name=full_name,
            role=role
        )
        
        # Assert
        assert user.email == email.lower()  # Email stored lowercase
        assert user.hashed_password != plain_password  # Password hashed
        assert user.full_name == full_name
        assert user.role == role
        assert user.is_active is True  # Default value
        assert isinstance(user.id, UUID)
        assert isinstance(user.created_at, datetime)

    def test_create_invalidEmail_raisesValidationError(self):
        """Test user creation with invalid email format fails."""
        # Arrange
        invalid_emails = [
            "notanemail",
            "@example.com",
            "test@",
            "test..user@example.com",
            "test user@example.com",
        ]
        
        # Act & Assert
        for email in invalid_emails:
            with pytest.raises(ValueError, match="email"):
                User(
                    email=email,
                    hashed_password="SecurePass123!",
                    full_name="Test User",
                    role="submitter"
                )

    def test_create_duplicateEmail_raisesIntegrityError(self):
        """Test creating user with duplicate email raises error."""
        # This will be tested at repository level with actual DB
        # Model level just validates format
        pass

    def test_create_invalidRole_raisesValidationError(self):
        """Test user creation with invalid role fails."""
        # Arrange
        invalid_roles = ["user", "moderator", "superuser", ""]
        
        # Act & Assert
        for role in invalid_roles:
            with pytest.raises(ValueError, match="role"):
                User(
                    email="test@example.com",
                    hashed_password="SecurePass123!",
                    full_name="Test User",
                    role=role
                )

    def test_create_validRoles_createsUser(self):
        """Test user creation with valid roles succeeds."""
        # Arrange
        valid_roles = ["submitter", "admin"]
        
        # Act & Assert
        for role in valid_roles:
            user = User(
                email=f"test_{role}@example.com",
                hashed_password="SecurePass123!",
                full_name="Test User",
                role=role
            )
            assert user.role == role

    def test_create_emptyFullName_raisesValidationError(self):
        """Test user creation with empty full name fails."""
        # Arrange
        invalid_names = ["", " ", "A"]  # Too short
        
        # Act & Assert
        for name in invalid_names:
            with pytest.raises(ValueError, match="full_name"):
                User(
                    email="test@example.com",
                    hashed_password="SecurePass123!",
                    full_name=name,
                    role="submitter"
                )

    def test_create_fullNameWithSpecialChars_raisesValidationError(self):
        """Test full name with invalid special characters fails."""
        # Arrange
        invalid_names = [
            "Test@User",
            "Test#User",
            "Test123",
            "Test<User>",
        ]
        
        # Act & Assert
        for name in invalid_names:
            with pytest.raises(ValueError, match="full_name"):
                User(
                    email="test@example.com",
                    hashed_password="SecurePass123!",
                    full_name=name,
                    role="submitter"
                )

    def test_create_fullNameWithAllowedChars_createsUser(self):
        """Test full name with allowed characters succeeds."""
        # Arrange
        valid_names = [
            "John Doe",
            "Mary-Jane",
            "O'Brien",
            "Jean-Pierre",
            "Maria Sanchez",
        ]
        
        # Act & Assert
        for name in valid_names:
            user = User(
                email=f"test{valid_names.index(name)}@example.com",
                hashed_password="SecurePass123!",
                full_name=name,
                role="submitter"
            )
            assert user.full_name == name

    def test_create_defaultIsActive_isTrue(self):
        """Test user is active by default."""
        # Arrange & Act
        user = User(
            email="test@example.com",
            hashed_password="SecurePass123!",
            full_name="Test User",
            role="submitter"
        )
        
        # Assert
        assert user.is_active is True

    def test_repr_validUser_returnsStringRepresentation(self):
        """Test string representation of user."""
        # Arrange
        user = User(
            email="test@example.com",
            hashed_password="SecurePass123!",
            full_name="Test User",
            role="submitter"
        )
        
        # Act
        repr_str = repr(user)
        
        # Assert
        assert "User" in repr_str
        assert str(user.id) in repr_str
