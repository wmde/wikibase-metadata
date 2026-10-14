# pylint: disable=redefined-outer-name
"""Test Add Wikibase"""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import WikibaseCategoryModel, WikibaseModel, WikibaseURLModel
from model.enum import WikibaseCategory, WikibaseType, WikibaseURLType
from tests.test_schema import test_schema

ADD_WIKIBASE_QUERY = """
mutation MyMutation($wikibaseInput: WikibaseInput!) {
  addWikibase(wikibaseInput: $wikibaseInput) {
    id
  }
}"""


@pytest.fixture
async def wikibase_categories(db_session):
    """Create wikibase categories"""
    async with AsyncSession(bind=db_session) as async_session:
        async_session.add(
            WikibaseCategoryModel(
                category=WikibaseCategory.EXPERIMENTAL_AND_PROTOTYPE_PROJECTS
            )
        )

        await async_session.commit()


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_add_wikibase_mutation(
    db_session, wikibase_categories
):  # pylint: disable=redefined-outer-name, unused-argument
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

    assert result.data is not None

    wikibase_id = int(result.data["addWikibase"]["id"])
    async with AsyncSession(bind=db_session) as session:
        wikibase = await session.scalar(
            select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
        )

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
async def test_recreates_wikibase_if_base_url_already_exists(
    db_session, wikibase_categories
):  # pylint: disable=unused-argument
    """Test recreates Wikibase if base URL already exists"""

    base_url = "https://example-wikibase.com"

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Example Wikibase 1",
                "urls": {
                    "baseUrl": base_url,
                    "articlePath": "wiki",
                },
            }
        },
    )

    assert result.errors is None
    original_id = int(result.data["addWikibase"]["id"])

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Example Wikibase 2",
                "urls": {
                    "baseUrl": base_url,
                    "articlePath": "wiki",
                },
            }
        },
    )

    assert result.errors is None
    assert result.data is not None

    new_id = int(result.data["addWikibase"]["id"])
    assert new_id != original_id

    async with AsyncSession(bind=db_session) as session:
        old_wikibase = await session.get(WikibaseModel, original_id)
        new_wikibase = await session.get(WikibaseModel, new_id)

        assert old_wikibase is None
        assert new_wikibase is not None
        assert new_wikibase.wikibase_name == "Example Wikibase 2"


@pytest.mark.asyncio
async def test_recreates_wikibase_if_sparql_url_already_exists(
    db_session, wikibase_categories
):  # pylint: disable=unused-argument
    """Test recreates Wikibase if a SPARQL URL already exists"""

    url_types = ["sparqlEndpointUrl", "sparqlFrontendUrl"]

    for i, url_type in enumerate(url_types):
        url = f"https://example.com/sparql{i}"

        result = await test_schema.execute(
            ADD_WIKIBASE_QUERY,
            variable_values={
                "wikibaseInput": {
                    "wikibaseName": f"Wikibase {i} A",
                    "urls": {
                        "baseUrl": f"https://example{i}.com",
                        url_type: url,
                    },
                }
            },
        )

        assert result.errors is None
        original_id = int(result.data["addWikibase"]["id"])

        result = await test_schema.execute(
            ADD_WIKIBASE_QUERY,
            variable_values={
                "wikibaseInput": {
                    "wikibaseName": f"Wikibase {i} B",
                    "urls": {
                        "baseUrl": f"https://example2{i}.com",
                        url_type: url,
                    },
                }
            },
        )

        assert result.errors is None
        assert result.data is not None

        new_id = int(result.data["addWikibase"]["id"])
        assert new_id != original_id

        async with AsyncSession(bind=db_session) as session:
            old_wikibase = await session.get(WikibaseModel, original_id)
            new_wikibase = await session.get(WikibaseModel, new_id)

            assert old_wikibase is None
            assert new_wikibase is not None
            assert new_wikibase.wikibase_name == f"Wikibase {i} B"

            matching_wikibases = (
                (
                    await session.scalars(
                        select(WikibaseModel)
                        .join(
                            WikibaseURLModel,
                            WikibaseURLModel.wikibase_id == WikibaseModel.id,
                        )
                        .where(WikibaseURLModel.url == url)
                    )
                )
                .unique()
                .all()
            )

            assert len(matching_wikibases) == 1
            assert matching_wikibases[0].id == new_id


@pytest.mark.asyncio
async def test_deletes_all_wikibases_with_matching_urls(
    db_session, wikibase_categories
):  # pylint: disable=unused-argument
    """Test deletes all Wikibases with matching URLs before creating a new one"""

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Wikibase A",
                "urls": {
                    "baseUrl": "https://base-1.com",
                    "sparqlEndpointUrl": "http://sparql-1.com",
                },
            }
        },
    )

    assert result.errors is None
    wikibase_a_id = int(result.data["addWikibase"]["id"])

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Wikibase B",
                "urls": {
                    "baseUrl": "https://base-2.com",
                    "sparqlEndpointUrl": "http://sparql-2.com",
                },
            }
        },
    )

    assert result.errors is None
    wikibase_b_id = int(result.data["addWikibase"]["id"])

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Wikibase C",
                "urls": {
                    "baseUrl": "https://base-1.com",
                    "sparqlEndpointUrl": "http://sparql-2.com",
                },
            }
        },
    )

    assert result.errors is None
    assert result.data is not None

    wikibase_c_id = int(result.data["addWikibase"]["id"])

    assert wikibase_c_id not in (wikibase_a_id, wikibase_b_id)

    async with AsyncSession(bind=db_session) as session:
        assert await session.get(WikibaseModel, wikibase_a_id) is None
        assert await session.get(WikibaseModel, wikibase_b_id) is None

        wikibase_c = await session.get(WikibaseModel, wikibase_c_id)
        assert wikibase_c is not None
        assert wikibase_c.wikibase_name == "Wikibase C"

        remaining_wikibases = (await session.scalars(select(WikibaseModel))).all()

        assert len(remaining_wikibases) == 1
        assert remaining_wikibases[0].id == wikibase_c_id


@pytest.mark.asyncio
async def test_normalizes_urls(
    db_session, wikibase_categories
):  # pylint: disable=unused-argument, redefined-outer-name
    """Test normalizes URLs and recreates Wikibases on collision"""

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

    previous_id = int(result.data["addWikibase"]["id"])

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

        assert result.errors is None
        assert result.data is not None

        new_id = int(result.data["addWikibase"]["id"])
        assert new_id != previous_id

        async with AsyncSession(bind=db_session) as session:
            assert await session.get(WikibaseModel, previous_id) is None

            matching_wikibases = (
                (
                    await session.scalars(
                        select(WikibaseModel)
                        .join(
                            WikibaseURLModel,
                            WikibaseURLModel.wikibase_id == WikibaseModel.id,
                        )
                        .where(WikibaseURLModel.url == f"https://{base_url}")
                    )
                )
                .unique()
                .all()
            )

            assert len(matching_wikibases) == 1
            assert matching_wikibases[0].id == new_id

        previous_id = new_id


@pytest.mark.asyncio
async def test_marks_localhost_urls_as_test(
    db_session, wikibase_categories
):  # pylint: disable=unused-argument, redefined-outer-name
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

    async with AsyncSession(bind=db_session) as session:
        db_result = await session.execute(
            select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
        )
        wikibase = db_result.scalar_one()
        assert wikibase.test is True
        assert wikibase_id == int(result.data["addWikibase"]["id"])
