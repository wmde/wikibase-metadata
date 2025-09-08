"""Test Bulk User Data Update"""

import pytest
from tests.test_schema import test_schema
from tests.utils import MockResponse, ParsedUrl, get_mock_context

ALL_USER_DATA_MUTATION = """
mutation MyMutation {
  updateAllUserData {
    failure
    success
    total
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="user-fail-all",
    depends=[
        "mutate-cloud-instances",
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
    ],
    scope="session",
)
@pytest.mark.mutation
async def test_update_all_user_observations_fail(mocker):
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
        ALL_USER_DATA_MUTATION,
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("updateAllUserData") is not None
    assert result.data["updateAllUserData"].get("failure") == 3
    assert result.data["updateAllUserData"].get("success") == 0
    assert result.data["updateAllUserData"].get("total") == 3
