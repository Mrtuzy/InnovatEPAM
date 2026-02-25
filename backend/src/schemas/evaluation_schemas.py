"""Evaluation request and response schemas."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import uuid
from typing import Literal


class EvaluatorInfo(BaseModel):
    """Evaluator (admin user) information."""
    id: str
    full_name: str
    email: str
    
    class Config:
        from_attributes = True


class EvaluateRequest(BaseModel):
    """Request schema for evaluating an idea."""
    new_status: Literal['under_review', 'accepted', 'rejected'] = Field(
        ...,
        description="New status for the idea"
    )
    comment: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Evaluation feedback (required, 10-2000 characters)"
    )
    
    @field_validator('comment')
    @classmethod
    def validate_comment(cls, v: str) -> str:
        """Validate comment is not just whitespace."""
        if not v or not v.strip():
            raise ValueError('Comment cannot be empty or whitespace')
        return v.strip()


class EvaluationResponse(BaseModel):
    """Response schema for evaluation data."""
    id: str
    idea_id: str
    evaluator: EvaluatorInfo
    previous_status: str
    new_status: str
    comment: str
    created_at: datetime
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm_with_evaluator(cls, evaluation):
        """Create response from ORM model with nested evaluator."""
        return cls(
            id=str(evaluation.id),
            idea_id=str(evaluation.idea_id),
            evaluator=EvaluatorInfo(
                id=str(evaluation.evaluator.id),
                full_name=evaluation.evaluator.full_name,
                email=evaluation.evaluator.email
            ),
            previous_status=evaluation.previous_status,
            new_status=evaluation.new_status,
            comment=evaluation.comment,
            created_at=evaluation.created_at
        )


class EvaluationListResponse(BaseModel):
    """Response schema for list of evaluations."""
    evaluations: list[EvaluationResponse]
    total: int
