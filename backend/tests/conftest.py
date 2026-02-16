"""Conftest"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from data.database_connection import async_engine
from unittest.mock import patch

@pytest.fixture(autouse=True)
async def db_session():
    """Each test runs in a transaction that gets rolled back"""
    async with async_engine.connect() as connection:
        async with connection.begin() as transaction:
            # Create a session maker bound to this test transaction
            test_session_local = async_sessionmaker(
                bind=connection,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )

            # Patch the session maker in your database module
            with patch('data.database_connection.async_session', test_session_local):
                yield connection

            # Rollback happens automatically when context exits
            await transaction.rollback()
