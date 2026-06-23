"""Test Aggregate Users Query"""

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_language_model import WikibaseLanguageModel
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
async def test_aggregate_languages_query(
    wikibase_fixture,
):  # pylint: disable=redefined-outer-name, unused-argument
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


@pytest.fixture
async def wikibases_with_languages(db_session):  # pylint: disable=unused-argument
    """
    Create wikibases with languages:
    - 1 SUITE wikibase with 7 languages (en + 6 others)
    - 1 non-SUITE wikibase with 1 language (en)
    Excluding SUITE drops from 7 to 1 (only 'en' remains via non-SUITE wikibase)
    """
    async with get_async_session() as session:
        # SUITE wikibase with 7 languages
        suite_wikibase = WikibaseModel(
            wikibase_name="Languages Suite Test Wikibase",
            base_url="https://languages-suite-example.com",
        )
        suite_wikibase.checked = True
        suite_wikibase.reuse = True
        suite_wikibase.test = False
        suite_wikibase.wikibase_type = WikibaseType.SUITE
        session.add(suite_wikibase)
        await session.flush()
        await session.refresh(suite_wikibase)

        for i, lang in enumerate(["en", "de", "fr", "es", "it", "nl", "pt"]):
            lang_model = WikibaseLanguageModel(
                language=lang, primary=(i == 0)
            )  # pylint: disable=superfluous-parens
            lang_model.wikibase_id = suite_wikibase.id
            session.add(lang_model)

        # non-SUITE wikibase with just 'en'
        other_wikibase = WikibaseModel(
            wikibase_name="Languages Other Test Wikibase",
            base_url="https://languages-other-example.com",
        )
        other_wikibase.checked = True
        other_wikibase.reuse = True
        other_wikibase.test = False
        other_wikibase.wikibase_type = None
        session.add(other_wikibase)
        await session.flush()
        await session.refresh(other_wikibase)

        lang_model = WikibaseLanguageModel(language="en", primary=True)
        lang_model.wikibase_id = other_wikibase.id
        session.add(lang_model)

        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
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
async def test_aggregate_languages_query_filtered(
    wikibases_with_languages, exclude: list, expected_count: int
):  # pylint: disable=redefined-outer-name, unused-argument
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
