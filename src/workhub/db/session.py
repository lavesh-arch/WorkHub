from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from workhub.core.config import config


async_engine = create_async_engine(
    config.DATABASE_URL,
    echo=True,
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with async_session_maker() as session:
        yield session