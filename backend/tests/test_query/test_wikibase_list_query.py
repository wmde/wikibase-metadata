"""Test Wikibase List"""

import pytest
from model.database.wikibase_model import WikibaseModel
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_value,
    assert_page_meta,
    assert_property_value,
)
from sqlalchemy.ext.asyncio import AsyncSession
from model.database.wikibase_category_model import WikibaseCategoryModel
from model.enum.wikibase_category_enum import WikibaseCategory
from sqlalchemy import select


@pytest.fixture
async def two_wikibases_with_full_data(db_session):
    """Create two wikibases with full data for wikibase list tests"""

    async with AsyncSession(bind=db_session) as session:
        # get or create category
        category = await session.scalar(
            select(WikibaseCategoryModel).where(
                WikibaseCategoryModel.category
                == WikibaseCategory.EXPERIMENTAL_AND_PROTOTYPE_PROJECTS
            )
        )
        if category is None:
            category = WikibaseCategoryModel()
            category.category = WikibaseCategory.EXPERIMENTAL_AND_PROTOTYPE_PROJECTS
            session.add(category)
            await session.flush()
            await session.refresh(category)

        wikibase = WikibaseModel(
            wikibase_name="Mock Wikibase",
            base_url="https://example.com",
            article_path="/wiki",
            script_path="/w/",
            sparql_endpoint_url="https://query.example.com/sparql",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        wikibase.description = "Mock wikibase for testing this codebase"
        wikibase.organization = "Wikibase Mockery International"
        wikibase.country = "Germany"
        wikibase.region = "Europe"
        wikibase.category_id = category.id
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        wikibase.set_primary_language("Hindi")
        wikibase.set_additional_languages(
            ["Albanian", "Babylonian", "Cymru", "Deutsch", "French"]
        )

        wikibase2 = WikibaseModel(
            wikibase_name="Mock Wikibase II",
            base_url="https://example2.com",
        )
        wikibase2.checked = True
        wikibase2.reuse = True
        wikibase2.test = False
        wikibase2.wikibase_type = None
        session.add(wikibase2)
        await session.flush()
        return wikibase.id, wikibase2.id


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_list_query(two_wikibases_with_full_data):
    """Test Wikibase List"""

    wikibase_id_1, _ = two_wikibases_with_full_data

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
    assert_property_value(result_datum, "id", str(wikibase_id_1))
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
        ("baseUrl", "https://example.com"),
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
@pytest.mark.parametrize(
    ["exclude", "expected_total"],
    [
        ([], 11),
        (["CLOUD"], 4),
        (["OTHER"], 10),
        (["SUITE"], 10),
        (["TEST"], 10),
        (["UNKNOWN"], 10),
        (["CLOUD", "OTHER"], 3),
        (["CLOUD", "SUITE"], 3),
        (["CLOUD", "TEST"], 3),
        (["CLOUD", "UNKNOWN"], 3),
        (["OTHER", "SUITE"], 9),
        (["OTHER", "TEST"], 9),
        (["OTHER", "UNKNOWN"], 9),
        (["SUITE", "TEST"], 9),
        (["SUITE", "UNKNOWN"], 9),
        (["TEST", "UNKNOWN"], 9),
        (["CLOUD", "OTHER", "SUITE"], 2),
        (["CLOUD", "OTHER", "TEST"], 2),
        (["CLOUD", "OTHER", "UNKNOWN"], 2),
        (["CLOUD", "SUITE", "TEST"], 2),
        (["CLOUD", "SUITE", "UNKNOWN"], 2),
        (["CLOUD", "TEST", "UNKNOWN"], 2),
        (["OTHER", "SUITE", "TEST"], 8),
        (["OTHER", "SUITE", "UNKNOWN"], 8),
        (["OTHER", "TEST", "UNKNOWN"], 8),
        (["SUITE", "TEST", "UNKNOWN"], 8),
        (["CLOUD", "OTHER", "SUITE", "TEST"], 1),
        (["CLOUD", "OTHER", "SUITE", "UNKNOWN"], 1),
        (["CLOUD", "OTHER", "TEST", "UNKNOWN"], 1),
        (["CLOUD", "SUITE", "TEST", "UNKNOWN"], 1),
        (["OTHER", "SUITE", "TEST", "UNKNOWN"], 7),
        (["CLOUD", "OTHER", "SUITE", "TEST", "UNKNOWN"], 0),
    ],
)
async def test_wikibase_list_query_filtered_exclude(exclude, expected_total):
    """Test Filtering - Exclude Wikibase Types"""

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
# @pytest.mark.dependency(
#     depends=[
#         "update-wikibase-type-other",
#         "update-wikibase-type-suite",
#         "update-wikibase-type-test",
#     ],
#     scope="session",
# )
@pytest.mark.parametrize(
    ["include", "expected_total"],
    [
        ([], 11),
        (["CLOUD"], 7),
        (["OTHER"], 1),
        (["SUITE"], 1),
        (["TEST"], 1),
        (["UNKNOWN"], 1),
        (["CLOUD", "OTHER"], 8),
        (["CLOUD", "SUITE"], 8),
        (["CLOUD", "TEST"], 8),
        (["CLOUD", "UNKNOWN"], 8),
        (["OTHER", "SUITE"], 2),
        (["OTHER", "TEST"], 2),
        (["OTHER", "UNKNOWN"], 2),
        (["SUITE", "TEST"], 2),
        (["SUITE", "UNKNOWN"], 2),
        (["TEST", "UNKNOWN"], 2),
        (["CLOUD", "OTHER", "SUITE"], 9),
        (["CLOUD", "OTHER", "TEST"], 9),
        (["CLOUD", "OTHER", "UNKNOWN"], 9),
        (["CLOUD", "SUITE", "TEST"], 9),
        (["CLOUD", "SUITE", "UNKNOWN"], 9),
        (["CLOUD", "TEST", "UNKNOWN"], 9),
        (["OTHER", "SUITE", "TEST"], 3),
        (["OTHER", "SUITE", "UNKNOWN"], 3),
        (["OTHER", "TEST", "UNKNOWN"], 3),
        (["SUITE", "TEST", "UNKNOWN"], 3),
        (["CLOUD", "OTHER", "SUITE", "TEST"], 10),
        (["CLOUD", "OTHER", "SUITE", "UNKNOWN"], 10),
        (["CLOUD", "OTHER", "TEST", "UNKNOWN"], 10),
        (["CLOUD", "SUITE", "TEST", "UNKNOWN"], 10),
        (["OTHER", "SUITE", "TEST", "UNKNOWN"], 4),
        (["CLOUD", "OTHER", "SUITE", "TEST", "UNKNOWN"], 11),
    ],
)
async def test_wikibase_list_query_filtered_include(include, expected_total):
    """Test Filtering - Include Wikibase Types"""

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
