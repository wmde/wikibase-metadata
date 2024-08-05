"""Test Wikibase Most Recent Property Popularity Observation Query"""

import pytest
from tests.test_query.test_wikibase_property_popularity_observation_query.assert_property_count import (
    assert_property_count,
)
from tests.test_query.test_wikibase_property_popularity_observation_query.wikibase_property_popularity_observation_fragment import (
    WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_property_value


WIKIBASE_PROPERTY_POPULARITY_MOST_RECENT_OBSERVATION_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    propertyPopularityObservations {
      mostRecent {
        ...WikibasePropertyPopularityObservationStrawberryModelFragment
      }
    }
  }
}

"""
    + WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(depends_on=["property-popularity-success"])
@pytest.mark.property
@pytest.mark.query
async def test_wikibase_property_popularity_most_recent_observation_query():
    """Test Wikibase Property Popularity Most Recent Observation"""

    result = await test_schema.execute(
        WIKIBASE_PROPERTY_POPULARITY_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": 1},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "propertyPopularityObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["propertyPopularityObservations"]
    most_recent = result_wikibase["propertyPopularityObservations"]["mostRecent"]

    assert_property_value(most_recent, "id", "1")
    assert "observationDate" in most_recent
    assert_property_value(most_recent, "returnedData", True)
    assert_layered_property_count(most_recent, ["propertyPopularityCounts"], 2)

    for index, (expected_id, expected_property_url, expected_usage_count) in enumerate(
        [
            ("1", "P1", 12),
            ("2", "P14", 1),
        ]
    ):
        assert_property_count(
            most_recent["propertyPopularityCounts"][index],
            expected_id,
            expected_property_url,
            expected_usage_count,
        )
