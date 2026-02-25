"""Idea schemas for API request/response validation."""
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, validator

from src.schemas.category_schemas import CategoryResponse


class IdeaCreateRequest(BaseModel):
    """Idea creation request schema (for form-data)."""
    
    title: str = Field(..., min_length=10, max_length=200, description="Idea title")
    description: str = Field(..., min_length=50, max_length=5000, description="Detailed description")
    category_id: UUID = Field(..., description="Category UUID")
    
    @validator('title')
    def validate_title(cls, v):
        """Validate title is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        """Validate description is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Description cannot be empty")
        return v.strip()


class SubmitterInfo(BaseModel):
    """Submitter user information."""
    
    id: UUID = Field(..., description="User UUID")
    full_name: str = Field(..., description="User full name")
    email: str = Field(..., description="User email")
    
    class Config:
        """Pydantic config."""
        from_attributes = True


class AttachmentInfo(BaseModel):
    """Attachment metadata."""
    
    filename: str = Field(..., description="Original filename")
    size: int = Field(..., description="File size in bytes")
    mimetype: str = Field(..., description="MIME type")


class IdeaResponse(BaseModel):
    """Idea response schema."""
    
    id: UUID = Field(..., description="Idea UUID")
    title: str = Field(..., description="Idea title")
    description: str = Field(..., description="Detailed description")
    status: str = Field(..., description="Current status")
    category: CategoryResponse = Field(..., description="Associated category")
    submitter: SubmitterInfo = Field(..., description="Idea submitter")
    attachment: Optional[AttachmentInfo] = Field(None, description="Attachment info if present")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        """Pydantic config."""
        from_attributes = True
    
    @classmethod
    def from_orm_with_attachment(cls, idea):
        """Create response from ORM model with attachment handling."""
        response_dict = {
            'id': idea.id,
            'title': idea.title,
            'description': idea.description,
            'status': idea.status,
            'category': idea.category,
            'submitter': idea.submitter,
            'created_at': idea.created_at,
            'updated_at': idea.updated_at,
            'attachment': None
        }
        
        # Add attachment info if present
        if idea.attachment_filename:
            response_dict['attachment'] = AttachmentInfo(
                filename=idea.attachment_filename,
                size=idea.attachment_size,
                mimetype=idea.attachment_mimetype
            )
        
        return cls(**response_dict)


class PaginationInfo(BaseModel):
    """Pagination metadata."""
    
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")


class IdeaListResponse(BaseModel):
    """Paginated idea list response."""
    
    items: List[IdeaResponse] = Field(..., description="List of ideas")
    pagination: PaginationInfo = Field(..., description="Pagination metadata")
