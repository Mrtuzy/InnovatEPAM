"""Integration tests for POST /auth/register endpoint."""
import pytest
from fastapi import status


class TestAuthRegister:
    """Integration tests for user registration."""

    def test_register_validData_returns201CreatedWithTokens(
        self,
        client,
        test_user_credentials
    ):
        """Test successful registration returns 201 with tokens."""
        # Act
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "user" in data
        assert data["user"]["email"] == test_user_credentials["email"].lower()
        assert data["user"]["full_name"] == test_user_credentials["full_name"]
        assert data["user"]["role"] == "submitter"
        assert data["token_type"] == "bearer"

    def test_register_duplicateEmail_returns409Conflict(self, client, test_user, test_user_credentials):
        """Test registering with existing email returns 409."""
        # Arrange
        test_user_credentials["email"] = test_user.email
        
        # Act
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        
        # Assert
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already registered" in response.json()["detail"].lower()

    def test_register_invalidEmail_returns422ValidationError(self, client, test_user_credentials):
        """Test registering with invalid email returns 422 validation error."""
        # Arrange
        test_user_credentials["email"] = "notanemail"
        
        # Act
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_weakPassword_returns400BadRequest(self, client, test_user_credentials):
        """Test registering with weak password (missing requirements) returns 400."""
        # Arrange - these pass Pydantic min_length but fail business logic validation
        weak_passwords = ["NoNumbers!", "nouppercase123!"]
        
        # Act & Assert
        for password in weak_passwords:
            test_user_credentials["password"] = password
            response = client.post("/api/v1/auth/register", json=test_user_credentials)
            assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_tooShortPassword_returns422ValidationError(self, client, test_user_credentials):
        """Test registering with too short password returns 422 validation error."""
        # Arrange
        test_user_credentials["password"] = "short"
        
        # Act
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_missingField_returns422ValidationError(self, client):
        """Test registering with missing required field returns validation error."""
        # Arrange
        incomplete_data = {"email": "test@example.com"}
        
        # Act
        response = client.post("/api/v1/auth/register", json=incomplete_data)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_validData_returnsUserWithoutPassword(self, client, test_user_credentials):
        """Test registered user response doesn't include password."""
        # Act
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        user = response.json()["user"]
        assert "hashed_password" not in user
        assert "password" not in user

    def test_register_validData_userIsActive(self, client, test_user_credentials):
        """Test newly registered user is active."""
        # Act
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        user = response.json()["user"]
        assert user["is_active"] is True

    def test_register_validData_userRoleIsSubmitter(self, client, test_user_credentials):
        """Test newly registered user is assigned submitter role."""
        # Act
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        user = response.json()["user"]
        assert user["role"] == "submitter"

    def test_register_validData_emailStoredLowercase(self, client, test_user_credentials):
        """Test email is stored in lowercase."""
        # Arrange
        test_user_credentials["email"] = "Test@EXAMPLE.COM"
        
        # Act
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        user = response.json()["user"]
        assert user["email"] == "test@example.com"

    def test_register_accessTokenIsValid(self, client, test_user_credentials):
        """Test returned access token is valid JWT."""
        # Act
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        access_token = response.json()["access_token"]
        
        # Token should be JWT format (3 parts separated by .)
        assert access_token.count(".") == 2

    def test_register_refreshTokenIsValid(self, client, test_user_credentials):
        """Test returned refresh token is valid JWT."""
        # Act
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        refresh_token = response.json()["refresh_token"]
        
        # Token should be JWT format (3 parts separated by .)
        assert refresh_token.count(".") == 2
