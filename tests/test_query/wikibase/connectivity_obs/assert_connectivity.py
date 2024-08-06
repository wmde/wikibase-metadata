"""Assert Connectivity Observation"""

from typing import Optional
from tests.utils import assert_layered_property_count, assert_property_value


def assert_connectivity_observation(
    returned_connectivity_observation: dict,
    expected_id: str,
    expected_returned_data: bool,
    expected_returned_links: Optional[int] = None,
    expected_total_connections: Optional[int] = None,
    expected_avg_connected_distance: Optional[float] = None,
    expected_connectivity: Optional[float] = None,
    expected_item_relationship_counts: list[tuple[str, int, int]] = [],
    expected_object_relationship_counts: list[tuple[str, int, int]] = [],
):  # pylint: disable=too-many-arguments,too-many-locals
    """Assert Connectivity Observation"""

    assert_property_value(returned_connectivity_observation, "id", expected_id)
    assert "observationDate" in returned_connectivity_observation
    assert_property_value(
        returned_connectivity_observation, "returnedData", expected_returned_data
    )
    assert_property_value(
        returned_connectivity_observation, "returnedLinks", expected_returned_links
    )
    assert_property_value(
        returned_connectivity_observation,
        "totalConnections",
        expected_total_connections,
    )
    assert_property_value(
        returned_connectivity_observation,
        "averageConnectedDistance",
        expected_avg_connected_distance,
    )
    assert_property_value(
        returned_connectivity_observation, "connectivity", expected_connectivity
    )

    assert_layered_property_count(
        returned_connectivity_observation,
        ["relationshipItemCounts"],
        len(expected_item_relationship_counts),
    )
    for ri_index, (
        expected_ri_id,
        expected_relationship_count,
        expected_item_count,
    ) in enumerate(expected_item_relationship_counts):
        assert_relationship_count(
            returned_connectivity_observation["relationshipItemCounts"][ri_index],
            expected_ri_id,
            expected_relationship_count,
            expected_item_count=expected_item_count,
        )

    assert_layered_property_count(
        returned_connectivity_observation,
        ["relationshipObjectCounts"],
        len(expected_object_relationship_counts),
    )
    for ro_index, (
        expected_ro_id,
        expected_relationship_count,
        expected_object_count,
    ) in enumerate(expected_object_relationship_counts):
        assert_relationship_count(
            returned_connectivity_observation["relationshipObjectCounts"][ro_index],
            expected_ro_id,
            expected_relationship_count,
            expected_object_count=expected_object_count,
        )


def assert_relationship_count(
    relationship_count_record: dict,
    expected_id: str,
    expected_relationship_count: int,
    expected_item_count: Optional[int] = None,
    expected_object_count: Optional[int] = None,
):
    """Assert Relationship Count"""

    assert (expected_item_count or expected_object_count) is not None

    assert_property_value(relationship_count_record, "id", expected_id)
    assert_property_value(
        relationship_count_record, "relationshipCount", expected_relationship_count
    )
    if expected_item_count is not None:
        assert_property_value(
            relationship_count_record, "itemCount", expected_item_count
        )
    if expected_object_count is not None:
        assert_property_value(
            relationship_count_record, "objectCount", expected_object_count
        )
