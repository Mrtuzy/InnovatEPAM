"""JWT token generation and validation."""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID

from jose import JWTError, jwt

from src.config.settings import get_settings

settings = get_settings()


class JWTHandler:
    """JWT token operations."""
    
    @staticmethod
    def create_access_token(
        user_id: UUID,
        email: str,
        role: str
    ) -> str:
        """
        Create JWT access token.
        
        Args:
            user_id: User UUID
            email: User email
            role: User role (submitter/admin)
            
        Returns:
            JWT token string
        """
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {
            "sub": str(user_id),
            "email": email,
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    
    @staticmethod
    def create_refresh_token(user_id: UUID) -> str:
        """
        Create JWT refresh token.
        
        Args:
            user_id: User UUID
            
        Returns:
            JWT refresh token string
        """
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Decode and validate JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Token payload dict or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify access token and return payload.
        
        Args:
            token: JWT access token
            
        Returns:
            Token payload or None if invalid
        """
        payload = JWTHandler.decode_token(token)
        if payload and payload.get("type") == "access":
            return payload
        return None
    
    @staticmethod
    def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify refresh token and return payload.
        
        Args:
            token: JWT refresh token
            
        Returns:
            Token payload or None if invalid
        """
        payload = JWTHandler.decode_token(token)
        if payload and payload.get("type") == "refresh":
            return payload
        return None


# Singleton instance
jwt_handler = JWTHandler()
