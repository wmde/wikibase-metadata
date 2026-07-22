"""Test Aggregate Statistics Query"""

from datetime import datetime, timezone

import pytest

from data import get_async_session
from model.database import WikibaseModel, WikibaseStatisticsObservationModel
from model.enum import WikibaseType
from tests.test_query.wikibase.statistics_obs.assert_statistics import (
    assert_edits,
    assert_files,
    assert_pages,
    assert_users,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value

AGGREGATED_STATISTICS_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateStatistics(wikibaseFilter: $wikibaseFilter) {
    wikibaseCount
    edits {
      editsPerPageAvg
      totalEdits
    }
    files {
      totalFiles
    }
    pages {
      contentPageWordCountAvg
      contentPageWordCountTotal
      contentPages
      totalPages
    }
    users {
      activeUsers
      totalAdmin
      totalUsers
    }
  }
}
"""


@pytest.fixture
async def wikibases_with_statistics(db_session):  # pylint: disable=unused-argument
    """Create a wikibase and a wikibase suite with statistics observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Statistics Test Wikibase",
            base_url="https://aggregate-statistics-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType.OTHER
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseStatisticsObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.total_pages = 12655622
        obs.content_pages = 851723
        obs.total_files = 30
        obs.total_edits = 36150323
        obs.content_page_word_count_total = 27750
        obs.total_users = 465
        obs.active_users = 5
        obs.total_admin = 17
        session.add(obs)
        await session.flush()

        wikibase_suite = WikibaseModel(
            wikibase_name="Aggregate Statistics Filtered Test Wikibase",
            base_url="https://aggregate-statistics-filtered-example.com",
        )
        wikibase_suite.checked = True
        wikibase_suite.reuse = True
        wikibase_suite.test = False
        wikibase_suite.wikibase_type = WikibaseType.SUITE
        session.add(wikibase_suite)
        await session.flush()
        await session.refresh(wikibase_suite)

        suite_obs = WikibaseStatisticsObservationModel()
        suite_obs.wikibase_id = wikibase_suite.id
        suite_obs.returned_data = True
        suite_obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        suite_obs.total_pages = 100
        suite_obs.content_pages = 50
        suite_obs.total_files = 5
        suite_obs.total_edits = 200
        suite_obs.content_page_word_count_total = 1000
        suite_obs.total_users = 20
        suite_obs.active_users = 2
        suite_obs.total_admin = 1
        session.add(suite_obs)
        await session.flush()

        return obs, suite_obs


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.statistics
@pytest.mark.query
async def test_aggregate_statistics_query(
    wikibases_with_statistics,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate Statistics Query"""

    obs, suite_obs = wikibases_with_statistics

    result = await test_schema.execute(AGGREGATED_STATISTICS_QUERY)

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateStatistics", "wikibaseCount"], 2
    )

    expected_total_edits = obs.total_edits + suite_obs.total_edits
    expected_average_edits = expected_total_edits / (
        obs.total_pages + suite_obs.total_pages
    )
    assert_edits(
        result.data["aggregateStatistics"], expected_total_edits, expected_average_edits
    )
    assert_files(
        result.data["aggregateStatistics"], obs.total_files + suite_obs.total_files
    )

    expected_content_pages = obs.content_pages + suite_obs.content_pages
    expected_word_count_total = (
        obs.content_page_word_count_total + suite_obs.content_page_word_count_total
    )
    expected_word_count_avg = expected_word_count_total / expected_content_pages
    expected_total_pages = obs.total_pages + suite_obs.total_pages
    assert_pages(
        result.data["aggregateStatistics"],
        expected_content_pages,
        expected_word_count_avg,
        expected_word_count_total,
        expected_total_pages,
    )

    expected_users = obs.active_users + suite_obs.active_users
    expected_total_admin = obs.total_admin + suite_obs.total_admin
    expected_total_users = obs.total_users + suite_obs.total_users
    assert_users(
        result.data["aggregateStatistics"],
        expected_users,
        expected_total_admin,
        expected_total_users,
    )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 2),
        (["CLOUD"], 2),
        (["OTHER"], 1),
        (["SUITE"], 1),
        (["CLOUD", "OTHER"], 1),
        (["CLOUD", "SUITE"], 1),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_statistics_query_filtered(
    wikibases_with_statistics, exclude: list, expected_count: int
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate Statistics Query"""

    result = await test_schema.execute(
        AGGREGATED_STATISTICS_QUERY,
        variable_values={"wikibaseFilter": {"wikibaseType": {"exclude": exclude}}},
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateStatistics", "wikibaseCount"], expected_count
    )
