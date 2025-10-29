"""Test Query Cloud Instances"""

import os
import pytest

from tests.test_schema import test_schema
from tests.test_upsert_cloud_instances.constant import (
    DATA_DIRECTORY,
    WIKIBASE_LIST_QUERY,
)
from tests.utils import get_mock_context
from tests.utils.assert_property_value import assert_layered_property_count
from tests.utils.mock_response import MockResponse


UPDATE_CLOUD_INSTANCES_MUTATION = """
mutation MyMutation {
  updateCloudInstances
}
"""


@pytest.mark.dependency(
    name="mutate-cloud-instances", depends=["query-cloud-instances"], scope="session"
)
@pytest.mark.asyncio
async def test_query_cloud_instance(mocker):
    """
    test whether querying the wikibase list via graphql returns a cloud instance
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
