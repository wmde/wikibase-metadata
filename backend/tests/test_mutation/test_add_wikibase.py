# pylint: disable=redefined-outer-name
"""Test Add Wikibase"""

import pytest
from sqlalchemy import select
from model.database.wikibase_category_model import WikibaseCategoryModel
from model.enum import WikibaseCategory, WikibaseType, WikibaseURLType
from model.database import WikibaseModel
from data.database_connection import get_async_session
from tests.test_schema import test_schema

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


@pytest.fixture
async def wikibase_categories(db_session):  # pylint: disable=unused-argument
    """Create wikibase categories"""
    async with get_async_session() as async_session:
        async_session.add(
            WikibaseCategoryModel(
                category=WikibaseCategory.EXPERIMENTAL_AND_PROTOTYPE_PROJECTS
            )
        )

        await async_session.commit()


@pytest.mark.asyncio
async def test_add_wikibase_mutation(wikibase_categories): # pylint: disable=redefined-outer-name, unused-argument
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
                    "sparqlEndpointUrl": "https://query.example.com/sparql-wrong",
                    "sparqlFrontendUrl": "https://query.example.com",
                },
                "reuse": True,
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
    assert wikibase.url.url == "https://example.com"


@pytest.mark.asyncio
async def test_does_not_allow_multiple_wikibases_with_same_base_url(
    db_session,
):  # pylint: disable=unused-argument
    """Test Can't Add Wikibase with existing base URL"""

    base_url = "https://example-wikibase.com"

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Wikibase Add",
                "description": "",
                "organization": "",
                "country": "",
                "region": "",
                "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                "urls": {
                    "baseUrl": base_url,
                    "articlePath": "wiki",
                },
            }
        },
    )

    assert result.errors is None
    assert result.data is not None

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Wikibase Add 2",
                "description": "",
                "organization": "",
                "country": "",
                "region": "",
                "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                "urls": {
                    "baseUrl": base_url,
                    "articlePath": "wiki",
                },
            }
        },
    )

    assert len(result.errors) == 1
    assert result.errors[0].message == f"URL {base_url} already exists"


@pytest.mark.asyncio
async def test_does_not_allow_multiple_wikibases_with_same_sparql_url(
    db_session,
):  # pylint: disable=unused-argument
    """Test Can't Add Wikibase with existing sqarql URL"""

    url_types = ["sparqlEndpointUrl", "sparqlFrontendUrl"]

    for i, url_type in enumerate(url_types):
        url = f"https://example.com/sparql{i}"
        result = await test_schema.execute(
            ADD_WIKIBASE_QUERY,
            variable_values={
                "wikibaseInput": {
                    "wikibaseName": f"Wikibase {i} A",
                    "description": "",
                    "organization": "",
                    "country": "",
                    "region": "",
                    "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                    "urls": {
                        "baseUrl": f"https://example{i}.com",
                        f"{url_type}": f"{url}",
                        "articlePath": "wiki",
                    },
                }
            },
        )

        assert result.errors is None
        assert result.data is not None

        result = await test_schema.execute(
            ADD_WIKIBASE_QUERY,
            variable_values={
                "wikibaseInput": {
                    "wikibaseName": f"Wikibase {i} B",
                    "description": "",
                    "organization": "",
                    "country": "",
                    "region": "",
                    "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                    "urls": {
                        "baseUrl": f"https://example2{i}.com",
                        f"{url_type}": f"{url}",
                        "articlePath": "wiki",
                    },
                }
            },
        )

        assert len(result.errors) == 1
        assert result.errors[0].message == f"URL {url} already exists"


@pytest.mark.asyncio
async def test_normalizes_urls(db_session):  # pylint: disable=unused-argument
    """Test Normalizes the base URL when adding a Wikibase"""

    base_url = "example-1234.com"

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Mock Wikibase Normalize",
                "description": "Mock wikibase for testing this codebase",
                "organization": "Wikibase Mockery International",
                "country": "Germany",
                "region": "Europe",
                "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                "urls": {
                    "baseUrl": f"http://{base_url}",
                    "articlePath": "/wiki",
                },
            }
        },
    )

    assert result.errors is None
    assert result.data is not None

    url_variations = [
        f"https://{base_url}",
        f"http://{base_url}/",
        f"https://{base_url}/",
    ]

    for i, url in enumerate(url_variations):
        result = await test_schema.execute(
            ADD_WIKIBASE_QUERY,
            variable_values={
                "wikibaseInput": {
                    "wikibaseName": f"Wikibase {i}",
                    "description": "",
                    "organization": "",
                    "country": "",
                    "region": "",
                    "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                    "urls": {
                        "baseUrl": url,
                        "articlePath": "wiki",
                    },
                }
            },
        )

        assert len(result.errors) == 1
        assert result.errors[0].message == f"URL https://{base_url} already exists"


@pytest.mark.asyncio
async def test_marks_localhost_urls_as_test(
    db_session,
):  # pylint: disable=unused-argument
    """Test marks all Wikibases with a URL containing 'localhost' as test"""

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Localhost Wikibase",
                "description": "Mock wikibase for testing this codebase",
                "organization": "Wikibase Mockery International",
                "country": "Germany",
                "region": "Europe",
                "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                "urls": {
                    "baseUrl": "http://localhost:8000",
                    "articlePath": "/wiki",
                },
            }
        },
    )

    assert result.errors is None
    wikibase_id = int(result.data["addWikibase"]["id"])

    async with get_async_session() as session:
        db_result = await session.execute(
            select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
        )
        wikibase = db_result.scalar_one()
        assert wikibase.test is True
