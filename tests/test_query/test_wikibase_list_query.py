"""Test Notices Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_property_value


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
      urls {
        baseUrl
        actionApi
        indexApi
        sparqlEndpointUrl
        sparqlUrl
        specialVersionUrl
      }
      connectivityObservations {
        mostRecent {
          id
        }
      }
      logObservations {
        mostRecent {
          id
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
async def test_wikibase_list_query():
    """Test Wikibase List"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY, variable_values={"pageNumber": 1, "pageSize": 1}
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert "meta" in result.data["wikibaseList"]
    assert_layered_property_value(
        result.data, ["wikibaseList", "meta", "pageNumber"], 1
    )
    assert_layered_property_value(result.data, ["wikibaseList", "meta", "pageSize"], 1)
    assert_layered_property_value(
        result.data, ["wikibaseList", "meta", "totalCount"], 1
    )
    assert_layered_property_value(
        result.data, ["wikibaseList", "meta", "totalPages"], 1
    )
    assert "data" in result.data["wikibaseList"]
    assert len(result.data["wikibaseList"]["data"]) == 1
    result_datum = result.data["wikibaseList"]["data"][0]
    assert_property_value(result_datum, "id", "1")
    assert_property_value(result_datum, "title", "Mock Wikibase")
    assert_property_value(
        result_datum, "category", "Experimental and Prototype Projects"
    )
    assert_property_value(
        result_datum, "description", "Mock wikibase for testing this codebase"
    )
    assert_property_value(
        result_datum, "organization", "Wikibase Mockery International"
    )
    assert_layered_property_value(result_datum, ["location", "country"], "Germany")
    assert_layered_property_value(result_datum, ["location", "region"], "Europe")

    for url_name, url in [
        ("baseUrl", "test.url"),
        ("actionApi", "test.url/w/api.php"),
        ("indexApi", "test.url/w/index.php"),
        ("sparqlEndpointUrl", "query.test.url/sparql"),
        ("sparqlUrl", "query.test.url"),
        ("specialVersionUrl", "test.url/wiki/Special:Version"),
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