"""Test Merge Software"""

import pytest

from backend.data.database_connection import get_async_session
from backend.fetch_data.soup_data.software.get_software_model import (
    get_or_create_software_model,
)
from backend.fetch_data.soup_data.software.get_update_software_data import (
    fetch_or_create_tags,
)
from backend.model.enum.wikibase_software_type_enum import WikibaseSoftwareType
from backend.tests.utils.assert_property_value import (
    assert_layered_property_count,
    assert_layered_property_value,
)
from tests.test_schema import test_schema
from tests.utils import get_mock_context


LIST_SOFTWARE_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!) {
  extensionList(pageNumber: $pageNumber, pageSize: $pageSize) {
    meta {
      totalCount
    }
    data {
      id
      softwareType
      softwareName
      url
      tags
    }
  }
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="add-test-software")
async def test_add_software():
    """Test Add Software"""

    before_result = await test_schema.execute(
        LIST_SOFTWARE_QUERY,
        variable_values={"pageNumber": 1, "pageSize": 3},
        context_value=get_mock_context("test-auth-token"),
    )
    assert before_result.errors is None
    assert before_result.data is not None
    assert_layered_property_value(
        before_result.data, ["extensionList", "meta", "totalCount"], 0
    )

    async with get_async_session() as async_session:

        first = await get_or_create_software_model(
            async_session,
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="Miraheze Magic",
        )
        first.url = "https://www.mediawiki.org/wiki/Extension:MirahezeMagic"
        first.tags = await fetch_or_create_tags(async_session, ["Magic"])
        await async_session.flush()

        await get_or_create_software_model(
            async_session,
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="Babel",
        )
        await async_session.flush()

        third = await get_or_create_software_model(
            async_session,
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="⧼mirahezemagic-extensionname⧽",
        )
        third.tags = await fetch_or_create_tags(
            async_session, ["Magic", "extensionname"]
        )
        await async_session.flush()

        await async_session.commit()

    after_result = await test_schema.execute(
        LIST_SOFTWARE_QUERY,
        variable_values={"pageNumber": 1, "pageSize": 3},
        context_value=get_mock_context("test-auth-token"),
    )
    assert after_result.errors is None
    assert after_result.data is not None
    assert_layered_property_value(
        after_result.data, ["extensionList", "meta", "totalCount"], 3
    )
    assert_layered_property_count(after_result.data, ["extensionList", "data"], 3)

    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 0, "id"], "1"
    )
    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 0, "softwareType"], "EXTENSION"
    )
    assert_layered_property_value(
        after_result.data,
        ["extensionList", "data", 0, "softwareName"],
        "Miraheze Magic",
    )
    assert_layered_property_value(
        after_result.data,
        ["extensionList", "data", 0, "url"],
        "https://www.mediawiki.org/wiki/Extension:MirahezeMagic",
    )
    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 0, "tags"], ["Magic"]
    )

    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 1, "id"], "2"
    )
    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 1, "softwareType"], "EXTENSION"
    )
    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 1, "softwareName"], "Babel"
    )
    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 1, "url"], None
    )
    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 1, "tags"], []
    )

    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 2, "id"], "3"
    )
    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 2, "softwareType"], "EXTENSION"
    )
    assert_layered_property_value(
        after_result.data,
        ["extensionList", "data", 2, "softwareName"],
        "⧼mirahezemagic-extensionname⧽",
    )
    assert_layered_property_value(
        after_result.data, ["extensionList", "data", 2, "url"], None
    )
    assert_layered_property_value(
        after_result.data,
        ["extensionList", "data", 2, "tags"],
        ["Magic", "extensionname"],
    )
