from json import JSONDecodeError
import pytest

from fetch_data.sparql_data.pull_wikidata import get_sparql_results


class MockQueryResult:
    def convert(self):
        raise JSONDecodeError("Fail", "{]}", 1)


class MockSPARQLWrapper:
    agent: str
    endpoint_url: str
    return_format: str

    def __init__(self, endpoint_url: str, agent: str, returnFormat: str):
        self.endpoint_url = endpoint_url
        self.agent = agent
        self.return_format = returnFormat

    def setQuery(query: str):
        pass

    def query():
        return MockQueryResult()

    def setTimeout(timeout: int):
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
