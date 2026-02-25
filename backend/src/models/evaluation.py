"""Evaluation model for admin idea assessment."""
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from src.models.base import BaseModel


class Evaluation(BaseModel):
    """
    Evaluation entity for tracking idea status changes by admins.
    
    Attributes:
        idea_id: Foreign key to Idea being evaluated
        evaluator_id: Foreign key to User (admin) performing evaluation
        previous_status: Status before this evaluation
        new_status: Status after this evaluation
        comment: Mandatory feedback/reasoning for the evaluation
    """
    
    __tablename__ = "evaluations"
    
    idea_id = Column(UUID(as_uuid=True), ForeignKey('ideas.id'), nullable=False, index=True)
    evaluator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    previous_status = Column(String(50), nullable=False)
    new_status = Column(String(50), nullable=False)
    comment = Column(Text, nullable=False)
    
    # Relationships
    idea = relationship("Idea", back_populates="evaluations")
    evaluator = relationship("User", back_populates="evaluations")
    
    def __init__(
        self,
        idea_id: uuid.UUID,
        evaluator_id: uuid.UUID,
        previous_status: str,
        new_status: str,
        comment: str,
        **kwargs
    ):
        """
        Initialize Evaluation with validation.
        
        Args:
            idea_id: UUID of idea being evaluated
            evaluator_id: UUID of admin performing evaluation
            previous_status: Previous idea status
            new_status: New idea status
            comment: Evaluation feedback (required)
            
        Raises:
            ValueError: If validation fails
        """
        # Validate comment
        if not comment or not comment.strip():
            raise ValueError("Evaluation comment is required")
        if len(comment.strip()) < 10:
            raise ValueError("Comment must be at least 10 characters")
        
        # Validate status values
        valid_statuses = ['submitted', 'under_review', 'accepted', 'rejected']
        if previous_status not in valid_statuses:
            raise ValueError(f"Invalid previous_status: {previous_status}")
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid new_status: {new_status}")
        
        super().__init__(**kwargs)
        self.idea_id = idea_id
        self.evaluator_id = evaluator_id
        self.previous_status = previous_status
        self.new_status = new_status
        self.comment = comment.strip()
    
    def __repr__(self):
        return f"<Evaluation {self.id} - {self.previous_status} → {self.new_status}>"
