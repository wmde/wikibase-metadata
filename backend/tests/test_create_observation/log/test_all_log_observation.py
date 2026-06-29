"""Test Bulk Log Update"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import WikibaseModel
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


@pytest.fixture
async def three_wikibases_with_script_path(db_session):
    """Create 3 test wikibases with script path for log observation tests"""

    async with AsyncSession(bind=db_session) as session:
        for i in range(3):
            wikibase = WikibaseModel(
                wikibase_name=f"Log Test Wikibase {i}",
                base_url=f"https://example-{i}.com",
                script_path="/w",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)
        await session.flush()
        await session.commit()


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_update_all_log_first_observations_fail(
    three_wikibases_with_script_path, mocker
):  # pylint: disable=redefined-outer-name, unused-argument
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
async def test_update_all_log_last_observations_fail(
    three_wikibases_with_script_path, mocker
):  # pylint: disable=redefined-outer-name, unused-argument
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
