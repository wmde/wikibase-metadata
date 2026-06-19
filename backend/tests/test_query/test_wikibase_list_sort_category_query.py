"""Test Sort Wikibase List"""

import pytest
from sqlalchemy import select
from model.database.wikibase_model import WikibaseModel
from data.database_connection import get_async_session
from model.database.wikibase_category_model import WikibaseCategoryModel
from model.enum.wikibase_category_enum import WikibaseCategory
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta


@pytest.fixture
async def eleven_wikibases_with_categories(db_session):
    """Create 11 wikibases - 9 with no category, 2 with EXPERIMENTAL_AND_PROTOTYPE_PROJECTS"""
    async with get_async_session() as session:
        category = WikibaseCategoryModel()
        category.category = WikibaseCategory.EXPERIMENTAL_AND_PROTOTYPE_PROJECTS
        session.add(category)
        await session.flush()
        await session.refresh(category)
        category_id = category.id

        for i in range(11):
            wikibase = WikibaseModel(
                wikibase_name=f"Category Sort Test Wikibase {i}",
                base_url=f"https://category-sort-example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            wikibase.category_id = category_id if i >= 9 else None
            session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_list_query_sort_category_asc(eleven_wikibases_with_categories):
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
async def test_wikibase_list_query_sort_category_desc(eleven_wikibases_with_categories):
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
