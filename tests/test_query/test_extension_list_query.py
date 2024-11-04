"""Test Wikibase List"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_page_meta


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
