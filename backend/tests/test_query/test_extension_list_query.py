"""Test Wikibase List"""

from datetime import datetime, timezone

import pytest

from data import get_async_session
from model.database import WikibaseSoftwareModel, WikibaseSoftwareTagModel
from model.enum import WikibaseSoftwareType
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
      wikibaseSuiteBundled
      publicWikiCount
      quarterlyDownloadCount
      tags
    }
  }
}"""


@pytest.fixture
async def extension_software_data(db_session):  # pylint: disable=unused-argument
    """Create a small set of extensions for list query tests"""
    async with get_async_session() as session:
        extensions = [
            {
                "name": "TestExtensionA",
                "url": "https://www.mediawiki.org/wiki/Extension:TestExtensionA",
                "archived": False,
                "description": "A test extension",
                "latest_version": "1.0.0",
                "mediawiki_bundled": True,
                "wbs_bundled": True,
                "public_wiki_count": 100,
                "quarterly_download_count": 50,
                "tags": ["API", "Hook"],
            },
            {
                "name": "TestExtensionB",
                "url": "https://www.mediawiki.org/wiki/Extension:TestExtensionB",
                "archived": True,
                "description": None,
                "latest_version": None,
                "mediawiki_bundled": False,
                "wbs_bundled": None,
                "public_wiki_count": None,
                "quarterly_download_count": None,
                "tags": [],
            },
        ]

        software_ids = []
        for ext in extensions:
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.EXTENSION,
                software_name=ext["name"],
            )
            software.url = ext["url"]
            software.data_fetched = datetime(2024, 3, 1, tzinfo=timezone.utc)
            software.archived = ext["archived"]
            software.description = ext["description"]
            software.latest_version = ext["latest_version"]
            software.mediawiki_bundled = ext["mediawiki_bundled"]
            software.wikibase_suite_bundled = ext["wbs_bundled"]
            software.public_wiki_count = ext["public_wiki_count"]
            software.quarterly_download_count = ext["quarterly_download_count"]
            software.tags = [WikibaseSoftwareTagModel(tag=t) for t in ext["tags"]]
            session.add(software)
            await session.flush()
            await session.refresh(software)
            software_ids.append(str(software.id))

    return software_ids


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.version
async def test_extension_list_query(
    extension_software_data,
):  # pylint: disable=unused-argument, redefined-outer-name
    """Test Extension List"""

    result = await test_schema.execute(
        EXTENSION_LIST_QUERY, variable_values={"pageNumber": 1, "pageSize": 10}
    )

    assert result.errors is None
    assert result.data is not None
    assert "extensionList" in result.data
    assert_page_meta(result.data["extensionList"], 1, 10, 2, 1)
    assert "data" in result.data["extensionList"]
    assert len(result.data["extensionList"]["data"]) == 2


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.version
@pytest.mark.parametrize(
    [
        "idx",
        "expected_name",
        "expected_archived",
        "expected_mediawiki_bundled",
        "expected_wbs_bundled",
        "expected_tags",
    ],
    [
        (0, "TestExtensionA", False, True, True, ["API", "Hook"]),
        (1, "TestExtensionB", True, False, None, []),
    ],
)
async def test_extension_list_query_parameterized(
    extension_software_data,
    idx,
    expected_name,
    expected_archived,
    expected_mediawiki_bundled,
    expected_wbs_bundled,
    expected_tags,
):  # pylint: disable=unused-argument, redefined-outer-name
    """Test Extension List"""

    result = await test_schema.execute(
        EXTENSION_LIST_QUERY, variable_values={"pageNumber": 1, "pageSize": 100}
    )

    assert result.errors is None
    assert result.data is not None
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "id"], extension_software_data[idx]
    )
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "softwareName"], expected_name
    )
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "softwareType"], "EXTENSION"
    )
    assert_layered_property_value(
        result.data, ["extensionList", "data", idx, "archived"], expected_archived
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
        result.data, ["extensionList", "data", idx, "tags"], expected_tags
    )
