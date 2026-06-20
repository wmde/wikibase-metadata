"""Test Sort Wikibase List"""

import datetime

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.recent_changes.recent_changes_observation_model import (
    WikibaseRecentChangesObservationModel,
)
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta
from datetime import timezone, datetime


@pytest.fixture
async def eleven_wikibases_with_one_recent_changes(db_session): # pylint: disable=unused-argument
    """Create 11 wikibases - 10 with no observations, 1 with recent changes"""
    async with get_async_session() as session:
        for i in range(11):
            wikibase = WikibaseModel(
                wikibase_name=f"Edits Sort Test Wikibase {i}",
                base_url=f"https://edits-sort-example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)
            await session.flush()
            await session.refresh(wikibase)

            if i == 10:
                observation = WikibaseRecentChangesObservationModel()
                observation.wikibase_id = wikibase.id
                observation.returned_data = True
                observation.observation_date = datetime(2024, 3, 6, tzinfo=timezone.utc)
                observation.human_change_count = 10
                observation.human_change_user_count = 5
                observation.human_change_active_user_count = 1
                observation.bot_change_count = 6
                observation.bot_change_user_count = 2
                observation.bot_change_active_user_count = 1
                observation.first_change_date = datetime(
                    2024, 3, 1, 12, 0, 0, tzinfo=timezone.utc
                )
                observation.last_change_date = datetime(
                    2024, 3, 5, 12, 0, 0, tzinfo=timezone.utc
                )
                session.add(observation)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_list_query_sort_edits_asc(
    eleven_wikibases_with_one_recent_changes,
): # pylint: disable=unused-argument, redefined-outer-name
    """Test Sort Edits Ascending"""

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
            result.data,
            ["wikibaseList", "data", i, "recentChangesObservations", "mostRecent"],
            None,
        )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            10,
            "recentChangesObservations",
            "mostRecent",
            "botChangeCount",
        ],
        6,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            10,
            "recentChangesObservations",
            "mostRecent",
            "humanChangeCount",
        ],
        10,
    )


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_list_query_sort_edits_desc(
    eleven_wikibases_with_one_recent_changes,
): # pylint: disable=unused-argument, redefined-outer-name
    """Test Sort Edits Descending"""

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
        result.data,
        [
            "wikibaseList",
            "data",
            0,
            "recentChangesObservations",
            "mostRecent",
            "botChangeCount",
        ],
        6,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            0,
            "recentChangesObservations",
            "mostRecent",
            "humanChangeCount",
        ],
        10,
    )
    for i in range(1, 11):
        assert_layered_property_value(
            result.data,
            ["wikibaseList", "data", i, "recentChangesObservations", "mostRecent"],
            None,
        )
