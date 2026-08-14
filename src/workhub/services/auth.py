import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from workhub.core.config import config
from workhub.core.security import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
    verify_password,
)
from workhub.models.refresh_token import RefreshToken
from workhub.repositories.refresh_token import RefreshTokenRepository
from workhub.repositories.user import UserRepository
from workhub.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
)


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.refresh_token_repository = RefreshTokenRepository()

    async def login(
        self,
        session: AsyncSession,
        data: LoginRequest,
    ) -> dict:

        user = await self.user_repository.get_by_email(
            session,
            data.email,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        password_valid = verify_password(
            data.password,
            user.password_hash,
        )

        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        raw_refresh_token = create_refresh_token()

        refresh_token = RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(
                raw_refresh_token
            ),
            expires_at=(
                datetime.utcnow()
                + timedelta(
                    days=config.REFRESH_TOKEN_EXPIRE_DAYS
                )
            ),
        )

        await self.refresh_token_repository.create(
            session,
            refresh_token,
        )

        return {
            "access_token": access_token,
            "refresh_token": raw_refresh_token,
            "token_type": "bearer",
        }

    async def refresh_access_token(
        self,
        session: AsyncSession,
        data: RefreshTokenRequest,
    ) -> dict:

        token_hash = hash_refresh_token(
            data.refresh_token
        )

        stored_token = (
            await self.refresh_token_repository.get_by_hash(
                session,
                token_hash,
            )
        )

        if not stored_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        if stored_token.revoked_at is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked",
            )

        if stored_token.expires_at <= datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired",
            )

        user = await self.user_repository.get_by_id(
            session,
            stored_token.user_id,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        # Rotate old refresh token.
        await self.refresh_token_repository.revoke(
            session,
            stored_token,
        )

        access_token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        new_raw_refresh_token = create_refresh_token()

        new_refresh_token = RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(
                new_raw_refresh_token
            ),
            expires_at=(
                datetime.utcnow()
                + timedelta(
                    days=config.REFRESH_TOKEN_EXPIRE_DAYS
                )
            ),
        )

        await self.refresh_token_repository.create(
            session,
            new_refresh_token,
        )

        return {
            "access_token": access_token,
            "refresh_token": new_raw_refresh_token,
            "token_type": "bearer",
        }

    async def logout(
        self,
        session: AsyncSession,
        data: RefreshTokenRequest,
    ) -> None:

        token_hash = hash_refresh_token(
            data.refresh_token
        )

        stored_token = (
            await self.refresh_token_repository.get_by_hash(
                session,
                token_hash,
            )
        )

        if stored_token and stored_token.revoked_at is None:
            await self.refresh_token_repository.revoke(
                session,
                stored_token,
            )