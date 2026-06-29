"""Test Query Cloud Instances"""

import os

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import WikibaseModel
from model.enum import WikibaseType
from tests.test_schema import test_schema
from tests.test_upsert_cloud_instances.constant import (
    DATA_DIRECTORY,
    WIKIBASE_LIST_QUERY,
)
from tests.utils import MockResponse, assert_layered_property_count, get_mock_context

UPDATE_CLOUD_INSTANCES_MUTATION = """
mutation MyMutation {
  updateCloudInstances
}
"""


@pytest.fixture
async def wikibase_list(db_session):
    """Create the wikibases required by the cloud instance test."""

    wikibases = [
        {"wikibase_name": "Local Wikibase", "type": WikibaseType["SUITE"]},
        {"wikibase_name": "Another Wikibase", "type": WikibaseType["OTHER"]},
        {"wikibase_name": "Existing Cloud Wikibase", "type": WikibaseType["CLOUD"]},
    ]

    async with AsyncSession(bind=db_session) as session:
        for i, wb in enumerate(wikibases):
            wikibase = WikibaseModel(
                wikibase_name=wb["wikibase_name"],
                wikibase_type=wb["type"],
                base_url=f"https://example-{i}.com",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            session.add(wikibase)

        await session.flush()
    return wikibases


@pytest.mark.asyncio
async def test_add_cloud_instance(
    wikibase_list, mocker
):  # pylint: disable=unused-argument, redefined-outer-name
    """
    test adding a list of cloud instances
    """

    with open(
        os.path.join(DATA_DIRECTORY, "instances-all.json"), "rb"
    ) as instances_json:

        mocker.patch(
            "requests.get", side_effect=[MockResponse("", 200, instances_json.read())]
        )

    before_update_result = await test_schema.execute(WIKIBASE_LIST_QUERY)
    assert before_update_result.errors is None
    assert before_update_result.data is not None
    assert_layered_property_count(
        before_update_result.data, ["wikibaseList", "data"], 3
    )
    assert (
        len(
            [
                w
                for w in before_update_result.data["wikibaseList"]["data"]
                if w["wikibaseType"] == "CLOUD"
            ]
        )
        == 1
    )

    update_result = await test_schema.execute(
        UPDATE_CLOUD_INSTANCES_MUTATION,
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is None
    assert update_result.data is not None
    assert update_result.data["updateCloudInstances"]

    after_update_result = await test_schema.execute(WIKIBASE_LIST_QUERY)
    assert after_update_result.errors is None
    assert after_update_result.data is not None
    assert_layered_property_count(
        after_update_result.data, ["wikibaseList", "data"], 11
    )
    assert (
        len(
            [
                w
                for w in after_update_result.data["wikibaseList"]["data"]
                if w["wikibaseType"] == "CLOUD"
            ]
        )
        == 9
    )
