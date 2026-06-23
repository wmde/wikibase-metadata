"""Test Aggregated Software Query"""

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

AGGREGATE_SOFTWARE_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
  aggregateSoftwarePopularity(
    pageNumber: $pageNumber
    pageSize: $pageSize
    wikibaseFilter: $wikibaseFilter
  ) {
    ...WikibaseSoftwareVersionDoubleAggregatePageFragment
  }
}

""" + SOFTWARE_VERSION_DOUBLE_AGGREGATE_FRAGMENT


@pytest.fixture
async def five_wikibases_with_software_versions(
    db_session,
):  # pylint: disable=unused-argument
    """Create 5 software entries; 4 reachable via UNKNOWN type, 1 only via SUITE"""
    async with get_async_session() as session:
        software_names = [
            "SoftwareA",
            "SoftwareB",
            "SoftwareC",
            "SoftwareD",
            "SoftwareE",
        ]
        software_entries = {}
        for name in software_names:
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.SOFTWARE,
                software_name=name,
            )
            session.add(software)
            await session.flush()
            await session.refresh(software)
            software_entries[name] = software

        # 4 software entries on UNKNOWN (None) type wikibases - never excluded by these filters
        # 1 software entry (SoftwareE) only on a SUITE wikibase - dropped when SUITE excluded
        assignments = [
            ("SoftwareA", None),
            ("SoftwareB", None),
            ("SoftwareC", None),
            ("SoftwareD", None),
            ("SoftwareE", WikibaseType.SUITE),
        ]

        for i, (software_name, wikibase_type) in enumerate(assignments):
            wikibase = WikibaseModel(
                wikibase_name=f"Aggregate Software Test Wikibase {i}",
                base_url=f"https://aggregate-software-example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = wikibase_type
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

            version = WikibaseSoftwareVersionModel(
                software=software_entries[software_name],
                version=(
                    f"{i+1}.{i}" if i != 3 else "7.2.24-0ubuntu0.18.04.3 (fpm-fcgi)"
                ),
                version_hash="fbca402" if i == 2 else None,
                version_date=datetime(2022, 12, 13, 5, 50) if i == 4 else None,
            )

            version.wikibase_software_version_observation_id = obs.id
            session.add(version)

        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_software_query(
    five_wikibases_with_software_versions,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregated Software Query"""

    result = await test_schema.execute(
        AGGREGATE_SOFTWARE_QUERY, variable_values={"pageNumber": 1, "pageSize": 5}
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateSoftwarePopularity"], 1, 5, 5, 1)
    assert_layered_property_count(
        result.data, ["aggregateSoftwarePopularity", "data"], 5
    )

    for index, (
        expected_software_name,
        expected_wikibase_count,
        expected_version_string,
        expected_version_semver,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("SoftwareA", 1, "1.0", (1, 0, None), None, None),
            ("SoftwareB", 1, "2.1", (2, 1, None), None, None),
            ("SoftwareC", 1, "3.2", (3, 2, None), None, "fbca402"),
            (
                "SoftwareD",
                1,
                "7.2.24-0ubuntu0.18.04.3 (fpm-fcgi)",
                (7, 2, 24),
                None,
                None,
            ),
            (
                "SoftwareE",
                1,
                "5.4",
                (5, 4, None),
                datetime(2022, 12, 13, 5, 50),
                None,
            ),
        ]
    ):

        assert_software_version_aggregate(
            result.data["aggregateSoftwarePopularity"]["data"][index],
            expected_software_name,
            expected_wikibase_count,
            expected_version_string,
            expected_version_semver,
            expected_version_date,
            expected_version_hash,
        )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 5),
        (["CLOUD"], 5),
        (["OTHER"], 5),
        (["SUITE"], 4),
        (["CLOUD", "OTHER"], 5),
        (["CLOUD", "SUITE"], 4),
        (["OTHER", "SUITE"], 4),
        (["CLOUD", "OTHER", "SUITE"], 4),
    ],
)
@pytest.mark.version
async def test_aggregate_software_query_filtered(
    five_wikibases_with_software_versions, exclude: list, expected_count: int
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregated Software Query"""

    result = await test_schema.execute(
        AGGREGATE_SOFTWARE_QUERY,
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
        ["aggregateSoftwarePopularity", "meta", "totalCount"],
        expected_count,
    )
