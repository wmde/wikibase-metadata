"""Test Aggregate External Identifier Query"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.enum.wikibase_type_enum import WikibaseType
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.external_identifier.wikibase_ei_obs_model import (
    WikibaseExternalIdentifierObservationModel,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value

AGGREGATED_QUANTITY_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateExternalIdentifier(wikibaseFilter: $wikibaseFilter) {
    totalExternalIdentifierProperties
    totalExternalIdentifierStatements
    totalUrlProperties
    totalUrlStatements
    wikibaseCount
  }
}
"""


@pytest.fixture
async def wikibase_with_ei_observation_agg(
    db_session,
):  # pylint: disable=unused-argument
    """Create a wikibase with an EI observation for aggregate tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate EI Test Wikibase",
            base_url="https://aggregate-ei-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseExternalIdentifierObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.total_external_identifier_properties = 16
        obs.total_external_identifier_statements = 32
        obs.total_url_properties = 64
        obs.total_url_statements = 128
        session.add(obs)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.ei
@pytest.mark.query
async def test_aggregate_external_identifier_query(
    wikibase_with_ei_observation_agg,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate ExternalIdentifier Query"""

    result = await test_schema.execute(AGGREGATED_QUANTITY_QUERY)

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data,
        ["aggregateExternalIdentifier", "totalExternalIdentifierProperties"],
        16,
    )
    assert_layered_property_value(
        result.data,
        ["aggregateExternalIdentifier", "totalExternalIdentifierStatements"],
        32,
    )
    assert_layered_property_value(
        result.data, ["aggregateExternalIdentifier", "totalUrlProperties"], 64
    )
    assert_layered_property_value(
        result.data, ["aggregateExternalIdentifier", "totalUrlStatements"], 128
    )
    assert_layered_property_value(
        result.data, ["aggregateExternalIdentifier", "wikibaseCount"], 1
    )


@pytest.fixture
async def wikibase_with_ei_observation_suite(
    db_session,
):  # pylint: disable=unused-argument
    """Create a SUITE wikibase with an EI observation for filtered aggregate tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate EI Filtered Test Wikibase",
            base_url="https://aggregate-ei-filtered-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType.SUITE
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseExternalIdentifierObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.total_external_identifier_properties = 16
        obs.total_external_identifier_statements = 32
        obs.total_url_properties = 64
        obs.total_url_statements = 128
        session.add(obs)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
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
async def test_aggregate_external_identifier_query_filtered(
    exclude: list, expected_count: int, wikibase_with_ei_observation_suite
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate ExternalIdentifier Query"""

    result = await test_schema.execute(
        AGGREGATED_QUANTITY_QUERY,
        variable_values={"wikibaseFilter": {"wikibaseType": {"exclude": exclude}}},
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateExternalIdentifier", "wikibaseCount"], expected_count
    )
