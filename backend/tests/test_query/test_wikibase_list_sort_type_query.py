"""Test Sort Wikibase List"""

import pytest
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-type-asc", depends=["mutate-cloud-instances"], scope="session"
)
async def test_wikibase_list_query_sort_type_asc():
    """Test Sort Type Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TYPE", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)

    assert [
        result.data["wikibaseList"]["data"][i]["wikibaseType"] for i in range(11)
    ] == []

    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 0, "wikibaseType"],
        "CLOUD",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 1, "wikibaseType"],
        "SUITE",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 2, "wikibaseType"],
        "TEST",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 3, "wikibaseType"],
        "UNKNOWN",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 4, "wikibaseType"],
        "CLOUD",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 5, "wikibaseType"],
        "SUITE",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 6, "wikibaseType"],
        "TEST",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 7, "wikibaseType"],
        "UNKNOWN",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 8, "wikibaseType"],
        "CLOUD",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 9, "wikibaseType"],
        "SUITE",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 10, "wikibaseType"],
        "TEST",
    )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-type-desc", depends=["mutate-cloud-instances"], scope="session"
)
async def test_wikibase_list_query_sort_type_desc():
    """Test Sort Type Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "CATEGORY", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)

    assert [
        result.data["wikibaseList"]["data"][i]["wikibaseType"] for i in range(11)
    ] == []

    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 0, "wikibaseType"],
        "CLOUD",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 1, "wikibaseType"],
        "SUITE",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 2, "wikibaseType"],
        "TEST",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 3, "wikibaseType"],
        "UNKNOWN",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 4, "wikibaseType"],
        "CLOUD",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 5, "wikibaseType"],
        "SUITE",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 6, "wikibaseType"],
        "TEST",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 7, "wikibaseType"],
        "UNKNOWN",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 8, "wikibaseType"],
        "CLOUD",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 9, "wikibaseType"],
        "SUITE",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 10, "wikibaseType"],
        "TEST",
    )
