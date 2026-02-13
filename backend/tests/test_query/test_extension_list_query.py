"""Test Wikibase List"""

from datetime import datetime, timezone
from typing import Optional
import pytest
from tests.test_schema import test_schema
from tests.test_create_observation.software_version.test_constants import (
    DATA_DIRECTORY,
)
from tests.utils import MockResponse
from fetch_data import update_software_data
from tests.utils import assert_layered_property_value, assert_page_meta, DATETIME_FORMAT
from data import get_async_session
from model.database import WikibaseSoftwareModel
from model.enum import WikibaseSoftwareType
from fetch_data.soup_data.software import (
    fetch_or_create_tags,
)

@pytest.fixture(scope="function")
async def software_data():
    """Setup: Create test software/extension data directly in database"""
    
    async with get_async_session() as async_session:

        fetched_time = datetime(2024, 3, 1, tzinfo=timezone.utc)
        # Babel
        babel = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="Babel",
        )
        babel.url = "https://www.mediawiki.org/wiki/Extension:Babel"
        babel.archived = False
        babel.description = "Adds a parser function to inform other users about language proficiency and categorize users of the same levels and languages."
        babel.data_fetched = fetched_time
        babel.latest_version = "Continuous updates"
        babel.mediawiki_bundled = False
        babel.wikibase_suite_bundled = True
        babel.public_wiki_count = 2416
        babel.quarterly_download_count = 63
        babel.tags = await fetch_or_create_tags(async_session, ["Parser function"])
        async_session.add(babel)
        await async_session.flush()
        
        # Google Analytics Integration
        gai = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="Google Analytics Integration",
        )
        gai.url = "https://www.mediawiki.org/wiki/Extension:Google_Analytics_Integration"
        gai.archived = False
        gai.description = "Automatically inserts Google Universal Analytics (and/or other web analytics) tracking code at the bottom of MediaWiki pages"
        gai.data_fetched = fetched_time
        gai.latest_version = "3.0.1 (2017-10-29)"
        gai.mediawiki_bundled = False
        gai.public_wiki_count = 1302
        gai.tags = await fetch_or_create_tags(async_session, ["Hook", "User activity"])
        async_session.add(gai)
        await async_session.flush()
        
        # LabeledSectionTransclusion
        lst = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="LabeledSectionTransclusion",
        )
        lst.url = "https://www.mediawiki.org/wiki/Extension:Labeled_Section_Transclusion"
        lst.archived = False
        lst.description = "Enables marked sections of text to be transcluded"
        lst.data_fetched = fetched_time
        lst.mediawiki_bundled = False
        lst.public_wiki_count = 6919
        lst.tags = await fetch_or_create_tags(async_session, ["Parser function", "Tag"])
        async_session.add(lst)
        await async_session.flush()
        
        # Miraheze Magic
        mm = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="Miraheze Magic",
        )
        mm.url = "https://www.mediawiki.org/wiki/Extension:MirahezeMagic"
        mm.data_fetched = fetched_time
        mm.tags = await fetch_or_create_tags(async_session, ["Magic", "extensionname"])
        async_session.add(mm)
        await async_session.flush()
        
        # ProofreadPage
        pp = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="ProofreadPage",
        )
        pp.url = "https://www.mediawiki.org/wiki/Extension:Proofread_Page"
        pp.archived = False
        pp.description = "The Proofread Page extension can render a book either as a column of OCR text beside a column of scanned images, or broken into its logical organization (such as chapters or poems) using transclusion."
        pp.data_fetched = fetched_time
        pp.latest_version = "Continuous updates"
        pp.mediawiki_bundled = False
        pp.tags = await fetch_or_create_tags(async_session, ["API", "ContentHandler", "Database", "Page action", "Tag"])
        async_session.add(pp)
        await async_session.flush()
        
        # Scribunto
        scribunto = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="Scribunto",
        )
        scribunto.url = "https://www.mediawiki.org/wiki/Extension:Scribunto"
        scribunto.archived = False
        scribunto.description = "Provides a framework for embedding scripting languages into MediaWiki pages"
        scribunto.data_fetched = fetched_time
        scribunto.latest_version = "Continuous updates"
        scribunto.mediawiki_bundled = True
        scribunto.wikibase_suite_bundled = True
        scribunto.public_wiki_count = 8789
        scribunto.quarterly_download_count = 450
        scribunto.tags = await fetch_or_create_tags(async_session, ["Parser extension"])
        async_session.add(scribunto)
        await async_session.flush()
        
        # UniversalLanguageSelector
        uls = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="UniversalLanguageSelector",
        )
        uls.url = "https://www.mediawiki.org/wiki/Extension:UniversalLanguageSelector"
        uls.archived = False
        uls.description = "Tool that allows users to select a language and configure its support in an easy way."
        uls.data_fetched = fetched_time
        uls.latest_version = "2024-07-16"
        uls.mediawiki_bundled = False
        uls.public_wiki_count = 1237
        uls.quarterly_download_count = 243
        uls.tags = await fetch_or_create_tags(async_session, ["Beta Feature", "Skin"])
        async_session.add(uls)
        await async_session.flush()
        
        # WikibaseClient
        wbc = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="WikibaseClient",
        )
        wbc.url = "https://www.mediawiki.org/wiki/Extension:Wikibase_Client"
        wbc.archived = False
        wbc.description = "Client for structured data repository"
        wbc.data_fetched = fetched_time
        wbc.mediawiki_bundled = False
        wbc.tags = await fetch_or_create_tags(async_session, ["Ajax", "Parser function"])
        async_session.add(wbc)
        await async_session.flush()
        
        # WikibaseLib
        wbl = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="WikibaseLib",
        )
        wbl.url = "https://www.mediawiki.org/wiki/Extension:WikibaseLib"
        wbl.archived = True
        wbl.description = "Provides common Wikibase functionality for Wikibase Repository and Wikibase Client"
        wbl.data_fetched = fetched_time
        wbl.latest_version = "Continuous updates"
        wbl.mediawiki_bundled = False
        wbl.tags = []
        async_session.add(wbl)
        await async_session.flush()
        
        # WikibaseManifest
        wbm = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="WikibaseManifest",
        )
        wbm.url = "https://www.mediawiki.org/wiki/Extension:WikibaseManifest"
        wbm.archived = False
        wbm.description = "API provided metadata for structured data repository"
        wbm.data_fetched = fetched_time
        wbm.latest_version = "0.0.1 (continuous updates)"
        wbm.mediawiki_bundled = False
        wbm.tags = await fetch_or_create_tags(async_session, ["API"])
        async_session.add(wbm)
        await async_session.flush()
        
        # WikibaseRepository
        wbr = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="WikibaseRepository",
        )
        wbr.url = "https://www.mediawiki.org/wiki/Extension:Wikibase_Repository"
        wbr.archived = False
        wbr.description = "Structured data repository"
        wbr.data_fetched = fetched_time
        wbr.latest_version = "Continuous updates"
        wbr.mediawiki_bundled = False
        wbr.tags = await fetch_or_create_tags(async_session, ["API", "Ajax", "ContentHandler"])
        async_session.add(wbr)
        await async_session.flush()
        
        # WikibaseView
        wbv = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="WikibaseView",
        )
        wbv.url = "https://www.mediawiki.org/wiki/Extension:WikibaseView"
        wbv.archived = False
        wbv.data_fetched = fetched_time
        wbv.tags = []
        async_session.add(wbv)
        await async_session.flush()
        
        await async_session.commit()

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
async def test_extension_list_query(software_data):
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
    software_data,
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
