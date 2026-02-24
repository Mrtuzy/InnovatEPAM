"""Base Pydantic schemas with common response models."""
from datetime import datetime
from uuid import UUID
from typing import Optional, Any, Dict

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }
    )


class BaseResponseSchema(BaseSchema):
    """Base response schema with common fields."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime


class ErrorDetail(BaseModel):
    """Error detail schema."""
    
    field: str
    message: str


class ErrorResponse(BaseModel):
    """Standard error response format."""
    
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


class SuccessResponse(BaseModel):
    """Standard success response format."""
    
    message: str
    data: Optional[Dict[str, Any]] = None


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    
    total: int
    page: int
    limit: int
    pages: int
