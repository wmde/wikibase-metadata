"""Test update_out_of_date_log_last_observations"""

from datetime import datetime
import json

from freezegun import freeze_time
import pytest
from fetch_data import (
    update_out_of_date_log_first_observations,
    update_out_of_date_log_last_observations,
)
from tests.utils import MockResponse, ParsedUrl


@freeze_time(datetime(2024, 2, 1))
@pytest.mark.asyncio
@pytest.mark.dependency(
    name="log-first-success-ood",
    depends=["add-wikibase", "add-wikibase-script-path"],
    scope="session",
)
@pytest.mark.log
async def test_update_out_of_date_log_first_observations_success(mocker):
    """Test Empty Scenario"""

    mock_logs: list[dict] = [
        {
            "logid": 1,
            "timestamp": datetime(2024, 1, 1).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "user": None,
            "type": "thanks",
            "action": "thank",
        }
    ]
    oldest_mock_log = mock_logs[0]

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
        raise NotImplementedError(query.raw_url)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mockery
    )
    assert await update_out_of_date_log_first_observations() == 1


@freeze_time(datetime(2024, 2, 1))
@pytest.mark.asyncio
@pytest.mark.dependency(
    name="log-last-success-ood",
    depends=["add-wikibase", "add-wikibase-script-path"],
    scope="session",
)
@pytest.mark.log
async def test_update_out_of_date_log_last_observations_success(mocker):
    """Test Empty Scenario"""

    mock_logs: list[dict] = [
        {
            "logid": 1,
            "timestamp": datetime(2024, 2, 1).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "user": None,
            "type": "thanks",
            "action": "thank",
        }
    ]

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
                    # first month
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
    assert await update_out_of_date_log_last_observations() == 1
