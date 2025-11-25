"""Test Sort Wikibase List"""

import pytest
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-title-asc", depends=["mutate-cloud-instances"], scope="session"
)
async def test_wikibase_list_query_sort_title_asc():
    """Test Sort Title Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TITLE", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)

    assert_layered_property_value(result.data, ["wikibaseList", "data", 0, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 1, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 2, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 3, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 4, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 5, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 6, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 7, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 8, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 9, "title"], "")
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 10, "title"], ""
    )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-title-desc", depends=["mutate-cloud-instances"], scope="session"
)
async def test_wikibase_list_query_sort_title_desc():
    """Test Sort Title Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TITLE", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)

    assert_layered_property_value(result.data, ["wikibaseList", "data", 0, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 1, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 2, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 3, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 4, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 5, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 6, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 7, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 8, "title"], "")
    assert_layered_property_value(result.data, ["wikibaseList", "data", 9, "title"], "")
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 10, "title"], ""
    )
