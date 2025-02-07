"""Test Aggregate Users Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value
from tests.utils.assert_meta import assert_page_meta


AGGREGATED_LANGUAGES_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!) {
  aggregateLanguagePopularity(pageNumber: $pageNumber, pageSize: $pageSize) {
    meta {
      pageNumber
      pageSize
      totalCount
      totalPages
    }
    data {
      language
      totalWikibases
      primaryWikibases
      additionalWikibases
    }
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["update-wikibase-primary-language-3"], scope="session")
@pytest.mark.query
async def test_aggregate_languages_query():
    """Test Aggregate Languages Query"""

    result = await test_schema.execute(
        AGGREGATED_LANGUAGES_QUERY, variable_values={"pageNumber": 1, "pageSize": 10}
    )

    assert result.errors is None
    assert result.data is not None

    assert_page_meta(
        result.data["aggregateLanguagePopularity"],
        expected_page_number=1,
        expected_page_size=10,
        expected_total_count=6,
        expected_total_pages=1,
    )

    for i, (
        expected_language,
        expected_total,
        expected_primary,
        expected_additional,
    ) in enumerate(
        [
            ("Hindi", 1, 1, 0),
            ("Albanian", 1, 0, 1),
            ("Babylonian", 1, 0, 1),
            ("Cymru", 1, 0, 1),
            ("Deutsch", 1, 0, 1),
            ("French", 1, 0, 1),
        ]
    ):
        assert_layered_property_value(
            result.data,
            ["aggregateLanguagePopularity", "data", i, "language"],
            expected_language,
        )
        assert_layered_property_value(
            result.data,
            ["aggregateLanguagePopularity", "data", i, "totalWikibases"],
            expected_total,
        )
        assert_layered_property_value(
            result.data,
            ["aggregateLanguagePopularity", "data", i, "primaryWikibases"],
            expected_primary,
        )
        assert_layered_property_value(
            result.data,
            ["aggregateLanguagePopularity", "data", i, "additionalWikibases"],
            expected_additional,
        )
