"""Password hashing utility using bcrypt."""
import bcrypt

from src.config.settings import get_settings

settings = get_settings()


class PasswordHasher:
    """Password hashing and verification using bcrypt."""
    
    # bcrypt max password length is 72 bytes
    MAX_PASSWORD_LENGTH = 72
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password as string
            
        Raises:
            ValueError: If password is empty
        """
        if not password:
            raise ValueError("Password cannot be empty")
        
        # Truncate to bcrypt max length if needed
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > PasswordHasher.MAX_PASSWORD_LENGTH:
            password_bytes = password_bytes[:PasswordHasher.MAX_PASSWORD_LENGTH]
        
        salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str
    ) -> bool:
        """
        Verify password against hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password to compare
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            # Truncate to bcrypt max length if needed
            password_bytes = plain_password.encode('utf-8')
            if len(password_bytes) > PasswordHasher.MAX_PASSWORD_LENGTH:
                password_bytes = password_bytes[:PasswordHasher.MAX_PASSWORD_LENGTH]
            
            return bcrypt.checkpw(
                password_bytes,
                hashed_password.encode('utf-8')
            )
        except (ValueError, TypeError):
            # Invalid hash format or other bcrypt error
            return False


# Singleton instance
password_hasher = PasswordHasher()
