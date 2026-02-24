"""Authentication service for user registration and login."""
from typing import Dict, Any, Optional
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
        Register new user.
        
        Args:
            email: User email
            password: Plain text password
            full_name: User's full name
            
        Returns:
            Created user
            
        Raises:
            ValueError: If validation fails or email exists
        """
        # Normalize email
        email = email.strip().lower()
        
        # Validate email format
        if not self._validate_email(email):
            raise ValueError(f"Invalid email format: {email}")
        
        # Validate full name
        if not full_name or len(full_name) < 2:
            raise ValueError("full_name must be at least 2 characters")
        
        # Validate password complexity
        if not self._validate_password_complexity(password):
            raise ValueError(
                "password must be 8+ characters with uppercase, lowercase, digit, and special character"
            )
        
        # Check if email already exists
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError(f"Email {email} already registered")
        
        # Hash password
        hashed_password = password_hasher.hash_password(password)
        
        # Create user
        try:
            user = self.user_repo.create_user(
                email=email,
                hashed_password=hashed_password,
                full_name=full_name,
                role="submitter"  # Default role
            )
            
            logger.info(
                "user_registered",
                user_id=str(user.id),
                email=user.email
            )
            
            return user
        except Exception as e:
            logger.error("registration_failed", error=str(e), email=email)
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
            logger.warning("login_failed_user_not_found", email=email)
            raise ValueError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            logger.warning("login_failed_inactive_user", user_id=str(user.id), email=email)
            raise ValueError("Account is inactive or disabled")
        
        # Verify password
        if not password_hasher.verify_password(password, user.hashed_password):
            logger.warning("login_failed_invalid_password", user_id=str(user.id), email=email)
            raise ValueError("Invalid credentials")
        
        # Generate tokens
        access_token = jwt_handler.create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value
        )
        
        refresh_token = jwt_handler.create_refresh_token(user_id=user.id)
        
        logger.info(
            "user_authenticated",
            user_id=str(user.id),
            email=user.email,
            role=user.role.value
        )
        
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
            logger.warning("token_refresh_failed_invalid_token")
            raise ValueError("Invalid refresh token")
        
        user_id = payload.get("sub")
        
        # Get user
        user = self.user_repo.get_by_id(UUID(user_id))
        
        if not user:
            logger.warning("token_refresh_failed_user_not_found", user_id=user_id)
            raise ValueError("User not found")
        
        if not user.is_active:
            logger.warning("token_refresh_failed_inactive_user", user_id=user_id)
            raise ValueError("User account is inactive")
        
        # Create new access token
        access_token = jwt_handler.create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value
        )
        
        logger.info("token_refreshed", user_id=str(user.id))
        
        return {
            "access_token": access_token,
            "user": user
        }
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Prevents:
        - Consecutive dots in local or domain part (test..user@example.com)
        - Leading/trailing dots in local or domain parts
        - Spaces in email address
        
        Args:
            email: Email to validate
            
        Returns:
            True if valid, False otherwise
        """
        import re
        # Pattern with negative lookahead to prevent consecutive dots
        # Allows: letters, digits, dots, underscores, plus, percent, hyphen
        # Pattern: (?!.*\.\.) prevents .. anywhere in the string
        pattern = r'^(?!.*\.\.)[a-zA-Z0-9][a-zA-Z0-9._+%-]*[a-zA-Z0-9]@(?!.*\.\.)[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def _validate_password_complexity(password: str) -> bool:
        """
        Validate password complexity.
        
        Requirements:
        - 8+ characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        
        Args:
            password: Password to validate
            
        Returns:
            True if valid, False otherwise
        """
        import re
        
        if len(password) < 8:
            return False
        
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password))
        
        return has_upper and has_lower and has_digit and has_special
