import datetime as dt

from sqlalchemy import Integer, func
from sqlalchemy.orm import Mapped, mapped_column


class IdTimestampMixin:
    """
    Abstract mixin for common identity and timestamps fields.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    created_at: Mapped[dt.datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
