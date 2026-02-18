# pylint: disable=redefined-outer-name
"""Test Add Wikibase"""

import pytest
from tests.test_schema import test_schema

ADD_WIKIBASE_QUERY = """
mutation MyMutation($wikibaseInput: WikibaseInput!) {
  addWikibase(wikibaseInput: $wikibaseInput) {
    id
  }
}"""


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
    assert isinstance(result.data["addWikibase"]["id"], str)


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
@pytest.mark.mutation
@pytest.mark.dependency(name="add-wikibase-ii", depends=["add-wikibase"])
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
    """Test Add Wikibase"""

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
