"""Test Merge Software"""

import pytest

from tests.test_schema import test_schema


MERGE_SOFTWARE_QUERY = """
mutation MyMutation($baseId: Int!, $additionalId: Int!) {
  mergeSoftwareById(baseId: $baseId, additionalId: $additionalId)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="merge-software-by-id")
async def test_merge_software_by_id_mutation():
    """Test Add Wikibase"""

    result = await test_schema.execute(
        MERGE_SOFTWARE_QUERY, variable_values={"baseId": 1, "additionalId": 3}
    )
    assert result.data.get("mergeSoftwareById")
