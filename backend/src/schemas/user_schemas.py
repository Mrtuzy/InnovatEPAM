"""User request and response schemas."""
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel as PydanticBase, EmailStr, Field, ConfigDict

from src.schemas.base_schemas import BaseSchema


class RegisterRequest(PydanticBase):
    """Registration request schema."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ...,
        min_length=8,
        description="Password (8+ chars, upper, lower, digit, special)"
    )
    full_name: str = Field(..., min_length=2, description="User's full name")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "password": "SecurePass123!",
                "full_name": "John Doe"
            }
        }
    )


class LoginRequest(PydanticBase):
    """Login request schema."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "password": "SecurePass123!"
            }
        }
    )


class UserResponse(BaseSchema):
    """User response schema (safe to expose in API)."""
    id: UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "john@example.com",
                "full_name": "John Doe",
                "role": "submitter",
                "is_active": True,
                "created_at": "2026-02-24T10:00:00Z",
                "updated_at": "2026-02-24T10:00:00Z"
            }
        }
    )


class TokenResponse(PydanticBase):
    """Token response schema."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    user: UserResponse = Field(..., description="User profile")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(default=900, description="Access token TTL in seconds")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "john@example.com",
                    "full_name": "John Doe",
                    "role": "submitter",
                    "is_active": True,
                    "created_at": "2026-02-24T10:00:00Z",
                    "updated_at": "2026-02-24T10:00:00Z"
                },
                "token_type": "bearer",
                "expires_in": 900
            }
        }
    )
