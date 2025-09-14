from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.value_objects.user_role import UserRole
from src.infrastructure.db.base import ORMBase
from src.infrastructure.db.mixins import IdTimestampMixin


class UserORM(IdTimestampMixin, ORMBase):
    """
    ORM model for users table.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str | None] = mapped_column(String(120))
    last_name: Mapped[str | None] = mapped_column(String(120))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
