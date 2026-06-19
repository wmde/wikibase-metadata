"""Test Merge Software"""

import pytest

from data.database_connection import get_async_session
from model.database.wikibase_software.software_model import WikibaseSoftwareModel
from model.enum.wikibase_software_type_enum import WikibaseSoftwareType
from tests.test_schema import test_schema
from tests.utils import get_mock_context

BUNDLE_SOFTWARE_MUTATION = """
mutation MyMutation($extensionId: Int!, $bundled: Boolean) {
  setExtensionWbsBundled(extensionId: $extensionId, bundled: $bundled)
}"""


@pytest.fixture
async def extension_software(db_session):
    """Create a test extension"""
    async with get_async_session() as session:
        software = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="Test Extension",
        )
        session.add(software)
        await session.flush()
        await session.refresh(software)
        return software


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="test-set-bundled")
async def test_set_bundled(extension_software):
    """Test Set Extension Bundled"""

    result = await test_schema.execute(
        BUNDLE_SOFTWARE_MUTATION,
        variable_values={"extensionId": extension_software.id},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("setExtensionWbsBundled")
