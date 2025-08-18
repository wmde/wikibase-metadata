"""Database Connection"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import database_connection_string

async_engine = create_async_engine(
    database_connection_string,
    pool_size=5,  # default
    max_overflow=10,  # default
    timeout=120,  # default 30, but we need more time for big queries, toolforge is slow
)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get Async Session"""
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()
