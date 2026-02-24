"""Base model with common fields for all database entities."""
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.config.database import Base


class BaseModel(Base):
    """
    Base model with UUID primary key and timestamps.
    
    All models should inherit from this class to get:
    - UUID primary key (id)
    - created_at timestamp
    - updated_at timestamp (auto-updated)
    """
    
    __abstract__ = True
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True,
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    
    def __repr__(self) -> str:
        """String representation."""
        return f"<{self.__class__.__name__}(id={self.id})>"
