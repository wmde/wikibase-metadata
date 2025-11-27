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

    assert [result.data["wikibaseList"]["data"][i]["title"] for i in range(11)] == [
        "biodiversity citizen science",
        "Doelgericht Digitaal Transformeren",
        "geokb",
        "Internet Domains",
        "LexBib",
        "MetaBase",
        "Mock Wikibase",
        "Mock Wikibase II",
        "Social Contagion",
        "Teochew Dictionary",
        "wikifcd",
    ]

    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 0, "title"],
        "biodiversity citizen science",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 1, "title"],
        "Doelgericht Digitaal Transformeren",
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 2, "title"], "geokb"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 3, "title"], "Internet Domains"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 4, "title"], "LexBib"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 5, "title"], "MetaBase"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 6, "title"], "Mock Wikibase"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 7, "title"], "Mock Wikibase II"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 8, "title"], "Social Contagion"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 9, "title"], "Teochew Dictionary"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 10, "title"], "wikifcd"
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

    assert [result.data["wikibaseList"]["data"][i]["title"] for i in range(11)] == [
        "wikifcd",
        "Teochew Dictionary",
        "Social Contagion",
        "Mock Wikibase II",
        "Mock Wikibase",
        "MetaBase",
        "LexBib",
        "Internet Domains",
        "geokb",
        "Doelgericht Digitaal Transformeren",
        "biodiversity citizen science",
    ]

    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 0, "title"], "wikifcd"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 1, "title"], "Teochew Dictionary"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 2, "title"], "Social Contagion"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 3, "title"], "Mock Wikibase II"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 4, "title"], "Mock Wikibase"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 5, "title"], "MetaBase"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 6, "title"], "LexBib"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 7, "title"], "Internet Domains"
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "data", 8, "title"], "geokb"
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 9, "title"],
        "Doelgericht Digitaal Transformeren",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 10, "title"],
        "biodiversity citizen science",
    )
