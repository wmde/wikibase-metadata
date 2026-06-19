"""Test Sort Wikibase List"""

import pytest
from model.database.wikibase_model import WikibaseModel
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import assert_page_meta


@pytest.fixture
async def wikibases_with_types(db_session):
    """Create test wikibases with various types"""
    from sqlalchemy.ext.asyncio import AsyncSession
    from model.enum import WikibaseType

    types = [
        WikibaseType.CLOUD,
        WikibaseType.CLOUD,
        WikibaseType.CLOUD,
        WikibaseType.CLOUD,
        WikibaseType.CLOUD,
        WikibaseType.CLOUD,
        WikibaseType.CLOUD,
        WikibaseType.OTHER,
        WikibaseType.SUITE,
        WikibaseType.TEST,
        None,  # UNKNOWN
    ]
    async with AsyncSession(bind=db_session) as session:
        for i, wikibase_type in enumerate(types):
            wikibase = WikibaseModel(
                wikibase_name=f"Type Sort Test Wikibase {i}",
                base_url=f"https://type-sort-example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = wikibase_type
            session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_list_query_sort_type_asc(wikibases_with_types):
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
async def test_wikibase_list_query_sort_type_desc(wikibases_with_types):
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
