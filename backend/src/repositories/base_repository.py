"""Base repository pattern with common CRUD operations."""
from typing import Generic, TypeVar, Type, Optional, List
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Base repository with common CRUD operations.
    
    All repositories should inherit from this class to get:
    - create: Create new entity
    - get_by_id: Get entity by UUID
    - get_all: Get all entities with optional limit/offset
    - update: Update entity
    - delete: Delete entity
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def create(self, **kwargs) -> ModelType:
        """
        Create new entity.
        
        Args:
            **kwargs: Model fields
            
        Returns:
            Created entity
        """
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def get_by_id(self, id: UUID) -> Optional[ModelType]:
        """
        Get entity by ID.
        
        Args:
            id: Entity UUID
            
        Returns:
            Entity or None
        """
        return self.db.query(self.model).filter(
            self.model.id == id
        ).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Get all entities with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            List of entities
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: UUID, **kwargs) -> Optional[ModelType]:
        """
        Update entity.
        
        Args:
            id: Entity UUID
            **kwargs: Fields to update
            
        Returns:
            Updated entity or None
        """
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance
    
    def delete(self, id: UUID) -> bool:
        """
        Delete entity.
        
        Args:
            id: Entity UUID
            
        Returns:
            True if deleted, False if not found
        """
        instance = self.get_by_id(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False
