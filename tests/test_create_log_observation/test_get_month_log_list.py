"""Test get_month_log_list_from_url"""

from datetime import datetime, timedelta
from typing import Optional

from freezegun import freeze_time
from fetch_data.log_data.fetch_log_data import get_month_log_list


@freeze_time("2024-03-01")
def test_get_month_log_list_from_url_one_pull(mocker):
    """Test Two-Pull Scenario"""

    mock_logs: list[dict] = []
    for i in range(70):
        mock_logs.append(
            {
                "logid": i + 1,
                "timestamp": (datetime(2024, 3, 1) - timedelta(hours=i * 24)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": None,
                "type": "thanks",
                "action": "thank",
            }
        )
    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[
            {
                "query": {"logevents": mock_logs[0:50]},
                "continue": {
                    "lecontinue": f"{mock_logs[49].get('timestamp')}|{mock_logs[49].get('logid')}"
                },
            },
            {"query": {"logevents": mock_logs[50:]}},
        ],
    )
    results = get_month_log_list("test.url", datetime.now())
    assert len(results) == 50


@freeze_time("2024-03-01")
def test_get_month_log_list_from_url_two_pulls(mocker):
    """Test Two-Pull Scenario"""

    mock_logs: list[dict] = []
    for i in range(70):
        mock_logs.append(
            {
                "logid": i + 1,
                "timestamp": (datetime(2024, 3, 1) - timedelta(hours=i * 12)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": None,
                "type": "thanks",
                "action": "thank",
            }
        )
    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[
            {
                "query": {"logevents": mock_logs[0:50]},
                "continue": {
                    "lecontinue": f"{mock_logs[49].get('timestamp')}|{mock_logs[49].get('logid')}"
                },
            },
            {"query": {"logevents": mock_logs[50:]}},
        ],
    )
    results = get_month_log_list("test.url", datetime.now())
    assert len(results) == 70


@freeze_time("2024-03-01")
def test_get_month_log_list_from_url_more_pulls(mocker):
    """Test More-Pull Scenario"""

    pull_limit = 500

    mock_logs: list[dict] = []
    for i in range(7000):
        mock_logs.append(
            {
                "logid": i + 1,
                "timestamp": (
                    datetime(2024, 3, 1) - timedelta(minutes=i * 17)
                ).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "user": None,
                "type": "thanks",
                "action": "thank",
            }
        )
    mock_side_effects: list[dict] = []
    for i in range(0, len(mock_logs), pull_limit):
        result = {
            "query": {"logevents": mock_logs[i : i + pull_limit]},
        }
        if i + pull_limit < len(mock_logs):
            result["continue"] = {
                "lecontinue": mock_logs[i + pull_limit].get("timestamp")
                + "|"
                + str(mock_logs[i + pull_limit].get("logid"))
            }

        mock_side_effects.append(result)

    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=mock_side_effects,
    )
    results = get_month_log_list("test.url", datetime.now())
    assert len(results) == 3000
