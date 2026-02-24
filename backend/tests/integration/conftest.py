"""Conftest for integration tests - test fixtures and database setup."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from src.main import app
from src.config.database import get_db
from src.models.base import BaseModel
from src.models.user import User


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override dependency to use test database."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Create test database session."""
    # Create tables
    BaseModel.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    yield db
    db.close()
    
    # Drop tables
    BaseModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client with test database."""
    app.dependency_overrides[get_db] = override_get_db
    
    client = TestClient(app)
    yield client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db):
    """Create test user."""
    from src.utils.password_hasher import password_hasher
    
    hashed_password = password_hasher.hash_password("TestPassword123!")
    
    user = User(
        email="test@example.com",
        hashed_password=hashed_password,
        full_name="Test User",
        role="submitter"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@pytest.fixture(scope="function")
def test_admin_user(db):
    """Create test admin user."""
    from src.utils.password_hasher import password_hasher
    
    hashed_password = password_hasher.hash_password("AdminPassword123!")
    
    user = User(
        email="admin@example.com",
        hashed_password=hashed_password,
        full_name="Admin User",
        role="admin"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@pytest.fixture(scope="function")
def test_user_credentials():
    """Test user credentials."""
    return {
        "email": "newuser@example.com",
        "password": "SecurePass123!",
        "full_name": "New User"
    }


@pytest.fixture(scope="function")
def auth_headers(test_user):
    """Auth headers with valid access token."""
    from src.utils.jwt_handler import jwt_handler
    
    access_token = jwt_handler.create_access_token(
        user_id=test_user.id,
        email=test_user.email,
        role=test_user.role.value
    )
    
    return {"Authorization": f"Bearer {access_token}"}
