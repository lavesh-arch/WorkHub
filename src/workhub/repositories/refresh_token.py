import uuid
from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from workhub.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    async def create(
        self,
        session: AsyncSession,
        refresh_token: RefreshToken,
    ) -> RefreshToken:

        session.add(refresh_token)
        await session.commit()
        await session.refresh(refresh_token)

        return refresh_token

    async def get_by_hash(
        self,
        session: AsyncSession,
        token_hash: str,
    ) -> RefreshToken | None:

        statement = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )

        result = await session.exec(statement)

        return result.first()

    async def revoke(
        self,
        session: AsyncSession,
        refresh_token: RefreshToken,
    ) -> RefreshToken:

        refresh_token.revoked_at = datetime.utcnow()

        session.add(refresh_token)
        await session.commit()
        await session.refresh(refresh_token)

        return refresh_token