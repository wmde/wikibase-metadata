"""Test Wikibase All Quantity Observations"""

import pytest
from tests.test_query.wikibase.statistics_obs.assert_statistics import assert_statistics
from tests.test_query.wikibase.statistics_obs.statistics_fragment import (
    WIKIBASE_STATISTICS_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value


WIKIBASE_STATISTICS_ALL_OBSERVATIONS_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    statisticsObservations {
      allObservations {
        ...WikibaseStatisticsObservationStrawberryModelFragment
      }
    }
  }
}

"""
    + WIKIBASE_STATISTICS_OBSERVATION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=[
        "statistics-success",
        "statistics-failure-500",
        "statistics-failure-not-found",
    ],
    scope="session",
)
@pytest.mark.query
@pytest.mark.statistics
async def test_wikibase_statistics_all_observations_query():
    """Test Wikibase All Statistics Observations"""

    result = await test_schema.execute(
        WIKIBASE_STATISTICS_ALL_OBSERVATIONS_QUERY, variable_values={"wikibaseId": 1}
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "statisticsObservations" in result_wikibase

    assert "allObservations" in result_wikibase["statisticsObservations"]
    assert (
        len(
            statistics_observation_list := result_wikibase["statisticsObservations"][
                "allObservations"
            ]
        )
        == 2
    )

    assert_statistics(
        statistics_observation_list[0],
        "1",
        True,
        (36150323, 36150323 / 12655622),
        (30,),
        (851723, 27750 / 851723, 27750, 12655622),
        (5, 17, 465),
    )
    assert_statistics(statistics_observation_list[1], "2", False)
