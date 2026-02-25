"""Category schemas for API request/response validation."""
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    """Category response schema."""
    
    id: UUID = Field(..., description="Category UUID")
    name: str = Field(..., description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    display_order: int = Field(..., description="Display order in dropdown")
    is_active: bool = Field(..., description="Whether category is active")
    
    class Config:
        """Pydantic config."""
        from_attributes = True
