"""Test get_log_list_from_url"""

from datetime import datetime, timedelta
from typing import Optional

from freezegun import freeze_time
import pytest
from fetch_data.log_data.fetch_log_data import get_log_list_from_url
from tests.test_create_observation.test_create_log_observation.assert_log_record import (
    assert_log_record,
)


@pytest.mark.log
def test_get_log_list_from_url_empty(mocker):
    """Test No Result Scenario"""

    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        return_value={"query": {"logevents": []}},
    )
    assert get_log_list_from_url("test.url") == []


@freeze_time("2024-03-01")
@pytest.mark.log
def test_get_log_list_from_url_single(mocker):
    """Test Single Result Scenario"""

    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        return_value={
            "query": {
                "logevents": [
                    {
                        "logid": 1,
                        "timestamp": "2024-01-01T12:04:15Z",
                        "type": "create",
                        "action": "create",
                        "title": "Property:P17",
                    }
                ]
            }
        },
    )
    results = get_log_list_from_url("test.url")
    assert len(results) == 1
    assert_log_record(
        results[0], 1, datetime(2024, 1, 1, 12, 4, 15), 59, None, "PROPERTY_CREATE"
    )


@freeze_time("2024-03-01")
@pytest.mark.log
def test_get_log_list_from_url_several(mocker):
    """Test Several Result Scenario"""

    mock_log_types: list[tuple[str, str]] = [
        ("managetags", "create"),
        ("thanks", "thank"),
        ("approval", "unapprove"),
    ]
    mock_users: list[Optional[str]] = [
        "User:A",
        None,
        "User:B",
        "User:C",
    ]

    mock_logs: list[dict] = []
    for i in range(7):
        mock_logs.append(
            {
                "logid": i + 1,
                "timestamp": (datetime(2024, 1, 1) + timedelta(days=i * 7)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": mock_users[i % len(mock_users)],
                "type": mock_log_types[i % len(mock_log_types)][0],
                "action": mock_log_types[i % len(mock_log_types)][1],
            }
        )
    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        return_value={"query": {"logevents": mock_logs}},
    )
    results = get_log_list_from_url("test.url")
    assert len(results) == 7
    assert_log_record(results[0], 1, datetime(2024, 1, 1), 60, "User:A", "TAG_CREATE")
    assert_log_record(results[1], 2, datetime(2024, 1, 8), 53, None, "THANK")
    assert_log_record(results[2], 3, datetime(2024, 1, 15), 46, "User:B", "UNAPPROVE")
    assert_log_record(results[3], 4, datetime(2024, 1, 22), 39, "User:C", "TAG_CREATE")
    assert_log_record(results[4], 5, datetime(2024, 1, 29), 32, "User:A", "THANK")
    assert_log_record(results[5], 6, datetime(2024, 2, 5), 25, None, "UNAPPROVE")
    assert_log_record(results[6], 7, datetime(2024, 2, 12), 18, "User:B", "TAG_CREATE")
