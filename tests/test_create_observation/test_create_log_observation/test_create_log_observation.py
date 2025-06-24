"""Test create_log_observation"""

from datetime import datetime, timedelta
import json

from freezegun import freeze_time
import pytest
from requests import ReadTimeout
from fetch_data import create_log_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context, MockResponse, ParsedUrl

LOG_DATA_MUTATION = """mutation MyMutation($wikibaseId: Int!, $firstMonth: Boolean!) {
  fetchLogData(wikibaseId: $wikibaseId, firstMonth: $firstMonth)
}"""


@freeze_time("2024-03-01")
@pytest.mark.asyncio
@pytest.mark.dependency(
    name="log-first-success-1", depends=["log-first-success-ood"], scope="session"
)
@pytest.mark.log
@pytest.mark.mutation
async def test_create_log_observation_first_success(mocker):
    """
    Test One-Pull Per Month, Data Returned Scenario

    log_month_id 1, first month, users, 'thanks/thank'
    """

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

    def mockery(*args, **kwargs) -> MockResponse:
        assert kwargs.get("timeout") == 10

        query = ParsedUrl(args[0])

        assert query.base_url == "https://example.com/w/api.php"
        assert query.params.get("action") == "query"
        assert query.params.get("format") == "json"

        match query.params.get("list"):
            case "logevents":
                assert query.params.get("formatversion") == 2
                match (query.params.get("ledir"), query.params.get("lelimit")):
                    # oldest
                    case ("newer", 1):
                        return MockResponse(
                            query,
                            200,
                            json.dumps({"query": {"logevents": [oldest_mock_log]}}),
                        )
                    # first month
                    case ("newer", 500):
                        return MockResponse(
                            query,
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
            case "users":
                users = []
                if "User:A" in query.params.get("ususers"):
                    users.append({"name": "User:A", "groups": ["*", "users", "admin"]})
                if "User:B" in query.params.get("ususers"):
                    users.append({"name": "User:B", "invalid": True})
                if "User:C" in query.params.get("ususers"):
                    users.append({"name": "User:C", "groups": ["*", "users", "bot"]})
                return MockResponse(
                    query.raw_url, 200, json.dumps({"query": {"users": users}})
                )

        raise NotImplementedError(query.raw_url)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mockery
    )

    result = await test_schema.execute(
        LOG_DATA_MUTATION,
        variable_values={"wikibaseId": 1, "firstMonth": True},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchLogData"]


@freeze_time("2024-03-01")
@pytest.mark.asyncio
@pytest.mark.dependency(
    name="log-last-success-1", depends=["log-last-success-ood"], scope="session"
)
@pytest.mark.log
@pytest.mark.mutation
async def test_create_log_observation_last_success(mocker):
    """
    Test One-Pull Per Month, Data Returned Scenario

    log_month_id 2, last month, None user, thanks/thank"""

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

    def mockery(*args, **kwargs) -> MockResponse:
        assert kwargs.get("timeout") == 10

        query = ParsedUrl(args[0])

        assert query.base_url == "https://example.com/w/api.php"
        assert query.params.get("action") == "query"
        assert query.params.get("format") == "json"
        assert query.params.get("list") == "logevents"
        assert query.params.get("formatversion") == 2

        match (query.params.get("ledir"), query.params.get("lelimit")):
            # last month
            case ("older", 500):
                return MockResponse(
                    query,
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
        raise NotImplementedError(query.raw_url)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mockery
    )

    result = await test_schema.execute(
        LOG_DATA_MUTATION,
        variable_values={"wikibaseId": 1, "firstMonth": False},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchLogData"]


@freeze_time("2024-03-02")
@pytest.mark.asyncio
@pytest.mark.dependency(
    name="log-first-failure", depends=["log-first-success-1"], scope="session"
)
@pytest.mark.log
async def test_create_log_first_observation_error(mocker):
    """
    Test One-Pull Per Month, Error Returned Scenario

    log_month_id 3, first month, fail
    """

    mocker.patch(
        "fetch_data.api_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[ReadTimeout()],
    )
    success = await create_log_observation(1, first_month=True)
    assert success is False


@freeze_time("2024-03-02")
@pytest.mark.asyncio
@pytest.mark.dependency(
    name="log-last-failure", depends=["log-last-success-1"], scope="session"
)
@pytest.mark.log
async def test_create_log_last_observation_error(mocker):
    """
    Test One-Pull Per Month, Error Returned Scenario

    log_month_id 4, last month, fail"""

    mocker.patch(
        "fetch_data.api_data.log_data.fetch_log_data.fetch_api_data",
        side_effect=[ReadTimeout()],
    )
    success = await create_log_observation(1, first_month=False)
    assert success is False


@freeze_time("2024-03-03")
@pytest.mark.asyncio
@pytest.mark.dependency(
    name="log-last-success-2",
    depends=[
        "log-first-success-1",
        "log-last-success-1",
        "log-first-failure",
        "log-last-failure",
    ],
    scope="session",
)
@pytest.mark.log
async def test_create_log_last_observation_no_last_month(mocker):
    """
    Test One-Pull Per Month, No Data In Range Returned Scenario

    log_month_id 5, last month, success, no data"""

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

    def mockery(*args, **kwargs):
        assert kwargs.get("timeout") == 10

        query = ParsedUrl(args[0])

        assert query.base_url == "https://example.com/w/api.php"
        assert query.params.get("format") == "json"
        assert query.params.get("formatversion") == 2
        assert query.params.get("action") == "query"
        assert query.params.get("list") == "logevents"
        assert query.params.get("ledir") == "older"
        assert query.params.get("lelimit") == 500

        return MockResponse(
            query.raw_url,
            200,
            json.dumps(
                {
                    "query": {
                        "logevents": sorted(
                            mock_logs, key=lambda x: x.get("timestamp"), reverse=True
                        )
                    }
                }
            ),
        )

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mockery
    )
    success = await create_log_observation(1, first_month=False)
    assert success
