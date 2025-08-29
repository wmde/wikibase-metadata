"""Test WikibaseRecentChangeRecord"""

from datetime import datetime, UTC
import pytest

from fetch_data.api_data.recent_changes_data import WikibaseRecentChangeRecord


@pytest.mark.parametrize(
    ["record", "expected_user", "expect_fail"],
    [
        (
            {
                "type": "edit",
                "timestamp": "2024-01-01T00:00:00Z",
                "user": "TestUser",
                "userid": 123,
            },
            "TestUser",
            False,
        ),
        (
            {
                "type": "edit",
                "timestamp": "2024-01-01T00:00:00Z",
                "user": "TestUser",
            },
            "TestUser",
            False,
        ),
        (
            {
                "type": "edit",
                "timestamp": "2024-01-01T00:00:00Z",
                "userid": 123,
            },
            "__generated_user_string__user:123",
            False,
        ),
        (
            {
                "type": "edit",
                "timestamp": "2024-01-01T00:00:00Z",
                "userid": 0,
                "anon": "",
            },
            "__generated_user_string__user:0",
            False,
        ),
        (
            {
                "type": "edit",
                "timestamp": "2024-01-01T00:00:00Z",
                "userid": 3,
                "userhidden": "",
            },
            "__generated_user_string__user:3",
            False,
        ),
        (
            {
                "type": "edit",
                "timestamp": "2024-01-01T00:00:00Z",
            },
            None,
            True,
        ),
    ],
)
def test_wikibase_recent_change_record_user_creation(
    record: dict, expected_user: str | None, expect_fail: bool, caplog
):
    """Test the creation of the user property on WikibaseRecentChangeRecord"""

    change_record = WikibaseRecentChangeRecord(record)

    if expect_fail:
        with pytest.raises(AttributeError):
            _ = change_record.user
        assert "No user or userid found in record" in caplog.text
    else:
        assert change_record.user == expected_user
        assert change_record.type == "edit"
        assert change_record.timestamp == datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
