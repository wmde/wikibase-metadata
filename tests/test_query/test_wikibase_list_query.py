"""Test Wikibase List"""

import pytest
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_value,
    assert_page_meta,
    assert_property_value,
    get_mock_context,
)


WIKIBASE_LIST_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
  wikibaseList(
    pageNumber: $pageNumber
    pageSize: $pageSize
    wikibaseFilter: $wikibaseFilter
  ) {
    data {
      id
      title
      category
      description
      organization
      location {
        country
        region
      }
      languages {
        primary
        additional
      }
      urls {
        baseUrl
        actionApi
        articlePath
        indexApi
        scriptPath
        sparqlEndpointUrl
        sparqlFrontendUrl
        sparqlUrl
        specialStatisticsUrl
        specialVersionUrl
      }
      connectivityObservations {
        mostRecent {
          id
        }
      }
      logObservations {
        firstMonth {
          mostRecent {
            id
          }
        }
        lastMonth {
          mostRecent {
            id
          }
        }
      }
      propertyPopularityObservations {
        mostRecent {
          id
        }
      }
      quantityObservations {
        mostRecent {
          id
        }
      }
      softwareVersionObservations {
        mostRecent {
          id
        }
      }
      userObservations {
        mostRecent {
          id
        }
      }
    }
    meta {
      pageNumber
      pageSize
      totalCount
      totalPages
    }
  }
}"""


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    depends=[
        "add-wikibase",
        "add-wikibase-script-path",
        "remove-wikibase-sparql-frontend-url",
        "update-wikibase-url",
        "update-wikibase-primary-language-3",
    ],
    scope="session",
)
async def test_wikibase_list_query():
    """Test Wikibase List"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={"pageNumber": 1, "pageSize": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 1, 1, 1)
    assert "data" in result.data["wikibaseList"]
    assert len(result.data["wikibaseList"]["data"]) == 1
    result_datum = result.data["wikibaseList"]["data"][0]
    assert_property_value(result_datum, "id", "1")
    assert_property_value(result_datum, "title", "Mock Wikibase")
    assert_property_value(
        result_datum, "category", "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS"
    )
    assert_property_value(
        result_datum, "description", "Mock wikibase for testing this codebase"
    )
    assert_property_value(
        result_datum, "organization", "Wikibase Mockery International"
    )
    assert_layered_property_value(result_datum, ["location", "country"], "Germany")
    assert_layered_property_value(result_datum, ["location", "region"], "Europe")

    assert_layered_property_value(result_datum, ["languages", "primary"], "Hindi")
    assert_layered_property_value(
        result_datum,
        ["languages", "additional"],
        ["Albanian", "Babylonian", "Cymru", "Deutsch", "French"],
    )

    for url_name, url in [
        ("baseUrl", "https://example.com/"),
        ("actionApi", "https://example.com/w/api.php"),
        ("articlePath", "/wiki"),
        ("indexApi", "https://example.com/w/index.php"),
        ("scriptPath", "/w/"),
        ("sparqlEndpointUrl", "https://query.example.com/sparql"),
        ("sparqlFrontendUrl", None),
        ("sparqlUrl", None),
        ("specialStatisticsUrl", "https://example.com/wiki/Special:Statistics"),
        ("specialVersionUrl", "https://example.com/wiki/Special:Version"),
    ]:
        assert_layered_property_value(result_datum, ["urls", url_name], url)

    for obs in [
        "connectivityObservations",
        "logObservations",
        "propertyPopularityObservations",
        "quantityObservations",
        "softwareVersionObservations",
        "userObservations",
    ]:
        assert obs in result_datum


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
    ],
    scope="session",
)
@pytest.mark.parametrize(
    ["exclude", "expected_total"],
    [
        ([], 10),
        (["CLOUD"], 2),
        (["OTHER"], 9),
        (["SUITE"], 9),
        (["CLOUD", "OTHER"], 1),
        (["CLOUD", "SUITE"], 1),
        (["OTHER", "SUITE"], 8),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
async def test_wikibase_list_query_filtered(exclude, expected_total):
    """Test Null Scenario"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 1,
            "wikibaseFilter": {"wikibaseType": {"exclude": exclude}},
        },
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 1, expected_total, expected_total)
