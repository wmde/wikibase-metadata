"""Test Aggregated Skins Query"""

from datetime import datetime, timezone

import pytest

from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.version.software_version_model import WikibaseSoftwareVersionModel
from model.database.wikibase_observation.version.wikibase_version_observation_model import WikibaseSoftwareVersionObservationModel
from model.database.wikibase_software.software_model import WikibaseSoftwareModel
from model.enum.wikibase_software_type_enum import WikibaseSoftwareType
from model.enum.wikibase_type_enum import WikibaseType
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

AGGREGATE_SKINS_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
  aggregateSkinPopularity(
    pageNumber: $pageNumber
    pageSize: $pageSize
    wikibaseFilter: $wikibaseFilter
  ) {
    ...WikibaseSoftwareVersionDoubleAggregatePageFragment
  }
}

""" + SOFTWARE_VERSION_DOUBLE_AGGREGATE_FRAGMENT

@pytest.fixture
async def wikibase_with_three_named_skins(db_session):
    """Create a wikibase with 3 specific skin software versions"""
    async with get_async_session() as session:
        skin_data = [
            ("MonoBook", None),
            ("Timeless", "0.8.9"),
            ("Vector", None),
        ]
        skins = {}
        for name, _ in skin_data:
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.SKIN,
                software_name=name,
            )
            session.add(software)
            await session.flush()
            await session.refresh(software)
            skins[name] = software

        wikibase = WikibaseModel(
            wikibase_name="Aggregate Skins Page One Test Wikibase",
            base_url="https://aggregate-skins-page-one-example.com",
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

        for name, version in skin_data:
            sv = WikibaseSoftwareVersionModel(software=skins[name], version=version)
            sv.wikibase_software_version_observation_id = obs.id
            session.add(sv)

        await session.flush()

@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_skins_query_page_one(wikibase_with_three_named_skins):
    """Test Aggregated Skins Query"""

    result = await test_schema.execute(
        AGGREGATE_SKINS_QUERY, variable_values={"pageNumber": 1, "pageSize": 5}
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateSkinPopularity"], 1, 5, 3, 1)
    assert_layered_property_count(result.data, ["aggregateSkinPopularity", "data"], 3)

    for index, (
        expected_software_name,
        expected_version_string,
        expected_version_semver,
    ) in enumerate(
        [
            ("MonoBook", None, (None, None, None)),
            ("Timeless", "0.8.9", (0, 8, 9)),
            ("Vector", None, (None, None, None)),
        ]
    ):

        assert_software_version_aggregate(
            result.data["aggregateSkinPopularity"]["data"][index],
            expected_software_name,
            1,
            expected_version_string,
            expected_version_semver,
            None,
            None,
        )

@pytest.fixture
async def wikibase_with_three_skins(db_session):
    """Create a SUITE wikibase with 3 distinct skin software versions"""
    async with get_async_session() as session:
        skin_names = ["SkinA", "SkinB", "SkinC"]
        skins = {}
        for name in skin_names:
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.SKIN,
                software_name=name,
            )
            session.add(software)
            await session.flush()
            await session.refresh(software)
            skins[name] = software

        wikibase = WikibaseModel(
            wikibase_name="Aggregate Skins Test Wikibase",
            base_url="https://aggregate-skins-example.com",
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

        for name, software in skins.items():
            version = WikibaseSoftwareVersionModel(software=software, version="1.0")
            version.wikibase_software_version_observation_id = obs.id
            session.add(version)

        await session.flush()


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
@pytest.mark.user
async def test_aggregate_users_query_filtered(wikibase_with_three_skins, exclude: list, expected_count: int):
    """Test Aggregate Users Query"""

    result = await test_schema.execute(
        AGGREGATE_SKINS_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 1,
            "wikibaseFilter": {"wikibaseType": {"exclude": exclude}},
        },
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateSkinPopularity", "meta", "totalCount"], expected_count
    )
