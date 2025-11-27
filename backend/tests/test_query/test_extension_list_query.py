"""Test Wikibase List"""

from datetime import datetime
from typing import Optional
import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta, DATETIME_FORMAT


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
      wikibaseSuiteBundled
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
    assert_page_meta(result.data["extensionList"], 1, 10, 12, 2)
    assert "data" in result.data["extensionList"]
    assert len(result.data["extensionList"]["data"]) == 10


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.version
@pytest.mark.dependency(
    depends=["update-software-data", "test-set-bundled"], scope="session"
)
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
        "expected_wbs_bundled",
        "expected_public_wiki_count",
        "expected_quarterly_download_count",
        "expected_tags",
    ],
    [
        (
            0,
            "2",
            "Babel",
            "Babel",
            False,
            # pylint: disable-next=line-too-long
            "Adds a parser function to inform other users about language proficiency and categorize users of the same levels and languages.",
            datetime(2024, 3, 1),
            "Continuous updates",
            False,
            True,
            2416,
            63,
            ["Parser function"],
        ),
        (
            1,
            "18",
            "Google Analytics Integration",
            "Google_Analytics_Integration",
            False,
            # pylint: disable-next=line-too-long
            "Automatically inserts Google Universal Analytics (and/or other web analytics) tracking code at the bottom of MediaWiki pages",
            datetime(2024, 3, 1),
            "3.0.1 (2017-10-29)",
            False,
            None,
            1302,
            None,
            ["Hook", "User activity"],
        ),
        (
            2,
            "12",
            "LabeledSectionTransclusion",
            "Labeled_Section_Transclusion",
            False,
            "Enables marked sections of text to be transcluded",
            datetime(2024, 3, 1),
            None,
            False,
            None,
            6919,
            None,
            ["Parser function", "Tag"],
        ),
        (
            3,
            "1",
            "Miraheze Magic",
            "MirahezeMagic",
            None,
            None,
            datetime(2024, 3, 1),
            None,
            None,
            None,
            None,
            None,
            ["Magic", "extensionname"],
        ),
        (
            4,
            "19",
            "ProofreadPage",
            "Proofread_Page",
            False,
            # pylint: disable-next=line-too-long
            "The Proofread Page extension can render a book either as a column of OCR text beside a column of scanned images, or broken into its logical organization (such as chapters or poems) using transclusion.",
            datetime(2024, 3, 1),
            "Continuous updates",
            False,
            None,
            None,
            None,
            ["API", "ContentHandler", "Database", "Page action", "Tag"],
        ),
        (
            5,
            "13",
            "Scribunto",
            "Scribunto",
            False,
            "Provides a framework for embedding scripting languages into MediaWiki pages",
            datetime(2024, 3, 1),
            "Continuous updates",
            True,
            True,
            8789,
            450,
            ["Parser extension"],
        ),
        (
            6,
            "20",
            "UniversalLanguageSelector",
            "UniversalLanguageSelector",
            False,
            "Tool that allows users to select a language and configure its support in an easy way.",
            datetime(2024, 3, 1),
            "2024-07-16",
            False,
            None,
            1237,
            243,
            ["Beta Feature", "Skin"],
        ),
        (
            7,
            "14",
            "WikibaseClient",
            "Wikibase_Client",
            False,
            "Client for structured data repository",
            datetime(2024, 3, 1),
            None,
            False,
            None,
            None,
            None,
            ["Ajax", "Parser function"],
        ),
        (
            8,
            "15",
            "WikibaseLib",
            "WikibaseLib",
            True,
            "Provides common Wikibase functionality for Wikibase Repository and Wikibase Client",
            datetime(2024, 3, 1),
            "Continuous updates",
            False,
            None,
            None,
            None,
            [],
        ),
        (
            9,
            "80",
            "WikibaseManifest",
            "WikibaseManifest",
            False,
            "API provided metadata for structured data repository",
            datetime(2024, 3, 1),
            "0.0.1 (continuous updates)",
            False,
            None,
            None,
            None,
            ["API"],
        ),
        (
            10,
            "16",
            "WikibaseRepository",
            "Wikibase_Repository",
            False,
            "Structured data repository",
            datetime(2024, 3, 1),
            "Continuous updates",
            False,
            None,
            None,
            None,
            ["API", "Ajax", "ContentHandler"],
        ),
        (
            11,
            "17",
            "WikibaseView",
            "WikibaseView",
            False,
            None,
            datetime(2024, 3, 1),
            None,
            None,
            None,
            None,
            None,
            [],
        ),
    ],
)
# pylint: disable-next=too-many-arguments,too-many-positional-arguments
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
    expected_wbs_bundled: Optional[bool],
    expected_public_wiki_count: Optional[int],
    expected_quarterly_download_count: Optional[int],
    expected_tags: list[str],
):
    """Test Extension List"""

    result = await test_schema.execute(
        EXTENSION_LIST_QUERY, variable_values={"pageNumber": 1, "pageSize": 100}
    )

    assert result.errors is None
    assert result.data is not None
    assert "extensionList" in result.data
    assert_page_meta(result.data["extensionList"], 1, 100, 12, 1)
    assert "data" in result.data["extensionList"]
    assert len(result.data["extensionList"]["data"]) == 12
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
        result.data,
        ["extensionList", "data", idx, "fetched"],
        expected_fetched.strftime(DATETIME_FORMAT),
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
        ["extensionList", "data", idx, "wikibaseSuiteBundled"],
        expected_wbs_bundled,
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
