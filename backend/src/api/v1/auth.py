"""Authentication API endpoints."""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID

from src.config.database import get_db
from src.api.middleware.auth_middleware import auth_middleware
from src.services.auth_service import AuthService
from src.repositories.user_repository import UserRepository
from src.utils.jwt_handler import jwt_handler
from src.schemas.user_schemas import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    UserResponse,
    TokenResponse
)
from src.schemas.base_schemas import ErrorResponse
from src.utils.logger import logger

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": TokenResponse},
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse}
    }
)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Register new user.
    
    Args:
        request: Registration request with email, password, full_name
        db: Database session
        
    Returns:
        TokenResponse with access token, refresh token, and user profile
        
    Raises:
        HTTPException: 400 for validation errors, 409 for duplicate email
    """
    auth_service = AuthService(db)
    
    try:
        user = auth_service.register_user(
            email=request.email,
            password=request.password,
            full_name=request.full_name
        )
        
        # Generate tokens (user.role is already string value)
        access_token = jwt_handler.create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role  # Already a string, not enum member
        )
        refresh_token = jwt_handler.create_refresh_token(user_id=user.id)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.model_validate(user),
            token_type="bearer",
            expires_in=900
        )
    
    except ValueError as e:
        error_msg = str(e)
        
        # Check for duplicate email error
        if "already registered" in error_msg.lower() or "already exists" in error_msg.lower():
            logger.warning(f"Duplicate email registration attempt: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        # Validation error
        logger.warning(f"Registration validation failed: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        200: {"model": TokenResponse},
        401: {"model": ErrorResponse},
        400: {"model": ErrorResponse}
    }
)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Login user with email and password.
    
    Args:
        request: Login request with email and password
        db: Database session
        
    Returns:
        TokenResponse with access token, refresh token, and user profile
        
    Raises:
        HTTPException: 401 for invalid credentials, 400 for validation errors
    """
    auth_service = AuthService(db)
    
    try:
        result = auth_service.authenticate_user(
            email=request.email,
            password=request.password
        )
        
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            user=UserResponse.model_validate(result["user"]),
            token_type="bearer",
            expires_in=900
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    except Exception as e:
        logger.error("login_failed", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Logout successful"},
        401: {"model": ErrorResponse}
    }
)
async def logout(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Response:
    """
    Logout user.
    
    Clears refresh token cookie and revokes session.
    
    Args:
        credentials: Current user authentication
        
    Returns:
        Response with 204 No Content
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validate token
    token = credentials.credentials
    payload = jwt_handler.verify_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # In JWT-based auth, logout is primarily client-side (token deletion)
    # Server-side: could track token on blacklist, but not implemented for MVP
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie("refresh_token")
    return response


@router.post(
    "/refresh",
    response_model=TokenResponse,
    responses={
        200: {"model": TokenResponse},
        401: {"model": ErrorResponse}
    }
)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Refresh access token using refresh token.
    
    Args:
        request: Contains refresh_token
        db: Database session
        
    Returns:
        TokenResponse with new access token
        
    Raises:
        HTTPException: 401 for invalid refresh token
    """
    auth_service = AuthService(db)
    
    try:
        result = auth_service.refresh_access_token(
            refresh_token=request.refresh_token
        )
        
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token="",  # Don't return refresh token again
            user=UserResponse.model_validate(result["user"]),
            token_type="bearer",
            expires_in=900
        )
    
    except ValueError as e:
        logger.warning(f"Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    except Exception as e:
        logger.error(f"Refresh token failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        200: {"model": UserResponse},
        401: {"model": ErrorResponse}
    }
)
async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Get current authenticated user profile.
    
    Args:
        credentials: Current user JWT credentials
        db: Database session
        
    Returns:
        UserResponse with current user profile
        
    Raises:
        HTTPException: 401 for unauthenticated request
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validate token
    token = credentials.credentials
    payload = jwt_handler.verify_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract and validate user_id from token
    try:
        user_id = UUID(payload.get("sub"))
    except (ValueError, TypeError):
        logger.warning(f"Invalid user_id in token: {payload.get('sub')}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get user from database
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    
    if not user:
        logger.warning(f"User not found for id: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return UserResponse.model_validate(user)
