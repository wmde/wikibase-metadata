"""Conftest"""

from unittest.mock import patch

from dotenv import load_dotenv
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from data.database_connection import async_engine
from model.database import WikibaseModel
from model.enum import WikibaseType

load_dotenv()


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


@pytest.fixture
async def wikibase_fixture(db_session):  # pylint: disable=redefined-outer-name
    """Create Wikibase Test Fixture"""

    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Test Wikibase",
            base_url="https://fixture-example.com",
            sparql_endpoint_url="https://fixture-example.com/sparql",
            script_path="/w",
            article_path="/wiki",
            reuse=True,
            wikibase_type=WikibaseType.CLOUD,
        )
        wikibase.checked = True
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        return wikibase
