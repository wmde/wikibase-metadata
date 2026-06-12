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
    from model.database.wikibase_software.software_tag_model import (
        WikibaseSoftwareTagModel,
    )
    from model.enum import WikibaseSoftwareType
    from sqlalchemy.ext.asyncio import AsyncSession

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
            "Extension 1",
            "url_1",
            False,
            # pylint: disable-next=line-too-long
            "Description 1",
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
            "Extension 2",
            "url_2",
            False,
            # pylint: disable-next=line-too-long
            "Description 2",
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
            "Extension 3",
            "url_3",
            False,
            "Description 3",
            datetime(2024, 3, 1),
            None,
            False,
            None,
            6919,
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
    assert_page_meta(result.data["extensionList"], 1, 100, 3, 1)
    assert "data" in result.data["extensionList"]
    assert len(result.data["extensionList"]["data"]) == 3
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
