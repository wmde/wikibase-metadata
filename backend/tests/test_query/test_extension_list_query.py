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


@pytest.fixture
async def extension_list(db_session):
    """Create test extensions"""
    from model.database import WikibaseSoftwareModel
    from model.database.wikibase_software.software_tag_model import WikibaseSoftwareTagModel
    from model.enum import WikibaseSoftwareType
    from sqlalchemy.ext.asyncio import AsyncSession

    extensions = [
        {"id": 2, "name": "Babel", "url": "https://www.mediawiki.org/wiki/Extension:Babel", "archived": False, "description": "Adds a parser function to inform other users about language proficiency and categorize users of the same levels and languages.", "latest_version": "Continuous updates", "mediawiki_bundled": False, "wbs_bundled": True, "public_wiki_count": 2416, "quarterly_download_count": 63, "tags": ["tag 1"]},
        {"id": 18, "name": "Google Analytics Integration", "url": "https://www.mediawiki.org/wiki/Extension:Google_Analytics_Integration", "archived": False, "description": "Automatically inserts Google Universal Analytics (and/or other web analytics) tracking code at the bottom of MediaWiki pages", "latest_version": "3.0.1 (2017-10-29)", "mediawiki_bundled": False, "wbs_bundled": None, "public_wiki_count": 1302, "quarterly_download_count": None, "tags": ["tag 2", "tag 3"]},
        {"id": 12, "name": "LabeledSectionTransclusion", "url": "https://www.mediawiki.org/wiki/Extension:Labeled_Section_Transclusion", "archived": False, "description": "Enables marked sections of text to be transcluded", "latest_version": None, "mediawiki_bundled": False, "wbs_bundled": None, "public_wiki_count": 6919, "quarterly_download_count": None, "tags": []},
        {"id": 1, "name": "Miraheze Magic", "url": "https://www.mediawiki.org/wiki/Extension:MirahezeMagic", "archived": None, "description": None, "latest_version": None, "mediawiki_bundled": None, "wbs_bundled": None, "public_wiki_count": None, "quarterly_download_count": None, "tags": []},
        {"id": 19, "name": "ProofreadPage", "url": "https://www.mediawiki.org/wiki/Extension:Proofread_Page", "archived": False, "description": "The Proofread Page extension can render a book either as a column of OCR text beside a column of scanned images, or broken into its logical organization (such as chapters or poems) using transclusion.", "latest_version": "Continuous updates", "mediawiki_bundled": False, "wbs_bundled": None, "public_wiki_count": None, "quarterly_download_count": None, "tags": []},
        {"id": 13, "name": "Scribunto", "url": "https://www.mediawiki.org/wiki/Extension:Scribunto", "archived": False, "description": "Provides a framework for embedding scripting languages into MediaWiki pages", "latest_version": "Continuous updates", "mediawiki_bundled": True, "wbs_bundled": True, "public_wiki_count": 8789, "quarterly_download_count": 450, "tags": []},
        {"id": 20, "name": "UniversalLanguageSelector", "url": "https://www.mediawiki.org/wiki/Extension:UniversalLanguageSelector", "archived": False, "description": "Tool that allows users to select a language and configure its support in an easy way.", "latest_version": "2024-07-16", "mediawiki_bundled": False, "wbs_bundled": None, "public_wiki_count": 1237, "quarterly_download_count": 243, "tags": []},
        {"id": 14, "name": "WikibaseClient", "url": "https://www.mediawiki.org/wiki/Extension:Wikibase_Client", "archived": False, "description": "Client for structured data repository", "latest_version": None, "mediawiki_bundled": False, "wbs_bundled": None, "public_wiki_count": None, "quarterly_download_count": None, "tags": []},
        {"id": 15, "name": "WikibaseLib", "url": "https://www.mediawiki.org/wiki/Extension:WikibaseLib", "archived": True, "description": "Provides common Wikibase functionality for Wikibase Repository and Wikibase Client", "latest_version": "Continuous updates", "mediawiki_bundled": False, "wbs_bundled": None, "public_wiki_count": None, "quarterly_download_count": None, "tags": []},
        {"id": 80, "name": "WikibaseManifest", "url": "https://www.mediawiki.org/wiki/Extension:WikibaseManifest", "archived": False, "description": "API provided metadata for structured data repository", "latest_version": "0.0.1 (continuous updates)", "mediawiki_bundled": False, "wbs_bundled": None, "public_wiki_count": None, "quarterly_download_count": None, "tags": []},
        {"id": 16, "name": "WikibaseRepository", "url": "https://www.mediawiki.org/wiki/Extension:Wikibase_Repository", "archived": False, "description": "Structured data repository", "latest_version": "Continuous updates", "mediawiki_bundled": False, "wbs_bundled": None, "public_wiki_count": None, "quarterly_download_count": None, "tags": []},
        {"id": 17, "name": "WikibaseView", "url": "https://www.mediawiki.org/wiki/Extension:WikibaseView", "archived": False, "description": None, "latest_version": None, "mediawiki_bundled": None, "wbs_bundled": None, "public_wiki_count": None, "quarterly_download_count": None, "tags": []},
    ]

    async with AsyncSession(bind=db_session) as session:
        for ext in extensions:
            model = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.EXTENSION,
                software_name=ext["name"],
            )
            model.url = ext["url"]
            model.data_fetched = datetime(2024, 3, 1)
            model.archived = ext["archived"]
            model.description = ext["description"]
            model.latest_version = ext["latest_version"]
            model.mediawiki_bundled = ext["mediawiki_bundled"]
            model.wikibase_suite_bundled = ext["wbs_bundled"]
            model.public_wiki_count = ext["public_wiki_count"]
            model.quarterly_download_count = ext["quarterly_download_count"]
            model.tags = [WikibaseSoftwareTagModel(tag=t) for t in ext["tags"]]
            session.add(model)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.version
async def test_extension_list_query(extension_list):
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
@pytest.mark.parametrize(
    [
        "idx",
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
            ["tag 1"],
        ),
        (
            1,
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
            ["tag 2", "tag 3"],
        ),
        (
            2,
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
            [],
        ),
        (
            3,
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
            [],
        ),
        (
            4,
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
            [],
        ),
        (
            5,
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
            [],
        ),
        (
            6,
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
            [],
        ),
        (
            7,
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
            [],
        ),
        (
            8,
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
            [],
        ),
        (
            10,
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
            [],
        ),
        (
            11,
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
    extension_list,
    idx: int,
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
