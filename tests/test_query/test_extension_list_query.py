"""Test Wikibase List"""

from datetime import datetime
from typing import Optional
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
@pytest.mark.version
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
@pytest.mark.version
@pytest.mark.dependency(depends=["update-software-data"], scope="session")
@pytest.mark.parametrize(
    [
        "idx",
        "expected_id",
        "expected_name",
        "expected_url",
        "expected_archived",
        "expected_description",
        "expected_fetched",
        "expected_latest_version",
        "expected_mediawiki_bundled",
        "expected_public_wiki_count",
        "expected_quarterly_download_count",
        "expected_tags",
    ],
    [
        (
            0,
            "9",
            "Babel",
            "Babel",
            False,
            # pylint: disable=line-too-long
            "Adds a parser function to inform other users about language proficiency and categorize users of the same levels and languages.",
            datetime(2024, 3, 1),
            "Continuous updates",
            False,
            2416,
            63,
            ["Parser function"],
        ),
        (
            1,
            "16",
            "Google Analytics Integration",
            "Google_Analytics_Integration",
            False,
            # pylint: disable=line-too-long
            "Automatically inserts Google Universal Analytics (and/or other web analytics) tracking code at the bottom of MediaWiki pages",
            datetime(2024, 3, 1),
            "3.0.1 (2017-10-29)",
            False,
            1302,
            None,
            ["User activity", "Hook"],
        ),
        (
            2,
            "10",
            "LabeledSectionTransclusion",
            "Labeled_Section_Transclusion",
            False,
            "Enables marked sections of text to be transcluded",
            datetime(2024, 3, 1),
            None,
            False,
            6919,
            None,
            ["Parser function", "Tag"],
        ),
        (
            3,
            "17",
            "ProofreadPage",
            "Proofread_Page",
            False,
            # pylint: disable=line-too-long
            "The Proofread Page extension can render a book either as a column of OCR text beside a column of scanned images, or broken into its logical organization (such as chapters or poems) using transclusion.",
            datetime(2024, 3, 1),
            "continuous updates",
            False,
            None,
            None,
            ["Tag", "Page action", "ContentHandler", "API", "Database"],
        ),
        (
            4,
            "11",
            "Scribunto",
            "Scribunto",
            False,
            "Provides a framework for embedding scripting languages into MediaWiki pages",
            datetime(2024, 3, 1),
            "Continuous updates",
            True,
            8789,
            450,
            ["Parser extension"],
        ),
        (
            5,
            "18",
            "UniversalLanguageSelector",
            "UniversalLanguageSelector",
            False,
            "Tool that allows users to select a language and configure its support in an easy way.",
            datetime(2024, 3, 1),
            "2024-07-16",
            False,
            1237,
            243,
            ["Skin", "Beta Feature"],
        ),
        (
            6,
            "12",
            "WikibaseClient",
            "Wikibase_Client",
            False,
            "Client for structured data repository",
            datetime(2024, 3, 1),
            None,
            False,
            None,
            None,
            ["Parser function", "Ajax"],
        ),
        (
            7,
            "13",
            "WikibaseLib",
            "WikibaseLib",
            True,
            "Provides common Wikibase functionality for Wikibase Repository and Wikibase Client",
            datetime(2024, 3, 1),
            "continuous updates",
            False,
            None,
            None,
            [],
        ),
        (
            8,
            "14",
            "WikibaseRepository",
            "Wikibase_Repository",
            False,
            "Structured data repository",
            datetime(2024, 3, 1),
            "continuous updates",
            False,
            None,
            None,
            ["ContentHandler", "API", "Ajax"],
        ),
        (
            9,
            "15",
            "WikibaseView",
            "WikibaseView",
            False,
            None,
            datetime(2024, 3, 1),
            None,
            None,
            None,
            None,
            [],
        ),
    ],
)
# pylint: disable=too-many-arguments,too-many-positional-arguments
async def test_extension_list_query_parameterized(
    idx: int,
    expected_id: str,
    expected_name: str,
    expected_url: str,
    expected_archived: bool,
    expected_description: Optional[str],
    expected_fetched: datetime,
    expected_latest_version: Optional[str],
    expected_mediawiki_bundled: Optional[bool],
    expected_public_wiki_count: Optional[int],
    expected_quarterly_download_count: Optional[int],
    expected_tags: list[str],
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
        result.data,
        ["extensionList", "data", idx, "url"],
        f"https://www.mediawiki.org/wiki/Extension:{expected_url}",
    )
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "archived"], expected_archived
    )
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "description"], expected_description
    )
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "fetched"], expected_fetched.strftime("%Y-%m-%dT%H:%M:%S")
    )
    assert_layered_property_value(
        result.data,
        ["extensionList", "data", idx, "latestVersion"],
        expected_latest_version,
    )
    assert_layered_property_value(
        result.data,
        ["extensionList", "data", idx, "mediawikiBundled"],
        expected_mediawiki_bundled,
    )
    assert_layered_property_value(
        result.data,
        ["extensionList", "data", idx, "publicWikiCount"],
        expected_public_wiki_count,
    )
    assert_layered_property_value(
        result.data,
        ["extensionList", "data", idx, "quarterlyDownloadCount"],
        expected_quarterly_download_count,
    )
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "tags"], expected_tags
    )
