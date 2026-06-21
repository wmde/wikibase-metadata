"""Test Aggregate Property Popularity Query"""

from datetime import datetime, timezone

import pytest
from model.database.wikibase_observation.log.wikibase_log_month_log_type_observation_model import WikibaseLogMonthLogTypeObservationModel
from model.database.wikibase_observation.log.wikibase_log_month_observation_model import WikibaseLogMonthObservationModel
from model.enum.wikibase_log_type_enum import WikibaseLogType
from model.enum.wikibase_type_enum import WikibaseType
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.property.count_model import WikibasePropertyPopularityCountModel
from model.database.wikibase_observation.property.popularity_observation_model import WikibasePropertyPopularityObservationModel
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_page_meta,
)

AGGREGATED_PROPERTY_POPULARITY_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
  aggregatePropertyPopularity(
    pageNumber: $pageNumber
    pageSize: $pageSize
    wikibaseFilter: $wikibaseFilter
  ) {
    meta {
      pageNumber
      pageSize
      totalCount
      totalPages
    }
    data {
      id
      propertyUrl
      usageCount
      wikibaseCount
    }
  }
}
"""

@pytest.fixture
async def wikibase_with_four_log_observations(db_session):
    """Create a wikibase with 4 last-month log observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Log All Observations Test Wikibase",
            base_url="https://log-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        observation_ids = []
        log_type_ids = []

        # observation 0: single THANK log
        obs0 = WikibaseLogMonthObservationModel(wikibase_id=wikibase.id, first_month=False)
        obs0.returned_data = True
        obs0.observation_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        obs0.first_log_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        obs0.last_log_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
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
        lt0.first_log_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        lt0.last_log_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        lt0.log_count = 1
        lt0.user_count = 0
        lt0.active_user_count = 0
        lt0.human_user_count = 0
        lt0.active_human_user_count = 0
        session.add(lt0)
        await session.flush()
        await session.refresh(lt0)
        observation_ids.append(str(obs0.id))
        log_type_ids.append(str(lt0.id))

        # observation 1: 31 THANK logs over the month
        obs1 = WikibaseLogMonthObservationModel(wikibase_id=wikibase.id, first_month=False)
        obs1.returned_data = True
        obs1.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs1.first_log_date = datetime(2024, 1, 31, tzinfo=timezone.utc)
        obs1.last_log_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs1.log_count = 31
        obs1.user_count = 0
        obs1.active_user_count = 0
        obs1.human_user_count = 0
        obs1.active_human_user_count = 0
        session.add(obs1)
        await session.flush()
        await session.refresh(obs1)

        lt1 = WikibaseLogMonthLogTypeObservationModel()
        lt1.log_month_observation_id = obs1.id
        lt1.log_type = WikibaseLogType.THANK
        lt1.first_log_date = datetime(2024, 1, 31, tzinfo=timezone.utc)
        lt1.last_log_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        lt1.log_count = 31
        lt1.user_count = 0
        lt1.active_user_count = 0
        lt1.human_user_count = 0
        lt1.active_human_user_count = 0
        session.add(lt1)
        await session.flush()
        await session.refresh(lt1)
        observation_ids.append(str(obs1.id))
        log_type_ids.append(str(lt1.id))

        # observation 2: failed fetch
        obs2 = WikibaseLogMonthObservationModel(wikibase_id=wikibase.id, first_month=False)
        obs2.returned_data = False
        obs2.observation_date = datetime(2024, 3, 2, tzinfo=timezone.utc)
        session.add(obs2)
        await session.flush()
        await session.refresh(obs2)
        observation_ids.append(str(obs2.id))

        # observation 3: empty success
        obs3 = WikibaseLogMonthObservationModel(wikibase_id=wikibase.id, first_month=False)
        obs3.returned_data = True
        obs3.observation_date = datetime(2024, 3, 3, tzinfo=timezone.utc)
        obs3.first_log_date = None
        obs3.last_log_date = None
        obs3.log_count = 0
        obs3.user_count = 0
        obs3.active_user_count = 0
        obs3.human_user_count = 0
        obs3.active_human_user_count = 0
        session.add(obs3)
        await session.flush()
        await session.refresh(obs3)
        observation_ids.append(str(obs3.id))

        wikibase_id = wikibase.id

    return {
        "wikibase_id": wikibase_id,
        "observation_ids": observation_ids,
        "log_type_ids": log_type_ids,
    }




@pytest.fixture
async def wikibase_with_property_popularity(db_session):
    """Create a wikibase with property popularity observation: P1=12, P14=1"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Property Popularity Test Wikibase",
            base_url="https://property-popularity-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibasePropertyPopularityObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs)
        await session.flush()
        await session.refresh(obs)

        p1 = WikibasePropertyPopularityCountModel(property_url="P1", usage_count=12)
        p1.wikibase_property_popularity_observation_id = obs.id
        session.add(p1)

        p14 = WikibasePropertyPopularityCountModel(property_url="P14", usage_count=1)
        p14.wikibase_property_popularity_observation_id = obs.id
        session.add(p14)

        await session.flush()
        await session.refresh(p1)
        await session.refresh(p14)

        wikibase_id = wikibase.id
        p1_id = str(p1.id)
        p14_id = str(p14.id)
    return wikibase_id, p1_id, p14_id


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.property
@pytest.mark.query
async def test_aggregate_property_popularity_query(wikibase_with_property_popularity):
    """Test Aggregate Property Popularity Query"""

    _, p1_id, p14_id = wikibase_with_property_popularity

    result = await test_schema.execute(
        AGGREGATED_PROPERTY_POPULARITY_QUERY,
        variable_values={"pageNumber": 1, "pageSize": 30},
    )

    assert result.errors is None
    assert result.data is not None

    assert_page_meta(result.data["aggregatePropertyPopularity"], 1, 30, 2, 1)

    assert_layered_property_count(
        result.data, ["aggregatePropertyPopularity", "data"], 2
    )

    for index, (expected_id, expected_property_url, expected_usage_count) in enumerate(
        [(p1_id, "P1", 12), (p14_id, "P14", 1)]
    ):
        assert_layered_property_value(
            result.data,
            ["aggregatePropertyPopularity", "data", index, "id"],
            expected_id,
        )
        assert_layered_property_value(
            result.data,
            ["aggregatePropertyPopularity", "data", index, "propertyUrl"],
            expected_property_url,
        )
        assert_layered_property_value(
            result.data,
            ["aggregatePropertyPopularity", "data", index, "usageCount"],
            expected_usage_count,
        )
        assert_layered_property_value(
            result.data,
            ["aggregatePropertyPopularity", "data", index, "wikibaseCount"],
            1,
        )


@pytest.fixture
async def wikibase_with_property_popularity_suite(db_session):
    """Create a SUITE wikibase with 2 distinct properties for filtered aggregate tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Property Popularity Filtered Test Wikibase",
            base_url="https://property-popularity-filtered-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType.SUITE
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibasePropertyPopularityObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs)
        await session.flush()
        await session.refresh(obs)

        p1 = WikibasePropertyPopularityCountModel(property_url="P1", usage_count=12)
        p1.wikibase_property_popularity_observation_id = obs.id
        session.add(p1)

        p14 = WikibasePropertyPopularityCountModel(property_url="P14", usage_count=1)
        p14.wikibase_property_popularity_observation_id = obs.id
        session.add(p14)

        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 2),
        (["CLOUD"], 2),
        (["OTHER"], 2),
        (["SUITE"], 0),
        (["CLOUD", "OTHER"], 2),
        (["CLOUD", "SUITE"], 0),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_property_popularity_query_filtered(
    exclude: list, expected_count: int, wikibase_with_property_popularity_suite
):
    """Test Aggregate Property Popularity Query"""

    result = await test_schema.execute(
        AGGREGATED_PROPERTY_POPULARITY_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 1,
            "wikibaseFilter": {"wikibaseType": {"exclude": exclude}},
        },
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data,
        ["aggregatePropertyPopularity", "meta", "totalCount"],
        expected_count,
    )