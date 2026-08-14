from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from workhub.api.dependencies import get_current_user
from workhub.db.session import get_session
from workhub.models.user import User
from workhub.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RefreshTokenRequest,
    TokenResponse,
)
from workhub.services.auth import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    return await auth_service.login(
        session,
        data,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh_token(
    data: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session),
):
    return await auth_service.refresh_access_token(
        session,
        data,
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def logout(
    data: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session),
):
    await auth_service.logout(
        session,
        data,
    )

    return {
        "message": "Logged out successfully"
    }


@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }