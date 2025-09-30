"""Test Wikibase Most Recent User Observation Query"""

import pytest
from tests.test_query.wikibase.user_obs.assert_user import assert_user_group
from tests.test_query.wikibase.user_obs.user_fragment import (
    WIKIBASE_USER_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_property_value


WIKIBASE_USER_MOST_RECENT_OBSERVATION_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    userObservations {
      mostRecent {
        ...WikibaseUserObservationFragment
      }
    }
  }
}

"""
    + WIKIBASE_USER_OBSERVATION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["user-2000"], scope="session")
@pytest.mark.query
@pytest.mark.user
async def test_wikibase_user_most_recent_observation_query():
    """Test Wikibase Most Recent User Observation"""

    result = await test_schema.execute(
        WIKIBASE_USER_MOST_RECENT_OBSERVATION_QUERY, variable_values={"wikibaseId": 1}
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "userObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["userObservations"]
    most_recent = result_wikibase["userObservations"]["mostRecent"]

    assert_property_value(most_recent, "id", "4")
    assert "observationDate" in most_recent
    assert_property_value(most_recent, "returnedData", True)
    assert_property_value(most_recent, "totalUsers", 2000)
    assert_layered_property_count(most_recent, ["userGroups"], 8)

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
            most_recent["userGroups"][index],
            expected_id,
            expected_group_id,
            expected_group_name,
            expected_wikibase_default,
            expected_group_implicit,
            expected_user_count,
        )
