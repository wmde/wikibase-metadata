"""Test Wikibase Most Recent Statistics Observation Query"""

import pytest
from tests.test_query.wikibase.statistics_obs.assert_statistics import assert_statistics
from tests.test_query.wikibase.statistics_obs.statistics_fragment import (
    WIKIBASE_STATISTICS_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value


WIKIBASE_STATISTICS_MOST_RECENT_OBSERVATION_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    statisticsObservations {
      mostRecent {
        ...WikibaseStatisticsObservationFragment
      }
    }
  }
}

"""
    + WIKIBASE_STATISTICS_OBSERVATION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["statistics-success"], scope="session")
@pytest.mark.query
@pytest.mark.statistics
async def test_wikibase_statistics_most_recent_observation_query():
    """Test Wikibase Most Recent Statistics Observation"""

    result = await test_schema.execute(
        WIKIBASE_STATISTICS_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": 1},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "statisticsObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["statisticsObservations"]
    most_recent = result_wikibase["statisticsObservations"]["mostRecent"]

    assert_statistics(
        most_recent,
        "1",
        True,
        (36150323, 36150323 / 12655622),  # edits
        (30,),  # files
        (851723, 27750 / 851723, 27750, 12655622),  # pages
        (5, 17, 465),  # users
    )
