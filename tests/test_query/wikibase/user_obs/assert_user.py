"""Assert User Group"""

from tests.utils import assert_layered_property_value, assert_property_value


def assert_user_group(
    returned_user_group: dict,
    expected_id: str,
    expected_group_id: str,
    expected_group_name: str,
    expected_wikibase_default: bool,
    expected_group_implicit: bool,
    expected_user_count,
):
    """Assert User Group"""

    assert_property_value(returned_user_group, "id", expected_id)
    assert_layered_property_value(
        returned_user_group, ["group", "id"], expected_group_id
    )
    assert_layered_property_value(
        returned_user_group, ["group", "groupName"], expected_group_name
    )
    assert_layered_property_value(
        returned_user_group,
        ["group", "wikibaseDefault"],
        expected_wikibase_default,
    )
    assert_property_value(returned_user_group, "groupImplicit", expected_group_implicit)
    assert_property_value(returned_user_group, "userCount", expected_user_count)
