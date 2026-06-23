"""Test Aggregate Quantity Query"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.quantity.wikibase_quantity_observation_model import WikibaseQuantityObservationModel
from model.enum.wikibase_type_enum import WikibaseType
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value

AGGREGATED_QUANTITY_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateQuantity(wikibaseFilter: $wikibaseFilter) {
    totalItems
    totalLexemes
    totalProperties
    totalTriples
    wikibaseCount
  }
}
"""

@pytest.fixture
async def wikibase_with_quantity_observation(db_session):
    """Create a wikibase with a quantity observation for aggregate tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Quantity Test Wikibase",
            base_url="https://aggregate-quantity-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseQuantityObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.total_items = 2
        obs.total_lexemes = 4
        obs.total_properties = 1
        obs.total_triples = 8
        session.add(obs)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.quantity
@pytest.mark.query
async def test_aggregate_quantity_query(wikibase_with_quantity_observation):
    """Test Aggregate Quantity Query"""

    result = await test_schema.execute(AGGREGATED_QUANTITY_QUERY)

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(result.data, ["aggregateQuantity", "totalItems"], 2)
    assert_layered_property_value(result.data, ["aggregateQuantity", "totalLexemes"], 4)
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalProperties"], 1
    )
    assert_layered_property_value(result.data, ["aggregateQuantity", "totalTriples"], 8)
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "wikibaseCount"], 1
    )

@pytest.fixture
async def wikibase_with_quantity_suite(db_session):
    """Create a SUITE wikibase with a quantity observation for filtered aggregate tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Quantity Filtered Test Wikibase",
            base_url="https://aggregate-quantity-filtered-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType.SUITE
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseQuantityObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.total_items = 10
        obs.total_lexemes = 0
        obs.total_properties = 5
        obs.total_triples = 100
        session.add(obs)
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
        ([], 1),
        (["CLOUD"], 1),
        (["OTHER"], 1),
        (["SUITE"], 0),
        (["CLOUD", "OTHER"], 1),
        (["CLOUD", "SUITE"], 0),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_quantity_query_filtered(wikibase_with_quantity_suite, exclude: list, expected_count: int):
    """Test Aggregate Quantity Query"""

    result = await test_schema.execute(
        AGGREGATED_QUANTITY_QUERY,
        variable_values={"wikibaseFilter": {"wikibaseType": {"exclude": exclude}}},
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateQuantity", "wikibaseCount"], expected_count
    )
