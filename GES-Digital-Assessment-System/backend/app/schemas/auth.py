"""Request and response schemas for authentication."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Credentials supplied to log in."""

    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """JWT token returned after a successful login."""

    access_token: str
    token_type: str = "bearer"
