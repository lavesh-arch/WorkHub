import hashlib
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from workhub.models.user import User
from workhub.models.user_profile import UserProfile
from workhub.repositories.user import UserRepository
from workhub.schemas.user import (
    UserCreate,
    UserProfileUpdate,
    UserUpdate,
)
from workhub.core.security import hash_password

class UserService:

    def __init__(self):
        self.repository = UserRepository()

    async def create_user(
        self,
        session: AsyncSession,
        data: UserCreate,
    ) -> User:

        existing_user = await self.repository.get_by_email(
            session,
            data.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            email=data.email,
            full_name=data.full_name,
            password_hash=hash_password(data.password),
            role=data.role,
        )

        return await self.repository.create(session, user)

    async def get_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> User:

        user = await self.repository.get_by_id(
            session,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    async def get_users(
        self,
        session: AsyncSession,
    ) -> list[User]:

        return await self.repository.get_all(session)

    async def update_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        data: UserUpdate,
    ) -> User:

        user = await self.get_user(session, user_id)

        if data.email and data.email != user.email:
            existing_user = await self.repository.get_by_email(
                session,
                data.email,
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered",
                )

            user.email = data.email

        if data.full_name is not None:
            user.full_name = data.full_name

        if data.role is not None:
            user.role = data.role

        user.updated_at = datetime.now(timezone.utc)

        return await self.repository.update(session, user)

    async def delete_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> None:

        user = await self.get_user(session, user_id)

        await self.repository.delete(session, user)

    async def activate_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> User:

        user = await self.get_user(session, user_id)

        user.is_active = True
        user.updated_at = datetime.now(timezone.utc)

        return await self.repository.update(session, user)

    async def deactivate_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> User:

        user = await self.get_user(session, user_id)

        user.is_active = False
        user.updated_at = datetime.now(timezone.utc)

        return await self.repository.update(session, user)

    async def get_profile(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> UserProfile:

        # First make sure the user exists.
        await self.get_user(session, user_id)

        profile = await self.repository.get_profile(
            session,
            user_id,
        )

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found",
            )

        return profile

    async def update_profile(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        data: UserProfileUpdate,
    ) -> UserProfile:

        await self.get_user(session, user_id)

        profile = await self.repository.get_profile(
            session,
            user_id,
        )

        if not profile:
            profile = UserProfile(
                user_id=user_id,
                avatar_url=data.avatar_url,
                bio=data.bio,
            )

            return await self.repository.create_profile(
                session,
                profile,
            )

        if data.avatar_url is not None:
            profile.avatar_url = data.avatar_url

        if data.bio is not None:
            profile.bio = data.bio

        profile.updated_at = datetime.now(timezone.utc)

        return await self.repository.update_profile(
            session,
            profile,
        )

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Temporary password hashing implementation.

        Authentication will replace this with a proper password
        hashing implementation when we build the authentication module.
        """
        return hashlib.sha256(password.encode()).hexdigest()