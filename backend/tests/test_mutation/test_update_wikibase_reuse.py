# pylint: disable=redefined-outer-name
"""Test Update Wikibase Reuse Flag"""

import pytest

from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context

WIKIBASE_FILTERED_AND_UNFILTERED_QUERY = """
query PageWikibases {
  filtered: wikibaseList(pageNumber: 1, pageSize: 100) {
    meta {
      totalCount
    }
    data {
      id
    }
  }
  unfiltered: wikibaseList(
    pageNumber: 1
    pageSize: 100
    wikibaseFilter: { ignoreReuse: true }
  ) {
    meta {
      totalCount
    }
    data {
      id
    }
  }
}"""

UPDATE_WIKIBASE_REUSE_MUTATION = """
mutation MyMutation($wikibaseId: Int!, $reuse: Boolean!) {
  setReuseFlag(wikibaseId: $wikibaseId, reuse: $reuse)
}
"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="wikibase-set-reuse-true",
    depends=["transform-cloud-instance", "wikibase-set-reuse-false"],
    scope="session",
)
async def test_set_wikibase_reuse_true():
    """Set Wikibase Reuse True"""

    before_adding_result = await test_schema.execute(
        WIKIBASE_FILTERED_AND_UNFILTERED_QUERY
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["filtered", "meta", "totalCount"], expected_value=1
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["unfiltered", "meta", "totalCount"],
        expected_value=3,
    )

    before_adding_reuse_all_ids = {
        int(w["id"]) for w in before_adding_result.data["unfiltered"]["data"]
    }
    before_adding_reuse_true_ids = {
        int(w["id"]) for w in before_adding_result.data["filtered"]["data"]
    }
    before_adding_reuse_false_ids = (
        before_adding_reuse_all_ids - before_adding_reuse_true_ids
    )
    assert len(before_adding_reuse_false_ids) == 2, f"{before_adding_result.data}"

    for wiki_id in before_adding_reuse_false_ids:
        update_result = await test_schema.execute(
            UPDATE_WIKIBASE_REUSE_MUTATION,
            variable_values={"wikibaseId": wiki_id, "reuse": True},
            context_value=get_mock_context("test-auth-token"),
        )
        assert update_result.errors is None
        assert update_result.data is not None
        assert update_result.data["setReuseFlag"] is True

    after_adding_result = await test_schema.execute(
        WIKIBASE_FILTERED_AND_UNFILTERED_QUERY
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["filtered", "meta", "totalCount"], expected_value=3
    )
    assert_layered_property_value(
        after_adding_result.data, ["unfiltered", "meta", "totalCount"], expected_value=3
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="cloud-wikibase-set-reuse-true",
    depends=["mutate-cloud-instances"],
    scope="session",
)
async def test_set_cloud_wikibase_reuse_true():
    """Set Cloud Wikibases Reuse True"""

    before_adding_result = await test_schema.execute(
        WIKIBASE_FILTERED_AND_UNFILTERED_QUERY
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["filtered", "meta", "totalCount"], expected_value=3
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["unfiltered", "meta", "totalCount"],
        expected_value=11,
    )

    before_adding_reuse_all_ids = {
        int(w["id"]) for w in before_adding_result.data["unfiltered"]["data"]
    }
    before_adding_reuse_true_ids = {
        int(w["id"]) for w in before_adding_result.data["filtered"]["data"]
    }
    before_adding_reuse_false_ids = (
        before_adding_reuse_all_ids - before_adding_reuse_true_ids
    )
    assert len(before_adding_reuse_false_ids) == 8, f"{before_adding_result.data}"

    for wiki_id in before_adding_reuse_false_ids:
        update_result = await test_schema.execute(
            UPDATE_WIKIBASE_REUSE_MUTATION,
            variable_values={"wikibaseId": wiki_id, "reuse": True},
            context_value=get_mock_context("test-auth-token"),
        )
        assert update_result.errors is None
        assert update_result.data is not None
        assert update_result.data["setReuseFlag"] is True

    after_adding_result = await test_schema.execute(
        WIKIBASE_FILTERED_AND_UNFILTERED_QUERY
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["filtered", "meta", "totalCount"], expected_value=11
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["unfiltered", "meta", "totalCount"],
        expected_value=11,
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="wikibase-set-reuse-false",
    depends=["transform-cloud-instance"],
)
async def test_set_wikibase_reuse_false():
    """Set Wikibase Reuse False"""

    before_adding_result = await test_schema.execute(
        WIKIBASE_FILTERED_AND_UNFILTERED_QUERY
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["filtered", "meta", "totalCount"], expected_value=2
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["unfiltered", "meta", "totalCount"],
        expected_value=3,
    )

    before_adding_reuse_true_ids = {
        int(w["id"]) for w in before_adding_result.data["filtered"]["data"]
    }

    update_result = await test_schema.execute(
        UPDATE_WIKIBASE_REUSE_MUTATION,
        variable_values={
            "wikibaseId": before_adding_reuse_true_ids.pop(),
            "reuse": True,
        },
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is None
    assert update_result.data is not None
    assert update_result.data["setReuseFlag"] is True

    after_adding_result = await test_schema.execute(
        WIKIBASE_FILTERED_AND_UNFILTERED_QUERY
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["filtered", "meta", "totalCount"], expected_value=1
    )
    assert_layered_property_value(
        after_adding_result.data, ["unfiltered", "meta", "totalCount"], expected_value=3
    )
