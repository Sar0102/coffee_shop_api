import time
from collections.abc import Mapping

import jwt

from src.configs.jwt import jwt_settings
from src.domain.ports.token_provider import TokenProvider


class JwtTokenProvider(TokenProvider):
    """
    PyJWT adapter for TokenProvider port.
    """

    def __init__(self) -> None:
        self._settings = jwt_settings

    def issue_access(self, subject: str, claims: Mapping[str, str]) -> str:
        now = int(time.time())
        payload = {
            "sub": subject,
            "type": "access",
            "iat": now,
            "exp": now + self._settings.access_ttl_min * 60,
            **claims,
        }
        return jwt.encode(payload, self._settings.secret, algorithm=self._settings.algorithm)

    def issue_refresh(self, subject: str) -> str:
        now = int(time.time())
        payload = {
            "sub": subject,
            "type": "refresh",
            "iat": now,
            "exp": now + self._settings.refresh_ttl_days * 86400,
        }
        return jwt.encode(payload, self._settings.secret, algorithm=self._settings.algorithm)

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self._settings.secret, algorithms=[self._settings.algorithm])


token_provider = JwtTokenProvider()
