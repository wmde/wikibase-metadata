"""Test create_software_version_observation"""

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
        match query:

            case "https://example.com/w/index.php?title=Main_Page&action=history&dir=prev":
                with open(f"{DATA_DIRECTORY}/Main_Page.html", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
            case (
                "https://example.com/w/index.php?title=Item:Q1&action=history&dir=prev"
            ):
                with open(f"{DATA_DIRECTORY}/Q1.html", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
            case (
                "https://example.com/w/index.php?title=Item:Q10&action=history&dir=prev"
            ):
                return MockResponse(query, 404)
            case (
                "https://example.com/w/index.php?title=Item:Q11&action=history&dir=prev"
            ):
                return MockResponse(query, 404)
            case (
                "https://example.com/w/index.php?title=Item:Q12&action=history&dir=prev"
            ):
                return MockResponse(query, 404)
            case (
                "https://example.com/w/index.php?title=Item:Q13&action=history&dir=prev"
            ):
                return MockResponse(query, 404)
            case (
                "https://example.com/w/index.php?title=Item:Q14&action=history&dir=prev"
            ):
                return MockResponse(query, 404)

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.soup_data.software.get_update_software_data.requests.get",
        side_effect=mockery,
    )

    result = await test_schema.execute(
        FETCH_TTFV_MUTATION,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchTimeToFirstValueData"]
