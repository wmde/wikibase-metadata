"""Test create_software_version_observation"""

import re
import time
import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from tests.test_schema import test_schema
from tests.utils import MockResponse
from tests.utils.mock_request import get_mock_context

DATA_DIRECTORY = "tests/test_create_observation/time_to_first_value/data"

FETCH_TTFV_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchTimeToFirstValueData(wikibaseId: $wikibaseId)
}"""

@pytest.fixture
async def wikibase(db_session):
    """Create a wikibase with article path for software version tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Software Version Test Wikibase",
            base_url="https://example.com",
            article_path="/wiki",
            script_path="/w"
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)
        wikibase_id = wikibase.id
    return wikibase_id

@pytest.mark.asyncio
@pytest.mark.soup
async def test_create_ttfv_observation_success(wikibase, mocker):
    """Test Data Returned Scenario"""

    time.sleep(1)

    # pylint: disable-next=unused-argument,too-many-return-statements
    def mockery(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (
            query
            # pylint: disable-next=line-too-long
            == "https://example.com/w/api.php?action=query&format=json&list=logevents&formatversion=2&ledir=newer&lelimit=1&leprop=timestamp"
        ):
            with open(f"{DATA_DIRECTORY}/creation.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())
        if (
            query_match := re.match(
                # pylint: disable-next=line-too-long
                r"https://example\.com/w/api\.php\?action=query&format=json&prop=revisions&titles=(Q\d+)&rvdir=newer&rvlimit=1&rvprop=timestamp",
                query,
            )
            or re.match(
                # pylint: disable-next=line-too-long
                r"https://example\.com/w/api\.php\?action=query&format=json&prop=revisions&titles=Item:(Q\d+)&rvdir=newer&rvlimit=1&rvprop=timestamp",
                query,
            )
        ) is not None:
            try:
                with open(
                    f"{DATA_DIRECTORY}/{query_match.group(1)}.json", mode="rb"
                ) as data:
                    return MockResponse(query, 200, data.read())
            # pylint: disable-next=bare-except
            except:
                return MockResponse(query, 404)
        if (
            query_match := re.match(
                # pylint: disable-next=line-too-long
                r"https://example\.com/w/api\.php\?action=query&format=json&prop=deletedrevisions&titles=(Q\d+)&drvdir=newer&drvlimit=1&drvprop=timestamp",
                query,
            )
            or re.match(
                # pylint: disable-next=line-too-long
                r"https://example\.com/w/api\.php\?action=query&format=json&prop=deletedrevisions&titles=Item:(Q\d+)&drvdir=newer&drvlimit=1&drvprop=timestamp",
                query,
            )
        ) is not None:
            try:
                with open(
                    f"{DATA_DIRECTORY}/{query_match.group(1)}_del.json", mode="rb"
                ) as data:
                    return MockResponse(query, 200, data.read())
            # pylint: disable-next=bare-except
            except:
                return MockResponse(query, 404)

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mockery
    )

    result = await test_schema.execute(
        FETCH_TTFV_MUTATION,
        variable_values={"wikibaseId": wikibase},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchTimeToFirstValueData"]
