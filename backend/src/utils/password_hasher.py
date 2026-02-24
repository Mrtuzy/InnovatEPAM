"""Password hashing utility using bcrypt."""
import bcrypt

from src.config.settings import get_settings

settings = get_settings()


class PasswordHasher:
    """Password hashing and verification using bcrypt."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password as string
        """
        salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            salt
        )
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
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )


# Singleton instance
password_hasher = PasswordHasher()
