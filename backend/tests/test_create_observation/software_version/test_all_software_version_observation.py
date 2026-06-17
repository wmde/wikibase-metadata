"""Test Bulk Software Version Update"""

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from tests.test_schema import test_schema
from tests.utils import get_mock_context

ALL_VERSION_DATA_MUTATION = """
mutation MyMutation {
  updateAllVersionData {
    failure
    success
    total
  }
}
"""

@pytest.fixture
async def three_wikibases_with_article_path(db_session):
    """Create 3 test wikibases with article path for software version tests"""
    async with get_async_session() as session:
        for i in range(3):
            wikibase = WikibaseModel(
                wikibase_name=f"Software Version Test Wikibase {i}",
                base_url=f"https://software-version-example-{i}.com",
                article_path="/wiki",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
async def test_update_all_software_version_observations_fail(three_wikibases_with_article_path, mocker):
    """Test Weird Error Scenario"""

    def mockery(*args, **kwargs):
        raise RuntimeError

    mocker.patch(
        "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
        side_effect=mockery,
    )

    result = await test_schema.execute(
        ALL_VERSION_DATA_MUTATION,
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("updateAllVersionData") is not None
    assert result.data["updateAllVersionData"].get("failure") == 3
    assert result.data["updateAllVersionData"].get("success") == 0
    assert result.data["updateAllVersionData"].get("total") == 3
