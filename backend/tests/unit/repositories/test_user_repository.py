"""
Unit tests for UserRepository CRUD operations.

Tests cover:
- Create user
- Get user by email
- Get user by ID
- Unique email constraint
- Case-insensitive email lookup
"""
import pytest
from uuid import uuid4
from sqlalchemy.exc import IntegrityError

# These imports will fail until implementation
from src.models.user import User
from src.repositories.user_repository import UserRepository


class TestUserRepository:
    """Test suite for UserRepository CRUD operations."""

    @pytest.fixture
    def mock_db_session(self, mocker):
        """Mock database session."""
        return mocker.Mock()

    @pytest.fixture
    def user_repository(self, mock_db_session):
        """Create UserRepository instance with mock session."""
        return UserRepository(mock_db_session)

    def test_createUser_validData_returnsUser(self, user_repository, mock_db_session):
        """Test creating user with valid data returns user."""
        # Arrange
        email = "test@example.com"
        hashed_password = "$2b$12$hashedpassword"
        full_name = "Test User"
        role = "submitter"
        
        # Mock behavior
        expected_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role
        )
        mock_db_session.add = lambda x: None
        mock_db_session.commit = lambda: None
        mock_db_session.refresh = lambda x: None
        
        # Act
        user = user_repository.create_user(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role
        )
        
        # Assert
        assert user is not None
        assert user.email == email.lower()
        assert user.hashed_password == hashed_password
        assert user.full_name == full_name
        assert user.role == role

    def test_createUser_duplicateEmail_raisesIntegrityError(self, user_repository, mock_db_session):
        """Test creating user with duplicate email raises IntegrityError."""
        # Arrange
        email = "duplicate@example.com"
        
        # Mock IntegrityError on commit
        mock_db_session.add = lambda x: None
        mock_db_session.commit = lambda: (_ for _ in ()).throw(
            IntegrityError("duplicate key", None, None)
        )
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            user_repository.create_user(
                email=email,
                hashed_password="$2b$12$hash",
                full_name="Test",
                role="submitter"
            )

    def test_getByEmail_existingUser_returnsUser(self, user_repository, mock_db_session):
        """Test getting user by email returns user."""
        # Arrange
        email = "test@example.com"
        expected_user = User(
            email=email,
            hashed_password="$2b$12$hash",
            full_name="Test User",
            role="submitter"
        )
        
        # Mock query
        mock_query = mock_db_session.query.return_value
        mock_query.filter.return_value.first.return_value = expected_user
        
        # Act
        user = user_repository.get_by_email(email)
        
        # Assert
        assert user is not None
        assert user.email == email.lower()

    def test_getByEmail_nonExistentUser_returnsNone(self, user_repository, mock_db_session):
        """Test getting non-existent user by email returns None."""
        # Arrange
        email = "nonexistent@example.com"
        
        # Mock query returning None
        mock_query = mock_db_session.query.return_value
        mock_query.filter.return_value.first.return_value = None
        
        # Act
        user = user_repository.get_by_email(email)
        
        # Assert
        assert user is None

    def test_getByEmail_caseInsensitive_returnsUser(self, user_repository, mock_db_session):
        """Test email lookup is case-insensitive."""
        # Arrange
        stored_email = "test@example.com"
        lookup_email = "TEST@EXAMPLE.COM"
        expected_user = User(
            email=stored_email,
            hashed_password="$2b$12$hash",
            full_name="Test User",
            role="submitter"
        )
        
        # Mock query
        mock_query = mock_db_session.query.return_value
        mock_query.filter.return_value.first.return_value = expected_user
        
        # Act
        user = user_repository.get_by_email(lookup_email)
        
        # Assert
        assert user is not None
        assert user.email.lower() == lookup_email.lower()

    def test_getById_existingUser_returnsUser(self, user_repository, mock_db_session):
        """Test getting user by ID returns user."""
        # Arrange
        user_id = uuid4()
        expected_user = User(
            email="test@example.com",
            hashed_password="$2b$12$hash",
            full_name="Test User",
            role="submitter"
        )
        expected_user.id = user_id
        
        # Mock query
        mock_query = mock_db_session.query.return_value
        mock_query.filter.return_value.first.return_value = expected_user
        
        # Act
        user = user_repository.get_by_id(user_id)
        
        # Assert
        assert user is not None
        assert user.id == user_id

    def test_getById_nonExistentUser_returnsNone(self, user_repository, mock_db_session):
        """Test getting non-existent user by ID returns None."""
        # Arrange
        user_id = uuid4()
        
        # Mock query returning None
        mock_query = mock_db_session.query.return_value
        mock_query.filter.return_value.first.return_value = None
        
        # Act
        user = user_repository.get_by_id(user_id)
        
        # Assert
        assert user is None

    def test_createUser_emailStoredLowercase_convertsToLowercase(self, user_repository, mock_db_session):
        """Test email is stored in lowercase."""
        # Arrange
        email = "Test@EXAMPLE.COM"
        
        # Mock behavior
        mock_db_session.add = lambda x: None
        mock_db_session.commit = lambda: None
        mock_db_session.refresh = lambda x: None
        
        # Act
        user = user_repository.create_user(
            email=email,
            hashed_password="$2b$12$hash",
            full_name="Test User",
            role="submitter"
        )
        
        # Assert
        assert user.email == email.lower()
        assert user.email == "test@example.com"
