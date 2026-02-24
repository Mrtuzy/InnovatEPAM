"""
Unit tests for password hasher utility.

Tests cover:
- Password hashing with bcrypt
- Password verification
- Hash uniqueness (salt)
- Invalid input handling
"""
import pytest

from src.utils.password_hasher import password_hasher


class TestPasswordHasher:
    """Test suite for password hashing utility."""

    def test_hashPassword_validPassword_returnsHashedString(self):
        """Test hashing a valid password returns hashed string."""
        # Arrange
        password = "SecurePassword123!"
        
        # Act
        hashed = password_hasher.hash_password(password)
        
        # Assert
        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) == 60  # bcrypt hash length
        assert hashed.startswith("$2b$")  # bcrypt prefix
        assert hashed != password  # Not plain text

    def test_hashPassword_samePasswordTwice_returnsDifferentHashes(self):
        """Test hashing same password twice returns different hashes due to salt."""
        # Arrange
        password = "SecurePassword123!"
        
        # Act
        hash1 = password_hasher.hash_password(password)
        hash2 = password_hasher.hash_password(password)
        
        # Assert
        assert hash1 != hash2  # Different salts
        assert len(hash1) == len(hash2)

    def test_hashPassword_emptyPassword_raisesError(self):
        """Test hashing empty password raises error."""
        # Arrange
        password = ""
        
        # Act & Assert
        with pytest.raises(ValueError):
            password_hasher.hash_password(password)

    def test_verifyPassword_correctPassword_returnsTrue(self):
        """Test verifying correct password returns True."""
        # Arrange
        password = "SecurePassword123!"
        hashed = password_hasher.hash_password(password)
        
        # Act
        result = password_hasher.verify_password(password, hashed)
        
        # Assert
        assert result is True

    def test_verifyPassword_incorrectPassword_returnsFalse(self):
        """Test verifying incorrect password returns False."""
        # Arrange
        password = "SecurePassword123!"
        wrong_password = "WrongPassword456!"
        hashed = password_hasher.hash_password(password)
        
        # Act
        result = password_hasher.verify_password(wrong_password, hashed)
        
        # Assert
        assert result is False

    def test_verifyPassword_emptyPassword_returnsFalse(self):
        """Test verifying empty password returns False."""
        # Arrange
        password = "SecurePassword123!"
        hashed = password_hasher.hash_password(password)
        
        # Act
        result = password_hasher.verify_password("", hashed)
        
        # Assert
        assert result is False

    def test_verifyPassword_invalidHash_returnsFalse(self):
        """Test verifying against invalid hash returns False."""
        # Arrange
        password = "SecurePassword123!"
        invalid_hash = "not_a_valid_hash"
        
        # Act
        result = password_hasher.verify_password(password, invalid_hash)
        
        # Assert
        assert result is False

    def test_verifyPassword_modifiedHash_returnsFalse(self):
        """Test verifying against modified hash returns False."""
        # Arrange
        password = "SecurePassword123!"
        hashed = password_hasher.hash_password(password)
        modified_hash = hashed[:-1] + "X"  # Modify last character
        
        # Act
        result = password_hasher.verify_password(password, modified_hash)
        
        # Assert
        assert result is False

    def test_hashPassword_unicodeCharacters_hashesSuccessfully(self):
        """Test hashing password with unicode characters."""
        # Arrange
        password = "Пароль123!"  # Cyrillic + numbers + special
        
        # Act
        hashed = password_hasher.hash_password(password)
        
        # Assert
        assert hashed is not None
        assert password_hasher.verify_password(password, hashed) is True

    def test_hashPassword_longPassword_hashesSuccessfully(self):
        """Test hashing password longer than bcrypt limit (72 bytes)."""
        # Arrange - 200 characters = > 72 bytes when encoded
        password = "A" * 200
        
        # Act
        hashed = password_hasher.hash_password(password)
        
        # Assert - should hash successfully (truncated internally)
        assert hashed is not None
        # Verify should work with original long password (gets truncated same way)
        assert password_hasher.verify_password(password, hashed) is True
