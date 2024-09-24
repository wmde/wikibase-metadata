"""Test Page Meta"""

from tests.utils.assert_property_value import assert_layered_property_value


def assert_page_meta(
    page: dict,
    expected_page_number: int,
    expected_page_size: int,
    expected_total_count: int,
    expected_total_pages: int,
):
    """Test Page Meta"""

    assert_layered_property_value(page, ["meta", "pageNumber"], expected_page_number)
    assert_layered_property_value(page, ["meta", "pageSize"], expected_page_size)
    assert_layered_property_value(page, ["meta", "totalCount"], expected_total_count)
    assert_layered_property_value(page, ["meta", "totalPages"], expected_total_pages)
