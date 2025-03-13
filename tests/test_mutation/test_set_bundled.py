"""Test Merge Software"""

import pytest

from tests.test_schema import test_schema


BUNDLE_SOFTWARE_QUERY = """
mutation MyMutation($extensionId: Int!, $bundled: Boolean) {
  setExtensionWbsBundled(extensionId: $extensionId, bundled: $bundled)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="test-set-bundled")
async def test_set_bundled():
    """Test Set Extension Bundled"""

    result = await test_schema.execute(
        BUNDLE_SOFTWARE_QUERY, variable_values={"extensionId": 2}
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("setExtensionWbsBundled")
