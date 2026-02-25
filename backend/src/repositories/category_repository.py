"""Category repository for data access operations."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.category import Category
from src.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """
    Repository for Category model operations.
    
    Extends BaseRepository with Category-specific queries:
    - get_active_categories: Get all active categories sorted by display_order
    - get_by_name: Find category by name (case-insensitive)
    """
    
    def __init__(self, db: Session):
        """
        Initialize CategoryRepository.
        
        Args:
            db: Database session
        """
        super().__init__(Category, db)
    
    def get_active_categories(self) -> List[Category]:
        """
        Get all active categories sorted by display_order.
        
        Returns:
            List of active categories
        """
        return self.db.query(Category).filter(
            Category.is_active == True
        ).order_by(
            Category.display_order,
            Category.name
        ).all()
    
    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        """
        Get category by ID.
        
        Args:
            category_id: Category UUID
            
        Returns:
            Category if found, None otherwise
        """
        return self.db.query(Category).filter(
            Category.id == category_id
        ).first()
    
    def get_by_name(self, name: str) -> Optional[Category]:
        """
        Get category by name (case-insensitive).
        
        Args:
            name: Category name
            
        Returns:
            Category if found, None otherwise
        """
        return self.db.query(Category).filter(
            Category.name.ilike(name)
        ).first()
    
    def get_all_categories(self, include_inactive: bool = False) -> List[Category]:
        """
        Get all categories.
        
        Args:
            include_inactive: Include inactive categories (default False)
            
        Returns:
            List of categories sorted by display_order
        """
        query = self.db.query(Category)
        
        if not include_inactive:
            query = query.filter(Category.is_active == True)
        
        return query.order_by(
            Category.display_order,
            Category.name
        ).all()
