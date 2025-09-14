from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class BaseEntity:
    """
    Pure domain base entity.
    Keeps identity and timestamps without any dependency on infrastructure.
    """

    id: int | None
    created_at: datetime
    updated_at: datetime | None
