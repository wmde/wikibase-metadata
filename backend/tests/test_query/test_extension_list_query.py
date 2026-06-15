"""Test Wikibase List"""

from datetime import datetime
import pytest
from tests.test_schema import test_schema
from tests.utils import DATETIME_FORMAT

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

extensions = [
        {
            "name": "Extension 1",
            "url": "https://www.mediawiki.org/wiki/Extension:url_1",
            "archived": False,
            "description": "Description 1",
            "latest_version": "Continuous updates",
            "mediawiki_bundled": False,
            "wbs_bundled": True,
            "public_wiki_count": 2416,
            "quarterly_download_count": 63,
            "tags": ["tag 1"],
        },
        {
            "name": "Extension 2",
            "url": "https://www.mediawiki.org/wiki/Extension:url_2",
            "archived": False,
            "description": "Description 2",
            "latest_version": "3.0.1 (2017-10-29)",
            "mediawiki_bundled": False,
            "wbs_bundled": None,
            "public_wiki_count": 1302,
            "quarterly_download_count": None,
            "tags": ["tag 2", "tag 3"],
        },
        {
            "name": "Extension 3",
            "url": "https://www.mediawiki.org/wiki/Extension:url_3",
            "archived": False,
            "description": "Description 3",
            "latest_version": None,
            "mediawiki_bundled": False,
            "wbs_bundled": None,
            "public_wiki_count": 6919,
            "quarterly_download_count": None,
            "tags": [],
        },
    ]


@pytest.fixture
async def extension_list(db_session): # pylint: disable=unused-argument
    """Create test extensions"""
    from model.database import WikibaseSoftwareModel
    from model.database.wikibase_software.software_tag_model import (
        WikibaseSoftwareTagModel,
    )
    from model.enum import WikibaseSoftwareType
    from sqlalchemy.ext.asyncio import AsyncSession

    

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
    # These assertions are commented out until T420325 is completed, as they currently
    # fail due to DB mutations from other tests
    # assert_page_meta(result.data["extensionList"], 1, 10, 3, 2)
    assert "data" in result.data["extensionList"]
    # assert len(result.data["extensionList"]["data"]) == 10


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.version
async def test_extension_list_query_parameterized(extension_list):
    result = await test_schema.execute(
        EXTENSION_LIST_QUERY, variable_values={"pageNumber": 1, "pageSize": 100}
    )
    assert result.errors is None
    assert result.data is not None
    assert "extensionList" in result.data

    for ext in extensions:
        entry = next(
       (item for item in result.data["extensionList"]['data'] if item["softwareName"] == ext["name"]),
        None,
)       
        assert entry is not None
        assert entry["softwareName"] == ext["name"]
        assert entry["softwareType"] == "EXTENSION"
        assert entry["url"] == ext["url"]
        assert entry["archived"] == ext["archived"]
        assert entry["description"] == ext["description"]
        # assert entry["fetched"] == ext["fetched"].strftime(DATETIME_FORMAT)
        assert entry["latestVersion"] == ext["latest_version"]
        assert entry["mediawikiBundled"] == ext["mediawiki_bundled"]
        assert entry["wikibaseSuiteBundled"] == ext["wbs_bundled"]
        assert entry["publicWikiCount"] == ext["public_wiki_count"]
        assert entry["quarterlyDownloadCount"] == ext["quarterly_download_count"]
        for tag in ext["tags"]:
            assert tag in entry["tags"]
        assert len(entry["tags"]) == len(ext["tags"])
