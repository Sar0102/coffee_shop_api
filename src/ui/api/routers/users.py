from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.application.dto.user import UserOutDTO, UserUpdateDTO
from src.application.services.user_service import UserService
from src.domain.value_objects.user_role import UserRole
from src.infrastructure.db.uow import SqlAlchemyUnitOfWork
from src.ui.api.deps import get_claims, get_subject_id, require_role
from src.ui.api.responses import GENERIC_ERROR_RESPONSES

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    responses=GENERIC_ERROR_RESPONSES,
    summary="Get current user",
    description="Returns profile of the caller.",
)
async def me(subject_id: Annotated[int, Depends(get_subject_id)]) -> UserOutDTO:
    """Return current user profile."""
    svc = UserService(SqlAlchemyUnitOfWork())
    user = await svc.me(subject_id)
    return UserOutDTO(
        id=user.id,
        email=user.email.as_str(),
        first_name=user.first_name,
        last_name=user.last_name,
        is_verified=user.is_verified,
        role=user.role,
    )


@router.get(
    "",
    responses=GENERIC_ERROR_RESPONSES,
    summary="List users (admin)",
    description="Returns a paginated list of users. Admin only.",
)
async def list_users(
    claims: Annotated[dict, Depends(get_claims)],
    offset: int = Query(0, ge=0),
    limit: int = Query(50, gt=0, le=200),
) -> list[UserOutDTO]:
    """Return users page (admin only)."""
    require_role(claims, UserRole.ADMIN)
    svc = UserService(SqlAlchemyUnitOfWork())
    users = await svc.list_users(offset, limit)
    return [
        UserOutDTO(
            id=u.id,
            email=u.email.as_str(),
            first_name=u.first_name,
            last_name=u.last_name,
            is_verified=u.is_verified,
            role=u.role,
        )
        for u in users
    ]


@router.get(
    "/{user_id}",
    summary="Get user by id (admin)",
    responses=GENERIC_ERROR_RESPONSES,
    description="Admin-only access to any user by id.",
)
async def get_user(user_id: int, claims: Annotated[dict, Depends(get_claims)]) -> UserOutDTO:
    """Return user by id."""
    require_role(claims, UserRole.ADMIN)
    svc = UserService(SqlAlchemyUnitOfWork())
    u = await svc.get_user(user_id)
    return UserOutDTO(
        id=u.id,
        email=u.email.as_str(),
        first_name=u.first_name,
        last_name=u.last_name,
        is_verified=u.is_verified,
        role=u.role,
    )


@router.patch(
    "/{user_id}",
    responses=GENERIC_ERROR_RESPONSES,
    summary="Patch user (admin)",
    description="Partial update of selected user fields. Admin only.",
)
async def patch_user(user_id: int, dto: UserUpdateDTO, claims: Annotated[dict, Depends(get_claims)]) -> UserOutDTO:
    """Partial update."""
    require_role(claims, UserRole.ADMIN)
    svc = UserService(SqlAlchemyUnitOfWork())
    u = await svc.patch_user(user_id, dto)
    return UserOutDTO(
        id=u.id,
        email=u.email.as_str(),
        first_name=u.first_name,
        last_name=u.last_name,
        is_verified=u.is_verified,
        role=u.role,
    )


@router.delete(
    "/{user_id}",
    status_code=204,
    responses=GENERIC_ERROR_RESPONSES,
    summary="Delete user (admin)",
    description="Deletes a user by id. Admin only.",
)
async def delete_user(user_id: int, claims: Annotated[dict, Depends(get_claims)]) -> None:
    """Delete user by id."""
    require_role(claims, UserRole.ADMIN)
    svc = UserService(SqlAlchemyUnitOfWork())
    await svc.delete_user(user_id)
    return
