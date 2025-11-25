"""Test Sort Wikibase List"""

import pytest
from tests.test_query.wikibase_list_query import WIKIBASE_LIST_QUERY
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_page_meta


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-trip-asc", depends=["mutate-cloud-instances"], scope="session"
)
async def test_wikibase_list_query_sort_triples_asc():
    """Test Sort Triples Ascending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TRIPLES", "dir": "ASC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)

    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            0,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            1,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            2,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            3,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            4,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            5,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            6,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            7,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            8,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            9,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            10,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(
    name="sort-trip-desc", depends=["mutate-cloud-instances"], scope="session"
)
async def test_wikibase_list_query_sort_triples_desc():
    """Test Sort Triples Descending"""

    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 11,
            "sortBy": {"column": "TRIPLES", "dir": "DESC"},
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibaseList" in result.data
    assert_page_meta(result.data["wikibaseList"], 1, 11, 11, 1)

    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            0,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            1,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            2,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            3,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            4,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            5,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            6,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            7,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            8,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            9,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibaseList",
            "data",
            10,
            "quantityObservations",
            "mostRecent",
            "totalTriples",
        ],
        0,
    )
