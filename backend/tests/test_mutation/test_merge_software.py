"""Test Merge Software"""

import pytest

from model.database.wikibase_software.software_model import WikibaseSoftwareModel
from model.enum.wikibase_software_type_enum import WikibaseSoftwareType
from data.database_connection import get_async_session
from tests.test_schema import test_schema
from tests.utils import get_mock_context

MERGE_SOFTWARE_MUTATION = """
mutation MyMutation($baseId: Int!, $additionalId: Int!) {
  mergeSoftwareById(baseId: $baseId, additionalId: $additionalId)
}"""


@pytest.fixture
async def wikibase_software(db_session):  # pylint: disable=unused-argument
    """Create two software entries with different types"""
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
async def test_merge_software_by_id_mutation():
    """Test Add Wikibase"""

    result = await test_schema.execute(
        MERGE_SOFTWARE_MUTATION,
        variable_values={"baseId": 1, "additionalId": 3},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("mergeSoftwareById")


@pytest.mark.asyncio
async def test_merge_software_by_id_mutation_fail_same_id(
    wikibase_software,
):  # pylint: disable=redefined-outer-name
    """Test Merge Software by ID - Same IDs"""

    result = await test_schema.execute(
        MERGE_SOFTWARE_MUTATION,
        variable_values={
            "baseId": wikibase_software.id,
            "additionalId": wikibase_software.id,
        },
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is not None
    assert result.errors[0].message == "Software IDs Must Be Distinct"


async def test_merge_software_by_id_mutation_fail_not_found(
    wikibase_software,
):  # pylint: disable=redefined-outer-name
    """Test Merge Software by ID - Not Found"""

    result = await test_schema.execute(
        MERGE_SOFTWARE_MUTATION,
        variable_values={"baseId": wikibase_software.id, "additionalId": 1000000},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is not None
    assert result.errors[0].message == "1 Record Found, 2 Needed to Merge"


@pytest.fixture
async def two_software_different_types(db_session):  # pylint: disable=unused-argument
    """Create two software entries with different types"""
    async with get_async_session() as session:
        software1 = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="Test Extension",
        )
        software2 = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.SKIN,
            software_name="Test Skin",
        )
        session.add(software1)
        session.add(software2)
        await session.flush()
        await session.refresh(software1)
        await session.refresh(software2)
        return software1.id, software2.id


@pytest.mark.asyncio
async def test_merge_software_by_id_mutation_fail_different_types(
    two_software_different_types,
):  # pylint: disable=redefined-outer-name
    """Test Add Wikibase"""

    base_id, additional_id = two_software_different_types
    result = await test_schema.execute(
        MERGE_SOFTWARE_MUTATION,
        variable_values={"baseId": base_id, "additionalId": additional_id},
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is not None
    assert result.errors[0].message == "Cannot Merge Differently-Typed Software"
