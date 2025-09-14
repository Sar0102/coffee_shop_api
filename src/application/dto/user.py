from pydantic import BaseModel

from src.domain.value_objects.user_role import UserRole


class UserOutDTO(BaseModel):
    id: int
    email: str
    first_name: str | None
    last_name: str | None
    is_verified: bool
    role: UserRole


class UserCreateDTO(BaseModel):
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    role: UserRole


class UserUpdateDTO(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    role: UserRole | None = None
