"""Test Recent Changes Observation Query"""

from datetime import datetime
import pytest
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_property_value,
)
from tests.utils.datetime_format import DATETIME_FORMAT


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
    name="ttfv-query-success", depends=["ttfv-success"], scope="session"
)
@pytest.mark.query
async def test_wikibase_query_ttfv_success():
    """Test success scenario"""
    result = await test_schema.execute(
        WIKIBASE_QUERY, variable_values={"wikibaseId": 1}
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
        "2012-10-26T20:05:09+00:00",
    )
    assert_layered_property_count(
        result.data,
        ["wikibase", "timeToFirstValueObservations", "mostRecent", "itemDates"],
        4,
    )
    assert_item_date(
        result.data["wikibase"]["timeToFirstValueObservations"]["mostRecent"][
            "itemDates"
        ][0],
        1,
        1,
        datetime(2012, 10, 29, 18, 18, 48),
    )
    assert_item_date(
        result.data["wikibase"]["timeToFirstValueObservations"]["mostRecent"][
            "itemDates"
        ][1],
        2,
        15,
        datetime(2012, 10, 29, 17, 3, 21),
    )
    assert_item_date(
        result.data["wikibase"]["timeToFirstValueObservations"]["mostRecent"][
            "itemDates"
        ][2],
        3,
        100,
        datetime(2012, 10, 29, 21, 48, 13),
    )
    assert_item_date(
        result.data["wikibase"]["timeToFirstValueObservations"]["mostRecent"][
            "itemDates"
        ][3],
        4,
        1001,
        datetime(2013, 8, 11, 4, 55, 58),
    )


def assert_item_date(
    data: dict, expected_id: int, expected_item_number: int, expected_date: datetime
):
    """Assert values of ItemDate"""

    assert_property_value(data, "id", str(expected_id))
    assert_property_value(data, "q", expected_item_number)
    assert_property_value(data, "creationDate", expected_date.strftime(DATETIME_FORMAT))
