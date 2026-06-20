"""Test Aggregate Created Query"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.log.wikibase_log_month_observation_model import WikibaseLogMonthObservationModel
from model.enum.wikibase_type_enum import WikibaseType
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_layered_property_value

AGGREGATED_CREATED_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateCreated(wikibaseFilter: $wikibaseFilter) {
    year
    wikibaseCount
  }
}
"""

@pytest.fixture
async def wikibase_with_first_month_log(db_session):
    """Create a SUITE wikibase with a first-month log observation with first_log_date set"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Created Test Wikibase",
            base_url="https://aggregate-created-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType["SUITE"]
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        observation = WikibaseLogMonthObservationModel(
            wikibase_id=wikibase.id, first_month=True
        )
        observation.returned_data = True
        observation.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        observation.first_log_date = datetime(2020, 5, 15, tzinfo=timezone.utc)
        observation.last_log_date = datetime(2020, 6, 1, tzinfo=timezone.utc)
        session.add(observation)
        await session.flush()

        wikibase_id = wikibase.id
    return wikibase_id


@pytest.mark.asyncio
@pytest.mark.agg
# @pytest.mark.dependency(depends=["log-first-success-1"], scope="session")
@pytest.mark.log
@pytest.mark.query
async def test_aggregate_created_query(wikibase_with_first_month_log):
    """Test Aggregate Created Query"""

    result = await test_schema.execute(AGGREGATED_CREATED_QUERY)

    assert result.errors is None
    assert result.data is not None
    assert_layered_property_count(result.data, ["aggregateCreated"], 1)
    assert_layered_property_value(result.data, ["aggregateCreated", 0, "year"], 2020)
    assert_layered_property_value(
        result.data, ["aggregateCreated", 0, "wikibaseCount"], 1
    )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count", "expected_wikibase_count"],
    [
        ([], 1, 1),
        (["CLOUD"], 1, 1),
        (["OTHER"], 1, 1),
        (["SUITE"], 0, 0),
        (["CLOUD", "OTHER"], 1, 1),
        (["CLOUD", "SUITE"], 0, 0),
        (["OTHER", "SUITE"], 0, 0),
        (["CLOUD", "OTHER", "SUITE"], 0, 0),
    ],
)
@pytest.mark.user
async def test_aggregate_created_query_filtered(
    wikibase_with_first_month_log, exclude: list, expected_count: int, expected_wikibase_count: int
):
    """Test Aggregate Created Query"""

    result = await test_schema.execute(
        AGGREGATED_CREATED_QUERY,
        variable_values={"wikibaseFilter": {"wikibaseType": {"exclude": exclude}}},
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_count(result.data, ["aggregateCreated"], expected_count)
    if expected_count > 0:
        assert_layered_property_value(
            result.data,
            ["aggregateCreated", 0, "wikibaseCount"],
            expected_wikibase_count,
        )
