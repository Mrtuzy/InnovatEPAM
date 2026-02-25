"""Idea model for innovation proposals."""
from sqlalchemy import Column, String, Text, Integer, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid
from datetime import datetime

from src.models.base import BaseModel


class IdeaStatus(str, enum.Enum):
    """Idea evaluation status enum."""
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Idea(BaseModel):
    """
    Idea entity for innovation proposals.
    
    Attributes:
        title: Brief idea title/headline (10-200 characters)
        description: Detailed idea description (50-5000 characters)
        category_id: Foreign key to Category
        submitter_id: Foreign key to User (idea owner)
        status: Current evaluation state (default: submitted)
        attachment_filename: Original uploaded filename
        attachment_path: Storage path/URL for file
        attachment_size: File size in bytes
        attachment_mimetype: File MIME type
    """
    
    __tablename__ = "ideas"
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False, index=True)
    submitter_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    status = Column(
        SQLEnum(IdeaStatus, values_callable=lambda x: [e.value for e in x], name='idea_status'),
        nullable=False,
        default='submitted',
        index=True
    )
    
    # Attachment fields (all nullable, but must be set together if present)
    attachment_filename = Column(String(255), nullable=True)
    attachment_path = Column(String(500), nullable=True)
    attachment_size = Column(Integer, nullable=True)
    attachment_mimetype = Column(String(100), nullable=True)
    
    # Relationships
    category = relationship("Category", back_populates="ideas")
    submitter = relationship("User", back_populates="ideas")
    evaluations = relationship("Evaluation", back_populates="idea", order_by="Evaluation.created_at.desc()")
    
    def __init__(
        self,
        title: str,
        description: str,
        category_id: uuid.UUID,
        submitter_id: uuid.UUID,
        status: str = "submitted",
        attachment_filename: str = None,
        attachment_path: str = None,
        attachment_size: int = None,
        attachment_mimetype: str = None,
        **kwargs
    ):
        """
        Initialize Idea with validation.
        
        Args:
            title: Idea title (10-200 chars)
            description: Detailed description (50-5000 chars)
            category_id: Category UUID
            submitter_id: Submitter User UUID
            status: Evaluation status (default: submitted)
            attachment_filename: Optional filename
            attachment_path: Optional storage path
            attachment_size: Optional file size in bytes
            attachment_mimetype: Optional MIME type
            
        Raises:
            ValueError: If validation fails
        """
        # Validate title
        if not title or len(title) < 10:
            raise ValueError("Title must be at least 10 characters")
        if len(title) > 200:
            raise ValueError("Title must be at most 200 characters")
        
        # Validate description
        if not description or len(description) < 50:
            raise ValueError("Description must be at least 50 characters")
        if len(description) > 5000:
            raise ValueError("Description must be at most 5000 characters")
        
        # Validate status
        valid_statuses = [s.value for s in IdeaStatus]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")
        
        # Validate attachment consistency (all or none)
        attachment_fields = [attachment_filename, attachment_path, attachment_size, attachment_mimetype]
        has_attachment = any(f is not None for f in attachment_fields)
        all_attachment = all(f is not None for f in attachment_fields)
        
        if has_attachment and not all_attachment:
            raise ValueError(
                "All attachment fields must be provided together: "
                "filename, path, size, and mimetype"
            )
        
        # Set attributes
        self.title = title.strip()
        self.description = description.strip()
        self.category_id = category_id
        self.submitter_id = submitter_id
        self.status = status
        
        # Set attachment fields
        self.attachment_filename = attachment_filename
        self.attachment_path = attachment_path
        self.attachment_size = attachment_size
        self.attachment_mimetype = attachment_mimetype
        
        # Handle BaseModel initialization
        if 'id' in kwargs:
            self.id = kwargs['id']
        elif self.id is None:
            self.id = uuid.uuid4()
        
        if 'created_at' in kwargs:
            self.created_at = kwargs['created_at']
        elif self.created_at is None:
            self.created_at = datetime.utcnow()
        
        if 'updated_at' in kwargs:
            self.updated_at = kwargs['updated_at']
        elif self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    @property
    def has_attachment(self) -> bool:
        """Check if idea has file attachment."""
        return self.attachment_filename is not None
    
    def __repr__(self) -> str:
        """Return string representation of idea."""
        return f"Idea(id={self.id}, title={self.title[:30]}..., status={self.status})"
