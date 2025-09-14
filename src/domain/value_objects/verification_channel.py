import enum


class VerificationChannel(enum.StrEnum):
    """
    Verification channel enum (business meaning).
    """

    EMAIL = "email"
    SMS = "sms"
