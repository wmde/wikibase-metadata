"""Test pull_wikidata"""

from json import JSONDecodeError
import pytest

from fetch_data.sparql_data.pull_wikidata import get_sparql_results


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
        pass

    # pylint: disable-next=no-self-argument
    def query():
        """Execute Query"""
        return MockQueryResult()

    # pylint: disable-next=invalid-name,no-self-argument
    def setTimeout(timeout: int):
        """Set Timeout"""
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
            "https://example.com/query/rdf", "SELECT \{\}", "SELECT QUERY", timeout=20
        )
        assert False
    except JSONDecodeError:
        assert True
