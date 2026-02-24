"""Role-based access control middleware."""
from typing import List
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.api.middleware.auth_middleware import auth_middleware


class RBACMiddleware:
    """Role-based access control middleware."""
    
    @staticmethod
    def require_role(
        credentials: HTTPAuthorizationCredentials,
        allowed_roles: List[str]
    ) -> dict:
        """
        Verify user has required role.
        
        Args:
            credentials: HTTP Bearer credentials
            allowed_roles: List of roles (e.g., ["admin", "submitter"])
            
        Returns:
            User payload if authorized
            
        Raises:
            HTTPException: If user lacks required role
        """
        payload = auth_middleware.get_current_user_payload(credentials)
        user_role = payload.get("role")
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This endpoint requires one of roles: {allowed_roles}",
            )
        
        return payload
    
    @staticmethod
    def require_admin(
        credentials: HTTPAuthorizationCredentials
    ) -> dict:
        """
        Verify user has admin role.
        
        Args:
            credentials: HTTP Bearer credentials
            
        Returns:
            User payload if admin
            
        Raises:
            HTTPException: If user not admin
        """
        return RBACMiddleware.require_role(credentials, ["admin"])
    
    @staticmethod
    def require_authenticated(
        credentials: HTTPAuthorizationCredentials
    ) -> dict:
        """
        Verify user is authenticated (any role).
        
        Args:
            credentials: HTTP Bearer credentials
            
        Returns:
            User payload
        """
        return RBACMiddleware.require_role(
            credentials,
            ["admin", "submitter"]
        )


# Singleton instance
rbac_middleware = RBACMiddleware()
