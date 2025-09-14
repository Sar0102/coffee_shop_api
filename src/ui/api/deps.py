from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError, PyJWTError, ExpiredSignatureError
from starlette import status

from src.domain.value_objects.user_role import UserRole
from src.infrastructure.security.jwt_token_provider import token_provider

bearer = HTTPBearer(auto_error=True)


def get_claims(creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]) -> dict:
    """
    Decode token from Authorization header.
    Returns decoded claims; raises HTTP 401 on failure.
    """
    try:
        return token_provider.decode(creds.credentials)
    except ExpiredSignatureError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired") from err
    except InvalidTokenError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from err
    except PyJWTError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from err


def get_subject_id(claims: Annotated[dict, Depends(get_claims)]) -> int:
    """Extract subject id from claims."""
    return int(claims.get("sub"))


def require_role(claims: dict, *roles: UserRole) -> None:
    """Role guard inside presentation layer."""
    role = claims.get("role")
    if roles and role not in {r.value for r in roles}:
        raise HTTPException(status_code=403, detail="Forbidden")
