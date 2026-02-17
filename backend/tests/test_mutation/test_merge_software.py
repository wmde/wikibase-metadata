# pylint: disable=redefined-outer-name
"""Test Merge Software"""

import pytest

from tests.test_schema import test_schema
from tests.utils import get_mock_context
from data.database_connection import get_async_session
from model.enum import WikibaseSoftwareType
from model.database import WikibaseSoftwareModel
from fetch_data.soup_data.software import (
    get_or_create_software_model,
    fetch_or_create_tags,
)


@pytest.fixture(scope="function")
async def test_software():
    """Setup: Create test software extensions in the database"""

    async with get_async_session() as async_session:
        first = await get_or_create_software_model(
            async_session,
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="Miraheze Magic",
        )
        await async_session.flush()

        # Second extension - Babel
        second = await get_or_create_software_model(
            async_session,
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="Babel",
        )
        await async_session.flush()

        # Third extension - with special characters
        third = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="⧼mirahezemagic-extensionname⧽",
        )
        third.tags = await fetch_or_create_tags(
            async_session, ["Magic", "extensionname"]
        )
        async_session.add(third)
        await async_session.commit()

        return {
            "first_id": first.id,
            "second_id": second.id,
            "third_id": third.id,
        }


MERGE_SOFTWARE_MUTATION = """
mutation MyMutation($baseId: Int!, $additionalId: Int!) {
  mergeSoftwareById(baseId: $baseId, additionalId: $additionalId)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_merge_software_by_id_mutation(test_software):
    """Test Add Wikibase"""

    result = await test_schema.execute(
        MERGE_SOFTWARE_MUTATION,
        variable_values={
            "baseId": test_software["first_id"],
            "additionalId": test_software["third_id"],
        },
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("mergeSoftwareById")


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_merge_software_by_id_mutation_fail_same_id(
    test_software,
):  # pylint: disable=unused-argument
    """Test Merge Software by ID - Same IDs"""

    result = await test_schema.execute(
        MERGE_SOFTWARE_MUTATION,
        variable_values={"baseId": 1, "additionalId": 1},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is not None
    assert result.errors[0].message == "Software IDs Must Be Distinct"


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_merge_software_by_id_mutation_fail_not_found(test_software):
    """Test Merge Software by ID - Not Found"""

    result = await test_schema.execute(
        MERGE_SOFTWARE_MUTATION,
        variable_values={"baseId": test_software["first_id"], "additionalId": 999999},
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
        MERGE_SOFTWARE_MUTATION,
        variable_values={"baseId": 1, "additionalId": 4},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is not None
    assert result.errors[0].message == "Cannot Merge Differently-Typed Software"
