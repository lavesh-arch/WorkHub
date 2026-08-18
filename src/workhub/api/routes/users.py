import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from workhub.api.dependencies import (
    allow_first_admin_or_require_admin,
    get_current_user,
    require_roles,
)
from workhub.db.session import get_session
from workhub.models.user import User, UserRole
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
    current_user: User | None = Depends(
        allow_first_admin_or_require_admin
    ),
):
    # Bootstrap protection:
    # If there are no users, the first user MUST be an Admin.
    if current_user is None and data.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The first user must have the admin role",
        )

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
    current_user: User = Depends(get_current_user),
):
    return await user_service.get_users(session)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
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
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    await user_service.delete_user(
        session,
        user_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse,
)
async def activate_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
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
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
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
    current_user: User = Depends(get_current_user),
):
    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own profile",
        )

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
    current_user: User = Depends(get_current_user),
):
    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile",
        )

    return await user_service.update_profile(
        session,
        user_id,
        data,
    )