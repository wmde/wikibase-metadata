"""Test create_recent_changes"""

from datetime import datetime

import pytest

from fetch_data.api_data.recent_changes_data.create_recent_changes_observation import (
    create_recent_changes,
)
from fetch_data.api_data.recent_changes_data.wikibase_recent_change_record import (
    WikibaseRecentChangeRecord,
)
from model.database import WikibaseRecentChangesObservationModel


@pytest.mark.asyncio
async def test_create_recent_changes_empty():
    """Test empty list scenario"""
    observation = WikibaseRecentChangesObservationModel()
    result = await create_recent_changes([], [], observation)
    assert result.change_count == 0
    assert result.user_count == 0
    assert result.first_change_date is None
    assert result.last_change_date is None


@pytest.mark.asyncio
async def test_create_recent_changes_counts():
    """Test that user and change counts are calculated correctly"""
    observation = WikibaseRecentChangesObservationModel()

    mock_changes_without_bots = [
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 1, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 1,
                "user": "UserA",
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 2, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 2,
                "user": "UserB",
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 3, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 1,
                "user": "UserA",
            }
        ),
        WikibaseRecentChangeRecord(  # an anonymous user
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 4, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": "127.0.0.1",
                "userid": 0,
                "anon": "",
            }
        ),
        WikibaseRecentChangeRecord(  # userhidden, so no 'user' field
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 5, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 3,
                "userhidden": "",
            }
        ),
    ]

    mock_changes_with_bots = [
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 1, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 1,
                "user": "UserA",
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 2, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 2,
                "user": "UserB",
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 3, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 1,
                "user": "UserA",
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 3, 0, 4, 5).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": "BOT_USER_1",
                "userid": 1001,
            }
        ),
        WikibaseRecentChangeRecord(  # an anonymous user
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 4, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": "127.0.0.1",
                "userid": 0,
                "anon": "",
            }
        ),
        WikibaseRecentChangeRecord(  # userhidden, so no 'user' field
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 5, 12, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "userid": 3,
                "userhidden": "",
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 5, 15, 2, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": "BOT_USER_1",
                "userid": 1001,
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "timestamp": datetime(2024, 3, 6, 0, 0, 0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": "BOT_USER_2",
                "userid": 1002,
            }
        ),
    ]
    result = await create_recent_changes(
        mock_changes_without_bots, mock_changes_with_bots, observation
    )

    assert result.change_count == 5
    assert (
        result.user_count == 4
    )  # User:A, User:B, 127.0.0.1, __generated_user_string__user:3

    assert result.total_change_count == 8
    assert result.total_user_count == 6  # above plus BOT_USER_1 and BOT_USER_2
    assert result.first_change_date == datetime(2024, 3, 1, 12, 0, 0)
    assert result.last_change_date == datetime(2024, 3, 6, 0, 0, 0)
