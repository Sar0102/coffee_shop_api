from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.domain.ports.password_hasher import PasswordHasher as PasswordHasherPort


class Argon2PasswordHasher(PasswordHasherPort):
    """
    Argon2 adapter for PasswordHasher port.
    """

    def __init__(self, time_cost: int = 3, memory_cost_kb: int = 64 * 1024, parallelism: int = 4) -> None:
        self._ph = PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost_kb,
            parallelism=parallelism,
        )

    def hash(self, raw: str) -> str:
        """Hash a raw password using Argon2."""
        return self._ph.hash(raw)

    def verify(self, raw: str, hashed: str) -> bool:
        """Verify a raw password against the stored hash."""
        try:
            return self._ph.verify(hashed, raw)
        except VerifyMismatchError:
            return False


hasher = Argon2PasswordHasher()
