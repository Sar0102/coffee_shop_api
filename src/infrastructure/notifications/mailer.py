from __future__ import annotations

import email.utils
from email.mime.text import MIMEText
from typing import Final

import aiosmtplib

from src.configs.mail_settings import MailSettings


class AioSMTPMailer:
    """
    Mailer adapter using aiosmtplib.
    """

    def __init__(self, settings: MailSettings) -> None:
        self._cfg = settings

    async def send_text(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        """
        Send a simple text email.

        Args:
            to_email: Recipient address.
            subject: Email subject.
            body: Plain text content.
        """
        msg = MIMEText(body, _charset="utf-8")
        sender_formatted = email.utils.formataddr((self._cfg.sender_name, self._cfg.sender_email))
        msg["From"] = sender_formatted
        msg["To"] = to_email
        msg["Subject"] = subject

        # Connect & send
        await aiosmtplib.send(
            msg,
            hostname=self._cfg.smtp_host,
            port=self._cfg.smtp_port,
            username=self._cfg.smtp_username,
            password=self._cfg.smtp_password,
            start_tls=self._cfg.smtp_starttls,
            timeout=10.0,
        )


async def send_verification_code_email(to_email: str, code: str) -> None:
    """
    Send verification code email, using default MailSettings.
    """
    settings = MailSettings()
    mailer = AioSMTPMailer(settings)
    subject: Final[str] = "Your Coffee Shop verification code"
    body: Final[str] = f"Your verification code: {code}\nIf you didn't request this, ignore this email."
    await mailer.send_text(to_email, subject, body)
