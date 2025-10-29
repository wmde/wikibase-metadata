"""Assert Property Popularity Count"""

from tests.utils import assert_property_value


def assert_property_count(
    returned_property_count: dict,
    expected_id: str,
    expected_property_url: str,
    expected_usage_count: int,
):
    """Assert Property Popularity Count"""

    assert_property_value(returned_property_count, "id", expected_id)
    assert_property_value(returned_property_count, "propertyUrl", expected_property_url)
    assert_property_value(returned_property_count, "usageCount", expected_usage_count)
