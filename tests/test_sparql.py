"""Test pull_wikidata"""

from json import JSONDecodeError
import pytest

from fetch_data.sparql_data.pull_wikidata import get_sparql_results

from urllib.error import HTTPError


class MockQueryResult:
    """Mock QueryResult"""

    def convert(self):
        """Convert Results to JSON"""

        raise JSONDecodeError("Fail", "{]}", 1)


class MockSPARQLWrapper:
    """Mock SPARQLWrapper"""

    agent: str
    endpoint_url: str
    return_format: str

    # pylint: disable-next=invalid-name
    def __init__(self, endpoint_url: str, agent: str, returnFormat: str):
        self.endpoint_url = endpoint_url
        self.agent = agent
        self.return_format = returnFormat

    # pylint: disable-next=invalid-name,no-self-argument
    def setQuery(query: str):
        """Set Query"""
        # pylint: disable-next=unnecessary-pass
        pass

    # pylint: disable-next=no-method-argument,no-self-argument
    def query():
        """Execute Query"""
        return MockQueryResult()

    # pylint: disable-next=invalid-name,no-self-argument
    def setTimeout(timeout: int):
        """Set Timeout"""
        # pylint: disable-next=unnecessary-pass
        pass


@pytest.mark.asyncio
@pytest.mark.sparql
async def test_sparql_fail(mocker):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.pull_wikidata.SPARQLWrapper",
        side_effect=[MockSPARQLWrapper],
    )

    try:
        await get_sparql_results(
            "https://example.com/query/rdf", "SELECT {?c}", "SELECT QUERY"
        )
        assert False
    except JSONDecodeError:
        assert True


@pytest.mark.asyncio
@pytest.mark.sparql
async def test_sparql_retry(mocker):
    """Test"""

    mock_get_results = mocker.patch(
        "fetch_data.sparql_data.pull_wikidata._get_results",
        side_effect=HTTPError("mock", 429, "mock", "mock", None),
    )

    try:
        await get_sparql_results(
            "https://example.com/query/rdf",
            "SELECT {?c}",
            "SELECT QUERY",
            max_retries=5,
            backup_time_init=0.0001,
            backup_time_multiplier=1.0,
        )
    except HTTPError as exc:
        assert exc.code == 429
        assert True

    assert mock_get_results.call_count == 5 + 1  # 1 for initial call
