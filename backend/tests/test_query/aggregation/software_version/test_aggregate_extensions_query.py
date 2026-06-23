"""Test Aggregated Extensions Query"""

from datetime import datetime, timezone
import pytest
from model.enum.wikibase_type_enum import WikibaseType
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.version.software_version_model import WikibaseSoftwareVersionModel
from model.database.wikibase_observation.version.wikibase_version_observation_model import WikibaseSoftwareVersionObservationModel
from model.database.wikibase_software.software_model import WikibaseSoftwareModel
from model.enum.wikibase_software_type_enum import WikibaseSoftwareType
from tests.test_query.aggregation.software_version.assert_software_version_aggregate import (
    assert_software_version_aggregate,
)
from tests.test_query.aggregation.software_version.software_version_aggregate_fragment import (
    SOFTWARE_VERSION_DOUBLE_AGGREGATE_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_page_meta,
)

AGGREGATE_EXTENSIONS_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
  aggregateExtensionPopularity(
    pageNumber: $pageNumber
    pageSize: $pageSize
    wikibaseFilter: $wikibaseFilter
  ) {
    ...WikibaseSoftwareVersionDoubleAggregatePageFragment
  }
}

""" + SOFTWARE_VERSION_DOUBLE_AGGREGATE_FRAGMENT

@pytest.fixture
async def wikibase_with_three_extensions(db_session):
    """Create a wikibase with 3 extension software versions"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Extensions Test Wikibase",
            base_url="https://aggregate-extensions-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseSoftwareVersionObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs)
        await session.flush()
        await session.refresh(obs)

        for name in ["ExtensionA", "ExtensionB", "ExtensionC"]:
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.EXTENSION,
                software_name=name,
            )
            session.add(software)
            await session.flush()
            await session.refresh(software)

            version = WikibaseSoftwareVersionModel(software=software, version="1.0")
            version.wikibase_software_version_observation_id = obs.id
            session.add(version)

        await session.flush()

@pytest.fixture
async def wikibases_with_extensions_for_filter(db_session):
    """11 extensions on UNKNOWN wikibase, 1 on SUITE for filtered aggregate tests"""
    async with get_async_session() as session:
        # UNKNOWN wikibase with 11 extensions
        wikibase_unknown = WikibaseModel(
            wikibase_name="Aggregate Extensions Unknown Wikibase",
            base_url="https://aggregate-extensions-unknown-example.com",
        )
        wikibase_unknown.checked = True
        wikibase_unknown.reuse = True
        wikibase_unknown.test = False
        wikibase_unknown.wikibase_type = None
        session.add(wikibase_unknown)
        await session.flush()
        await session.refresh(wikibase_unknown)

        obs_unknown = WikibaseSoftwareVersionObservationModel()
        obs_unknown.wikibase_id = wikibase_unknown.id
        obs_unknown.returned_data = True
        obs_unknown.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs_unknown)
        await session.flush()
        await session.refresh(obs_unknown)

        for i in range(11):
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.EXTENSION,
                software_name=f"FilterExtension{i}",
            )
            session.add(software)
            await session.flush()
            await session.refresh(software)

            version = WikibaseSoftwareVersionModel(software=software, version="1.0")
            version.wikibase_software_version_observation_id = obs_unknown.id
            session.add(version)

        # SUITE wikibase with 1 extension (SUITE-only)
        wikibase_suite = WikibaseModel(
            wikibase_name="Aggregate Extensions Suite Wikibase",
            base_url="https://aggregate-extensions-suite-example.com",
        )
        wikibase_suite.checked = True
        wikibase_suite.reuse = True
        wikibase_suite.test = False
        wikibase_suite.wikibase_type = WikibaseType.SUITE
        session.add(wikibase_suite)
        await session.flush()
        await session.refresh(wikibase_suite)

        obs_suite = WikibaseSoftwareVersionObservationModel()
        obs_suite.wikibase_id = wikibase_suite.id
        obs_suite.returned_data = True
        obs_suite.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs_suite)
        await session.flush()
        await session.refresh(obs_suite)

        suite_software = WikibaseSoftwareModel(
            software_type=WikibaseSoftwareType.EXTENSION,
            software_name="SuiteOnlyExtension",
        )
        session.add(suite_software)
        await session.flush()
        await session.refresh(suite_software)

        suite_version = WikibaseSoftwareVersionModel(software=suite_software, version="1.0")
        suite_version.wikibase_software_version_observation_id = obs_suite.id
        session.add(suite_version)

        await session.flush()

@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_extensions_query_page_one(wikibase_with_three_extensions):
    """Test Aggregated Extensions Query - page 1"""

    result = await test_schema.execute(
        AGGREGATE_EXTENSIONS_QUERY, variable_values={"pageNumber": 1, "pageSize": 2}
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateExtensionPopularity"], 1, 2, 3, 2)
    assert_layered_property_count(result.data, ["aggregateExtensionPopularity", "data"], 2)


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_extensions_query_page_two(wikibase_with_three_extensions):
    """Test Aggregated Extensions Query - page 2"""

    result = await test_schema.execute(
        AGGREGATE_EXTENSIONS_QUERY, variable_values={"pageNumber": 2, "pageSize": 2}
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateExtensionPopularity"], 2, 2, 3, 2)
    assert_layered_property_count(result.data, ["aggregateExtensionPopularity", "data"], 1)


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_extensions_query_page_three(wikibase_with_three_extensions):
    """Test Aggregated Extensions Query - page 3 empty"""

    result = await test_schema.execute(
        AGGREGATE_EXTENSIONS_QUERY, variable_values={"pageNumber": 3, "pageSize": 2}
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateExtensionPopularity"], 3, 2, 3, 2)
    assert_layered_property_count(result.data, ["aggregateExtensionPopularity", "data"], 0)


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 12),
        (["CLOUD"], 12),
        (["OTHER"], 12),
        (["SUITE"], 11),
        (["CLOUD", "OTHER"], 12),
        (["CLOUD", "SUITE"], 11),
        (["OTHER", "SUITE"], 11),
        (["CLOUD", "OTHER", "SUITE"], 11),
    ],
)

@pytest.mark.version
async def test_aggregate_extensions_query_filtered(
    exclude: list, expected_count: int, wikibases_with_extensions_for_filter
):
    """Test Aggregate Extensions Query filtered"""

    result = await test_schema.execute(
        AGGREGATE_EXTENSIONS_QUERY,
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
        ["aggregateExtensionPopularity", "meta", "totalCount"],
        expected_count,
    )