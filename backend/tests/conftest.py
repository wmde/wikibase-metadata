"""Conftest"""

from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from model.database.wikibase_observation.property.count_model import (
    WikibasePropertyPopularityCountModel,
)
from model.database.wikibase_observation.property.popularity_observation_model import (
    WikibasePropertyPopularityObservationModel,
)
from model.database.wikibase_observation.log.wikibase_log_month_log_type_observation_model import (
    WikibaseLogMonthLogTypeObservationModel,
)
from model.database.wikibase_observation.log.wikibase_log_month_observation_model import (
    WikibaseLogMonthObservationModel,
)
from model.database.wikibase_observation.log.wikibase_log_month_user_type_observation_model import (
    WikibaseLogMonthUserTypeObservationModel,
)
from model.enum.wikibase_log_type_enum import WikibaseLogType
from model.enum.wikibase_user_type_enum import WikibaseUserType
from model.database.wikibase_observation.user.wikibase_user_group_model import (
    WikibaseUserGroupModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_group_model import (
    WikibaseUserObservationGroupModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_model import (
    WikibaseUserObservationModel,
)
from model.database.wikibase_model import WikibaseModel
from data.database_connection import async_engine, get_async_session
from unittest.mock import patch
from dotenv import load_dotenv
from resolvers.update.update_wikibase_language import add_wikibase_language

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
async def wikibase_without_type(db_session):  # pylint: disable=redefined-outer-name
    """Create Wikibase Test Fixture"""

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
        session.add(wikibase)
        await session.flush()

        return wikibase


@pytest.fixture
# pylint: disable-next=too-many-statements, too-many-locals
async def wikibase_with_first_month_log_observations(
    db_session,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Create a wikibase with 3 first-month log observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Log First Month All Observations Test Wikibase",
            base_url="https://log-first-month-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        ids = {"obs": [], "log_type": [], "user_type": []}

        # observation 0: single THANK log
        obs0 = WikibaseLogMonthObservationModel(
            wikibase_id=wikibase.id, first_month=True
        )
        obs0.returned_data = True
        obs0.observation_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        obs0.first_log_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        obs0.last_log_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        obs0.last_log_user_type = None
        obs0.log_count = 1
        obs0.user_count = 0
        obs0.active_user_count = 0
        obs0.human_user_count = 0
        obs0.active_human_user_count = 0
        session.add(obs0)
        await session.flush()
        await session.refresh(obs0)

        lt0 = WikibaseLogMonthLogTypeObservationModel()
        lt0.log_month_observation_id = obs0.id
        lt0.log_type = WikibaseLogType.THANK
        lt0.first_log_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        lt0.last_log_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        lt0.log_count = 1
        lt0.user_count = 0
        lt0.active_user_count = 0
        lt0.human_user_count = 0
        lt0.active_human_user_count = 0
        session.add(lt0)
        await session.flush()
        await session.refresh(lt0)
        ids["obs"].append(str(obs0.id))
        ids["log_type"].append(str(lt0.id))

        # observation 1: 31 THANK logs, 3 users across 3 user types
        obs1 = WikibaseLogMonthObservationModel(
            wikibase_id=wikibase.id, first_month=True
        )
        obs1.returned_data = True
        obs1.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs1.first_log_date = datetime(2023, 10, 24, tzinfo=timezone.utc)
        obs1.last_log_date = datetime(2023, 11, 23, tzinfo=timezone.utc)
        obs1.last_log_user_type = WikibaseUserType.USER
        obs1.log_count = 31
        obs1.user_count = 3
        obs1.active_user_count = 3
        obs1.human_user_count = 1
        obs1.active_human_user_count = 1
        session.add(obs1)
        await session.flush()
        await session.refresh(obs1)

        lt1 = WikibaseLogMonthLogTypeObservationModel()
        lt1.log_month_observation_id = obs1.id
        lt1.log_type = WikibaseLogType.THANK
        lt1.first_log_date = datetime(2023, 10, 24, tzinfo=timezone.utc)
        lt1.last_log_date = datetime(2023, 11, 23, tzinfo=timezone.utc)
        lt1.log_count = 31
        lt1.user_count = 3
        lt1.active_user_count = 3
        lt1.human_user_count = 1
        lt1.active_human_user_count = 1
        session.add(lt1)
        await session.flush()
        await session.refresh(lt1)
        ids["obs"].append(str(obs1.id))
        ids["log_type"].append(str(lt1.id))

        user_type_data = [
            (
                WikibaseUserType.BOT,
                datetime(2023, 10, 26),
                datetime(2023, 11, 21),
                10,
                1,
                1,
            ),
            (
                WikibaseUserType.MISSING,
                datetime(2023, 10, 25),
                datetime(2023, 11, 22),
                10,
                1,
                1,
            ),
            (
                WikibaseUserType.USER,
                datetime(2023, 10, 24),
                datetime(2023, 11, 23),
                11,
                1,
                1,
            ),
        ]
        for (
            user_type,
            first_date,
            last_date,
            log_count,
            user_count,
            active_count,
        ) in user_type_data:
            ut = WikibaseLogMonthUserTypeObservationModel()
            ut.log_month_observation_id = obs1.id
            ut.user_type = user_type
            ut.first_log_date = first_date.replace(tzinfo=timezone.utc)
            ut.last_log_date = last_date.replace(tzinfo=timezone.utc)
            ut.log_count = log_count
            ut.user_count = user_count
            ut.active_user_count = active_count
            session.add(ut)
            await session.flush()
            await session.refresh(ut)
            ids["user_type"].append(str(ut.id))

        # observation 2: failed fetch
        obs2 = WikibaseLogMonthObservationModel(
            wikibase_id=wikibase.id, first_month=True
        )
        obs2.returned_data = False
        obs2.observation_date = datetime(2024, 3, 2, tzinfo=timezone.utc)
        session.add(obs2)
        await session.flush()
        await session.refresh(obs2)
        ids["obs"].append(str(obs2.id))

        wikibase_id = wikibase.id

    return {"wikibase_id": wikibase_id, **ids}


@pytest.fixture
async def wikibase_with_three_property_popularity_observations(
    db_session,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Create a wikibase with 3 property popularity observations: empty, P1/P14, and failed"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Property Popularity All Observations Test Wikibase",
            base_url="https://property-popularity-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        # observation 0: empty, no properties
        obs0 = WikibasePropertyPopularityObservationModel()
        obs0.wikibase_id = wikibase.id
        obs0.returned_data = True
        obs0.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs0)
        await session.flush()
        await session.refresh(obs0)

        # observation 1: P1=12, P14=1
        obs1 = WikibasePropertyPopularityObservationModel()
        obs1.wikibase_id = wikibase.id
        obs1.returned_data = True
        obs1.observation_date = datetime(2024, 3, 2, tzinfo=timezone.utc)
        session.add(obs1)
        await session.flush()
        await session.refresh(obs1)

        p1 = WikibasePropertyPopularityCountModel(property_url="P1", usage_count=12)
        p1.wikibase_property_popularity_observation_id = obs1.id
        session.add(p1)

        p14 = WikibasePropertyPopularityCountModel(property_url="P14", usage_count=1)
        p14.wikibase_property_popularity_observation_id = obs1.id
        session.add(p14)

        await session.flush()
        await session.refresh(p1)
        await session.refresh(p14)

        # observation 2: failed fetch
        obs2 = WikibasePropertyPopularityObservationModel()
        obs2.wikibase_id = wikibase.id
        obs2.returned_data = False
        obs2.observation_date = datetime(2024, 3, 3, tzinfo=timezone.utc)
        session.add(obs2)
        await session.flush()
        await session.refresh(obs2)

        wikibase_id = wikibase.id

    return {
        "wikibase_id": wikibase_id,
        "obs0_id": str(obs0.id),
        "obs1_id": str(obs1.id),
        "obs2_id": str(obs2.id),
        "p1_id": str(p1.id),
        "p14_id": str(p14.id),
    }


@pytest.fixture
async def wikibase_with_user_observation(
    db_session,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Create a wikibase with user observation for aggregate users tests"""
    async with AsyncSession(bind=db_session) as session:
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
        # observation.user_group_observations = 8
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
        group_obs.wikibase_user_observation = observation
        session.add(group_obs)
        await session.flush()

        return wikibase.id, observation.id
