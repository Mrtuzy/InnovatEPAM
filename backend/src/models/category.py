"""Category model for idea classification."""
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class Category(BaseModel):
    """
    Category entity for idea classification.
    
    Attributes:
        name: Unique category display name (3-50 characters)
        description: Brief category explanation
        display_order: Sort order for UI display (lower = higher priority)
        is_active: Visibility in idea submission form
    """
    
    __tablename__ = "categories"
    
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    display_order = Column(Integer, nullable=False, default=0, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    
    # Relationship to ideas (one category has many ideas)
    ideas = relationship("Idea", back_populates="category")
    
    def __init__(
        self,
        name: str,
        description: str = None,
        display_order: int = 0,
        is_active: bool = True,
        **kwargs
    ):
        """
        Initialize Category with validation.
        
        Args:
            name: Category name (will be title-cased)
            description: Optional description
            display_order: Sort order (default 0)
            is_active: Visibility status (default True)
            
        Raises:
            ValueError: If validation fails
        """
        # Validate name
        if not name or len(name) < 3:
            raise ValueError("Category name must be at least 3 characters")
        if len(name) > 50:
            raise ValueError("Category name must be at most 50 characters")
        
        # Normalize name (title case for consistency)
        name = name.strip()
        
        # Set attributes
        self.name = name
        self.description = description
        self.display_order = display_order
        self.is_active = is_active
        
        # Handle BaseModel initialization (id, timestamps)
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'created_at' in kwargs:
            self.created_at = kwargs['created_at']
        if 'updated_at' in kwargs:
            self.updated_at = kwargs['updated_at']
    
    def __repr__(self) -> str:
        """Return string representation of category."""
        return f"Category(id={self.id}, name={self.name}, display_order={self.display_order})"
