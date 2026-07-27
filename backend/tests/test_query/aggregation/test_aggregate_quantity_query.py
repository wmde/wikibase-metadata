"""Test Aggregate Quantity Query"""

from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import WikibaseModel, WikibaseQuantityObservationModel
from model.enum import WikibaseType
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
async def wikibases_with_quantity_observation(
    db_session,
):  # pylint: disable=unused-argument
    """Create a wikibase with a quantity observation for aggregate tests"""
    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Quantity Test Wikibase",
            base_url="https://aggregate-quantity-example.com",
            reuse=True,
            wikibase_type=WikibaseType.OTHER,
        )
        wikibase.checked = True
        wikibase.test = False
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

        wikibase_suite = WikibaseModel(
            wikibase_name="Aggregate Quantity Filtered Test Wikibase",
            base_url="https://aggregate-quantity-filtered-example.com",
            reuse=True,
            wikibase_type=WikibaseType.SUITE,
        )
        wikibase_suite.checked = True
        wikibase_suite.test = False
        session.add(wikibase_suite)
        await session.flush()
        await session.refresh(wikibase_suite)

        suite_obs = WikibaseQuantityObservationModel()
        suite_obs.wikibase_id = wikibase_suite.id
        suite_obs.returned_data = True
        suite_obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        suite_obs.total_items = 10
        suite_obs.total_lexemes = 0
        suite_obs.total_properties = 5
        suite_obs.total_triples = 100
        session.add(suite_obs)
        await session.flush()

        return obs, suite_obs


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.quantity
@pytest.mark.query
async def test_aggregate_quantity_query(
    wikibases_with_quantity_observation,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate Quantity Query"""

    obs, suite_obs = wikibases_with_quantity_observation

    result = await test_schema.execute(AGGREGATED_QUANTITY_QUERY)

    assert result.errors is None
    assert result.data is not None

    expected_total_items = obs.total_items + suite_obs.total_items
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalItems"], expected_total_items
    )
    expected_total_lexemes = obs.total_lexemes + suite_obs.total_lexemes
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalLexemes"], expected_total_lexemes
    )
    expected_total_properties = obs.total_properties + suite_obs.total_properties
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalProperties"], expected_total_properties
    )
    expected_total_triples = obs.total_triples + suite_obs.total_triples
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalTriples"], expected_total_triples
    )
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "wikibaseCount"], 2
    )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 2),
        (["CLOUD"], 2),
        (["OTHER"], 1),
        (["SUITE"], 1),
        (["CLOUD", "OTHER"], 1),
        (["CLOUD", "SUITE"], 1),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_quantity_query_filtered(
    wikibases_with_quantity_observation, exclude: list, expected_count: int
):  # pylint: disable=redefined-outer-name, unused-argument
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
