# pylint: disable=redefined-outer-name
"""Test Add Wikibase"""

import pytest
from sqlalchemy import func, select
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


async def execute_add_wikibase(name: str, urls: dict):
    """Run the addWikibase mutation with a name and URLs"""

    return await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={"wikibaseInput": {"wikibaseName": name, "urls": urls}},
    )


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
async def test_updates_wikibase_if_base_url_already_exists(
    db_session, wikibase_categories
):  # pylint: disable=unused-argument
    """Test updates the existing Wikibase if the base URL already exists"""

    base_url = "https://example-wikibase.com"

    result = await execute_add_wikibase(
        "Example Wikibase 1", {"baseUrl": base_url, "articlePath": "wiki"}
    )

    assert result.errors is None
    original_id = int(result.data["addWikibase"]["id"])

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Example Wikibase 2",
                "description": "Updated description",
                "urls": {
                    "baseUrl": base_url,
                    "articlePath": "wiki",
                },
            }
        },
    )

    assert result.errors is None
    assert result.data is not None

    assert int(result.data["addWikibase"]["id"]) == original_id

    async with AsyncSession(bind=db_session) as session:
        wikibases = (await session.scalars(select(WikibaseModel))).all()
        assert len(wikibases) == 1

        wikibase = await session.get(WikibaseModel, original_id)
        assert wikibase is not None
        assert wikibase.wikibase_name == "Example Wikibase 2"
        assert wikibase.description == "Updated description"
        assert wikibase.url.url == base_url


@pytest.mark.asyncio
async def test_updates_wikibase_if_sparql_url_already_exists(
    db_session, wikibase_categories
):  # pylint: disable=unused-argument
    """Test updates the existing Wikibase if only a SPARQL URL matches"""

    url_types = ["sparqlEndpointUrl", "sparqlFrontendUrl"]

    for i, url_type in enumerate(url_types):
        url = f"https://example.com/sparql{i}"
        old_base_url = f"https://example{i}.com"
        new_base_url = f"https://example2{i}.com"

        result = await execute_add_wikibase(
            f"Wikibase {i} A", {"baseUrl": old_base_url, url_type: url}
        )

        assert result.errors is None
        original_id = int(result.data["addWikibase"]["id"])

        result = await execute_add_wikibase(
            f"Wikibase {i} B", {"baseUrl": new_base_url, url_type: url}
        )

        assert result.errors is None
        assert result.data is not None

        assert int(result.data["addWikibase"]["id"]) == original_id

        async with AsyncSession(bind=db_session) as session:
            wikibase = await session.get(WikibaseModel, original_id)

            assert wikibase is not None
            assert wikibase.wikibase_name == f"Wikibase {i} B"
            assert wikibase.url.url == new_base_url

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
            assert matching_wikibases[0].id == original_id

            old_base_url_count = await session.scalar(
                # pylint: disable-next=not-callable
                select(func.count()).where(WikibaseURLModel.url == old_base_url)
            )
            assert old_base_url_count == 0


@pytest.mark.asyncio
async def test_keeps_base_url_match_and_deletes_sparql_match(
    db_session, wikibase_categories
):  # pylint: disable=unused-argument
    """Test that if 2 different Wikibases match on base URL and SPARQL URL, the Wikibase
    matching the base URL is updated and the SPARQL-matching Wikibase is deleted.
    """

    result = await execute_add_wikibase(
        "Wikibase A",
        {"baseUrl": "https://base-a.com", "sparqlEndpointUrl": "https://sparql-a.com"},
    )

    assert result.errors is None
    wikibase_a_id = int(result.data["addWikibase"]["id"])

    result = await execute_add_wikibase(
        "Wikibase B",
        {"baseUrl": "https://base-b.com", "sparqlEndpointUrl": "https://sparql-b.com"},
    )

    assert result.errors is None
    wikibase_b_id = int(result.data["addWikibase"]["id"])

    result = await execute_add_wikibase(
        "Wikibase C",
        {"baseUrl": "https://base-a.com", "sparqlEndpointUrl": "https://sparql-b.com"},
    )

    assert result.errors is None
    assert result.data is not None

    # A is kept (and updated), B is deleted, no new Wikibase is created
    assert int(result.data["addWikibase"]["id"]) == wikibase_a_id

    async with AsyncSession(bind=db_session) as session:
        assert await session.get(WikibaseModel, wikibase_b_id) is None

        wikibase_a = await session.get(WikibaseModel, wikibase_a_id)
        assert wikibase_a is not None
        assert wikibase_a.wikibase_name == "Wikibase C"
        assert wikibase_a.url.url == "https://base-a.com"

        remaining_wikibases = (await session.scalars(select(WikibaseModel))).all()
        assert len(remaining_wikibases) == 1
        assert remaining_wikibases[0].id == wikibase_a_id

        # the SPARQL URL formerly owned by B now belongs to A
        sparql_url = await session.scalar(
            select(WikibaseURLModel).where(
                WikibaseURLModel.url == "https://sparql-b.com"
            )
        )
        assert sparql_url is not None
        assert sparql_url.wikibase_id == wikibase_a_id

        old_sparql_count = await session.scalar(
            # pylint: disable-next=not-callable
            select(func.count()).where(WikibaseURLModel.url == "https://sparql-a.com")
        )
        assert old_sparql_count == 0


@pytest.mark.asyncio
async def test_errors_when_multiple_matches_but_none_share_base_url(
    db_session, wikibase_categories
):  # pylint: disable=unused-argument
    """Test errors and changes nothing if matches exist but none owns the base URL"""

    result = await execute_add_wikibase(
        "Wikibase A",
        {"baseUrl": "https://base-a.com", "sparqlEndpointUrl": "https://sparql-a.com"},
    )
    assert result.errors is None
    wikibase_a_id = int(result.data["addWikibase"]["id"])

    result = await execute_add_wikibase(
        "Wikibase B",
        {
            "baseUrl": "https://base-b.com",
            "sparqlFrontendUrl": "https://frontend-b.com",
        },
    )
    assert result.errors is None
    wikibase_b_id = int(result.data["addWikibase"]["id"])

    # new base URL, but the SPARQL URLs match A and B respectively
    result = await execute_add_wikibase(
        "Wikibase C",
        {
            "baseUrl": "https://base-c.com",
            "sparqlEndpointUrl": "https://sparql-a.com",
            "sparqlFrontendUrl": "https://frontend-b.com",
        },
    )

    assert result.errors is not None

    async with AsyncSession(bind=db_session) as session:
        assert await session.get(WikibaseModel, wikibase_a_id) is not None
        assert await session.get(WikibaseModel, wikibase_b_id) is not None

        remaining_wikibases = (await session.scalars(select(WikibaseModel))).all()
        assert len(remaining_wikibases) == 2


@pytest.mark.asyncio
async def test_normalizes_urls(
    db_session, wikibase_categories
):  # pylint: disable=unused-argument, redefined-outer-name
    """Test normalizes URLs and updates the same Wikibase on collision"""

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

    original_id = int(result.data["addWikibase"]["id"])

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

        assert int(result.data["addWikibase"]["id"]) == original_id

        async with AsyncSession(bind=db_session) as session:
            wikibase = await session.get(WikibaseModel, original_id)
            assert wikibase is not None
            assert wikibase.wikibase_name == f"Wikibase {i}"

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
            assert matching_wikibases[0].id == original_id


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
