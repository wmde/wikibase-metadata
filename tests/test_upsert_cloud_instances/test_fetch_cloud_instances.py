"""Test Fetch Cloud Instances"""

import os
import pytest

from fetch_data import fetch_cloud_instances
from tests.test_upsert_cloud_instances.constant import DATA_DIRECTORY
from tests.utils import MockResponse


@pytest.mark.asyncio
async def test_fetch_cloud_instances(mocker):
    """
    test fetching a long list of cloud instances and
    examine some examples if their values are correctly parsed
    """

    with open(
        os.path.join(DATA_DIRECTORY, "instances-all.json"), "rb"
    ) as instances_json:

        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )

        instances = await fetch_cloud_instances()

        assert instances
        assert len(instances) == 8

        assert instances[0].id == 167
        assert instances[0].sitename == "Doelgericht Digitaal Transformeren"
        assert instances[0].domain == "osloddt.wikibase.cloud"
        assert instances[0].domain_decoded == "osloddt.wikibase.cloud"
        assert instances[0].description is None

        assert instances[7].id == 326
        assert instances[7].sitename == "MetaBase"
        assert instances[7].domain == "metabase.wikibase.cloud"
        assert instances[7].domain_decoded == "metabase.wikibase.cloud"
        assert instances[7].description is None


@pytest.mark.asyncio
async def test_fetch_cloud_instances_broken_response(mocker):
    """
    test fetching a list with one broken cloud instance and
    examine the remaining correct instance
    """

    with open(
        os.path.join(DATA_DIRECTORY, "instances-broken.json"), "rb"
    ) as instances_json:

        mocker.patch(
            "requests.get",
            side_effect=[MockResponse("", 200, instances_json.read())],
        )

        instances = await fetch_cloud_instances()

        assert instances
        assert len(instances) == 1
        assert instances[0].id == 32
