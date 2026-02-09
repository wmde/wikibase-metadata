"""Test Sort Wikibase List"""

import pytest
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import assert_page_meta


@pytest.mark.asyncio
@pytest.mark.query
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
    ] == [
        "CLOUD",
        "CLOUD",
        "CLOUD",
        "CLOUD",
        "CLOUD",
        "CLOUD",
        "CLOUD",
        "OTHER",
        "SUITE",
        "TEST",
        "UNKNOWN",
    ]


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_list_query_sort_type_desc():
    """Test Sort Type Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TYPE", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)

    assert [
        result.data["wikibaseList"]["data"][i]["wikibaseType"] for i in range(11)
    ] == [
        "UNKNOWN",
        "TEST",
        "SUITE",
        "OTHER",
        "CLOUD",
        "CLOUD",
        "CLOUD",
        "CLOUD",
        "CLOUD",
        "CLOUD",
        "CLOUD",
    ]
