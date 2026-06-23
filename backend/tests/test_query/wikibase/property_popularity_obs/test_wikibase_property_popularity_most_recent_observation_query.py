"""Test Wikibase Most Recent Property Popularity Observation Query"""

import pytest
from tests.test_query.wikibase.property_popularity_obs.assert_property_popularity import (
    assert_property_count,
)
from tests.test_query.wikibase.property_popularity_obs.property_popularity_fragment import (
    WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_property_value

WIKIBASE_PROPERTY_POPULARITY_MOST_RECENT_OBSERVATION_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    propertyPopularityObservations {
      mostRecent {
        ...WikibasePropertyPopularityObservationFragment
      }
    }
  }
}

""" + WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT


@pytest.mark.asyncio
@pytest.mark.property
@pytest.mark.query
async def test_wikibase_property_popularity_most_recent_observation_query(
    wikibase_with_three_property_popularity_observations
):
    """Test Wikibase Most Recent Property Popularity Observation"""

    data = wikibase_with_three_property_popularity_observations

    result = await test_schema.execute(
        WIKIBASE_PROPERTY_POPULARITY_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": data["wikibase_id"]},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(data["wikibase_id"]))
    assert "propertyPopularityObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["propertyPopularityObservations"]
    most_recent = result_wikibase["propertyPopularityObservations"]["mostRecent"]

    assert_property_value(most_recent, "id", data["obs1_id"])
    assert "observationDate" in most_recent
    assert_property_value(most_recent, "returnedData", True)
    assert_layered_property_count(most_recent, ["propertyPopularityCounts"], 2)

    for index, (expected_id, expected_property_url, expected_usage_count) in enumerate(
        [
            (data["p1_id"], "P1", 12),
            (data["p14_id"], "P14", 1),
        ]
    ):
        assert_property_count(
            most_recent["propertyPopularityCounts"][index],
            expected_id,
            expected_property_url,
            expected_usage_count,
        )
