"""Test Wikibase Most Recent Connectivity Observation"""

from datetime import datetime
from freezegun import freeze_time
import pytest
from tests.test_query.wikibase.connectivity_obs.assert_connectivity import (
    assert_connectivity_observation,
)
from tests.test_query.wikibase.connectivity_obs.connectivity_fragment import (
    WIKIBASE_CONNECTIVITY_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value, get_mock_context


WIKIBASE_CONNECTIVITY_MOST_RECENT_OBSERVATION_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    connectivityObservations {
      mostRecent {
        ...WikibaseConnectivityObservationFragment
      }
    }
  }
}

"""
    + WIKIBASE_CONNECTIVITY_OBSERVATION_FRAGMENT
)


@freeze_time(datetime(2024, 4, 1))
@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.dependency(depends=["connectivity-success-complex"], scope="session")
@pytest.mark.query
async def test_wikibase_connectivity_most_recent_observation_query():
    """Test Wikibase Most Recent Connectivity Observation"""

    result = await test_schema.execute(
        WIKIBASE_CONNECTIVITY_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": 1},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "connectivityObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["connectivityObservations"]
    most_recent = result_wikibase["connectivityObservations"]["mostRecent"]

    expected_relationship_item_counts = [
        ("9", 6, 1),
        ("10", 7, 52),
        ("11", 8, 98),
        ("12", 9, 50),
        ("13", 10, 53),
        ("14", 11, 99),
        ("15", 12, 51),
        ("16", 13, 51),
        ("17", 14, 45),
    ]
    expected_relationship_object_counts = [
        ("9", 1, 1),
        ("10", 2, 1),
        ("11", 3, 1),
        ("12", 4, 193),
        ("13", 5, 196),
        ("14", 6, 98),
        ("15", 55, 1),
        ("16", 104, 1),
        ("17", 154, 1),
        ("18", 204, 1),
        ("19", 254, 1),
        ("20", 303, 1),
        ("21", 353, 1),
        ("22", 403, 1),
        ("23", 453, 1),
        ("24", 499, 1),
    ]

    assert_connectivity_observation(
        most_recent,
        "7",
        True,
        5627,
        5128,
        1853523 / 249500,
        249500 / (500 * (500 - 1)),
        expected_relationship_item_counts,
        expected_relationship_object_counts,
    )
