"""Test Aggregate Statistics Query"""

import pytest
from tests.test_query.wikibase.statistics_obs.assert_statistics import (
    assert_edits,
    assert_files,
    assert_pages,
    assert_users,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context


AGGREGATED_STATISTICS_QUERY = """
query MyQuery {
  aggregateStatistics {
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


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["statistics-success"], scope="session")
@pytest.mark.statistics
@pytest.mark.query
async def test_aggregate_statistics_query():
    """Test Aggregate Statistics Query"""

    result = await test_schema.execute(
        AGGREGATED_STATISTICS_QUERY, context_value=get_mock_context("test-auth-token")
    )

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
