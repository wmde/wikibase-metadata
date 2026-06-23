"""Test Aggregate Libraries Query"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.version.software_version_model import (
    WikibaseSoftwareVersionModel,
)
from model.database.wikibase_observation.version.wikibase_version_observation_model import (
    WikibaseSoftwareVersionObservationModel,
)
from model.database.wikibase_software.software_model import WikibaseSoftwareModel
from model.enum.wikibase_software_type_enum import WikibaseSoftwareType
from model.enum.wikibase_type_enum import WikibaseType
from tests.test_query.aggregation.software_version.software_version_aggregate_fragment import (
    SOFTWARE_VERSION_DOUBLE_AGGREGATE_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_page_meta,
)

AGGREGATE_LIBRARIES_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
  aggregateLibraryPopularity(
    pageNumber: $pageNumber
    pageSize: $pageSize
    wikibaseFilter: $wikibaseFilter
  ) {
    ...WikibaseSoftwareVersionDoubleAggregatePageFragment
  }
}

""" + SOFTWARE_VERSION_DOUBLE_AGGREGATE_FRAGMENT


@pytest.fixture
async def wikibase_with_three_libraries(db_session):  # pylint: disable=unused-argument
    """Create a wikibase with 3 library software versions for pagination tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Libraries Test Wikibase",
            base_url="https://aggregate-libraries-example.com",
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

        for name, version in [
            ("lib/a", "1.0.0"),
            ("lib/b", "2.0.0"),
            ("lib/c", "3.0.0"),
        ]:
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.LIBRARY,
                software_name=name,
            )
            session.add(software)
            await session.flush()
            await session.refresh(software)

            sv = WikibaseSoftwareVersionModel(software=software, version=version)
            sv.wikibase_software_version_observation_id = obs.id
            session.add(sv)

        await session.flush()


@pytest.fixture
async def wikibases_with_libraries_for_filter(
    db_session,
):  # pylint: disable=unused-argument
    """SUITE wikibase with libraries — drops to 0 when SUITE excluded"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Libraries Suite Wikibase",
            base_url="https://aggregate-libraries-suite-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType.SUITE
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

        for i in range(3):
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.LIBRARY,
                software_name=f"suite-lib-{i}",
            )
            session.add(software)
            await session.flush()
            await session.refresh(software)

            sv = WikibaseSoftwareVersionModel(software=software, version="1.0")
            sv.wikibase_software_version_observation_id = obs.id
            session.add(sv)

        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_libraries_query_page_one(
    wikibase_with_three_libraries,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregated Libraries Query - page 1"""

    result = await test_schema.execute(
        AGGREGATE_LIBRARIES_QUERY, variable_values={"pageNumber": 1, "pageSize": 2}
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateLibraryPopularity"], 1, 2, 3, 2)
    assert_layered_property_count(
        result.data, ["aggregateLibraryPopularity", "data"], 2
    )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_libraries_query_page_two(
    wikibase_with_three_libraries,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregated Libraries Query - page 2"""

    result = await test_schema.execute(
        AGGREGATE_LIBRARIES_QUERY, variable_values={"pageNumber": 2, "pageSize": 2}
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateLibraryPopularity"], 2, 2, 3, 2)
    assert_layered_property_count(
        result.data, ["aggregateLibraryPopularity", "data"], 1
    )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 3),
        (["CLOUD"], 3),
        (["OTHER"], 3),
        (["SUITE"], 0),
        (["CLOUD", "OTHER"], 3),
        (["CLOUD", "SUITE"], 0),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.version
async def test_aggregate_libraries_query_filtered(
    exclude: list, expected_count: int, wikibases_with_libraries_for_filter
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate Library Query"""

    result = await test_schema.execute(
        AGGREGATE_LIBRARIES_QUERY,
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
        ["aggregateLibraryPopularity", "meta", "totalCount"],
        expected_count,
    )
