"""Database Connection"""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from config import database_connection_string

TESTING = os.getenv("TESTING", "0") == "1"


if TESTING:
    async_engine = create_async_engine(
        database_connection_string, connect_args={"timeout": 30}, poolclass=NullPool
    )
else:
    async_engine = create_async_engine(
        database_connection_string,
        connect_args={"timeout": 30},
        pool_size=20,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
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
