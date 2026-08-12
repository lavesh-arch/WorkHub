import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlmodel.ext.asyncio.session import AsyncSession

from workhub.db.session import get_session
from workhub.schemas.user import (
    UserCreate,
    UserProfileResponse,
    UserProfileUpdate,
    UserResponse,
    UserUpdate,
)
from workhub.services.user import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

user_service = UserService()


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.create_user(
        session,
        data,
    )


@router.get(
    "",
    response_model=list[UserResponse],
)
async def get_users(
    session: AsyncSession = Depends(get_session),
):
    return await user_service.get_users(session)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.get_user(
        session,
        user_id,
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.update_user(
        session,
        user_id,
        data,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    await user_service.delete_user(
        session,
        user_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse,
)
async def activate_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.activate_user(
        session,
        user_id,
    )


@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse,
)
async def deactivate_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.deactivate_user(
        session,
        user_id,
    )


@router.get(
    "/{user_id}/profile",
    response_model=UserProfileResponse,
)
async def get_profile(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.get_profile(
        session,
        user_id,
    )


@router.patch(
    "/{user_id}/profile",
    response_model=UserProfileResponse,
)
async def update_profile(
    user_id: uuid.UUID,
    data: UserProfileUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.update_profile(
        session,
        user_id,
        data,
    )