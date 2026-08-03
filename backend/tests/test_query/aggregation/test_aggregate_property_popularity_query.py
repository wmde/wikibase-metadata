"""Test Aggregate Property Popularity Query"""

from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import (
    WikibaseModel,
    WikibasePropertyPopularityCountModel,
    WikibasePropertyPopularityObservationModel,
)
from model.enum import WikibaseType
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
async def wikibases_with_property_popularity(
    db_session,
):  # pylint: disable=unused-argument, too-many-statements
    """Create two wikibases with distinct property popularity observations:
    OTHER: P1=12, P14=1
    SUITE: P99=5, P100=3
    """
    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Property Popularity Test Wikibase",
            base_url="https://property-popularity-example.com",
            reuse=True,
            wikibase_type=WikibaseType.OTHER,
        )
        wikibase.checked = True
        wikibase.test = False
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

        wikibase_suite = WikibaseModel(
            wikibase_name="Property Popularity Filtered Test Wikibase",
            base_url="https://property-popularity-filtered-example.com",
            wikibase_type=WikibaseType.SUITE,
            reuse=True,
        )
        wikibase_suite.checked = True
        wikibase_suite.test = False
        session.add(wikibase_suite)
        await session.flush()
        await session.refresh(wikibase_suite)

        suite_obs = WikibasePropertyPopularityObservationModel()
        suite_obs.wikibase_id = wikibase_suite.id
        suite_obs.returned_data = True
        suite_obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(suite_obs)
        await session.flush()
        await session.refresh(suite_obs)

        p99 = WikibasePropertyPopularityCountModel(property_url="P99", usage_count=5)
        p99.wikibase_property_popularity_observation_id = suite_obs.id
        session.add(p99)

        p100 = WikibasePropertyPopularityCountModel(property_url="P100", usage_count=3)
        p100.wikibase_property_popularity_observation_id = suite_obs.id
        session.add(p100)

        await session.flush()
        await session.refresh(p99)
        await session.refresh(p100)

        p99_id = str(p99.id)
        p100_id = str(p100.id)

    return wikibase_id, p1_id, p14_id, p99_id, p100_id


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.property
@pytest.mark.query
async def test_aggregate_property_popularity_query(
    wikibases_with_property_popularity,
):  # pylint: disable=redefined-outer-name
    """Test Aggregate Property Popularity Query"""

    _, p1_id, p14_id, p99_id, p100_id = wikibases_with_property_popularity

    result = await test_schema.execute(
        AGGREGATED_PROPERTY_POPULARITY_QUERY,
        variable_values={"pageNumber": 1, "pageSize": 30},
    )

    assert result.errors is None
    assert result.data is not None

    assert_page_meta(result.data["aggregatePropertyPopularity"], 1, 30, 4, 1)

    assert_layered_property_count(
        result.data, ["aggregatePropertyPopularity", "data"], 4
    )

    for index, (expected_id, expected_property_url, expected_usage_count) in enumerate(
        [
            (p1_id, "P1", 12),
            (p99_id, "P99", 5),
            (p100_id, "P100", 3),
            (p14_id, "P14", 1),
        ]
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


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 4),
        (["CLOUD"], 4),
        (["OTHER"], 2),
        (["SUITE"], 2),
        (["CLOUD", "OTHER"], 2),
        (["CLOUD", "SUITE"], 2),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_property_popularity_query_filtered(
    exclude: list, expected_count: int, wikibases_with_property_popularity
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
