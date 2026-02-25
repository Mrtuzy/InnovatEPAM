"""Authentication service for user registration and login."""
from typing import Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session

from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.utils.password_hasher import password_hasher
from src.utils.jwt_handler import jwt_handler
from src.utils.logger import logger


class AuthService:
    """
    Authentication service for user registration and login.
    
    Handles:
    - User registration with validation
    - User login with credential verification
    - Token generation and management
    - Password security
    """
    
    def __init__(self, db: Session):
        """
        Initialize AuthService.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    def register_user(
        self,
        email: str,
        password: str,
        full_name: str
    ) -> User:
        """
        Register new user without duplicate validation.
        
        The User model handles validation internally.
        Repository will check for duplicate email.
        
        Args:
            email: User email
            password: Plain text password
            full_name: User's full name
            
        Returns:
            Created user
            
        Raises:
            ValueError: If validation fails or email exists
        """
        try:
            # Create user (this triggers all validations in User.__init__)
            hashed_password = password_hasher.hash_password(password)
            user = self.user_repo.create_user(
                email=email.strip().lower(),
                hashed_password=hashed_password,
                full_name=full_name,
                role="submitter"  # Default role
            )
            
            logger.info(
                f"User registered: {user.email}",
                user_id=str(user.id)
            )
            
            return user
        except ValueError as e:
            # Repository/model validation error
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}", exc_info=True)
            raise ValueError(f"Registration failed: {str(e)}")
    
    def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Dict[str, Any]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Dictionary with user, access_token, refresh_token
            
        Raises:
            ValueError: If authentication fails
        """
        # Normalize email
        email = email.strip().lower()
        
        # Get user by email
        user = self.user_repo.get_by_email(email)
        
        if not user:
            # Don't reveal whether user exists for security
            logger.warning(f"Login failed - user not found: {email}")
            raise ValueError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login failed - inactive user: {email}")
            raise ValueError("Account is inactive or disabled")
        
        # Verify password
        if not password_hasher.verify_password(password, user.hashed_password):
            logger.warning(f"Login failed - invalid password: {email}")
            raise ValueError("Invalid credentials")
        
        # Generate tokens (user.role is already a string)
        access_token = jwt_handler.create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role  # Already a string value
        )
        
        refresh_token = jwt_handler.create_refresh_token(user_id=user.id)
        
        logger.info(f"User authenticated: {user.email}", user_id=str(user.id))
        
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: JWT refresh token
            
        Returns:
            Dictionary with new access_token and user
            
        Raises:
            ValueError: If token is invalid
        """
        # Verify refresh token
        payload = jwt_handler.verify_refresh_token(refresh_token)
        
        if not payload:
            logger.warning("Token refresh failed - invalid refresh token")
            raise ValueError("Invalid refresh token")
        
        try:
            user_id = UUID(payload.get("sub"))
        except (ValueError, TypeError):
            logger.warning(f"Token refresh failed - invalid user_id: {payload.get('sub')}")
            raise ValueError("Invalid refresh token payload")
        
        # Get user
        user = self.user_repo.get_by_id(user_id)
        
        if not user:
            logger.warning(f"Token refresh failed - user not found: {user_id}")
            raise ValueError("User not found")
        
        if not user.is_active:
            logger.warning(f"Token refresh failed - inactive user: {user_id}")
            raise ValueError("User account is inactive")
        
        # Create new access token (user.role is already a string)
        access_token = jwt_handler.create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role  # Already a string value
        )
        
        logger.info(f"Access token refreshed for user: {user.email}", user_id=str(user.id))
        
        return {
            "access_token": access_token,
            "user": user
        }
