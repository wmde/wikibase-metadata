"""Test Merge Software"""

import pytest

from tests.test_schema import test_schema
from tests.utils import get_mock_context


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
        MERGE_SOFTWARE_QUERY,
        variable_values={"baseId": 1, "additionalId": 3},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("mergeSoftwareById")


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="merge-software-by-id-fail-same-id")
async def test_merge_software_by_id_mutation_fail_same_id():
    """Test Merge Software by ID - Same IDs"""

    result = await test_schema.execute(
        MERGE_SOFTWARE_QUERY,
        variable_values={"baseId": 1, "additionalId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is not None
    assert result.errors[0].message == "Software IDs Must Be Distinct"


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="merge-software-by-id-fail-not-found")
async def test_merge_software_by_id_mutation_fail_not_found():
    """Test Merge Software by ID - Not Found"""

    result = await test_schema.execute(
        MERGE_SOFTWARE_QUERY,
        variable_values={"baseId": 1, "additionalId": 1000000},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is not None
    assert result.errors[0].message == "1 Record Found, 2 Needed to Merge"


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    depends=["software-version-success"],
    name="merge-software-by-id-fail-different-types",
    scope="session",
)
async def test_merge_software_by_id_mutation_fail_different_types():
    """Test Add Wikibase"""

    result = await test_schema.execute(
        MERGE_SOFTWARE_QUERY,
        variable_values={"baseId": 1, "additionalId": 4},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is not None
    assert result.errors[0].message == "Cannot Merge Differently-Typed Software"
