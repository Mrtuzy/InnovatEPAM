"""User repository for data access operations."""
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.user import User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model operations.
    
    Extends BaseRepository with User-specific queries:
    - get_by_email: Find user by email (case-insensitive)
    - create_user: Create new user with password hashing
    """
    
    def __init__(self, db: Session):
        """
        Initialize UserRepository.
        
        Args:
            db: Database session
        """
        super().__init__(User, db)
    
    def create_user(
        self,
        email: str,
        hashed_password: str,
        full_name: str,
        role: str = "submitter"
    ) -> User:
        """
        Create new user.
        
        Args:
            email: User email (will be converted to lowercase)
            hashed_password: Hashed password
            full_name: User's full name
            role: User role (submitter/admin)
            
        Returns:
            Created user
            
        Raises:
            ValueError: If validation fails
            IntegrityError: If email already exists
        """
        # Validate role value against enum
        from src.models.user import UserRole
        valid_roles = [r.value for r in UserRole]
        if role not in valid_roles:
            raise ValueError(f"Invalid role: {role}. Must be one of {valid_roles}")
        
        try:
            user = User(
                email=email,
                hashed_password=hashed_password,
                full_name=full_name,
                role=role
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError as e:
            self.db.rollback()
            # Extract meaningful error from database
            if "users_email_key" in str(e) or "uq_users_email" in str(e):
                raise ValueError(f"Email {email} already registered")
            raise ValueError(f"Database constraint error: {str(e)}")
        except ValueError:
            raise
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to create user: {str(e)}")
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email (case-insensitive).
        
        Args:
            email: Email to search for
            
        Returns:
            User if found, None otherwise
        """
        email = email.strip().lower()
        return self.db.query(User).filter(
            User.email == email
        ).first()
    
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User UUID
            
        Returns:
            User if found, None otherwise
        """
        return self.db.query(User).filter(
            User.id == user_id
        ).first()
    
    def get_active_by_email(self, email: str) -> Optional[User]:
        """
        Get active user by email.
        
        Args:
            email: Email to search for
            
        Returns:
            User if found and active, None otherwise
        """
        email = email.strip().lower()
        return self.db.query(User).filter(
            User.email == email,
            User.is_active == True
        ).first()
