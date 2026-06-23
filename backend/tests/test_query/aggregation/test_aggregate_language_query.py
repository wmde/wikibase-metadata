"""Test Aggregate Users Query"""

import pytest
from model.database.wikibase_model import WikibaseModel
from model.enum.wikibase_type_enum import WikibaseType
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta

AGGREGATED_LANGUAGES_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
  aggregateLanguagePopularity(
    pageNumber: $pageNumber
    pageSize: $pageSize
    wikibaseFilter: $wikibaseFilter
  ) {
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
@pytest.mark.query
async def test_aggregate_languages_query(wikibase_fixture):
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
        expected_total_count=3,
        expected_total_pages=1,
    )

    for i, (
        expected_language,
        expected_total,
        expected_primary,
        expected_additional,
    ) in enumerate(
        [
            ("French", 1, 1, 0),
            ("Cymru", 1, 0, 1),
            ("Deutsch", 1, 0, 1),
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

# TODO: why doesn't this work?
@pytest.fixture
async def wikibases(db_session):
    """Create 3 test wikibases for connectivity tests"""
    from sqlalchemy.ext.asyncio import AsyncSession

    async with AsyncSession(bind=db_session) as session:
        for i in range(6):
            wikibase = WikibaseModel(
                wikibase_name=f"Test Wikibase {i}",
                base_url=f"https://example-{i}.com",
                sparql_endpoint_url=f"https://example-{i}.com/sparql",
                wikibase_type=WikibaseType.OTHER
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = WikibaseType.OTHER
            session.add(wikibase)
            await session.flush()
        
        wikibase = WikibaseModel(
                wikibase_name=f"Test Wikibase Suite",
                base_url=f"https://example-suite.com",
                sparql_endpoint_url=f"https://example-suite.com/sparql",
                wikibase_type=WikibaseType.SUITE
            )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType.SUITE
        session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
# @pytest.mark.dependency(
#     depends=["update-wikibase-type-other", "update-wikibase-type-suite"],
#     scope="session",
# )
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 7),
        (["CLOUD"], 7),
        (["OTHER"], 7),
        (["SUITE"], 1),
        (["CLOUD", "OTHER"], 7),
        (["CLOUD", "SUITE"], 1),
        (["OTHER", "SUITE"], 1),
        (["CLOUD", "OTHER", "SUITE"], 1),
    ],
)
@pytest.mark.user
async def test_aggregate_languages_query_filtered(wikibases, exclude: list, expected_count: int):
    """Test Aggregate Languages Query"""

    result = await test_schema.execute(
        AGGREGATED_LANGUAGES_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 1,
            "wikibaseFilter": {"wikibaseType": {"exclude": exclude}},
        },
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data,
        ["aggregateLanguagePopularity", "meta", "totalCount"],
        expected_count,
    )
