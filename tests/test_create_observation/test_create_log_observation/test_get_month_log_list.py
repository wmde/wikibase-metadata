"""Test get_month_log_list_from_url"""

from datetime import datetime, timedelta

from freezegun import freeze_time
import pytest
from fetch_data.api_data.log_data.fetch_log_data import get_month_log_list


@freeze_time(datetime(2024, 3, 1))
@pytest.mark.asyncio
@pytest.mark.log
async def test_get_month_log_list_from_url_one_pull(mocker):
    """Test One-Pull, Newest Logs Scenario"""

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
        "fetch_data.api_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[
            {
                "query": {"logevents": mock_logs[0:50]},
                "continue": {
                    "lecontinue": f"{mock_logs[50].get('timestamp')}|{mock_logs[50].get('logid')}"
                },
            },
            {"query": {"logevents": mock_logs[50:]}},
        ],
    )
    results = await get_month_log_list("example.com", datetime.now())
    assert len(results) == 31

    newest_log = max(results, key=lambda x: x.log_date)
    assert newest_log.log_date == datetime(2024, 3, 1)
    assert newest_log.age() == 0
    oldest_log = min(results, key=lambda x: x.log_date)
    assert oldest_log.log_date == datetime(2024, 1, 31)
    assert oldest_log.age() == 30


@freeze_time(datetime(2024, 3, 1))
@pytest.mark.asyncio
@pytest.mark.log
async def test_get_month_log_list_from_url_two_pulls(mocker):
    """Test Two-Pull, Newest Logs Scenario"""

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
        "fetch_data.api_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[
            {
                "query": {"logevents": mock_logs[0:50]},
                "continue": {
                    "lecontinue": f"{mock_logs[50].get('timestamp')}|{mock_logs[50].get('logid')}"
                },
            },
            {"query": {"logevents": mock_logs[50:]}},
        ],
    )
    results = await get_month_log_list("example.com", datetime.now())
    assert len(results) == 62

    newest_log = max(results, key=lambda x: x.log_date)
    assert newest_log.log_date == datetime(2024, 3, 1)
    assert newest_log.age() == 0
    oldest_log = min(results, key=lambda x: x.log_date)
    assert oldest_log.log_date == datetime(2024, 1, 30, 12)
    assert oldest_log.age() == 30


@freeze_time(datetime(2024, 3, 1))
@pytest.mark.asyncio
@pytest.mark.log
async def test_get_month_log_list_from_url_more_pulls(mocker):
    """Test More-Pull, Newest Logs Scenario"""

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
        result = {"query": {"logevents": mock_logs[i : i + pull_limit]}}
        if i + pull_limit < len(mock_logs):
            result["continue"] = {
                "lecontinue": mock_logs[i + pull_limit].get("timestamp")
                + "|"
                + str(mock_logs[i + pull_limit].get("logid"))
            }

        mock_side_effects.append(result)

    mocker.patch(
        "fetch_data.api_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=mock_side_effects,
    )
    results = await get_month_log_list("example.com", datetime.now())
    assert len(results) == 2626

    newest_log = max(results, key=lambda x: x.log_date)
    assert newest_log.log_date == datetime(2024, 3, 1)
    assert newest_log.age() == 0
    oldest_log = min(results, key=lambda x: x.log_date)
    assert oldest_log.log_date == datetime(2024, 1, 30, 0, 15)
    assert oldest_log.age() == 30


@freeze_time(datetime(2024, 3, 1))
@pytest.mark.asyncio
@pytest.mark.log
async def test_get_month_log_list_from_url_oldest_one_pull(mocker):
    """Test One-Pull, Oldest Logs Scenario"""

    mock_logs: list[dict] = []
    for i in range(70):
        mock_logs.append(
            {
                "logid": i + 1,
                "timestamp": (datetime(2020, 3, 1) + timedelta(hours=i * 24)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": None,
                "type": "thanks",
                "action": "thank",
            }
        )
    mocker.patch(
        "fetch_data.api_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[
            {
                "query": {"logevents": mock_logs[0:50]},
                "continue": {
                    "lecontinue": f"{mock_logs[50].get('timestamp')}|{mock_logs[50].get('logid')}"
                },
            },
            {"query": {"logevents": mock_logs[50:]}},
        ],
    )
    results = await get_month_log_list("example.com", datetime(2020, 3, 1), oldest=True)
    assert len(results) == 31

    newest_log = max(results, key=lambda x: x.log_date)
    assert newest_log.log_date == datetime(2020, 3, 31)
    assert newest_log.age() == 1431
    oldest_log = min(results, key=lambda x: x.log_date)
    assert oldest_log.log_date == datetime(2020, 3, 1)
    assert oldest_log.age() == 1461
