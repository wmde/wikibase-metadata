"""Test Wikibase List"""

import pytest
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_value,
    assert_page_meta,
    assert_property_value,
)


WIKIBASE_LIST_QUERY = """
query PageWikibases($pageNumber: Int!, $pageSize: Int!, $sortBy: WikibaseSortInput, $wikibaseFilter: WikibaseFilterInput) {
  wikibaseList(
    pageNumber: $pageNumber
    pageSize: $pageSize
    sortBy: $sortBy
    wikibaseFilter: $wikibaseFilter
  ) {
    meta {
      pageNumber
      pageSize
      totalCount
      totalPages
    }
    data {
      ...WB
    }
  }
}

fragment WB on Wikibase {
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
  wikibaseType
  connectivityObservations {
    mostRecent {
      id
    }
  }
  externalIdentifierObservations {
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
      totalTriples
    }
  }
  recentChangesObservations {
    mostRecent {
      id
      botChangeCount
      humanChangeCount
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
"""


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    depends=[
        "add-wikibase",
        "add-wikibase-script-path",
        "remove-wikibase-sparql-frontend-url",
        "update-wikibase-url",
        "update-wikibase-primary-language-3",
        "add-wikibase-ii",
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
    assert_page_meta(result.data["wikibaseList"], 1, 1, 2, 2)
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
        "externalIdentifierObservations",
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
        "add-wikibase",
        "add-wikibase-ii",
        "update-missing-wikibase-script-path",
        "update-missing-wikibase-sparql",
    ],
    scope="session",
)
async def test_wikibase_list_query_page_two():
    """Test Wikibase List"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY, variable_values={"pageNumber": 2, "pageSize": 1}
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 2, 1, 2, 2)
    assert "data" in result.data["wikibaseList"]
    assert len(result.data["wikibaseList"]["data"]) == 1
    result_datum = result.data["wikibaseList"]["data"][0]
    assert_property_value(result_datum, "id", "2")
    assert_property_value(result_datum, "title", "Mock Wikibase II")
    assert_property_value(
        result_datum, "category", "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS"
    )
    assert_property_value(
        result_datum, "description", "Another Mock wikibase for testing this codebase"
    )
    assert_property_value(
        result_datum, "organization", "Wikibase Mockery International"
    )
    assert_layered_property_value(result_datum, ["location", "country"], "Germany")
    assert_layered_property_value(result_datum, ["location", "region"], "Europe")

    assert_layered_property_value(result_datum, ["languages", "primary"], None)
    assert_layered_property_value(result_datum, ["languages", "additional"], [])

    for url_name, url in [
        ("baseUrl", "https://mock-wikibase.com/"),
        # ("actionApi", "https://mock-wikibase.com/w/api.php"),
        ("articlePath", "wiki"),
        # ("indexApi", "https://mock-wikibase.com/w/index.php"),
        ("scriptPath", "/mockwiki"),
        ("sparqlEndpointUrl", "https://mock-wikibase.com/query/sparql"),
        ("sparqlFrontendUrl", "https://mock-wikibase.com/query"),
    ]:
        assert_layered_property_value(result_datum, ["urls", url_name], url)

    for obs in [
        "connectivityObservations",
        "externalIdentifierObservations",
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
        "update-wikibase-type-test",
    ],
    scope="session",
)
@pytest.mark.parametrize(
    ["exclude", "expected_total"],
    [
        ([], 11),
        (["CLOUD"], 4),
        (["OTHER"], 10),
        (["SUITE"], 10),
        (["TEST"], 10),
        (["CLOUD", "OTHER"], 3),
        (["CLOUD", "SUITE"], 3),
        (["CLOUD", "TEST"], 3),
        (["OTHER", "SUITE"], 9),
        (["OTHER", "TEST"], 9),
        (["SUITE", "TEST"], 9),
        (["CLOUD", "OTHER", "SUITE"], 2),
        (["CLOUD", "OTHER", "TEST"], 2),
        (["CLOUD", "SUITE", "TEST"], 2),
        (["OTHER", "SUITE", "TEST"], 8),
        (["CLOUD", "OTHER", "SUITE", "TEST"], 1),
    ],
)
async def test_wikibase_list_query_filtered_exclude(exclude, expected_total):
    """Test Null Scenario"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 1,
            "wikibaseFilter": {"wikibaseType": {"exclude": exclude}},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 1, expected_total, expected_total)


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
    ],
    scope="session",
)
@pytest.mark.parametrize(
    ["include", "expected_total"],
    [
        ([], 11),
        (["CLOUD"], 7),
        (["OTHER"], 1),
        (["SUITE"], 1),
        (["TEST"], 1),
        (["CLOUD", "OTHER"], 8),
        (["CLOUD", "SUITE"], 8),
        (["CLOUD", "TEST"], 8),
        (["OTHER", "SUITE"], 2),
        (["OTHER", "TEST"], 2),
        (["SUITE", "TEST"], 2),
        (["CLOUD", "OTHER", "SUITE"], 9),
        (["CLOUD", "OTHER", "TEST"], 9),
        (["CLOUD", "SUITE", "TEST"], 9),
        (["OTHER", "SUITE", "TEST"], 3),
        (["CLOUD", "OTHER", "SUITE", "TEST"], 10),
    ],
)
async def test_wikibase_list_query_filtered_include(include, expected_total):
    """Test Null Scenario"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 1,
            "wikibaseFilter": {"wikibaseType": {"include": include}},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 1, expected_total, expected_total)


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-cat-asc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_category_asc():
    """Test Sort Category Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "CATEGORY", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    for i in range(9):
        assert_layered_property_value(
            result.data, ["wikibaseList", "data", i, "category"], None
        )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 9, "category"],
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 10, "category"],
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
    )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-cat-desc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        "sort-cat-asc",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_category_desc():
    """Test Sort Category Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "CATEGORY", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 0, "category"],
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
    )
    assert_layered_property_value(
        result.data,
        ["wikibaseList", "data", 1, "category"],
        "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
    )
    for i in range(2, 11):
        assert_layered_property_value(
            result.data, ["wikibaseList", "data", i, "category"], None
        )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-edit-asc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        "sort-cat-asc",
        "sort-cat-desc",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_edit_asc():
    """Test Sort Edit Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "EDITS", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    for i in range(10):
        assert_layered_property_value(
            result.data["wikibaseList"]["data"],
            [i, "recentChangesObservations", "mostRecent"],
            None,
        )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [10, "recentChangesObservations", "mostRecent", "botChangeCount"],
        6,
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [10, "recentChangesObservations", "mostRecent", "humanChangeCount"],
        10,
    )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-edit-desc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        "sort-edit-asc",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_edit_desc():
    """Test Sort Edit Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "EDITS", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [0, "recentChangesObservations", "mostRecent", "botChangeCount"],
        6,
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [0, "recentChangesObservations", "mostRecent", "humanChangeCount"],
        10,
    )
    for i in range(1, 11):
        assert_layered_property_value(
            result.data["wikibaseList"]["data"],
            [i, "recentChangesObservations", "mostRecent"],
            None,
        )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-title-asc",
    depends=["mutate-cloud-instances", "sort-edit-asc", "sort-edit-desc"],
    scope="session",
)
async def test_wikibase_list_query_sort_title_asc():
    """Test Sort Title Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TITLE", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [0, "title"],
        "biodiversity citizen science",
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [1, "title"],
        "Doelgericht Digitaal Transformeren",
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [2, "title"], "geokb"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [3, "title"], "Internet Domains"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [4, "title"], "LexBib"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [5, "title"], "MetaBase"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [6, "title"], "Mock Wikibase"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [7, "title"], "Mock Wikibase II"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [8, "title"], "Social Contagion"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [9, "title"], "Teochew Dictionary"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [10, "title"], "wikifcd"
    )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-title-desc",
    depends=["mutate-cloud-instances", "sort-title-asc"],
    scope="session",
)
async def test_wikibase_list_query_sort_title_desc():
    """Test Sort Title Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TITLE", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [0, "title"], "wikifcd"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [1, "title"], "Teochew Dictionary"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [2, "title"], "Social Contagion"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [3, "title"], "Mock Wikibase II"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [4, "title"], "Mock Wikibase"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [5, "title"], "MetaBase"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [6, "title"], "LexBib"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [7, "title"], "Internet Domains"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [8, "title"], "geokb"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [9, "title"],
        "Doelgericht Digitaal Transformeren",
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [10, "title"],
        "biodiversity citizen science",
    )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-triples-asc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        "sort-title-asc",
        "sort-title-desc",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_triples_asc():
    """Test Sort Triples Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TRIPLES", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    for i in range(10):
        assert_layered_property_value(
            result.data["wikibaseList"]["data"],
            [i, "quantityObservations", "mostRecent"],
            None,
        )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [10, "quantityObservations", "mostRecent", "totalTriples"],
        8,
    )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-triples-desc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        "sort-triples-asc",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_triples_desc():
    """Test Sort Triples Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TRIPLES", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    assert_layered_property_value(
        result.data["wikibaseList"]["data"],
        [0, "quantityObservations", "mostRecent", "totalTriples"],
        8,
    )
    for i in range(1, 11):
        assert_layered_property_value(
            result.data["wikibaseList"]["data"],
            [i, "quantityObservations", "mostRecent"],
            None,
        )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-type-asc",
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
        "sort-triples-asc",
        "sort-triples-desc",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_type_asc():
    """Test Sort Type Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TYPE", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [0, "wikibaseType"], "UNKNOWN"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [1, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [2, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [3, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [4, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [5, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [6, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [7, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [8, "wikibaseType"], "OTHER"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [9, "wikibaseType"], "SUITE"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [10, "wikibaseType"], "SUITE"
    )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
    ],
    scope="session",
)
async def test_wikibase_list_query_sort_type_desc():
    """Test Sort Type Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TYPE", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [0, "wikibaseType"], "SUITE"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [1, "wikibaseType"], "SUITE"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [2, "wikibaseType"], "OTHER"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [3, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [4, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [5, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [6, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [7, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [8, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [9, "wikibaseType"], "CLOUD"
    )
    assert_layered_property_value(
        result.data["wikibaseList"]["data"], [10, "wikibaseType"], "UNKNOWN"
    )
