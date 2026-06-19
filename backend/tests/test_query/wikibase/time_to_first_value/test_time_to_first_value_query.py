"""Test Recent Changes Observation Query"""

from datetime import datetime
import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.time_to_first_value.item_date_model import (
    WikibaseItemDateModel,
)
from model.database.wikibase_observation.time_to_first_value.ttfv_observation_model import (
    WikibaseTimeToFirstValueObservationModel,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_property_value,
)
from tests.utils.datetime_format import DATETIME_FORMAT
from datetime import timezone

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


@pytest.fixture
async def wikibase_with_ttfv_observation(db_session):
    """Create a wikibase with a time to first value observation"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="TTFV Query Test Wikibase",
            base_url="https://ttfv-query-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        observation = WikibaseTimeToFirstValueObservationModel(wikibase_id=wikibase.id)
        observation.returned_data = True
        observation.initiation_date = datetime(
            2012, 10, 26, 20, 5, 9, tzinfo=timezone.utc
        )
        session.add(observation)
        await session.flush()
        await session.refresh(observation)

        item_dates = [
            (1, datetime(2012, 10, 29, 18, 18, 48, tzinfo=timezone.utc)),
            (15, datetime(2012, 10, 29, 17, 3, 21, tzinfo=timezone.utc)),
            (100, datetime(2012, 10, 29, 21, 48, 13, tzinfo=timezone.utc)),
            (1001, datetime(2013, 8, 11, 4, 55, 58, tzinfo=timezone.utc)),
        ]

        item_date_ids = []
        for item_number, creation_date in item_dates:
            item_date = WikibaseItemDateModel()
            item_date.wikibase_time_to_first_value_observation_id = observation.id
            item_date.item_number = item_number
            item_date.creation_date = creation_date
            session.add(item_date)
            await session.flush()
            await session.refresh(item_date)
            item_date_ids.append(item_date.id)

        wikibase_id = wikibase.id
        observation_id = str(observation.id)
    return wikibase_id, observation_id, item_date_ids


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_query_ttfv_success(wikibase_with_ttfv_observation):
    """Test success scenario"""

    wikibase_id, observation_id, item_date_ids = wikibase_with_ttfv_observation

    result = await test_schema.execute(
        WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_id}
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data,
        ["wikibase", "timeToFirstValueObservations", "mostRecent", "id"],
        str(observation_id),
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
        item_date_ids[0],
        1,
        datetime(2012, 10, 29, 18, 18, 48),
    )
    assert_item_date(
        result.data["wikibase"]["timeToFirstValueObservations"]["mostRecent"][
            "itemDates"
        ][1],
        item_date_ids[1],
        15,
        datetime(2012, 10, 29, 17, 3, 21),
    )
    assert_item_date(
        result.data["wikibase"]["timeToFirstValueObservations"]["mostRecent"][
            "itemDates"
        ][2],
        item_date_ids[2],
        100,
        datetime(2012, 10, 29, 21, 48, 13),
    )
    assert_item_date(
        result.data["wikibase"]["timeToFirstValueObservations"]["mostRecent"][
            "itemDates"
        ][3],
        item_date_ids[3],
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
