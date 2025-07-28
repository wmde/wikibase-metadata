"""Test create_recent_changes"""

from datetime import datetime

import pytest

from fetch_data.api_data.recent_changes_data.create_recent_changes_observation import (
    create_recent_changes,
)
from fetch_data.api_data.recent_changes_data.wikibase_recent_change_record import (
    WikibaseRecentChangeRecord,
)
from model.database import WikibaseModel, WikibaseRecentChangesObservationModel


@pytest.mark.asyncio
async def test_create_recent_changes_empty():
    """Test empty list scenario"""
    observation = WikibaseRecentChangesObservationModel()
    result = await create_recent_changes([], observation)
    assert result.change_count == 0
    assert result.user_count == 0
    assert result.first_change_date is None
    assert result.last_change_date is None


@pytest.mark.asyncio
async def test_create_recent_changes_counts():
    """Test that user and change counts are calculated correctly"""
    observation = WikibaseRecentChangesObservationModel()
    records = [
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "ns": 0,
                "title": "Page 1",
                "comment": "c1",
                "timestamp": "2024-03-01T12:00:00Z",
                "user": "User:A",
                "userid": 1,
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "ns": 0,
                "title": "Page 2",
                "comment": "c2",
                "timestamp": "2024-03-02T12:00:00Z",
                "user": "User:B",
                "userid": 2,
            }
        ),
        WikibaseRecentChangeRecord(
            {
                "type": "edit",
                "ns": 0,
                "title": "Page 3",
                "comment": "c3",
                "timestamp": "2024-03-03T12:00:00Z",
                "user": "User:A",
                "userid": 1,
            }
        ),
        WikibaseRecentChangeRecord(  # an anonymous user
            {
                "type": "edit",
                "ns": 0,
                "title": "Page 4",
                "comment": "c4",
                "timestamp": "2024-03-04T12:00:00Z",
                "user": "127.0.0.1",
                "userid": 0,
                "anon": "",
            }
        ),
        WikibaseRecentChangeRecord(  # userhidden, so no 'user' field
            {
                "type": "edit",
                "ns": 0,
                "title": "Page 5",
                "comment": "c5",
                "timestamp": "2024-03-05T12:00:00Z",
                "userid": 3,
                "userhidden": "",
            }
        ),
    ]
    result = await create_recent_changes(records, observation)

    assert result.change_count == 5
    assert result.user_count == 3  # User:A, User:B, 127.0.0.1
    assert result.first_change_date == datetime(2024, 3, 1, 12, 0, 0)
    assert result.last_change_date == datetime(2024, 3, 5, 12, 0, 0)
