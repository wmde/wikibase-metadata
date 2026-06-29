"""Test Sort Wikibase List"""

from datetime import datetime, timezone

import pytest

from data import get_async_session
from model.database import WikibaseModel, WikibaseQuantityObservationModel
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta


@pytest.fixture
async def eleven_wikibases_with_one_quantity(
    db_session,
):  # pylint: disable=unused-argument
    """Create 11 wikibases - 10 with no observations, 1 with quantity observation"""
    async with get_async_session() as session:
        for i in range(11):
            wikibase = WikibaseModel(
                wikibase_name=f"Triples Sort Test Wikibase {i}",
                base_url=f"https://triples-sort-example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)
            await session.flush()
            await session.refresh(wikibase)

            if i == 10:
                observation = WikibaseQuantityObservationModel()
                observation.wikibase_id = wikibase.id
                observation.returned_data = True
                observation.observation_date = datetime(2024, 3, 6, tzinfo=timezone.utc)
                observation.total_triples = 8
                observation.total_items = 0
                observation.total_lexemes = 0
                observation.total_properties = 0
                session.add(observation)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_list_query_sort_triples_asc(
    eleven_wikibases_with_one_quantity,
):  # pylint: disable=unused-argument, redefined-outer-name
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
            result.data,
            ["wikibaseList", "data", i, "quantityObservations", "mostRecent"],
            None,
        )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            10,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        8,
    )


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_list_query_sort_triples_desc(
    eleven_wikibases_with_one_quantity,
):  # pylint: disable=unused-argument, redefined-outer-name
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
        result.data,
        [
            "wikibaseList",
            "data",
            0,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        8,
    )
    for i in range(1, 11):
        assert_layered_property_value(
            result.data,
            ["wikibaseList", "data", i, "quantityObservations", "mostRecent"],
            None,
        )
