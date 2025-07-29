"""Test Recent Changes Observation Query"""

from datetime import datetime

import pytest
from tests.test_schema import test_schema
from tests.utils import DATETIME_FORMAT, assert_layered_property_value, get_mock_context


WIKIBASE_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    recentChangesObservations {
      mostRecent {
        id
        observationDate
        returnedData
        changeCount
        userCount
        totalChangeCount
        totalUserCount
        firstChangeDate
        lastChangeDate
      }
    }
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="recent-changes-query-success",
    depends=["recent-changes-success-ood"],
    scope="session",
)
@pytest.mark.query
async def test_wikibase_query_recent_changes_success():
    """Test success scenario"""
    result = await test_schema.execute(
        WIKIBASE_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data,
        [
            "wikibase",
            "recentChangesObservations",
            "mostRecent",
            "changeCount",
        ],
        5,
    )

    assert_layered_property_value(
        result.data,
        [
            "wikibase",
            "recentChangesObservations",
            "mostRecent",
            "totalChangeCount",
        ],
        5,
    )

    assert_layered_property_value(
        result.data,
        [
            "wikibase",
            "recentChangesObservations",
            "mostRecent",
            "userCount",
        ],
        4,
    )

    assert_layered_property_value(
        result.data,
        [
            "wikibase",
            "recentChangesObservations",
            "mostRecent",
            "totalUserCount",
        ],
        4,
    )

    assert_layered_property_value(
        result.data,
        [
            "wikibase",
            "recentChangesObservations",
            "mostRecent",
            "firstChangeDate",
        ],
        datetime(2024, 3, 1, 12, 0, 0).strftime(DATETIME_FORMAT),
    )

    assert_layered_property_value(
        result.data,
        [
            "wikibase",
            "recentChangesObservations",
            "mostRecent",
            "lastChangeDate",
        ],
        datetime(2024, 3, 5, 12, 0, 0).strftime(DATETIME_FORMAT),
    )
