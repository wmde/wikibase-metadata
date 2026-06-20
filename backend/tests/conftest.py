"""Conftest"""

from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from model.database.wikibase_observation.user.wikibase_user_group_model import (
    WikibaseUserGroupModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_group_model import (
    WikibaseUserObservationGroupModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_model import (
    WikibaseUserObservationModel,
)
from data.database_connection import async_engine, get_async_session
from unittest.mock import patch
from dotenv import load_dotenv
import pytest
from model.database.wikibase_model import WikibaseModel

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
async def wikibase_fixture(db_session):
    """Create Wikibase Test Fixture"""
    from sqlalchemy.ext.asyncio import AsyncSession
    from resolvers import add_wikibase_language

    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Test Wikibase",
            base_url="https://example.com",
            sparql_endpoint_url="https://example.com/sparql",
            script_path="/w",
            article_path="/wiki",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = "CLOUD"
        session.add(wikibase)
        await session.flush()

        await add_wikibase_language(wikibase.id, "French")
        for lang in ["Deutsch", "Cymru"]:
            await add_wikibase_language(wikibase_id=wikibase.id, language=lang)

        return wikibase


@pytest.fixture
async def three_wikibases_fixture(db_session):
    """Create 3 test wikibases for connectivity tests"""
    from sqlalchemy.ext.asyncio import AsyncSession

    async with AsyncSession(bind=db_session) as session:
        wikibase_ids = []
        for i in range(3):
            wikibase = WikibaseModel(
                wikibase_name=f"Test Wikibase",
                base_url=f"https://example-{i}.com",
                sparql_endpoint_url=f"https://example-{i}.com/sparql",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)
            await session.flush()
            wikibase_ids.append(wikibase.id)

        return wikibase_ids


@pytest.fixture
async def wikibase_with_user_observation(db_session): # pylint: disable=unused-argument
    """Create a wikibase with user observation for aggregate users tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Users Test Wikibase",
            base_url="https://aggregate-users-example.com",
            script_path="/w",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        observation = WikibaseUserObservationModel()
        observation.wikibase_id = wikibase.id
        observation.returned_data = True
        observation.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        observation.total_users = 2000
        session.add(observation)
        await session.flush()
        await session.refresh(observation)

        sysop_group = WikibaseUserGroupModel(
            group_name="sysop",
            wikibase_default_group=True,
        )
        session.add(sysop_group)
        await session.flush()
        await session.refresh(sysop_group)

        group_obs = WikibaseUserObservationGroupModel(
            user_group=sysop_group,
            user_count=715,
            group_implicit=False,
        )
        group_obs.wikibase_user_observation_id = observation.id
        session.add(group_obs)
        await session.flush()
