from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from starlette.responses import JSONResponse

from src.application.dto.auth import AccessTokenOUTDTO, LoginDTO, SignUpDTO, SignUpResponseDTO, TokenPairDTO, VerifyDTO
from src.application.services.auth_service import AuthService
from src.configs.jwt import jwt_settings
from src.infrastructure.db.uow import SqlAlchemyUnitOfWork
from src.infrastructure.notifications.mailer import send_verification_code_email
from src.infrastructure.security.argon2_password_hasher import hasher
from src.infrastructure.security.jwt_token_provider import token_provider
from src.ui.api.deps import get_claims
from src.ui.api.responses import AUTH_LOGIN_RESPONSES, AUTH_SIGNUP_RESPONSES, AUTH_VERIFY_RESPONSES, GENERIC_ERROR_RESPONSES

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    status_code=201,
    responses=AUTH_SIGNUP_RESPONSES,
    summary="Register a new user",
    description="Creates an unverified user and sends a verification code (printed to logs).",
)
async def signup(payload: SignUpDTO, bg: Annotated[BackgroundTasks, BackgroundTasks]) -> SignUpResponseDTO:
    """Create user and emit verification code (email channel)."""
    svc = AuthService(
        uow=SqlAlchemyUnitOfWork(),
        hasher=hasher,
        tokens=token_provider,
        verif_ttl_min=jwt_settings.access_ttl_min,
    )
    user = await svc.signup(payload.email, payload.password, payload.first_name, payload.last_name)

    async with SqlAlchemyUnitOfWork() as uow:
        ver = await uow.verifications.get_latest_for_user(user.id)
        if ver:
            bg.add_task(send_verification_code_email, user.email.as_str(), ver.code)
    return SignUpResponseDTO(id=user.id, email=user.email.as_str(), is_verified=user.is_verified)


@router.post(
    "/login",
    responses=AUTH_LOGIN_RESPONSES,
    summary="Login with email/password",
    description="Issues access and refresh tokens for a verified user.",
)
async def login(payload: LoginDTO) -> TokenPairDTO:
    """Authenticate user and return JWT pair."""
    svc = AuthService(SqlAlchemyUnitOfWork(), hasher, token_provider, verif_ttl_min=jwt_settings.access_ttl_min)
    access, refresh_ = await svc.login(payload.email, payload.password)
    return TokenPairDTO(access_token=access, refresh_token=refresh_)


@router.post(
    "/refresh",
    responses=GENERIC_ERROR_RESPONSES,
    summary="Refresh access token",
    description="Exchanges a refresh token for a new access token. Send refresh token in Authorization header.",
)
async def refresh(claims: Annotated[dict, Depends(get_claims)]) -> AccessTokenOUTDTO:
    """Refresh access token using a valid refresh token."""
    if claims.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Not a refresh token")

    svc = AuthService(SqlAlchemyUnitOfWork(), hasher, token_provider, verif_ttl_min=jwt_settings.access_ttl_min)
    access = await svc.refresh(claims["sub"])
    return AccessTokenOUTDTO(access_token=access)


@router.post(
    "/verify",
    summary="Verify user",
    responses=AUTH_VERIFY_RESPONSES,
    description="Confirms user verification by code.",
)
async def verify(payload: VerifyDTO) -> JSONResponse:
    """Consume verification code and mark user verified."""
    svc = AuthService(SqlAlchemyUnitOfWork(), hasher, token_provider, verif_ttl_min=jwt_settings.access_ttl_min)
    await svc.verify(payload.email, payload.code)
    return JSONResponse(content={"message": "User verified"})
