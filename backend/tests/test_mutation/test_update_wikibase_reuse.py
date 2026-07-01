# pylint: disable=redefined-outer-name
"""Test Update Wikibase Reuse Flag"""

import pytest

from data import get_async_session
from model.database import WikibaseModel
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


@pytest.fixture
async def wikibase(db_session):  # pylint: disable=unused-argument
    """Create a test wikibase"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Test Wikibase",
            base_url="https://example.com",
            sparql_endpoint_url="https://query.example.com",
        )
        wikibase.checked = True
        session.add(wikibase)
        await session.flush()
        return wikibase


@pytest.fixture
async def wikibases_mixed_reuse(db_session):  # pylint: disable=unused-argument
    """Create wikibases with mixed reuse flags - 3 reuse=True, 2 reuse=False"""
    async with get_async_session() as session:
        for i in range(3):
            wikibase = WikibaseModel(
                wikibase_name=f"Reuse True Wikibase {i}",
                base_url=f"https://reuse-true-example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)

        for i in range(2):
            wikibase = WikibaseModel(
                wikibase_name=f"Reuse False Wikibase {i}",
                base_url=f"https://reuse-false-example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = False
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)

        await session.flush()


@pytest.fixture
async def wikibase_reuse_false_fixture(db_session):  # pylint: disable=unused-argument
    """Create wikibases"""
    async with get_async_session() as session:
        for i in range(2):
            wikibase = WikibaseModel(
                wikibase_name=f"Reuse False Wikibase {i}",
                base_url=f"https://reuse-false-example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = False
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)

        await session.flush()


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_set_wikibase_reuse_false(
    wikibase_reuse_true_fixture,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Set Wikibase Reuse False"""

    before_adding_result = await test_schema.execute(
        WIKIBASE_FILTERED_AND_UNFILTERED_QUERY
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    print(before_adding_result.data["filtered"])
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
    affecting_id = before_adding_reuse_true_ids.pop()

    update_result = await test_schema.execute(
        UPDATE_WIKIBASE_REUSE_MUTATION,
        variable_values={
            "wikibaseId": affecting_id,
            "reuse": False,
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
    assert affecting_id not in [
        int(w["id"]) for w in after_adding_result.data["filtered"]["data"]
    ]
    assert_layered_property_value(
        after_adding_result.data, ["unfiltered", "meta", "totalCount"], expected_value=3
    )
    assert affecting_id in [
        int(w["id"]) for w in after_adding_result.data["unfiltered"]["data"]
    ]


@pytest.fixture
async def wikibase_reuse_true_fixture(db_session):  # pylint: disable=unused-argument
    """Create 2 reuse=True and 1 reuse=False wikibase"""
    async with get_async_session() as session:
        for i in range(2):
            wikibase = WikibaseModel(
                wikibase_name=f"Reuse True Wikibase {i}",
                base_url=f"https://reuse-true-example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)

        wikibase = WikibaseModel(
            wikibase_name="Reuse False Wikibase",
            base_url="https://reuse-false-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = False
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)

        await session.flush()


@pytest.fixture
async def wikibase_reuse_false_majority_fixture(
    db_session,
):  # pylint: disable=unused-argument
    """Create 1 reuse=True and 2 reuse=False wikibases"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Reuse True Wikibase",
            base_url="https://reuse-true-single-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)

        for i in range(2):
            wikibase = WikibaseModel(
                wikibase_name=f"Reuse False Wikibase {i}",
                base_url=f"https://reuse-false-majority-example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = False
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)

        await session.flush()


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_set_wikibase_reuse_true(
    wikibase_reuse_false_majority_fixture,
):  # pylint: disable=redefined-outer-name, unused-argument
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
async def test_set_cloud_wikibase_reuse_true(
    wikibases_mixed_reuse,
):  # pylint: disable=redefined-outer-name, unused-argument
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
        expected_value=5,
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
        after_adding_result.data, ["filtered", "meta", "totalCount"], expected_value=5
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["unfiltered", "meta", "totalCount"],
        expected_value=5,
    )
