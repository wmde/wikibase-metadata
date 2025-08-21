"""Test Recent Changes Observation Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context
from tests.utils.assert_property_value import assert_layered_property_count


WIKIBASE_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    timeToFirstValueObservations {
      mostRecent {
        id
        observationDate
        returnedData
        initiationDate
        itemDates {
          id
          q
          creationDate
        }
      }
    }
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="ttfv-query-success",
    depends=["ttfv-success"],
    scope="session",
)
@pytest.mark.query
async def test_wikibase_query_ttfv_success():
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
        ["wikibase", "timeToFirstValueObservations", "mostRecent", "id"],
        "2",
    )
    assert_layered_property_value(
        result.data,
        ["wikibase", "timeToFirstValueObservations", "mostRecent", "returnedData"],
        True,
    )
    assert_layered_property_value(
        result.data,
        ["wikibase", "timeToFirstValueObservations", "mostRecent", "initiationDate"],
        "2022-09-09T23:25:00",
    )
    assert_layered_property_count(
        result.data,
        ["wikibase", "timeToFirstValueObservations", "mostRecent", "itemDates"],
        1,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibase",
            "timeToFirstValueObservations",
            "mostRecent",
            "itemDates",
            0,
            "id",
        ],
        "1",
    )
    assert_layered_property_value(
        result.data,
        ["wikibase", "timeToFirstValueObservations", "mostRecent", "itemDates", 0, "q"],
        1,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibase",
            "timeToFirstValueObservations",
            "mostRecent",
            "itemDates",
            0,
            "creationDate",
        ],
        "2020-05-02T19:11:00",
    )
