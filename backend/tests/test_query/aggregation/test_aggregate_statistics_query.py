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
async def wikibase_with_statistics(db_session):  # pylint: disable=unused-argument
    """Create a wikibase with a statistics observation"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Statistics Test Wikibase",
            base_url="https://aggregate-statistics-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
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


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.statistics
@pytest.mark.query
async def test_aggregate_statistics_query(
    wikibase_with_statistics,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate Statistics Query"""

    result = await test_schema.execute(AGGREGATED_STATISTICS_QUERY)

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateStatistics", "wikibaseCount"], 1
    )
    assert_edits(result.data["aggregateStatistics"], 36150323, 36150323 / 12655622)
    assert_files(result.data["aggregateStatistics"], 30)
    assert_pages(
        result.data["aggregateStatistics"], 851723, 27750 / 851723, 27750, 12655622
    )
    assert_users(result.data["aggregateStatistics"], 5, 17, 465)


@pytest.fixture
async def wikibase_with_statistics_suite(db_session):  # pylint: disable=unused-argument
    """Create a SUITE wikibase with a statistics observation for filtered tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Statistics Filtered Test Wikibase",
            base_url="https://aggregate-statistics-filtered-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType.SUITE
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseStatisticsObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.total_pages = 100
        obs.content_pages = 50
        obs.total_files = 5
        obs.total_edits = 200
        obs.content_page_word_count_total = 1000
        obs.total_users = 20
        obs.active_users = 2
        obs.total_admin = 1
        session.add(obs)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 1),
        (["CLOUD"], 1),
        (["OTHER"], 1),
        (["SUITE"], 0),
        (["CLOUD", "OTHER"], 1),
        (["CLOUD", "SUITE"], 0),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_statistics_query_filtered(
    wikibase_with_statistics_suite, exclude: list, expected_count: int
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
