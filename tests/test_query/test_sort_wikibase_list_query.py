"""Test Sort Wikibase List"""

import pytest
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-cat-asc",
    depends=["mutate-cloud-instances"],
    scope="session",
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


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-cat-desc",
    depends=[
        "mutate-cloud-instances",
        # "sort-cat-asc",
    ],
    scope="session",
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


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-edit-asc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        # "sort-cat-asc",
        # "sort-cat-desc",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_edit_asc():
    """Test Sort Edit Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "EDITS", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    for i in range(10):
        assert_layered_property_value(
            result.data["wikibaseList"]["data"],
            [i, "recentChangesObservations", "mostRecent"],
            None,
        )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [10, "recentChangesObservations", "mostRecent", "botChangeCount"],
        6,
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [10, "recentChangesObservations", "mostRecent", "humanChangeCount"],
        10,
    )


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-edit-desc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        # "sort-edit-asc",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_edit_desc():
    """Test Sort Edit Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "EDITS", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [0, "recentChangesObservations", "mostRecent", "botChangeCount"],
        6,
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [0, "recentChangesObservations", "mostRecent", "humanChangeCount"],
        10,
    )
    for i in range(1, 11):
        assert_layered_property_value(
            result.data["wikibaseList"]["data"],
            [i, "recentChangesObservations", "mostRecent"],
            None,
        )


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-title-asc",
    depends=[
        "mutate-cloud-instances",
        #  "sort-edit-asc",
        #  "sort-edit-desc"
    ],
    scope="session",
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
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [0, "title"],
        "biodiversity citizen science",
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [1, "title"],
        "Doelgericht Digitaal Transformeren",
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [2, "title"], "geokb"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [3, "title"], "Internet Domains"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [4, "title"], "LexBib"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [5, "title"], "MetaBase"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [6, "title"], "Mock Wikibase"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [7, "title"], "Mock Wikibase II"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [8, "title"], "Social Contagion"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [9, "title"], "Teochew Dictionary"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [10, "title"], "wikifcd"
    )


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-title-desc",
    depends=[
        "mutate-cloud-instances",
        #  "sort-title-asc"
    ],
    scope="session",
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
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [0, "title"], "wikifcd"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [1, "title"], "Teochew Dictionary"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [2, "title"], "Social Contagion"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [3, "title"], "Mock Wikibase II"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [4, "title"], "Mock Wikibase"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [5, "title"], "MetaBase"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [6, "title"], "LexBib"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [7, "title"], "Internet Domains"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [8, "title"], "geokb"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [9, "title"],
        "Doelgericht Digitaal Transformeren",
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [10, "title"],
        "biodiversity citizen science",
    )


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-triples-asc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        # "sort-title-asc",
        # "sort-title-desc",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_triples_asc():
    """Test Sort Triples Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TRIPLES", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    for i in range(10):
        assert_layered_property_value(
            result.data["wikibaseList"]["data"],
            [i, "quantityObservations", "mostRecent"],
            None,
        )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [10, "quantityObservations", "mostRecent", "totalTriples"],
        8,
    )


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-triples-desc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        # "sort-triples-asc",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_triples_desc():
    """Test Sort Triples Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TRIPLES", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [0, "quantityObservations", "mostRecent", "totalTriples"],
        8,
    )
    for i in range(1, 11):
        assert_layered_property_value(
            result.data["wikibaseList"]["data"],
            [i, "quantityObservations", "mostRecent"],
            None,
        )


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-type-asc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        # "sort-triples-asc",
        # "sort-triples-desc",
    ],
    scope="session",
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
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [0, "wikibaseType"], "UNKNOWN"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [1, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [2, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [3, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [4, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [5, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [6, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [7, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [8, "wikibaseType"], "OTHER"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [9, "wikibaseType"], "SUITE"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [10, "wikibaseType"], "SUITE"
    )


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-type-desc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        # "sort-type-asc",
    ],
    scope="session",
)
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
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [0, "wikibaseType"], "SUITE"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [1, "wikibaseType"], "SUITE"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [2, "wikibaseType"], "OTHER"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [3, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [4, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [5, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [6, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [7, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [8, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [9, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [10, "wikibaseType"], "UNKNOWN"
    )
