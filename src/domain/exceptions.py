"""
Domain-specific exceptions with default codes/messages.
Keep them framework-agnostic.
"""


class DomainError(Exception):
    """
    Base class for all domain-related errors.
    Subclasses must override `code` and `default_message`.
    """

    code: str = "domain_error"
    default_message: str = "Domain error occurred."

    def __init__(self, message: str | None = None) -> None:
        """
        Initialize error with optional override message.
        If message is omitted, `default_message` is used.
        """
        super().__init__(message or self.default_message)
        self.message = message or self.default_message  # explicit attribute for convenience


class EmailAlreadyTakenError(DomainError):
    code = "email_already_taken"
    default_message = "Email is already in use."


class UserNotFoundError(DomainError):
    code = "user_not_found"
    default_message = "User not found."


class UserNotVerifiedError(DomainError):
    code = "user_not_verified"
    default_message = "User must be verified before performing this action."


class InvalidCredentialsError(DomainError):
    code = "invalid_credentials"
    default_message = "Invalid email or password."


class VerificationCodeInvalidError(DomainError):
    code = "verification_invalid"
    default_message = "Invalid or expired verification code."


class AccessDeniedError(DomainError):
    code = "access_denied"
    default_message = "You do not have permission to perform this action."


class InvalidEmailAddressError(DomainError):
    code = "invalid_email"
    default_message = "The provided email address is not valid."
