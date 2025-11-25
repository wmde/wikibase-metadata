"""Test Sort Wikibase List"""

import pytest
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-cat-asc", depends=["mutate-cloud-instances"], scope="session"
)
async def test_wikibase_list_query_sort_category_asc():
    """Test Sort Category Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "CATEGORY", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)

    assert [result.data["wikibaseList"]["data"][i]["category"] for i in range(11)] == [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
    ]

    for i in range(9):
        assert_layered_property_value(
            result.data, ["wikibaseList", "data", i, "category"], None
        )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 9, "category"],
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 10, "category"],
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
    )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-cat-desc", depends=["mutate-cloud-instances"], scope="session"
)
async def test_wikibase_list_query_sort_category_desc():
    """Test Sort Category Descending"""

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

    assert [result.data["wikibaseList"]["data"][i]["category"] for i in range(11)] == [
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]

    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 0, "category"],
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 1, "category"],
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
    )
    for i in range(2, 11):
        assert_layered_property_value(
            result.data, ["wikibaseList", "data", i, "category"], None
        )
