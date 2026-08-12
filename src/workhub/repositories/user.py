import uuid

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from workhub.models.user import User
from workhub.models.user_profile import UserProfile


class UserRepository:

    async def create(
        self,
        session: AsyncSession,
        user: User,
    ) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def get_by_id(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> User | None:
        statement = select(User).where(User.id == user_id)

        result = await session.exec(statement)

        return result.first()

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> User | None:
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        return result.first()

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[User]:
        statement = select(User).order_by(User.created_at.desc())

        result = await session.exec(statement)

        return list(result.all())

    async def update(
        self,
        session: AsyncSession,
        user: User,
    ) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def delete(
        self,
        session: AsyncSession,
        user: User,
    ) -> None:
        await session.delete(user)
        await session.commit()

    async def get_profile(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> UserProfile | None:
        statement = select(UserProfile).where(
            UserProfile.user_id == user_id
        )

        result = await session.exec(statement)

        return result.first()

    async def create_profile(
        self,
        session: AsyncSession,
        profile: UserProfile,
    ) -> UserProfile:
        session.add(profile)
        await session.commit()
        await session.refresh(profile)

        return profile

    async def update_profile(
        self,
        session: AsyncSession,
        profile: UserProfile,
    ) -> UserProfile:
        session.add(profile)
        await session.commit()
        await session.refresh(profile)

        return profile