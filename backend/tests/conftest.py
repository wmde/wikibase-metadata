"""Conftest"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from data.database_connection import async_engine
from unittest.mock import patch


@pytest.fixture()
async def db_session():
    """Each test runs in a transaction that gets rolled back"""
    async with async_engine.connect() as connection:
        async with connection.begin() as transaction:
            test_session_local = async_sessionmaker(
                bind=connection,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )

            with patch("data.database_connection.async_session", test_session_local):
                yield connection

            await transaction.rollback()
