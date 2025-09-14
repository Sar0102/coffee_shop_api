import datetime as dt

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.value_objects.verification_channel import VerificationChannel
from src.infrastructure.db.base import ORMBase
from src.infrastructure.db.mixins import IdTimestampMixin


class VerificationORM(IdTimestampMixin, ORMBase):
    """
    ORM model for verification.
    """

    __tablename__ = "verifications"
    __table_args__ = (Index("ix_verif_user_created", "user_id", "created_at"),)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(String(32))
    channel: Mapped[VerificationChannel]
    expires_at: Mapped[dt.datetime]
    consumed_at: Mapped[dt.datetime | None]
