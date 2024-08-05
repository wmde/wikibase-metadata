"""Test Wikibase All User Observations Query"""

import pytest
from tests.test_query.test_wikibase_user_observation_query.assert_user_group import (
    assert_user_group,
)
from tests.test_query.test_wikibase_user_observation_query.wikibase_user_observation_fragment import (
    WIKIBASE_USER_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_property_value,
)


WIKIBASE_USER_ALL_OBSERVATIONS_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    userObservations {
      allObservations {
        ...WikibaseUserObservationStrawberryModelFragment
      }
    }
  }
}

"""
    + WIKIBASE_USER_OBSERVATION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends_on=["user-empty", "user-failure", "user-20", "user-2000"]
)
@pytest.mark.query
@pytest.mark.user
async def test_wikibase_user_all_observations_query():
    """Test Wikibase All User Observations"""

    result = await test_schema.execute(
        WIKIBASE_USER_ALL_OBSERVATIONS_QUERY, variable_values={"wikibaseId": 1}
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "userObservations" in result_wikibase

    assert "allObservations" in result_wikibase["userObservations"]
    assert (
        len(
            user_observation_list := result_wikibase["userObservations"][
                "allObservations"
            ]
        )
        == 4
    )

    assert_layered_property_value(user_observation_list, [0, "id"], "1")
    assert "observationDate" in user_observation_list[0]
    assert_layered_property_value(user_observation_list, [0, "returnedData"], True)
    assert_layered_property_value(user_observation_list, [0, "totalUsers"], 0)
    assert_layered_property_count(user_observation_list, [0, "userGroups"], 0)

    assert_layered_property_value(user_observation_list, [1, "id"], "2")
    assert "observationDate" in user_observation_list[1]
    assert_layered_property_value(user_observation_list, [1, "returnedData"], False)

    assert_layered_property_value(user_observation_list, [2, "id"], "3")
    assert "observationDate" in user_observation_list[2]
    assert_layered_property_value(user_observation_list, [2, "returnedData"], True)
    assert_layered_property_value(user_observation_list, [2, "totalUsers"], 20)
    assert_layered_property_count(user_observation_list, [2, "userGroups"], 8)

    for index, (
        expected_id,
        expected_group_id,
        expected_group_name,
        expected_wikibase_default,
        expected_group_implicit,
        expected_user_count,
    ) in enumerate(
        [
            ("1", "1", "*", True, True, 20),
            ("3", "3", "autoconfirmed", True, True, 20),
            ("8", "8", "user", True, True, 20),
            ("2", "2", "administrator", False, False, 8),
            ("4", "4", "bot", False, False, 8),
            ("6", "6", "editor", False, False, 8),
            ("7", "7", "sysop", True, False, 8),
            ("5", "5", "bureaucrat", True, False, 4),
        ]
    ):
        assert_user_group(
            user_observation_list[2]["userGroups"][index],
            expected_id,
            expected_group_id,
            expected_group_name,
            expected_wikibase_default,
            expected_group_implicit,
            expected_user_count,
        )

    assert_layered_property_value(user_observation_list, [3, "id"], "4")
    assert "observationDate" in user_observation_list[3]
    assert_layered_property_value(user_observation_list, [3, "returnedData"], True)
    assert_layered_property_value(user_observation_list, [3, "totalUsers"], 2000)
    assert_layered_property_count(user_observation_list, [3, "userGroups"], 8)

    for index, (
        expected_id,
        expected_group_id,
        expected_group_name,
        expected_wikibase_default,
        expected_group_implicit,
        expected_user_count,
    ) in enumerate(
        [
            ("9", "1", "*", True, True, 2000),
            ("11", "3", "autoconfirmed", True, True, 2000),
            ("16", "8", "user", True, True, 2000),
            ("12", "4", "bot", False, False, 754),
            ("13", "5", "bureaucrat", True, False, 715),
            ("15", "7", "sysop", True, False, 715),
            ("10", "2", "administrator", False, False, 708),
            ("14", "6", "editor", False, False, 708),
        ]
    ):
        assert_user_group(
            user_observation_list[3]["userGroups"][index],
            expected_id,
            expected_group_id,
            expected_group_name,
            expected_wikibase_default,
            expected_group_implicit,
            expected_user_count,
        )
