"""Test Aggregate Property Popularity Query"""

from datetime import datetime, timezone

import pytest

from data import get_async_session
from model.database import (
    WikibaseLogMonthLogTypeObservationModel,
    WikibaseLogMonthObservationModel,
    WikibaseModel,
    WikibasePropertyPopularityCountModel,
    WikibasePropertyPopularityObservationModel,
)
from model.enum import WikibaseLogType, WikibaseType
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
async def wikibase_with_property_popularity(
    db_session,
):  # pylint: disable=unused-argument
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
async def test_aggregate_property_popularity_query(
    wikibase_with_property_popularity,
):  # pylint: disable=redefined-outer-name
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
async def wikibase_with_property_popularity_suite(
    db_session,
):  # pylint: disable=unused-argument
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
):  # pylint: disable=redefined-outer-name, unused-argument
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
