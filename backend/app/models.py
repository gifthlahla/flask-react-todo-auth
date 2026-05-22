from pydantic import BaseModel, Field, field_validator
import re

class UserRegister(BaseModel):
    """Schema for user registration requests."""
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username for the new account"
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Password for the new account"
    )
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format."""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v.strip()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v.strip()) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class UserLogin(BaseModel):
    """Schema for user login requests."""
    username: str = Field(..., min_length=1, description="Username for login")
    password: str = Field(..., min_length=1, description="Password for login")

class TokenResponse(BaseModel):
    """Schema for successful login response."""
    access_token: str = Field(..., description="Bearer token for authentication")
    token_type: str = Field(default="bearer", description="Token type")

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str = Field(..., description="Error message")

class SuccessResponse(BaseModel):
    """Schema for success responses."""
    message: str = Field(..., description="Success message")

class ProtectedResponse(BaseModel):
    """Schema for protected endpoint response."""
    message: str = Field(..., description="Welcome message with username")
    username: str = Field(..., description="Authenticated username")