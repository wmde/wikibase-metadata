"""Test create_software_version_observation"""

import re
import time
import pytest
from tests.test_schema import test_schema
from tests.utils import MockResponse
from tests.utils.mock_request import get_mock_context

DATA_DIRECTORY = "tests/test_create_observation/time_to_first_value/data"

FETCH_TTFV_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchTimeToFirstValueData(wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="ttfv-success",
    depends=["ttfv-fail-ood"],
    scope="session",
)
@pytest.mark.mutation
@pytest.mark.soup
async def test_create_ttfv_observation_success(mocker):
    """Test Data Returned Scenario"""

    time.sleep(1)

    # pylint: disable-next=unused-argument,too-many-return-statements
    def mockery(*args, **kwargs):
        assert kwargs.get("timeout") == 10
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
                r"https://example\.com/w/api\.php\?action=query&format=json&prop=revisions&titles=(Q\d+)\|Item:Q\d+&rvdir=newer&rvlimit=1&rvprop=timestamp",
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

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mockery
    )

    result = await test_schema.execute(
        FETCH_TTFV_MUTATION,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchTimeToFirstValueData"]
