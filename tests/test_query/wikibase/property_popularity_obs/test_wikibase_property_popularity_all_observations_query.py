"""Test Wikibase All Property Popularity Observations Query"""

import pytest
from tests.test_query.wikibase.property_popularity_obs.assert_property_popularity import (
    assert_property_count,
)
from tests.test_query.wikibase.property_popularity_obs.property_popularity_fragment import (
    WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_property_value,
)


WIKIBASE_PROPERTY_POPULARITY_ALL_OBSERVATIONS_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    propertyPopularityObservations {
      allObservations {
        ...WikibasePropertyPopularityObservationStrawberryModelFragment
      }
    }
  }
}

"""
    + WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=["property-popularity-success", "property-popularity-failure"],
    scope="session",
)
@pytest.mark.property
@pytest.mark.query
async def test_wikibase_property_popularity_all_observations_query():
    """Test Wikibase All Property Popularity Observations Query"""

    result = await test_schema.execute(
        WIKIBASE_PROPERTY_POPULARITY_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": 1},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "propertyPopularityObservations" in result_wikibase

    assert "allObservations" in result_wikibase["propertyPopularityObservations"]
    assert (
        len(
            property_popularity_observation_list := result_wikibase[
                "propertyPopularityObservations"
            ]["allObservations"]
        )
        == 2
    )

    assert_layered_property_value(property_popularity_observation_list, [0, "id"], "1")
    assert "observationDate" in property_popularity_observation_list[0]
    assert_layered_property_value(
        property_popularity_observation_list, [0, "returnedData"], True
    )
    assert_layered_property_count(
        property_popularity_observation_list, [0, "propertyPopularityCounts"], 2
    )

    for index, (expected_id, expected_property_url, expected_usage_count) in enumerate(
        [
            ("1", "P1", 12),
            ("2", "P14", 1),
        ]
    ):
        assert_property_count(
            property_popularity_observation_list[0]["propertyPopularityCounts"][index],
            expected_id,
            expected_property_url,
            expected_usage_count,
        )

    assert_layered_property_value(property_popularity_observation_list, [1, "id"], "2")
    assert "observationDate" in property_popularity_observation_list[1]
    assert_layered_property_value(
        property_popularity_observation_list, [1, "returnedData"], False
    )
    assert_layered_property_count(
        property_popularity_observation_list, [1, "propertyPopularityCounts"], 0
    )
