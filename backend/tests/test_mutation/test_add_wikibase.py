"""Test Add Wikibase"""

import pytest
from sqlalchemy import select
from model.enum.wikibase_url_type_enum import WikibaseURLType
from model.enum.wikibase_category_enum import WikibaseCategory
from model.enum.wikibase_type_enum import WikibaseType
from model.database.wikibase_model import WikibaseModel
from data.database_connection import get_async_session
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value

ADD_WIKIBASE_QUERY = """
mutation MyMutation($wikibaseInput: WikibaseInput!) {
  addWikibase(wikibaseInput: $wikibaseInput) {
    id
  }
}"""


async def get_wikibase_by_id(wikibase_id: int) -> WikibaseModel:
    """Get Wikibase from Database by ID"""
    async with get_async_session() as session:
        return await session.scalar(
            select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
        )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="add-wikibase", depends=["add-test-categories"], scope="session"
)
async def test_add_wikibase_mutation():
    """Test Add Wikibase"""

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Mock Wikibase",
                "wikibaseType": "SUITE",
                "description": "Mock wikibase for testing this codebase",
                "organization": "Wikibase Mockery International",
                "country": "Germany",
                "region": "Europe",
                "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                "urls": {
                    "baseUrl": "https://example.com/",
                    "articlePath": "/wiki",
                    # "scriptPath": "/w",  # will be set in add-wikibase-script-path test
                    "sparqlEndpointUrl": "https://query.example.com/sparql-wrong",
                    "sparqlFrontendUrl": "https://query.example.com",
                },
            }
        },
    )

    assert result.errors is None
    assert result.data is not None

    wikibase_id = int(result.data["addWikibase"]["id"])
    wikibase = await get_wikibase_by_id(wikibase_id)

    assert wikibase.wikibase_name == "Mock Wikibase"
    assert wikibase.wikibase_type == WikibaseType.SUITE
    assert wikibase.description == "Mock wikibase for testing this codebase"
    assert wikibase.organization == "Wikibase Mockery International"
    assert wikibase.country == "Germany"
    assert wikibase.region == "Europe"
    assert (
        wikibase.category.category
        == WikibaseCategory.EXPERIMENTAL_AND_PROTOTYPE_PROJECTS
    )
    assert wikibase.url.url_type == WikibaseURLType.BASE_URL
    assert wikibase.url.url == "https://example.com/"

    # Set wikibase_type to None, as other tests require this database entry to be peristed
    # without a wikibase_type
    async with get_async_session() as session:
        wikibase_to_update = await session.scalar(
            select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
        )
        wikibase_to_update.wikibase_type = None
        await session.commit()


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="add-wikibase-ii", depends=["add-wikibase"])
async def test_add_wikibase_ii_mutation():
    """Test Add Another Wikibase"""

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Mock Wikibase II",
                "description": "Another Mock wikibase for testing this codebase",
                "organization": "Wikibase Mockery International",
                "country": "Germany",
                "region": "Europe",
                "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                "urls": {
                    "baseUrl": "https://mock-wikibase.com/",
                    "articlePath": "wiki",
                },
            }
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert_layered_property_value(result.data, ["addWikibase", "id"], "2")
