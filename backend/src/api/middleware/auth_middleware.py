"""Authentication middleware for JWT validation."""
from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils.jwt_handler import jwt_handler


security = HTTPBearer(auto_error=False)


class AuthMiddleware:
    """JWT authentication middleware."""
    
    @staticmethod
    def get_current_user_id(
        credentials: Optional[HTTPAuthorizationCredentials] = None
    ) -> str:
        """
        Extract and validate user from JWT token.
        
        Args:
            credentials: HTTP Bearer credentials
            
        Returns:
            User ID from token
            
        Raises:
            HTTPException: If token invalid or expired
        """
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = credentials.credentials
        payload = jwt_handler.verify_access_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_id
    
    @staticmethod
    def get_current_user_payload(
        credentials: Optional[HTTPAuthorizationCredentials] = None
    ) -> dict:
        """
        Get full user payload from token.
        
        Args:
            credentials: HTTP Bearer credentials
            
        Returns:
            User payload dict with id, email, role
            
        Raises:
            HTTPException: If token invalid
        """
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = credentials.credentials
        payload = jwt_handler.verify_access_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role"),
        }


# Singleton instance
auth_middleware = AuthMiddleware()
