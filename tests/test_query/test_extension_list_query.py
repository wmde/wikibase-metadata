"""Test Wikibase List"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta


EXTENSION_LIST_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!) {
  extensionList(pageNumber: $pageNumber, pageSize: $pageSize) {
    meta {
      pageNumber
      pageSize
      totalCount
      totalPages
    }
    data {
      id
      softwareName
      softwareType
      url
      archived
      description
      fetched
      latestVersion
      mediawikiBundled
      publicWikiCount
      quarterlyDownloadCount
      tags
    }
  }
}"""


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(depends=["update-software-data"], scope="session")
async def test_extension_list_query():
    """Test Extension List"""

    result = await test_schema.execute(
        EXTENSION_LIST_QUERY, variable_values={"pageNumber": 1, "pageSize": 10}
    )

    assert result.errors is None
    assert result.data is not None
    assert "extensionList" in result.data
    assert_page_meta(result.data["extensionList"], 1, 10, 77, 8)
    assert "data" in result.data["extensionList"]
    assert len(result.data["extensionList"]["data"]) == 10


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(depends=["update-software-data"], scope="session")
@pytest.mark.parametrize(
    ["idx", "expected_id", "expected_name", "expected_url"],
    [
        (0, "9", "Babel", "https://www.mediawiki.org/wiki/Extension:Babel"),
        (1, "16", "Google Analytics Integration", "https://www.mediawiki.org/wiki/Extension:Google_Analytics_Integration"),
        (2, "10", "LabeledSectionTransclusion", "https://www.mediawiki.org/wiki/Extension:Labeled_Section_Transclusion"),
        (3, "17", "ProofreadPage", "https://www.mediawiki.org/wiki/Extension:Proofread_Page"),
        (4, "11", "Scribunto", "https://www.mediawiki.org/wiki/Extension:Scribunto"),
        (5, "18", "UniversalLanguageSelector", "https://www.mediawiki.org/wiki/Extension:UniversalLanguageSelector"),
        (6, "12", "WikibaseClient", "https://www.mediawiki.org/wiki/Extension:Wikibase_Client"),
        (7, "13", "WikibaseLib", "https://www.mediawiki.org/wiki/Extension:WikibaseLib"),
        (8, "14", "WikibaseRepository", "https://www.mediawiki.org/wiki/Extension:Wikibase_Repository"),
        (9, "15", "WikibaseView", "https://www.mediawiki.org/wiki/Extension:WikibaseView"),
    ],
)
async def test_extension_list_query_parameterized(
    idx: int, expected_id: str, expected_name: str, expected_url: str
):
    """Test Extension List"""

    result = await test_schema.execute(
        EXTENSION_LIST_QUERY, variable_values={"pageNumber": 1, "pageSize": 10}
    )

    assert result.errors is None
    assert result.data is not None
    assert "extensionList" in result.data
    assert_page_meta(result.data["extensionList"], 1, 10, 77, 8)
    assert "data" in result.data["extensionList"]
    assert len(result.data["extensionList"]["data"]) == 10
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "id"], expected_id
    )
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "softwareName"], expected_name
    )
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "softwareType"], "EXTENSION"
    )
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "url"], expected_url
    )
