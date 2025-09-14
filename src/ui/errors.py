from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from src.domain.exceptions import (
    AccessDeniedError,
    DomainError,
    EmailAlreadyTakenError,
    InvalidCredentialsError,
    InvalidEmailAddressError,
    UserNotFoundError,
    UserNotVerifiedError,
    VerificationCodeInvalidError,
)
from src.ui.schemas.error import ErrorResponse

# Mapping domain errors -> HTTP status codes
DOMAIN_HTTP_STATUS = {
    EmailAlreadyTakenError: status.HTTP_409_CONFLICT,
    InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
    UserNotVerifiedError: status.HTTP_403_FORBIDDEN,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    VerificationCodeInvalidError: status.HTTP_400_BAD_REQUEST,
    AccessDeniedError: status.HTTP_403_FORBIDDEN,
    InvalidEmailAddressError: status.HTTP_422_UNPROCESSABLE_ENTITY,
}


def install_error_handlers(app: FastAPI) -> None:
    """
    Register exception handlers that convert domain errors to HTTP responses.
    """

    @app.exception_handler(DomainError)
    async def domain_error_handler(_req: Request, exc: DomainError) -> JSONResponse:
        """
        Map any DomainError (and its subclasses) to a JSON API error response.
        """
        http_status = DOMAIN_HTTP_STATUS.get(type(exc), status.HTTP_400_BAD_REQUEST)
        payload = ErrorResponse(code=exc.code, message=exc.message).model_dump()
        return JSONResponse(status_code=http_status, content=payload)
