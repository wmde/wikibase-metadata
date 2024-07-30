"""Test get_month_log_list_from_url"""

from datetime import datetime, timedelta
from typing import Optional

from freezegun import freeze_time
from fetch_data.log_data.fetch_log_data import get_month_log_list


@freeze_time("2024-03-01")
def test_get_month_log_list_from_url(mocker):
    """Test Two-Pull Scenario"""

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
    for i in range(70):
        mock_logs.append(
            {
                "logid": i + 1,
                "timestamp": (datetime(2024, 3, 1) - timedelta(hours=i * 12)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": mock_users[i % len(mock_users)],
                "type": mock_log_types[i % len(mock_log_types)][0],
                "action": mock_log_types[i % len(mock_log_types)][1],
            }
        )
    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[
            {
                "query": {"logevents": mock_logs[0:50]},
                "continue": {
                    "lecontinue": mock_logs[49].get("timestamp")
                    + "|"
                    + str(mock_logs[49].get("logid"))
                },
            },
            {"query": {"logevents": mock_logs[50:]}},
        ],
    )
    results = get_month_log_list("test.url", datetime.now())
    assert len(results) == 70
