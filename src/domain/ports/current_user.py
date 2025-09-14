from typing import Protocol


class CurrentUser(Protocol):
    """
    Port that represents the caller identity in the current context.
    """

    def subject(self) -> str | None:
        """Return the subject id (as string) or None if unauthenticated."""

    def claims(self) -> dict:
        """Return a dict of claims associated with the caller."""
