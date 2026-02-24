"""User model for authentication and profile management."""
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import enum
import re

from src.models.base import BaseModel
from src.utils.password_hasher import password_hasher


class UserRole(str, enum.Enum):
    """User roles for authorization."""
    SUBMITTER = "submitter"
    ADMIN = "admin"


class User(BaseModel):
    """
    User entity for authentication and profile management.
    
    Attributes:
        email: Unique email address (stored lowercase)
        hashed_password: bcrypt hashed password
        full_name: User's full name
        role: User role (submitter/admin)
        is_active: Account active status
    """
    
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.SUBMITTER)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        full_name: str,
        role: str = "submitter",
        is_active: bool = True,
        **kwargs
    ):
        """
        Initialize User with validation.
        
        Args:
            email: Email address (will be converted to lowercase)
            hashed_password: Password to hash or already hashed password
            full_name: Full name
            role: User role (submitter/admin)
            is_active: Account active status (default True)
            
        Raises:
            ValueError: If validation fails
        """
        # Validate and normalize email
        email = email.strip().lower()
        if not self._validate_email(email):
            raise ValueError(f"Invalid email format: {email}")
        
        # Validate full name
        if not self._validate_full_name(full_name):
            raise ValueError(
                f"Invalid full_name: Must be 2+ characters, letters/spaces/hyphens/apostrophes only"
            )
        
        # Validate role
        if role not in [r.value for r in UserRole]:
            raise ValueError(f"Invalid role: {role}")
        
        # Hash password if not already hashed (starts with $2b$ indicates bcrypt)
        if not hashed_password.startswith("$2b$"):
            if not self._validate_password(hashed_password):
                raise ValueError(
                    "Invalid password: Must be 8+ characters with uppercase, lowercase, digit, and special character"
                )
            hashed_password = password_hasher.hash_password(hashed_password)
        
        # Set attributes directly (SQLAlchemy style)
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.role = UserRole(role)
        self.is_active = is_active
        
        # Generate UUID if not provided
        if 'id' not in kwargs and self.id is None:
            import uuid as uuid_module
            self.id = uuid_module.uuid4()
        
        # Set timestamps if not provided
        if self.created_at is None:
            from datetime import datetime
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            from datetime import datetime
            self.updated_at = datetime.utcnow()
    
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
        # Pattern with negative lookahead to prevent consecutive dots
        # Allows: letters, digits, dots, underscores, plus, percent, hyphen
        # Pattern: (?!.*\.\.) prevents .. anywhere in the string
        pattern = r'^(?!.*\.\.)[a-zA-Z0-9][a-zA-Z0-9._+%-]*[a-zA-Z0-9]@(?!.*\.\.)[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def _validate_full_name(name: str) -> bool:
        """
        Validate full name format.
        
        Args:
            name: Full name to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not name or len(name) < 2:
            return False
        # Allow letters, spaces, hyphens, apostrophes
        pattern = r"^[a-zA-Z\s\-']+$"
        return bool(re.match(pattern, name))
    
    @staticmethod
    def _validate_password(password: str) -> bool:
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
        if len(password) < 8:
            return False
        
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password))
        
        return has_upper and has_lower and has_digit and has_special
    
    def __repr__(self) -> str:
        """Return string representation of user."""
        return f"User(id={self.id}, email={self.email}, role={self.role})"
