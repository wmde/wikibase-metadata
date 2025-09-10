"""Test Aggregate External Identifier Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context


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


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["external-identifier-success"], scope="session")
@pytest.mark.ei
@pytest.mark.query
async def test_aggregate_external_identifier_query():
    """Test Aggregate ExternalIdentifier Query"""

    result = await test_schema.execute(
        AGGREGATED_QUANTITY_QUERY, context_value=get_mock_context("test-auth-token")
    )

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


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.dependency(
    depends=["update-wikibase-type-other", "update-wikibase-type-suite"],
    scope="session",
)
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
    exclude: list, expected_count: int
):
    """Test Aggregate ExternalIdentifier Query"""

    result = await test_schema.execute(
        AGGREGATED_QUANTITY_QUERY,
        variable_values={"wikibaseFilter": {"wikibaseType": {"exclude": exclude}}},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateExternalIdentifier", "wikibaseCount"], expected_count
    )
