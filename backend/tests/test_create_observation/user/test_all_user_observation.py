"""Test Bulk User Data Update"""

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
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


@pytest.fixture
async def three_wikibases_with_script_path_user(
    db_session,
):  # pylint: disable=unused-argument
    """Create 3 test wikibases with script path for user observation tests"""
    async with get_async_session() as session:
        for i in range(3):
            wikibase = WikibaseModel(
                wikibase_name=f"User Test Wikibase {i}",
                base_url=f"https://user-example-{i}.com",
                script_path="/w",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_update_all_user_observations_fail(
    three_wikibases_with_script_path_user, mocker
):
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
