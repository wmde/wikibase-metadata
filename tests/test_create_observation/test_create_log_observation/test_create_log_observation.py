"""Test get_month_log_list_from_url"""

from datetime import datetime, timedelta
import json
import time

from freezegun import freeze_time
import pytest
from requests import ReadTimeout
from fetch_data import create_log_observation
from tests.utils import MockResponse, ParsedUrl


@freeze_time("2024-03-01")
@pytest.mark.asyncio
@pytest.mark.dependency(name="log-success-1", depends=["add-wikibase"], scope="session")
@pytest.mark.log
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
        "fetch_data.api_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[
            {"query": {"logevents": [oldest_mock_log]}},  # oldest
            {"query": {"logevents": [newest_mock_log]}},  # newest
            {
                "query": {
                    "logevents": sorted(mock_logs, key=lambda x: x.get("timestamp"))
                }
            },  # first month
            {
                "query": {
                    "logevents": sorted(
                        mock_logs, key=lambda x: x.get("timestamp"), reverse=True
                    )
                }
            },  # last month
        ],
    )
    success = await create_log_observation(1)
    assert success


@freeze_time("2024-03-01")
@pytest.mark.asyncio
@pytest.mark.dependency(name="log-failure", depends=["add-wikibase"], scope="session")
@pytest.mark.log
async def test_create_log_observation_error(mocker):
    """Test One-Pull Per Month, Error Returned Scenario"""

    mocker.patch(
        "fetch_data.api_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[ReadTimeout()],
    )
    success = await create_log_observation(1)
    assert success is False


@freeze_time("2024-03-01")
@pytest.mark.asyncio
@pytest.mark.dependency(name="log-success-2", depends=["log-success-1", "log-failure"])
@pytest.mark.log
async def test_create_log_observation_no_last_month(mocker):
    """Test One-Pull Per Month, No Data In Range Returned Scenario"""

    time.sleep(1)

    mock_logs: list[dict] = []
    for i in range(70):
        mock_logs.append(
            {
                "logid": i + 1,
                "timestamp": (datetime(2024, 1, 1) - timedelta(hours=i * 24)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "user": (
                    "User:A" if i % 3 == 0 else "User:B" if i % 2 == 0 else "User:C"
                ),
                "type": "thanks",
                "action": "thank",
            }
        )
    oldest_mock_log = min(mock_logs, key=lambda x: x.get("timestamp"))
    newest_mock_log = max(mock_logs, key=lambda x: x.get("timestamp"))

    # pylint: disable=unused-argument
    def mockery(*args, **kwargs):
        query = ParsedUrl(args[0])
        match (query.params.get("action"), query.params.get("list")):
            case ("query", "logevents"):
                match (query.params.get("ledir"), query.params.get("lelimit")):
                    case ("newer", 1):
                        return MockResponse(
                            200, json.dumps({"query": {"logevents": [oldest_mock_log]}})
                        )
                    case ("newer", 500):
                        return MockResponse(
                            200,
                            json.dumps(
                                {
                                    "query": {
                                        "logevents": sorted(
                                            mock_logs, key=lambda x: x.get("timestamp")
                                        )
                                    }
                                }
                            ),
                        )
                    case ("older", 1):
                        return MockResponse(
                            200, json.dumps({"query": {"logevents": [newest_mock_log]}})
                        )
                    case ("older", 500):
                        return MockResponse(
                            200,
                            json.dumps(
                                {
                                    "query": {
                                        "logevents": sorted(
                                            mock_logs,
                                            key=lambda x: x.get("timestamp"),
                                            reverse=True,
                                        )
                                    }
                                }
                            ),
                        )
            case ("query", "users"):
                users = []
                if "User:A" in query.params.get("ususers"):
                    users.append({"name": "User:A", "groups": ["*", "users", "admin"]})
                if "User:B" in query.params.get("ususers"):
                    users.append({"name": "User:B", "invalid": True})
                if "User:C" in query.params.get("ususers"):
                    users.append({"name": "User:C", "groups": ["*", "users", "bot"]})
                return MockResponse(200, json.dumps({"query": {"users": users}}))
        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mockery
    )
    success = await create_log_observation(1)
    assert success
