"""
Shared pytest fixtures for all tests.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return Mock()


@pytest.fixture
def mock_user_repo(mocker):
    """Create a mocked UserRepository."""
    repo = MagicMock()
    repo.get_by_email = MagicMock(return_value=None)
    repo.get_by_id = MagicMock(return_value=None)
    repo.create_user = MagicMock()
    repo.get_active_by_email = MagicMock(return_value=None)
    return repo


@pytest.fixture
def auth_service(mocker, mock_db, mock_user_repo):
    """
    Create AuthService instance with properly mocked dependencies.
    
    The UserRepository mock is injected after service creation to ensure
    the mock is used instead of creating a real repository instance.
    """
    from src.services.auth_service import AuthService
    
    service = AuthService(mock_db)
    service.user_repo = mock_user_repo
    return service


@pytest.fixture
def mock_jwt_handler(mocker):
    """Create a mocked JWT handler."""
    handler = MagicMock()
    handler.create_access_token = MagicMock(return_value="access_token_mock")
    handler.create_refresh_token = MagicMock(return_value="refresh_token_mock")
    handler.verify_access_token = MagicMock()
    handler.verify_refresh_token = MagicMock()
    return handler


@pytest.fixture
def mock_password_hasher(mocker):
    """Create a mocked password hasher."""
    hasher = MagicMock()
    hasher.hash_password = MagicMock(return_value="$2b$12$hashed_password_mock")
    hasher.verify_password = MagicMock(return_value=True)
    return hasher
