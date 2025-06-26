"""Test Wikibase All Connectivity Observations Query"""

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


WIKIBASE_CONNECTIVITY_ALL_OBSERVATIONS_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    connectivityObservations {
      allObservations {
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
@pytest.mark.dependency(
    depends=[
        "connectivity-success-ood",
        "connectivity-success-simple-1",
        "connectivity-success-simple-2",
        "connectivity-success-simple-3",
        "connectivity-success-simple-4",
        "connectivity-success-simple-5",
        "connectivity-success-complex",
        "connectivity-failure",
    ],
    scope="session",
)
@pytest.mark.query
async def test_wikibase_connectivity_all_observations_query():
    """Test Wikibase All Connectivity Observations Query"""

    result = await test_schema.execute(
        WIKIBASE_CONNECTIVITY_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "connectivityObservations" in result_wikibase

    assert "allObservations" in result_wikibase["connectivityObservations"]
    assert (
        len(
            connectivity_observation_list := result_wikibase[
                "connectivityObservations"
            ]["allObservations"]
        )
        == 8
    )

    for index, (
        expected_id,
        expected_returned_links,
        expected_total_connections,
        expected_avg_connected_distance,
        expected_connectivity,
        expected_item_relationship_counts,
        expected_object_relationship_counts,
    ) in enumerate(
        [
            ("1", 0, 0, None, None, [], []),
            ("2", 1, 0, None, None, [("1", 0, 1)], [("1", 0, 1)]),
            (
                "3",
                1,
                1,
                1 / 1,
                1 / 2,
                [("2", 0, 1), ("3", 1, 1)],
                [("2", 0, 1), ("3", 1, 1)],
            ),
            (
                "4",
                6,
                1,
                1 / 1,
                1 / 2,
                [("4", 0, 1), ("5", 1, 1)],
                [("4", 0, 1), ("5", 1, 1)],
            ),
            ("5", 2, 2, 2 / 2, 2 / (2 * (2 - 1)), [("6", 1, 2)], [("6", 1, 2)]),
            (
                "6",
                2,
                2,
                4 / 3,
                3 / (3 * (3 - 1)),
                [("7", 0, 1), ("8", 1, 2)],
                [("7", 0, 1), ("8", 1, 2)],
            ),
            (
                "7",
                5627,
                5128,
                1853523 / 249500,
                249500 / (500 * (500 - 1)),
                [
                    ("9", 6, 1),
                    ("10", 7, 52),
                    ("11", 8, 98),
                    ("12", 9, 50),
                    ("13", 10, 53),
                    ("14", 11, 99),
                    ("15", 12, 51),
                    ("16", 13, 51),
                    ("17", 14, 45),
                ],
                [
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
                ],
            ),
        ]
    ):
        assert_connectivity_observation(
            connectivity_observation_list[index],
            expected_id,
            True,
            expected_returned_links,
            expected_total_connections,
            expected_avg_connected_distance,
            expected_connectivity,
            expected_item_relationship_counts,
            expected_object_relationship_counts,
        )

    assert_connectivity_observation(connectivity_observation_list[7], "8", False)
