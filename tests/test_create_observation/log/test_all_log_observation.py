"""Test Bulk Log Update"""

import pytest
from tests.test_schema import test_schema
from tests.utils import MockResponse, ParsedUrl, get_mock_context

ALL_LOG_DATA_MUTATION = """
mutation MyMutation($firstMonth: Boolean!) {
  updateAllLogData(firstMonth: $firstMonth) {
    failure
    success
    total
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="log-first-fail-all",
    depends=[
        "mutate-cloud-instances",
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
    ],
    scope="session",
)
@pytest.mark.mutation
async def test_update_all_log_first_observations_fail(mocker):
    """Test Weird Error Scenario"""

    def mockery(*args, **kwargs) -> MockResponse:
        assert kwargs.get("timeout") == 300

        query = ParsedUrl(args[0])

        assert query.base_url == "https://example.com/w/api.php"
        assert query.params.get("action") == "query"
        assert query.params.get("format") == "json"

        raise RuntimeError

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mockery
    )

    result = await test_schema.execute(
        ALL_LOG_DATA_MUTATION,
        variable_values={"firstMonth": True},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("updateAllLogData") is not None
    assert result.data["updateAllLogData"].get("failure") == 3
    assert result.data["updateAllLogData"].get("success") == 0
    assert result.data["updateAllLogData"].get("total") == 3


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="log-last-fail-all",
    depends=[
        "mutate-cloud-instances",
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
    ],
    scope="session",
)
@pytest.mark.mutation
async def test_update_all_log_last_observations_fail(mocker):
    """Test Weird Error Scenario"""

    def mockery(*args, **kwargs) -> MockResponse:
        assert kwargs.get("timeout") == 300

        query = ParsedUrl(args[0])

        assert query.base_url == "https://example.com/w/api.php"
        assert query.params.get("action") == "query"
        assert query.params.get("format") == "json"

        raise RuntimeError

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mockery
    )

    result = await test_schema.execute(
        ALL_LOG_DATA_MUTATION,
        variable_values={"firstMonth": False},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("updateAllLogData") is not None
    assert result.data["updateAllLogData"].get("failure") == 3
    assert result.data["updateAllLogData"].get("success") == 0
    assert result.data["updateAllLogData"].get("total") == 3
