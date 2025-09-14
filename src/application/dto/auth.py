from pydantic import BaseModel, Field


class SignUpResponseDTO(BaseModel):
    """
    Response returned after successful signup.
    """

    id: int
    email: str
    is_verified: bool


class SignUpDTO(BaseModel):
    """Payload for user registration."""

    email: str
    password: str = Field(min_length=8)
    first_name: str | None = None
    last_name: str | None = None


class LoginDTO(BaseModel):
    """Payload for login."""

    email: str
    password: str


class VerifyDTO(BaseModel):
    """Payload for verification."""

    email: str
    code: str


class TokenPairDTO(BaseModel):
    """Issued token pair."""

    access_token: str
    refresh_token: str


class AccessTokenOUTDTO(BaseModel):
    access_token: str
