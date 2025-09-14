import secrets
from datetime import datetime

from src.application.dto.user import UserCreateDTO
from src.domain.entities.user import UserEntity
from src.domain.entities.verification import VerificationEntity
from src.domain.exceptions import (
    EmailAlreadyTakenError,
    InvalidCredentialsError,
    UserNotFoundError,
    UserNotVerifiedError,
    VerificationCodeInvalidError,
)
from src.domain.interfaces.uow import IUnitOfWork
from src.domain.ports.password_hasher import PasswordHasher
from src.domain.ports.token_provider import TokenProvider
from src.domain.value_objects.email_address import EmailAddress
from src.domain.value_objects.user_role import UserRole
from src.domain.value_objects.verification_channel import VerificationChannel


class AuthService:
    """
    Authentication & verification use-cases.
    """

    def __init__(self, uow: IUnitOfWork, hasher: PasswordHasher, tokens: TokenProvider, verif_ttl_min: int) -> None:
        self.uow = uow
        self.hasher = hasher
        self.tokens = tokens
        self.verif_ttl_min = verif_ttl_min

    async def signup(self, email: str, password: str, first: str | None, last: str | None) -> UserEntity:
        """Create a new unverified user and issue a verification code."""
        async with self.uow as uow:
            if await uow.users.get_by_email(EmailAddress(email)):
                raise EmailAlreadyTakenError(f"Email {email} is already taken")
            now = datetime.now()
            user = UserCreateDTO(
                email=EmailAddress(email).as_str(),
                password=self.hasher.hash(password),
                first_name=first,
                last_name=last,
                role=UserRole.USER,
            )
            user = await uow.users.add(user.model_dump())

            code = secrets.token_hex(3)  # 6 hex chars
            ver = VerificationEntity.new(
                user_id=user.id, code=code, channel=VerificationChannel.EMAIL, ttl_minutes=self.verif_ttl_min, now=now
            )
            await uow.verifications.add(ver)
            return user

    async def login(self, email: str, password: str) -> tuple[str, str]:
        """Validate credentials and return (access, refresh) tokens."""
        async with self.uow as uow:
            user = await uow.users.get_by_email(EmailAddress(email))
            if not user:
                raise InvalidCredentialsError("Invalid email or password")
            if not self.hasher.verify(password, user.password):
                raise InvalidCredentialsError("Invalid email or password")
            if not user.is_verified:
                raise UserNotVerifiedError("User must be verified before login")

            access = self.tokens.issue_access(str(user.id), {"role": user.role.value})
            refresh = self.tokens.issue_refresh(str(user.id))
            return access, refresh

    async def refresh(self, subject: str) -> str:
        """Issue a new access token for given subject id."""
        async with self.uow as uow:
            user = await uow.users.get_by_id(int(subject))
            if not user:
                raise UserNotFoundError("Subject not found")
            return self.tokens.issue_access(str(user.id), {"role": user.role.value})

    async def verify(self, email: str, code: str) -> None:
        """Confirm verification by code."""
        async with self.uow as uow:
            user = await uow.users.get_by_email(EmailAddress(email))
            if not user:
                raise UserNotFoundError("User not found")

            latest = await uow.verifications.get_latest_for_user(user.id)
            now = datetime.now()
            if not latest or latest.code != code or latest.is_expired(now) or latest.is_consumed():
                raise VerificationCodeInvalidError("Invalid or expired verification code")

            latest.consume(now)
            await uow.verifications.mark_consumed(latest)
            user.verify()
            await uow.users.update(user_id=user.id, data={"is_verified": user.is_verified})
