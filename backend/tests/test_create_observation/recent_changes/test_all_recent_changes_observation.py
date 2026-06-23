"""Test Bulk Recent Changes Update"""

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from tests.test_schema import test_schema
from tests.utils import MockResponse, ParsedUrl, get_mock_context

ALL_RECENT_CHANGES_DATA_MUTATION = """
mutation MyMutation {
  updateAllRecentChangesData {
    failure
    success
    total
  }
}
"""


@pytest.fixture
async def three_wikibases_with_script_path(
    db_session,
):  # pylint: disable=unused-argument
    """Create 3 test wikibases with script path for recent changes tests"""
    async with get_async_session() as session:
        for i in range(3):
            wikibase = WikibaseModel(
                wikibase_name=f"Recent Changes Test Wikibase {i}",
                base_url=f"https://recent-changes-example-{i}.com",
                script_path="/w",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
async def test_update_all_recent_changes_observations_fail(
    three_wikibases_with_script_path, mocker
):  # pylint: disable=unused-argument, redefined-outer-name
    """Test Weird Error Scenario"""

    def mockery(*args, **kwargs) -> MockResponse:
        assert kwargs.get("timeout") == 300

        query = ParsedUrl(args[0])

        assert query.base_url.endswith("/w/api.php")
        assert query.params.get("action") == "query"
        assert query.params.get("format") == "json"

        raise RuntimeError

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mockery
    )

    result = await test_schema.execute(
        ALL_RECENT_CHANGES_DATA_MUTATION,
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("updateAllRecentChangesData") is not None
    assert result.data["updateAllRecentChangesData"].get("failure") == 3
    assert result.data["updateAllRecentChangesData"].get("success") == 0
    assert result.data["updateAllRecentChangesData"].get("total") == 3
