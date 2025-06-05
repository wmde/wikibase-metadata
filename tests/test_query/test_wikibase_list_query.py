"""Test Wikibase List"""

import pytest
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_value,
    assert_page_meta,
    assert_property_value,
)


WIKIBASE_LIST_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!) {
  wikibaseList(pageNumber: $pageNumber, pageSize: $pageSize) {
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
        "add-wikibase-url",
        "remove-wikibase-url",
        "update-wikibase-url",
        "update-wikibase-primary-language-3",
    ],
    scope="session",
)
async def test_wikibase_list_query():
    """Test Wikibase List"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY, variable_values={"pageNumber": 1, "pageSize": 1}
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
        ("baseUrl", "example.com"),
        ("actionApi", "https://example.com/w/api.php"),
        ("articlePath", "example.com/wiki"),
        ("indexApi", "https://example.com/w/index.php"),
        ("scriptPath", "https://example.com/w/"),
        ("sparqlEndpointUrl", "https://query.example.com/sparql"),
        ("sparqlFrontendUrl", None),
        ("sparqlUrl", None),
        ("specialStatisticsUrl", "example.com/wiki/Special:Statistics"),
        ("specialVersionUrl", "example.com/wiki/Special:Version"),
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
