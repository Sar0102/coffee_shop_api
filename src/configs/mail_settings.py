from pydantic_settings import BaseSettings, SettingsConfigDict


class MailSettings(BaseSettings):
    """
    SMTP/MailDev configuration.
    In dev, MailDev listens on host: maildev, smtp: 1025, webui: 1080.
    """

    smtp_host: str = "maildev"
    smtp_port: int = 1025
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_starttls: bool = False
    sender_email: str = "no-reply@coffeeshop.local"
    sender_name: str = "Coffee Shop"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="MAIL_",
        extra="ignore",
    )
