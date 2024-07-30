"""Test get_month_log_list_from_url"""

from datetime import datetime, timedelta

from freezegun import freeze_time
import pytest
from requests import ReadTimeout
from fetch_data.log_data import create_log_observation


@freeze_time("2024-03-01")
@pytest.mark.asyncio
async def test_create_log_observation(mocker):
    """Test One-Pull Per Month, Data Returned Scenario"""

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
    oldest_mock_log = min(mock_logs, key=lambda x: x.get("timestamp"))
    newest_mock_log = max(mock_logs, key=lambda x: x.get("timestamp"))

    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[
            {"query": {"logevents": [oldest_mock_log]}},  # oldest
            {"query": {"logevents": [newest_mock_log]}},  # newest
            {
                "query": {
                    "logevents": sorted(mock_logs, key=lambda x: x.get("timestamp"))
                },
            },  # first month
            {
                "query": {
                    "logevents": sorted(
                        mock_logs, key=lambda x: x.get("timestamp"), reverse=True
                    )
                },
            },  # last month
        ],
    )
    success = await create_log_observation(1)
    assert success


@freeze_time("2024-03-01")
@pytest.mark.asyncio
async def test_create_log_observation_error(mocker):
    """Test One-Pull Per Month, Error Returned Scenario"""

    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data", side_effect=[ReadTimeout()]
    )
    success = await create_log_observation(1)
    assert success is False


@freeze_time("2024-03-01")
@pytest.mark.asyncio
async def test_create_log_observation_no_last_month(mocker):
    """Test One-Pull Per Month, No Data In Range Returned Scenario"""

    mock_logs: list[dict] = []
    for i in range(70):
        mock_logs.append(
            {
                "logid": i + 1,
                "timestamp": (datetime(2024, 1, 1) - timedelta(hours=i * 24)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": None,
                "type": "thanks",
                "action": "thank",
            }
        )
    oldest_mock_log = min(mock_logs, key=lambda x: x.get("timestamp"))
    newest_mock_log = max(mock_logs, key=lambda x: x.get("timestamp"))

    mocker.patch(
        "fetch_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[
            {"query": {"logevents": [oldest_mock_log]}},  # oldest
            {"query": {"logevents": [newest_mock_log]}},  # newest
            {
                "query": {
                    "logevents": sorted(mock_logs, key=lambda x: x.get("timestamp"))
                },
            },  # first month
            {
                "query": {
                    "logevents": sorted(
                        mock_logs, key=lambda x: x.get("timestamp"), reverse=True
                    )
                },
            },  # last month
        ],
    )
    success = await create_log_observation(1)
    assert success
