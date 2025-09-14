from dataclasses import dataclass

from src.domain.exceptions import InvalidEmailAddressError


@dataclass(frozen=True, slots=True)
class EmailAddress:
    """
    Simple email address value object.

    Note:
        Validation is intentionally minimal here; perform stricter checks at application boundary.
    """

    value: str

    def __post_init__(self) -> None:
        """Perform basic sanity check to avoid obviously broken values."""
        if "@" not in self.value or len(self.value) < 5:
            raise InvalidEmailAddressError("Invalid email address format")

    def as_str(self) -> str:
        """Return the raw email string."""
        return self.value.lower()
