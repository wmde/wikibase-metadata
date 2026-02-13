"""Test Merge Software"""

import pytest

from tests.test_schema import test_schema
from tests.utils import get_mock_context
from data.database_connection import get_async_session
from model.database import WikibaseSoftwareModel
from model.enum import WikibaseSoftwareType


@pytest.fixture(scope="function")
async def test_extension():
    """Setup: Create a test extension in the database"""
    
    async with get_async_session() as async_session:
        extension = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="something"
        )
        extension.id = 3
        async_session.add(extension)
        await async_session.commit()

        return extension.id

BUNDLE_SOFTWARE_MUTATION = """
mutation MyMutation($extensionId: Int!, $bundled: Boolean) {
  setExtensionWbsBundled(extensionId: $extensionId, bundled: $bundled)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="test-set-bundled")
async def test_set_bundled(test_extension):
    """Test Set Extension Bundled"""

    extension_id = test_extension

    result = await test_schema.execute(
        BUNDLE_SOFTWARE_MUTATION,
        variable_values={"extensionId": extension_id},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("setExtensionWbsBundled")
