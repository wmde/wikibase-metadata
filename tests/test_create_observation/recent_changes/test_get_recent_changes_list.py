"""Test get_recent_changes_list"""

from datetime import datetime, timedelta, UTC

from freezegun import freeze_time
import pytest
from fetch_data.api_data.recent_changes_data import get_recent_changes_list


@freeze_time(datetime(2024, 3, 1))
@pytest.mark.asyncio
async def test_get_recent_changes_list_one_pull(mocker):
    """Test One-Pull Scenario"""

    mock_changes: list[dict] = []
    for i in range(70):
        mock_changes.append(
            {
                "type": "edit",
                "ns": 0,
                "title": f"Page {i}",
                "comment": "comment",
                "timestamp": (datetime(2024, 3, 1) - timedelta(hours=i * 24)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": "User:A",
                "userid": 1,
            }
        )

    mocker.patch(
        "fetch_data.api_data.recent_changes_data.fetch_recent_changes_data.fetch_api_data",
        side_effect=[
            {
                "query": {"recentchanges": mock_changes[:50]},
                "continue": {"rccontinue": "2024-02-10T01:00:00Z|12345"},
            },
            {"query": {"recentchanges": mock_changes[50:]}},
        ],
    )
    results = await get_recent_changes_list("example.com")
    assert len(results) == 31

    newest_change = max(results, key=lambda x: x.timestamp)
    assert newest_change.timestamp == datetime(2024, 3, 1, tzinfo=UTC)
    oldest_change = min(results, key=lambda x: x.timestamp)
    assert oldest_change.timestamp == datetime(2024, 1, 31, tzinfo=UTC)


@freeze_time(datetime(2024, 3, 1))
@pytest.mark.asyncio
async def test_get_recent_changes_list_multiple_pulls(mocker):
    """Test Multiple-Pull Scenario"""

    mock_changes: list[dict] = []
    for i in range(70):
        mock_changes.append(
            {
                "type": "edit",
                "ns": 0,
                "title": f"Page {i}",
                "comment": "comment",
                "timestamp": (datetime(2024, 3, 1) - timedelta(hours=i * 12)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": "User:A",
                "userid": 1,
            }
        )
    mocker.patch(
        "fetch_data.api_data.recent_changes_data.fetch_recent_changes_data.fetch_api_data",
        side_effect=[
            {
                "query": {"recentchanges": mock_changes[:50]},
                "continue": {"rccontinue": "2024-02-04T12:00:00Z|54321"},
            },
            {"query": {"recentchanges": mock_changes[50:]}},
        ],
    )
    results = await get_recent_changes_list("example.com")
    assert len(results) == 61

    newest_change = max(results, key=lambda x: x.timestamp)
    assert newest_change.timestamp == datetime(2024, 3, 1, tzinfo=UTC)
    oldest_change = min(results, key=lambda x: x.timestamp)
    assert oldest_change.timestamp == datetime(2024, 1, 31, tzinfo=UTC)


@pytest.mark.asyncio
async def test_get_recent_changes_list_empty_response(mocker):
    """Test handling of empty API response (no recent changes)."""

    mocker.patch(
        "fetch_data.api_data.recent_changes_data.fetch_recent_changes_data.fetch_api_data",
        return_value={
            "batchcomplete": "",
            "query": {"recentchanges": []},
        },
    )

    results = await get_recent_changes_list("example.com")
    assert isinstance(results, list)
    assert len(results) == 0
